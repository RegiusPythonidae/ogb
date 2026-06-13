from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

from src.admin_views.book import BookView
from src.admin_views.paragraph import ParagraphView
from src.admin_views.base import SecureIndexView

admin = Admin(name="OGB", index_view=SecureIndexView(), theme=Bootstrap4Theme(base_template="admin/admin_base.html"))