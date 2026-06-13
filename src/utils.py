from string import punctuation as default_punctuation
from os import path
import re

from src import Config

def remove_punctuation(text, punctuation=None):
    if punctuation is None:
        translation_table = str.maketrans('', '', default_punctuation)
    else:
        translation_table = str.maketrans('', '', punctuation)

    unpunctuated_text = text.translate(translation_table)
    return unpunctuated_text

def remove_trailing_spaces(text):
    while '  ' in text:
        text = text.replace('  ', ' ')

    return text

def load_svg(name, width=None, height=None, css_class=None):
    if '..' in name or name.startswith('/'):
        raise ValueError("Directory traversal not allowed")

    svg_dir = path.join(Config.PROJECT_ROOT, 'static', 'img', name)
    if not path.isfile(svg_dir):
        raise FileNotFoundError(f"{name} not found")

    with open(svg_dir, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    attrs = ""
    if css_class: attrs += f' class="{css_class}"'
    if width: attrs += f' width="{width}"'
    if height: attrs += f' height="{height}"'

    if attrs:
        svg_content = re.sub(r'<svg\b', f'<svg{attrs}', svg_content, count=1)
    return svg_content