import streamlit as st
from frontend.styles import get_css
from frontend.components import render_board, render_player_card, render_log

st.set_page_config(page_title="Monopoly Replay", layout="wide", page_icon="🎲")
st.markdown(get_css(), unsafe_allow_html=True)