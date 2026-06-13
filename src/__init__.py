from flask import Flask
from werkzeug import serving


from src.config import Config
from src.ext import db, login_manager, ckeditor
from src.commands import initialize_db, populate_db, import_xml
from src.models import User, Book, Paragraph
from src.views import main_bp, auth_bp
from src.admin_views import admin, BookView, ParagraphView
from src.utils import load_svg


COMMANDS = [
    initialize_db,
    populate_db,
    import_xml
]

BLUEPRINTS = [
    main_bp,
    auth_bp
]


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    app.jinja_env.globals['utils'] = {'load_svg': load_svg}

    initialize_extensions(app)
    register_blueprints(app)
    register_commands(app)

    if Config.SUPPRESS_REQUEST_LOGGING:
        configure_logger()

    return app


def initialize_extensions(app):

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Admin
    admin.init_app(app)
    admin.add_view(BookView(Book, db.session, name="წიგნი"))
    admin.add_view(ParagraphView(Paragraph, db.session, name="პარაგრაფი"))

    # Flask-Login
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(_id):
        return User.query.get(_id)

    # CKEditor
    ckeditor.init_app(app)

def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)


def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)


def configure_logger():
    default_logger = serving.WSGIRequestHandler.log_request

    def log_request(self, *args, **kwargs):
        if str(args[0]) == '304':
            return

        if 'static' in self.path:
            return

        default_logger(self, *args, **kwargs)

    serving.WSGIRequestHandler.log_request = log_request
