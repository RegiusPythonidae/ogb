from src.ext import db
from src.models.base import BaseModel

class Word(BaseModel):

    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    paragraph_id = db.Column(db.Integer, db.ForeignKey('paragraphs.id'), nullable=False)

    text = db.Column(db.String(32), nullable=False)
    greek_text = db.Column(db.Text(32), nullable=True)
    armenian_text = db.Column(db.Text(32), nullable=True)
    english_text = db.Column(db.Text(32), nullable=True)

    position = db.Column(db.Integer, nullable=False)
    lemma = db.Column(db.Text(32), nullable=True)
    grammar = db.Column(db.Text(128), nullable=True)

    paragraph = db.relationship('Paragraph', back_populates='words', lazy=True, uselist=False)

    def __repr__(self):
        return self.text

    def is_untagged(self):
        return any([self.greek_text is None, self.armenian_text is None, self.english_text is None, self.lemma is None, self.paragraph is None])