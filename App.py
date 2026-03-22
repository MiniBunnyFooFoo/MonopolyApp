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
    
# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎮 Controls")
 
    game_choice = st.selectbox("Select game", list(rolls_data.keys()))
    snapshots = get_snapshots(game_choice, rolls_data[game_choice])
 
    # Reset step counter when game changes
    if "step" not in st.session_state or st.session_state.get("game") != game_choice:
        st.session_state.step = 0
        st.session_state.game = game_choice
 
    step  = st.session_state.step
    total = len(snapshots)
 
    st.progress(step / max(total - 1, 1))
    st.caption(f"Turn {step} of {total - 1}")
 
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⏮"):
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("◀") and step > 0:
            st.session_state.step -= 1
            st.rerun()
    with col3:
        if st.button("▶") and step < total - 1:
            st.session_state.step += 1
            st.rerun()
    with col4:
        if st.button("⏭"):
            st.session_state.step = total - 1
            st.rerun()
 
    st.markdown("---")
    st.markdown("### 📋 Players")
 
    snap = snapshots[st.session_state.step]

    try:
        player_count = len(snap["players"])
    
    except TypeError:
        player_count = 4
    
    current_player = max(0, (st.session_state.step - 1)) % player_count
 
    for idx, player in enumerate(snap["players"]):
        st.html(render_player_card(player, idx, idx == current_player))

# ─── Board ──────────────────────────────────────────────────────────────────
st.markdown("## 🎲 Monopoly Replay")
 
board_col, info_col = st.columns([3, 2])

with board_col:
    st.html(render_board(snap["tiles"], snap["players"]))
    
with info_col:
    st.markdown("#### 📜 Event Log")
    st.markdown(render_log(snap["log"]), unsafe_allow_html=True)
 
    if snap.get("game_over"):
        st.success(f"🏆 {snap.get('winner')} wins!")
 
    st.markdown("#### 🏠 Property Ownership")
    owned = [(t["name"], t["owner"]) for t in snap["tiles"] if t["owner"] is not None]
    if owned:
        for tile_name, owner_id in owned:
            owner_name = snap["players"][owner_id]["name"]
            st.caption(f"{tile_name} → {owner_name}")
    else:
        st.caption("No properties owned yet")