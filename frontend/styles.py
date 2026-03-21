from frontend.utils import load_css

def get_css():
    log_box = load_css("log_box.css")
    board = load_css("board.css")
    p_card = load_css("player_card.css")
    return "<style>" + board + p_card + log_box + "</style>"