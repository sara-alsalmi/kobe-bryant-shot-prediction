# Mamba Shot 🏀

A basketball game where you play as Kobe Bryant. Every shot is decided by the Logistic Regression model from `Test2.ipynb`.

## Run it

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

`model.json` is created automatically on the first run (or run `python export_model.py`).

## Files

| File | What it does |
|---|---|
| `export_model.py` | Trains the same model as Test2 (C=0.1) and saves its weights to `model.json` |
| `game.html` | The game (court, players, animations, sounds) and the model formula in JavaScript |
| `app.py` | The Streamlit app: Play tab + explanation tabs |
