# Train the same Logistic Regression as Test2.ipynb and export it to model.json,
# so the game can compute predictions directly in the browser.
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

APP_DIR = Path(__file__).parent
DATA_PATH = APP_DIR.parent / "dataset" / "data.csv"
MODEL_PATH = APP_DIR / "model.json"

NUMERIC_FEATURES = ["loc_x", "loc_y", "shot_distance", "time_remaining",
                    "period", "playoffs", "home", "season_start"]
CATEGORICAL_FEATURES = ["action_type", "combined_shot_type", "shot_type",
                        "shot_zone_area", "shot_zone_basic", "shot_zone_range", "opponent"]

# Zone grid: 5x5 unit cells covering the half court (units = tenths of a foot)
GRID_CELL = 5
GRID_X0, GRID_X1 = -250, 250
GRID_Y0, GRID_Y1 = -50, 430


def load_data():
    df = pd.read_csv(DATA_PATH)
    df.drop(columns=["team_name", "team_id", "shot_id", "game_event_id", "game_id", "lat", "lon"], inplace=True)
    df["home"] = df["matchup"].str.contains("vs.", regex=False).astype(int)
    df["season_start"] = df["season"].str[:4].astype(int)
    df["time_remaining"] = df["minutes_remaining"] * 60 + df["seconds_remaining"]
    return df


