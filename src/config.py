import os

class Config(object):
    PROJECT = "OGB"
    PROJECT_NAME = "OGB"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "TemporarySecretKeyChangeLater"

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')

    SUPPRESS_REQUEST_LOGGING = bool(os.environ.get("NOLOGS"))

    # Flask-CKEditor
    CKEDITOR_PKG_TYPE = 'basic'