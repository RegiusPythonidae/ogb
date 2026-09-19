from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy import or_

from src.models.word import Word


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return False
        return None


class SecureIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return False
        return None

    @expose('/')
    def index(self):
        untagged_words = Word.query.filter(
            or_(
                Word.lemma == None,
                Word.grammar == None,
                Word.greek_text == None,
                Word.english_text == None,
                Word.armenian_text == None
            )
        ).limit(20).all()

        return self.render('admin/dashboard.html', untagged_words=untagged_words)