from flask import Blueprint
from src.modules.book.views import blueprint as book_blueprint
from src.modules.public.views import blueprint as public_blueprint

blueprints: list[Blueprint] = [public_blueprint, book_blueprint]
