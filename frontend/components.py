from frontend.utils import load_html

def render_board(tiles, players, current_player):
    t = load_html("board.html")
    return t.format()

def render_player_card(player, idx, is_current):
    t = load_html("player_card.html")
    return t.format()

def render_log(log_text):
    t = load_html("log_box.html")
    return t.format()