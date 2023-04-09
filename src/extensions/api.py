import logging

from flask_restx import Api
# Import and Add Namespaces
from src.modules.book.resources import api as book_api

api = Api(
    doc='/doc/',
    title='Athonite API',
    version='1.0',
    description='A description',
    prefix='/api'
)


api.add_namespace(book_api, path="/word_tags")
