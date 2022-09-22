import os
import os.path as op

from flask import current_app

from src.extensions.database import PkModel, db, reference_col
from src.tools.docx_processor import (
    document_to_paragraph_sections,
    open_docx,
    paragraph_section_to_text,
    split_paragraph_on_comma,
)

# Create directory for file fields to use
from src.tools.greek_csv_processor import CSVFile

file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass


def is_new_chapter(text):
    return text.isdigit()


class Books(PkModel):
    title = db.Column(db.String, unique=False, nullable=False)

    edition = db.Column(db.String, unique=False, nullable=True)
    editor = db.Column(db.String, unique=False, nullable=True)
    email = db.Column(db.String, unique=False, nullable=True)
    publisher = db.Column(db.String, unique=False, nullable=True)
    publication_place = db.Column(db.String, unique=False, nullable=True)
    publication_date = db.Column(db.DateTime, unique=False, nullable=True)
    source = db.Column(db.String, unique=False, nullable=True)
    location = db.Column(db.String, unique=False, nullable=True)
    date = db.Column(db.DateTime, unique=False, nullable=True)
    additional_details = db.Column(db.String, unique=False, nullable=True)

    file_path = db.Column(db.String, unique=False, nullable=True)
    greek_csv_path = db.Column(db.String, unique=False, nullable=True)
    chapters = db.relationship("Chapters", backref="books", lazy=True, cascade="all, delete")
    length = db.Column(db.Integer, default=0)

    def __init__(
            self,
            title,
            file_path,
            edition=None,
            editor=None,
            email=None,
            publisher=None,
            publication_place=None,
            publication_date=None,
            source=None,
            location=None,
            date=None,
            additional_details=None,
    ):

        self.title = title
        self.file_path = file_path

        self.edition = edition
        self.editor = editor
        self.email = email
        self.publisher = publisher
        self.publication_place = publication_place
        self.publication_date = publication_date
        self.source = source
        self.location = location
        self.date = date
        self.additional_details = additional_details

        self.chapters = []
        self.length = 0

        self.__document = None

    def process_file(self):
        path = op.join(file_path, self.file_path)
        self.__document = open_docx(path)

        if self.greek_csv_path is not None:
            greek_csv = CSVFile(self.greek_csv_path)

        paragraph_sections = document_to_paragraph_sections(self.__document)

        chapter = None
        previous_index = 0
        paragraph = None

        for section in paragraph_sections:
            text = paragraph_section_to_text(section)
            # create new chapter and jump to next line
            if is_new_chapter(text):
                # if exists save the previous chapter
                if chapter is not None:
                    chapter.save()

                index = int(text)
                chapter = Chapters(book_id=self.id, index=index)
                chapter.save()
                self.add_chapter(chapter)

                previous_index = 0
                continue

            # if paragraph contains text to process
            if parts := split_paragraph_on_comma(text):
                # read index and content of paragraph
                current_index, current_text = parts
                # if new index
                if previous_index != current_index:
                    # if exists save the previous paragraph
                    if paragraph is not None:
                        paragraph.prepare_words()
                        paragraph.save()

                    paragraph = Paragraphs(current_index, current_text, chapter.id)
                    if self.greek_csv_path is not None:
                        paragraph.greek = greek_csv.get_paragraph(chapter.index, paragraph.index)
                    paragraph.save()

                    chapter.add_paragraph(paragraph)
                    previous_index = current_index

                else:
                    paragraph.add_notes(current_text)

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"{self.title}"

    def add_chapter(self, chapter):
        self.chapters.append(chapter)
        self.length += 1
        self.save()

    def get_chapters(self):
        return Chapters.query.filter_by(book_id=self.id).order_by(Chapters.index).all()

    def get_chapter(self, index):
        return Chapters.query.filter_by(book_id=self.id, index=index).first()


class Chapters(PkModel):
    id = db.Column(db.Integer, primary_key=True)
    book_id = reference_col("books")

    index = db.Column(db.Integer)
    length = db.Column(db.Integer)

    paragraphs = db.relationship("Paragraphs", backref="chapters", lazy=True, cascade="all, delete")

    def __init__(self, book_id, index):
        self.book_id = book_id
        self.index = index
        self.paragraphs = []
        self.length = 0

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"Chapter {self.index}"

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)
        self.length += 1

    def clear(self):
        self.paragraphs.clear()
        self.length = 0


class Paragraphs(PkModel):
    chapter_id = reference_col("chapters")

    index = db.Column(db.Integer)
    length = db.Column(db.Integer)

    text = db.Column(db.String, unique=False, default="")
    greek = db.Column(db.String, unique=False, default="")
    notes = db.relationship("Notes", backref="paragraphs", lazy=True, cascade="all, delete")
    words = db.relationship("Words", backref="paragraphs", lazy=True, cascade="all, delete")

    def __init__(self, index, text, chapter_id=0):
        self.index = index
        self.chapter_id = chapter_id

        self.text = text

    @property
    def get_words(self):
        return Words.query.filter_by(paragraph_id=self.id).order_by(Words.index).all()

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"Paragraph {self.index}"

    def add_notes(self, text):
        for note_content in text.split("|"):
            note = Notes(note_content, self.id)
            note.save()

    def prepare_words(self):
        for index, word in enumerate(self.text.split()):
            new_word = Words(index=index,
                             content=word,
                             paragraph_id=self.id)
            new_word.save()

    def __repr__(self):
        return f"{self.index}. ტექსტი: {self.text} \n\tანოტაცია: {self.notes}"


class Words(PkModel):
    index = db.Column(db.Integer)
    content = db.Column(db.String, unique=False, default="")

    lemma = db.Column(db.String, unique=False)
    gram = db.Column(db.String, unique=False)
    grc = db.Column(db.String, unique=False)
    arm = db.Column(db.String, unique=False)
    eng = db.Column(db.String, unique=False)
    paragraph_id = reference_col("paragraphs")
    paragraph = db.relationship('Paragraphs', back_populates="words", lazy=True, cascade="all, delete")

    @classmethod
    def propose_word(cls, word):
        # words = cls.query.filter(cls.content.contains(word)).all()
        words = cls.query.filter_by(content=word).all()
        scored_words = []
        for word in words:
            word_score = 0
            vals = word.json().values()
            current_app.logger.info(vals)
            for val in vals:
                if val is None:
                    continue
                if val != "":
                    word_score += 1
            scored_words.append((word_score, word))
        scored_words.sort(key=lambda x: x[0], reverse=True)
        current_app.logger.info(scored_words)
        return scored_words[0][1]

    def __init__(self, index, content, paragraph_id):
        self.index = index
        self.content = content
        self.paragraph_id = paragraph_id

    def __repr__(self):
        return self.content


class Notes(PkModel):
    id = db.Column(db.Integer, primary_key=True)
    paragraph_id = reference_col("paragraphs")

    text = db.Column(db.String, unique=False, default="")
    color = db.Column(db.String, unique=False, default="black")
    version = db.Column(db.String, unique=False, default=None)

    def __init__(self, text, paragraph_id):
        self.paragraph_id = paragraph_id
        self.text = text

    def __repr__(self):
        return self.text


# Create models
class File(PkModel):
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name


selectors = ["ბერძნული ტექსტი", "გიორგის რეცენზია", "იენიში", "კომენტარი"]
