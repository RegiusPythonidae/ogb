from src.ext import db
from src.models.base import BaseModel

class Book(BaseModel):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    additional_details = db.Column(db.String(1024), nullable=True)

    paragraphs = db.relationship('Paragraph', back_populates='book', lazy=True)

    def __repr__(self):
        return self.title

    def get_chapter_count(self):
        return len({paragraph.chapter_number for paragraph in self.paragraphs})