def train_model(df_model):
    X = df_model[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df_model["shot_made_flag"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # Same pipeline and best Grid Search settings as Test2.ipynb (C=0.1, no class weight)
    model = Pipeline([
        ("preprocessor", ColumnTransformer([
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES)
        ])),
        ("model", LogisticRegression(C=0.1, max_iter=2000, random_state=42))
    ])
    model.fit(X_train, y_train)
    return model, X_test, y_test


def export_weights(model):
    pre = model.named_steps["preprocessor"]
    lr = model.named_steps["model"]
    scaler = pre.named_transformers_["num"]
    encoder = pre.named_transformers_["cat"]
    coef = lr.coef_[0]

    n_num = len(NUMERIC_FEATURES)
    numeric = {f: {"mean": float(scaler.mean_[i]), "scale": float(scaler.scale_[i]), "coef": float(coef[i])}
               for i, f in enumerate(NUMERIC_FEATURES)}

    categorical, pos = {}, n_num
    for f, cats in zip(CATEGORICAL_FEATURES, encoder.categories_):
        categorical[f] = {str(c): float(coef[pos + j]) for j, c in enumerate(cats)}
        pos += len(cats)

    return {"intercept": float(lr.intercept_[0]), "numeric": numeric, "categorical": categorical}


def predict_like_js(weights, row):
    # Same formula the game uses: sigmoid(intercept + scaled numbers + one-hot categories)
    z = weights["intercept"]
    for f, w in weights["numeric"].items():
        z += w["coef"] * (row[f] - w["mean"]) / w["scale"]
    for f, table in weights["categorical"].items():
        z += table.get(str(row[f]), 0.0)
    return 1 / (1 + np.exp(-z))


def zone_range_rule(distance, zone_basic):
    if zone_basic == "Backcourt":
        return "Back Court Shot"
    if distance < 8:
        return "Less Than 8 ft."
    if distance < 16:
        return "8-16 ft."
    if distance < 24:
        return "16-24 ft."
    return "24+ ft."


def build_zone_grid(df):
    # Most common zone labels for each small cell of the court, taken from the real shots
    cols = (GRID_X1 - GRID_X0) // GRID_CELL
    rows = (GRID_Y1 - GRID_Y0) // GRID_CELL
    court = df[(df["loc_y"] >= GRID_Y0) & (df["loc_y"] < GRID_Y1)].copy()
    court["col"] = ((court["loc_x"] - GRID_X0) // GRID_CELL).clip(0, cols - 1).astype(int)
    court["row"] = ((court["loc_y"] - GRID_Y0) // GRID_CELL).clip(0, rows - 1).astype(int)

    labels = {}
    grids = {}
    for f in ["shot_zone_area", "shot_zone_basic", "shot_type"]:
        names = sorted(df[f].unique())
        labels[f] = names
        majority = court.groupby(["row", "col"])[f].agg(lambda s: s.value_counts().index[0])
        filled = np.array([[r, c] for r, c in majority.index])
        values = np.array([names.index(v) for v in majority.values])

        grid = np.zeros((rows, cols), dtype=int)
        rr, cc = np.meshgrid(np.arange(rows), np.arange(cols), indexing="ij")
        cells = np.stack([rr.ravel(), cc.ravel()], axis=1)
        # Empty cells take the label of the nearest cell that has real shots
        for start in range(0, len(cells), 2000):
            chunk = cells[start:start + 2000]
            d2 = ((chunk[:, None, :] - filled[None, :, :]) ** 2).sum(axis=2)
            grid.ravel()[start:start + 2000] = values[d2.argmin(axis=1)]
        grids[f] = grid.ravel().tolist()

    return {"cell": GRID_CELL, "x0": GRID_X0, "y0": GRID_Y0, "cols": cols, "rows": rows,
            "labels": labels, "grids": grids}


def build_move_ranges(df_model):
    # Distance range (feet) where each shot type really happens in the data
    ranges = {}
    for action, group in df_model.groupby("action_type"):
        if len(group) >= 80:
            ranges[action] = {
                "min": int(np.floor(group["shot_distance"].quantile(0.03))),
                "max": int(np.ceil(group["shot_distance"].quantile(0.97))),
                "count": int(len(group)),
                "made_rate": round(float(group["shot_made_flag"].mean()), 3),
                "combined": group["combined_shot_type"].iloc[0],
            }
    return ranges


def explain_shot(weights, row):
    # Split the model's score into readable reasons, then keep the strongest one that helps and hurts
    num = {f: w["coef"] * (row[f] - w["mean"]) / w["scale"] for f, w in weights["numeric"].items()}
    cat = {f: weights["categorical"][f].get(str(row[f]), 0.0) for f in CATEGORICAL_FEATURES}
    minutes, seconds = divmod(int(row["time_remaining"]), 60)
    reasons = {
        f"Shot type: {row['action_type']}": cat["action_type"] + cat["combined_shot_type"],
        f"Distance: {int(row['shot_distance'])} ft": num["shot_distance"],
        f"Spot: {row['shot_zone_basic']}": (num["loc_x"] + num["loc_y"] + cat["shot_type"]
                                            + cat["shot_zone_area"] + cat["shot_zone_basic"] + cat["shot_zone_range"]),
        f"Opponent: {row['opponent']}": cat["opponent"],
        f"Season: {int(row['season_start'])}": num["season_start"],
        f"Time: {minutes}:{seconds:02d} left": num["time_remaining"] + num["period"],
        ("Home game" if row["home"] else "Away game"): num["home"],
        ("Playoffs" if row["playoffs"] else "Regular season"): num["playoffs"],
    }
    ordered = sorted(reasons.items(), key=lambda kv: kv[1])
    hurts, helps = ordered[0], ordered[-1]
    return (helps[0] if helps[1] > 0 else None), (hurts[0] if hurts[1] < 0 else None)


def build_quiz(model, weights, X_test, y_test, size=400):
    # Real shots from the test set (the model never saw them while training)
    shots = X_test.assign(made=y_test.values)
    shots = shots[(shots["loc_y"] < 400)].sample(size, random_state=7)
    proba = model.predict_proba(shots[NUMERIC_FEATURES + CATEGORICAL_FEATURES])[:, 1]
    quiz = []
    for (_, row), p in zip(shots.iterrows(), proba):
        helps, hurts = explain_shot(weights, row)
        quiz.append({
            "x": int(row["loc_x"]), "y": int(row["loc_y"]), "dist": int(row["shot_distance"]),
            "action": row["action_type"], "combined": row["combined_shot_type"], "three": row["shot_type"] == "3PT Field Goal",
            "period": int(row["period"]), "time": int(row["time_remaining"]), "opp": row["opponent"],
            "season": int(row["season_start"]), "home": int(row["home"]), "playoffs": int(row["playoffs"]),
            "made": int(row["made"]), "p": round(float(p), 4), "helps": helps, "hurts": hurts,
        })
    return quiz


def main():
    df = load_data()
    df_model = df.dropna(subset=["shot_made_flag"]).copy()

    model, X_test, y_test = train_model(df_model)
    weights = export_weights(model)

    # Check that the game formula gives exactly the same probabilities as scikit-learn
    sk_proba = model.predict_proba(X_test)[:, 1]
    js_proba = np.array([predict_like_js(weights, row) for _, row in X_test.iterrows()])
    max_diff = float(np.abs(sk_proba - js_proba).max())
    assert max_diff < 1e-9, max_diff

    # Check the distance and zone range rules used by the game
    calc_dist = np.floor(np.sqrt(df["loc_x"] ** 2 + df["loc_y"] ** 2) / 10)
    assert (calc_dist == df["shot_distance"]).all()
    range_match = (df.apply(lambda r: zone_range_rule(r["shot_distance"], r["shot_zone_basic"]), axis=1)
                   == df["shot_zone_range"]).mean()

    output = {
        "weights": weights,
        "zones": build_zone_grid(df),
        "moves": build_move_ranges(df_model),
        "opponents": sorted(df_model["opponent"].unique().tolist()),
        "quiz": build_quiz(model, weights, X_test, y_test),
        "zone_rates": {zone: {"made_rate": round(float(g["shot_made_flag"].mean()), 3), "count": int(len(g))}
                       for zone, g in df_model.groupby("shot_zone_basic")},
        "distance_rates": [{"ft": int(ft), "made_rate": round(float(g["shot_made_flag"].mean()), 3), "count": int(len(g))}
                           for ft, g in df_model[df_model["shot_distance"] <= 30].groupby(df_model["shot_distance"] // 2 * 2)],
        "metrics": {
            "test_accuracy": round(float(accuracy_score(y_test, model.predict(X_test))), 4),
            "baseline_accuracy": round(float((y_test == 0).mean()), 4),
            "encoded_columns": int(len(model.named_steps["preprocessor"].get_feature_names_out())),
            "train_rows": int(len(df_model) - len(X_test)),
            "test_rows": int(len(X_test)),
        },
    }
    MODEL_PATH.write_text(json.dumps(output), encoding="utf-8")

    print("Test accuracy:", output["metrics"]["test_accuracy"])
    print("Game formula vs scikit-learn max difference:", max_diff)
    print("Zone range rule match:", round(range_match, 4))
    print("Saved:", MODEL_PATH)


if __name__ == "__main__":
    main()
