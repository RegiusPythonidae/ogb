from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField, HiddenField
from src.modules.book.models import Words


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
    form_extra_fields = dict(old_text=HiddenField())

    def on_form_prefill(self, form, id):
        form.old_text.data = form.text.data

    def on_model_change(self, form, model, is_created):
        if form.old_text.data != form.text.data:
            new_text = form.text.data.split()
            old_text = form.old_text.data.split()
            changed_indexes = {}
            index = 0
            for old_word, new_word in zip(old_text, new_text):
                if old_word != new_word:
                    changed_indexes[index] = new_word
                index += 1

            for word_index, word in changed_indexes.items():
                word_model = Words.query.filter_by(paragraph_id=model.id, index=word_index).first()
                if word_model:
                    word_model.content = word
                    word_model.save()
