import os

BASE_DIR = os.path.dirname(__file__)

def load_html(filename):
    path = os.path.join(BASE_DIR, "html", filename)
    with open(path) as f:
        return f.read()
    
def load_css(filename):
    path = os.path.join(BASE_DIR, "css", filename)
    with open(path) as f:
        return f"<style>{f.read()}</style>"