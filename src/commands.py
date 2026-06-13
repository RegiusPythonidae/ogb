from flask.cli import with_appcontext
import click
import xml.etree.ElementTree as ET

from src.ext import db
from src.models import User, Book, Paragraph, Word, Note
from src.utils import remove_punctuation

@click.command('init_db')
@with_appcontext
def initialize_db():
    click.echo("Initializing database")

    db.drop_all()
    db.create_all()

    click.echo("Finished")


@click.command('populate_db')
@with_appcontext
def populate_db():
    click.echo("Creating admin user")

    admin_user = User(username="admin", password="password123")
    admin_user.create()

    click.echo("Finished")


@click.command('import_xml')
@with_appcontext
def import_xml():
    tree = ET.parse("Matthew.xml")
    xml_tree = tree.getroot()
    for node in xml_tree:
        if node.tag == "metadata":
            title = node.findtext("Title")
            recension = node.findtext("Recension")
            author = node.findtext("Author")
            source = node.findtext("Source")
            location = node.findtext("Location")
            details = node.findtext("Details")

            book = Book(title=title, additional_details=f"{recension} - {author} - {source} - {location} - {details}")
            book.create(commit=False)

        if node.tag == "chapters":
            for chapter_node in node:
                for paragraph_nodes in chapter_node:
                    for paragraph_node in paragraph_nodes:
                        index = paragraph_node.attrib.get("index")
                        text = paragraph_node.attrib.get("text").strip()
                        greek = paragraph_node.attrib.get("greek").strip()

                        paragraph = Paragraph(book_id=book.id, chapter_number=chapter_node.attrib.get("index"),
                                              index = index, text = text, greek_text = greek)
                        paragraph.create(commit=False)

                        for child in paragraph_node:
                            if child.tag == "notes":
                                for note_node in child:
                                    note = Note(paragraph_id = paragraph.id, text=note_node.attrib.get("text").strip())
                                    note.create(commit=False)

                            if child.tag == "words":
                                for word_node in child:
                                    index = word_node.attrib.get("index").strip()
                                    content = remove_punctuation(word_node.attrib.get("content")).strip()

                                    lemma = word_node.attrib.get("lemma")
                                    if lemma: lemma = lemma.strip()

                                    gram = word_node.attrib.get("gram")
                                    if gram: gram = gram.strip()

                                    grc = word_node.attrib.get("grc")
                                    if grc: grc = grc.strip()

                                    arm = word_node.attrib.get("arm")
                                    if arm: arm = arm.strip()

                                    eng = word_node.attrib.get("eng")
                                    if eng: eng = eng.strip()

                                    word = Word(paragraph_id = paragraph.id, position = index, text = content,
                                                greek_text = grc, armenian_text = arm, english_text = eng,
                                                lemma = lemma, grammar = gram)
                                    word.create(commit=False)
                print("Finished Chapter")
    Book.save()