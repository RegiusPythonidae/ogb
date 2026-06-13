from flask import Blueprint, render_template, request
from flask_login import current_user
from sqlalchemy import or_

from src.models import Book, Paragraph, Word

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    books = Book.query.all()
    return render_template("main/index.html", books=books)

@main_bp.route('/book')
@main_bp.route("/book/<int:book_id>")
@main_bp.route("/book/<int:book_id>/<int:chapter_number>")
@main_bp.route("/book/<int:book_id>/<int:chapter_number>/<int:paragraph_index>")
def view_book(book_id=1, chapter_number=1, paragraph_index=None):
    book = Book.query.get(book_id)

    paragraphs = Paragraph.query.filter_by(book_id=book_id, chapter_number=chapter_number)
    if paragraph_index is not None:
        paragraphs = paragraphs.filter_by(index=paragraph_index)

    paragraphs = paragraphs.order_by(Paragraph.index).all()
    return render_template("main/view_book.html", book=book, paragraphs=paragraphs)

@main_bp.route('/word/<int:word_id>', methods=['GET', 'POST'])
def tagger(word_id):
    if not current_user.is_authenticated:
        return "Unauthorized", 401

    word = Word.query.get(word_id)
    if request.method == "GET":
        similar_word = Word.query.filter(or_(Word.text == word.text, Word.lemma == word.lemma),
                                          Word.greek_text != None,
                                          Word.english_text != None,
                                          Word.armenian_text != None,
                                          Word.lemma != None,
                                          Word.grammar != None).order_by(Word.id.desc()).first()

        if similar_word is None:
            return "Similar word not found", 404

        response = {
            "lemma": similar_word.lemma,
            "grammar": similar_word.grammar,
            "english": similar_word.english_text,
            "armenian": similar_word.armenian_text,
            "greek": similar_word.greek_text
        }
        return response

    elif request.method == "POST":
        word.lemma = request.json['lemma'] if request.json['lemma'] != "None" else None
        word.greek_text = request.json['greek'] if request.json['greek'] != "None" else None
        word.english_text = request.json['english'] if request.json['english'] != "None" else None
        word.armenian_text = request.json['armenian'] if request.json['armenian'] != "None" else None
        word.grammar = request.json['grammar'] if request.json['grammar'] != "None" else None
        word.save()
        return "Success", 200

    return "Method not allowed", 405

@main_bp.route('/about')
def about():
    return render_template("main/about.html")

@main_bp.route('/methodology')
def methodology():
    return render_template("main/methodology.html")