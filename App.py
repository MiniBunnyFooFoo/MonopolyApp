import streamlit as st

from frontend.styles import get_css
from frontend.components import render_board, render_player_card, render_log
from backend.utils import load_jsons
from backend.Game import Game

st.set_page_config(page_title="Monopoly Replay", layout="wide", page_icon="🎲")
st.markdown(get_css(), unsafe_allow_html=True)

# * Data caching 
@st.cache_data
def load_rolls():
    rolls = {}
    for name, filename in [("Game 1", "rolls_1"), ("Game 2", "rolls_2")]:
        rolls[name] = load_jsons(filename)
        
    return rolls

@st.cache_data
def get_snapshots( _rolls_key, _rolls):
    game = Game()
    return game.run(_rolls)

# * Load data
rolls_data = load_rolls()
if not rolls_data:
    st.error("No dice roll JSON files found.")
    st.stop()
    
snapshots = get_snapshots(0, rolls_data['Game 1'])

st.warning(f"SNAPSHOTS: {snapshots}")

