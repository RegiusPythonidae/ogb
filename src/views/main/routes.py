from collections import defaultdict
from io import BytesIO
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from flask import Blueprint, render_template, request, send_file
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

@main_bp.route("/export_xml/<int:book_id>")
def export_xml(book_id):
    book = Book.query.get(book_id)

    root = Element("book")
    metadata = SubElement(root, "metadata")
    title = SubElement(metadata, "Title")
    title.text = book.title

    details = SubElement(metadata, "Details")
    details.text = book.additional_details or ""

    chapters_el = SubElement(root, "chapters")
    chapters = defaultdict(list)

    for paragraph in sorted(book.paragraphs, key=lambda p: (p.chapter_number, p.index)):
        chapters[paragraph.chapter_number].append(paragraph)

    for chapter_number, paragraphs in sorted(chapters.items()):
        chapter_el = SubElement(chapters_el,"chapter",{"index": str(chapter_number)})
        paragraphs_el = SubElement(chapter_el, "paragraphs")

        for paragraph in paragraphs:
            paragraph_el = SubElement(
                paragraphs_el,"paragraph",{
                    "index": str(paragraph.index),
                    "text": paragraph.text,
                    "greek": paragraph.greek_text,
                },
            )

            notes_el = SubElement(paragraph_el, "notes")
            for note in paragraph.notes:
                note_attrs = {"text": note.text}
                if note.color: note_attrs["color"] = note.color
                SubElement(notes_el, "note", note_attrs)

            words_el = SubElement(paragraph_el, "words")

            for word in sorted(paragraph.words, key=lambda w: w.position):
                SubElement(words_el,"word",{
                        "index": str(word.position),
                        "content": word.text or "",
                        "lemma": word.lemma or "",
                        "gram": word.grammar or "",
                        "grc": word.greek_text or "",
                        "arm": word.armenian_text or "",
                        "eng": word.english_text or "",
                    },
                )


    xml_bytes = minidom.parseString(tostring(root, encoding="utf-8")).toprettyxml(indent="\t", encoding="utf-8")
    xml_string = xml_bytes.decode("utf-8")
    buffer = BytesIO(xml_string.encode("utf-8"))
    return send_file(buffer, mimetype="application/xml", as_attachment=True, download_name=f"{book.title}.xml")

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