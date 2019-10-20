"""Routes for user authentication."""
from flask import redirect, render_template, Blueprint, request, url_for, abort
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from .models import db, User
from . import login_manager

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

# allow these user's even if they're not staff
explicitly_allowed_users = ['s4434177', 's4200694', 's4317687', 's4386414', 
    's4432329', 's4436755', 'dev'] 

#ignore_auth = True

@auth_bp.route('/login')
def login():
    """User login. Note we don't have an actual login page, so we assume anyone
    who makes it to this point has passed through UQ SSO"""
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        n = request.args.get('next')
        return redirect(n or url_for('main_bp.home'))
    if app.config['FLASK_ENV'] == 'development':
        username = 'dev'
    else:
        username = request.headers.get('X-Uq-User')
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        n = request.args.get('next')
        return redirect(n or url_for('main_bp.home'))
    
    # user didn't exist
    # check to see if they should be allowed to create an account
    if username in explicitly_allowed_users or \
        'staff' in request.headers.get('X-Uq-User-Type').lower():
        # create user
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        n = request.args.get('next')
        return redirect(n or url_for('main_bp.home'))
    return "You are not authorized to use this tool"

@auth_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect('https://api.uqcloud.net/logout')


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(int(user_id))
    return None