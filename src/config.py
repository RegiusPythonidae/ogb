import os

class Config(object):
    PROJECT = "OGB"
    PROJECT_NAME = "OGB"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "TemporarySecretKeyChangeLater"

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    if os.environ.get('FLASK_DB') == "prod":
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@217.147.233.8:5432/defaultdb'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')

    SUPPRESS_REQUEST_LOGGING = bool(os.environ.get("NOLOGS"))

    # Flask-CKEditor
    CKEDITOR_PKG_TYPE = 'basic'