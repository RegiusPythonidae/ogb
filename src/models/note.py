from src.ext import db
from src.models.base import BaseModel

class Note(BaseModel):

    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    paragraph_id = db.Column(db.Integer, db.ForeignKey('paragraphs.id'), nullable=False)

    text = db.Column(db.String(256), nullable=False)
    color = db.Column(db.String(16), nullable=False, default="black")

    paragraph = db.relationship('Paragraph', back_populates='notes', lazy=True, uselist=False)