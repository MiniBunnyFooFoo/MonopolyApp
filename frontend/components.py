from frontend.utils import load_html
import streamlit as streamlit

PLAYER_COLOURS = ["p0", "p1", "p2", "p3"]
 
COLOUR_CLASS_MAP = {
    "brown": "brown",
    "red":   "red",
    "green": "green",
    "blue":  "blue",
    "go":    "go",
}

def render_board(tiles, players):
    tile_html = "".join(_render_tile(tile, players, idx) for idx, tile in enumerate(tiles))
    t = load_html("board.html")
    return t.replace("{tiles}",tile_html)

def _render_tile(tile, players, tile_idx):
    colour      = (tile.get("colour") or tile.get("type") or "").lower()
    colour_class = COLOUR_CLASS_MAP.get(colour, "")
    is_go        = tile.get("type") == "go"
 
    # Owner dot — small circle showing who owns this tile
    owner = tile.get("owner")
    if owner is not None:
        owner_dot = f'<div class="owner-dot {PLAYER_COLOURS[owner]}"></div>'
    else:
        owner_dot = ""
 
    # Price label — hidden for GO tile
    price_html = f'<div class="tile-price">${tile.get("price")}</div>' if not is_go else ""
 
    # Token circles — one per player currently standing here
    tokens = "".join(
        f'<div class="token {PLAYER_COLOURS[i]}"></div>'
        for i, p in enumerate(players)
        if p["position"] == tile_idx
    )
 
    t = load_html("tile.html")

    return (t
            .replace("{colour_class}", colour_class)
            .replace("{owner_dot}", owner_dot)
            .replace("{name}", tile["name"])
            .replace("{price_html}", price_html)
            .replace("{tokens}", tokens)
        )
def render_player_card(player, idx, is_current):
    active_class = "active" if is_current else ""
 
    properties = "".join(
        f'<span class="property-pill">{p}</span>'
        for p in player["properties"]
    ) or '<span class="muted">no properties</span>'
    
    t = load_html("player_card.html")
    return (t
        .replace("{active_class}", active_class)
        .replace("{name}", player["name"])
        .replace("{money}", str(player["money"]))
        .replace("{properties}", properties)
    )

def render_log(log_text):
    t = load_html("log_box.html")
    return t.replace("{log}", log_text)