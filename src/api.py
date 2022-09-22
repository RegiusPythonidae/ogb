from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__, url_prefix='/api')


api = Api(
    api_blueprint,
    title='OGB API',
    version='1.0',
    # Other metadata
)

# Namespaces
from src.modules.book.resources import api as book_api
api.add_namespace(book_api, path="/word_tags")
