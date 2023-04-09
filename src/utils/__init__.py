from functools import wraps
from flask import make_response
import datetime
from src.modules.book.models import Books


def get_current_year() -> int:
    """Returns current year"""
    return datetime.datetime.now().year


def add_csp_header(f):
    """Creates wrapper function to add Content Security Policy to a Header"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers[
            'Content-Security-Policy'] = "default-src 'self' cdn.jsdelivr.net code.jquery.com style-src " \
                                         "'unsafe-inline' "
        return response

    return decorated_function


jinja_mapper = dict(
    get_current_year=get_current_year,
    Books=Books,
)
