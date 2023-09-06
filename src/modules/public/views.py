from flask import Blueprint, render_template

from src.utils import add_csp_header
from src.modules.book.models import Books

blueprint = Blueprint("public", __name__)


@blueprint.route('/', methods=["GET", "POST"])
@add_csp_header
def index():
    """Render the home page."""
    return render_template('home.html',
                           books=Books.load(5))


@blueprint.route('/about', methods=["GET", "POST"])
@add_csp_header
def about():
    """Render the about page."""
    return render_template('about.html')


@blueprint.route('/method', method=["GET", "POST"])
@add_csp_header
def method():
    """Render the method page."""
    return render_template('method.html')
