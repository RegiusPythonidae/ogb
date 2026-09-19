from flask import redirect, url_for
from flask_login import current_user
from wtforms import PasswordField
from wtforms.validators import ValidationError

from src.admin_views.base import SecureModelView

class UserView(SecureModelView):
    column_list = ("username", "is_admin")

    form_columns = ("username", "new_password", "is_admin")
    form_extra_fields = {"new_password": PasswordField("New Password")}

    def on_model_change(self, form, model, is_created):
        if form.new_password.data:
            model.password = form.new_password.data

        if is_created and not form.new_password.data:
            form.new_password.errors = ("Password is required when creating a new user",)
            raise ValidationError("Password is required")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.index"))
