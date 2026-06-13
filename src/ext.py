from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
login_manager = LoginManager()
ckeditor = CKEditor()