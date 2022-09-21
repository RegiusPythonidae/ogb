from flask import Flask
from src.extensions import extensions, extensions_with_db, login_manager
from src.database import db
from src.settings import Config


def import_models():
    # User models
    from src.modules.user.model import (
        UserModel,
        RoleModel,
        UserStudentsModel,
        UserCompleted,
        UserCourseModel
    )

    # Course models
    from src.modules.courses.models import (
        LanguageModel,
        CourseModel,
        LessonModel,
        TopicModel,
        ExerciseModel
    )


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
    from src.utils import blueprints

    if not blueprints and app.get("CHECK_FOR_BLUEPRINTS") is True:
        message = "The list of blueprints is empty. App won't have any blueprints."
        app.logger.warning(message)
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


def create_app(config_object=Config):
    """Create application factory, as explained here: https://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["DEBUG"] = True
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)
    configure_logger(app)
    import_models()

    @login_manager.user_loader
    def load_user(user_id):
        return None

    return app
