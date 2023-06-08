import os
import os.path as op

from flask import Markup, redirect, request, url_for, current_app, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual
from flask_login import current_user
from flask_admin.form import FileUploadField

from src.modules.book.models import file_path


# Formatters
def _name_formatter(views, context, model, name):
    url = url_for('book.book_view', book_id=model.id)
    markup_string = f"<a href='{url}'> {model.title} </a> "
    return Markup(markup_string)


class BookModelView(ModelView):
    edit_modal = True
    can_export = True
    # can_create = False
    column_display_pk = False

    form_excluded_columns = ["chapters", "length", "edition", "email", "editor"]

    column_list = ["title", "publisher", "publication_date"]
    column_labels = {
        "title": "სახელი",
        "edition": "ვერსია",
        "editor": "რედაქტორი",
        "email": "ელ-ფოსტა",
        "publisher": "გამომცემელი",
        "publication_place": "გამოცემის ადგილი",
        "publication_date": "გამოცემის თარიღი",
        "source": "წყარო",
        "location": "ხელნაწერის შენახვის ადგილი",
        "date": "ხელნაწერის თარიღი",
        "additional_details": "დამატებითი ინფორმაცია",
        "file_path": "სამუშაო ფაილი",
        "recension": "რეცენზია",
        "author_of_the_electronic_edition": "ელექტრონული გამოცემის ავტორი",
        "sources_for_variant_readings": "ვარიანტული წაკითხვების წყაროები",
        "additional_details": "დამატებითი ინფორმაცია",
        "file_path": "სამუშაო ფაილი",
        "source_of_main_text": "ძირითადი ტექსტის წყარო"
    }

    column_searchable_list = ("title", "edition", "publisher")
    column_sortable_list = ("title", "publication_date")
    column_formatters = dict(title=_name_formatter)
    column_default_sort = "title"

    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'file_path': FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'file_path': {
            'label': 'File',
            'base_path': file_path,
            'allow_overwrite': True,
            "allowed_extensions": ["docx"]
        }
    }

    # def is_accessible(self):
    #     return current_user.is_authenticated
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for("public.home", next=request.url))

    def after_model_change(self, form, model, is_created):
        book = f"{model.id}-{model.title}"
        if is_created:
            message = f"Processing New Book {book} "
            current_app.logger.info(message)
            try:
                model.process_file()
            except Exception as e:
                flash(f"დაფიქსირდა ფორმატირების შეცდომა პროექტის დამუშავებისას: {e}", "error")
                os.remove(op.join(file_path, model.file_path))
                model.delete()
                message = f"Processing New Book {book} has Failed!"
                current_app.logger.error(message)
            else:
                message = f"Processing New Book {book} has been Completed!"
                current_app.logger.info(message)

    def after_model_delete(self, model):
        if model.file_path:
            try:
                os.remove(op.join(file_path, model.file_path))
            except OSError:
                # Don't care if was not deleted because it does not exist
                pass
