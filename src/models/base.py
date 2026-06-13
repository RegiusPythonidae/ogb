from datetime import datetime

from src.ext import db

class BaseModel(db.Model):

    __abstract__ = True

    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime(), nullable=True, default=None)

    def create(self, commit=True):
        db.session.add(self)
        if commit:
            self.save()
        else:
            db.session.flush()

    @staticmethod
    def save():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        self.save()