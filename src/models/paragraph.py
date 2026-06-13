from src.ext import db
from src.models.base import BaseModel

class Paragraph(BaseModel):

    __tablename__ = 'paragraphs'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    index = db.Column(db.Integer, nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)

    text = db.Column(db.String, nullable=False)
    greek_text = db.Column(db.String, nullable=False)

    book = db.relationship('Book', back_populates='paragraphs', lazy=True, uselist=False)
    words = db.relationship('Word', back_populates='paragraph', lazy=True, order_by='Word.position')
    notes = db.relationship('Note', back_populates='paragraph', lazy=True)


