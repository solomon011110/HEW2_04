from flask import Blueprint, render_template
from .database import get_db
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = db.execute('SELECT * FROM item').fetchall()
    return render_template('home.html', items=items)

@bp.route('/register')
def register():
    return render_template('register.html')

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/profile')
def profile():
    return render_template('profile.html')

@bp.route('/create_project')
def create_project():
    return render_template('create_project.html')

@bp.route('/project_list')
def project_list():
    return render_template('project_list.html')

@bp.route('/project_detail')
def project_detail():
    return render_template('project_detail.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/notifications')
def notifications():
    return render_template('notifications.html')

@bp.route('/terms')
def terms():
    return render_template('terms.html')

@bp.route('/ichi')
def ichi():
    return render_template('1.html')
