# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_static_digest import FlaskStaticDigest
from flask_wtf.csrf import CSRFProtect

from src.extensions.database import db
# from src.extensions.admin import admin
from src.extensions.api import api

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()

extensions = [bcrypt, csrf_protect, login_manager, db, cache, debug_toolbar, flask_static_digest, api]
extensions_with_db = [migrate]


