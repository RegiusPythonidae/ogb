from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from src.views.auth.forms import LoginForm
from src.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash("* ელფოსტა ან პაროლი არასწორია, გთხოვთ სცადოთ თავიდან")
    return render_template("auth/login.html", form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))