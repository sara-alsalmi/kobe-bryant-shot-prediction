import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

import export_model
import tabs_html

APP_DIR = Path(__file__).parent

st.set_page_config(page_title="Beat the Model", layout="wide")


@st.cache_data
def load_model():
    # Train and export the Test2 model the first time the app runs
    if not export_model.MODEL_PATH.exists():
        export_model.main()
    return json.loads(export_model.MODEL_PATH.read_text(encoding="utf-8"))


@st.cache_data
def load_game(model_json, modified):
    # `modified` makes the cache reload the game when game.html changes
    html = (APP_DIR / "game.html").read_text(encoding="utf-8")
    return html.replace("/*__MODEL_DATA__*/null", model_json)


model = load_model()
metrics = model["metrics"]

st.markdown(
    """
    <style>
      header[data-testid="stHeader"], footer { display: none; }
      .block-container { max-width: 1400px; padding-top: .5rem; padding-bottom: 0; }
      /* The game always fills the screen height, so there is no scrolling */
      iframe[data-testid="stIFrame"] { height: calc(100vh - 90px) !important; }
      [data-testid="stElementContainer"]:has(> iframe[data-testid="stIFrame"]) { height: auto !important; flex: 0 0 auto !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

play_tab, how_tab, model_tab = st.tabs(["Play", "How it works", "Model"])

with play_tab:
    game = load_game(json.dumps(model), (APP_DIR / "game.html").stat().st_mtime)
    components.html(game, height=860, scrolling=False)

with how_tab:
    st.html(tabs_html.how_it_works_html(model))

with model_tab:
    st.html(tabs_html.model_html(model))
