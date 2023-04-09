import logging

from flask import Flask

from src.extensions import extensions, extensions_with_db, login_manager
from src.extensions.database import db
from src.utils import jinja_mapper
from src.settings import ProductionConfig


def import_models():
    # Course models
    pass


def register_extensions(app):
    """Register Flask extensions."""
    for extension in extensions:
        extension.init_app(app=app)

    for extension in extensions_with_db:
        extension.init_app(app=app, db=db)


def register_blueprints(app: Flask):
    """
    Method to register list of blueprints to the app

    param app: Flask application
    """
    # To check if app contains blueprints we need to be inside the app context
    from src.blueprints import blueprints

    if not blueprints and app.get("CHECK_FOR_BLUEPRINTS") is True:
        message = "The list of blueprints is empty. App won't have any blueprints."
        logging.warning(message)
    else:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)


def register_error_handlers(app):
    pass


def register_shell_context(app):
    pass


def register_commands(app):
    pass


def configure_logger(app):
    pass


def pass_functions_to_jinja(app, **kwargs):
    """Pass functions to jinja templates."""
    app.jinja_env.globals.update(**kwargs)


def create_app(config_object=ProductionConfig):
    """Create application factory, as explained here: https://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    # TODO: error handling when db is not available/timeouts
    logging.info(f"Loading config from: '{config_object}'")

    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["DEBUG"] = True
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)
    configure_logger(app)
    pass_functions_to_jinja(app, **jinja_mapper)  # pass dict of functions as kwargs
    import_models()

    @login_manager.user_loader
    def load_user(user_id):
        return None

    return app
