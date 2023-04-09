from flask import Blueprint, session, render_template, request

from src.modules.book.models import Books, selectors

blueprint = Blueprint("book", __name__)


@blueprint.route("/book/", methods=["GET", "POST"])
@blueprint.route("/book/<int:book_id>", methods=["GET", "POST"])
@blueprint.route("/book/<int:book_id>/<int:chapter_id>", methods=["GET", "POST"])
@blueprint.route("/book/<int:book_id>/<int:chapter_id>/<int:paragraph_id>", methods=["GET", "POST"])
def book_view(book_id=1, chapter_id=None, paragraph_id=None):
    # TODO: Implement sessions
    book = Books.get_by_id(book_id)
    session['selector'] = request.args.get('selector')

    if chapter_id is not None:
        session['chapter_id'] = chapter_id
    elif session.get('chapter_id') is None:
        session['chapter_id'] = 1

    chapter = book.get_chapter(session['chapter_id'])
    try:
        paragraphs = chapter.paragraphs
    except AttributeError as error:
        pass
    session['paragraph_id'] = paragraph_id

    if paragraph_id is not None:
        paragraphs = [paragraphs[paragraph_id - 1]]

    return render_template(
        "book.html",
        file=book,
        chapters=book.get_chapters(),
        paragraphs=paragraphs,
        selectors=selectors,
        # TODO: Implement real options model
        options=["ბერძნული ტექსტი", "გიორგის რეცენზია", "იენიში", "კომენტარი"],
    )


@blueprint.route("/book/<int:book_id>/download", methods=["GET", "POST"])
def download_book_XML(book_id):
    book = Books.get_by_id(book_id)
    return book.download_XML()
