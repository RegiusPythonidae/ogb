from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField


class ParagraphModelView(ModelView):
    edit_modal = True
    column_display_pk = False

    form_excluded_columns = ["length", "greek", "chapter_id", "words", "notes", "chapters"]
    column_exclude_list = ["length", "greek", "chapter_id", "chapters"]
    column_labels = {"text": "ტექსტი", "index": "ნომერი"}
    column_searchable_list = ["text"]
    form_overrides = {
        'text': TextAreaField
    }