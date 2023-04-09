from flask import current_app

from .models import Words
from flask_restx import Resource, fields, reqparse, Namespace

api = Namespace('words', description='words related operations')

model = api.model('Word', {
    'id': fields.Integer,
    'content': fields.String,
    'lemma': fields.String,
    'gram': fields.String,
    'grc': fields.String,
    'arm': fields.String,
    'eng': fields.String,
})


@api.route('/<int:word_id>')
class WordTags(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('word', type=str)
    parser.add_argument('lemma', type=str)
    parser.add_argument('gram', type=str)
    parser.add_argument('grc', type=str)
    parser.add_argument('arm', type=str)
    parser.add_argument('eng', type=str)

    @api.marshal_with(model)
    def get(self, word_id):
        word = Words.get_by_id(word_id)
        if word is None:
            return {'message': 'Word not found'}, 404
        return word

    def delete(self, word_id):
        word = Words.get_by_id(word_id)
        if word is None:
            return {'message': 'Word not found'}, 404
        args = self.parser.parse_args()
        word.update(**args)
        return {'message': 'Word deleted'}, 200

    def put(self, word_id):
        word = Words.get_by_id(word_id)
        if word is None:
            return {'message': 'Word not found'}, 404
        args = self.parser.parse_args()
        word.update(**args)
        current_app.logger.info(word)
        return word


@api.route('/similar/<string:word>')
class SuggestWord(Resource):
    @api.marshal_with(model)
    def get(self, word):
        word = Words.propose_word(word)
        current_app.logger.info(word)

        if word is not None:
            return word
        else:
            return {'message': 'Word not found'}, 404
