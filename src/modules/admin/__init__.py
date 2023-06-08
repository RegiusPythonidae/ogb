from flask_admin import Admin, AdminIndexView, BaseView, expose

from src.modules.book.models import Books, Chapters, Notes, Paragraphs, File

# Model Views
from src.modules.admin.book_model_view import BookModelView
from src.modules.admin.paragraph_model_view import ParagraphModelView

# Flask-SQLAlchemy initialization here
from src.extensions.database import db


class MyAdminIndexView(AdminIndexView):
    # def is_accessible(self):
    #     return (
    #         current_user.is_authenticated
    #     )  # This does the trick rendering the view only if the user is authenticated
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for("public.home", next=request.url))

    @expose("/", methods=["GET", "POST"])
    def index(self):
        return self.render("admin/analytics_index.html")


admin = Admin(
    name="სამართავი პანელი",
    template_mode="bootstrap4"
)


admin.add_view(BookModelView(Books, db.session, name="წიგნები"))
admin.add_view(ParagraphModelView(Paragraphs, db.session, name="პარაგრაფები"))
