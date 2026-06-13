from datetime import datetime
from flask_ckeditor import CKEditorField

from src.admin_views.base import SecureModelView

class BookView(SecureModelView):
    can_delete = False

    column_list = ("title", "additional_details")
    form_excluded_columns = ("date_created", "paragraphs", "date_modified")
    form_overrides = {"additional_details": CKEditorField}

    def on_model_change(self, form, model, is_created):
        model.date_modified = datetime.now()