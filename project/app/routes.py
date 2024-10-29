from flask import Flask, Blueprint, redirect, render_template, request
from werkzeug.security import generate_password_hash
from app.models import db, User
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    
    
    return render_template('home.html')

@bp.route('/register')
def register():
    return render_template('register.html')

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

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userのインスタンスを作成
        user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    else:
        return render_template('signup.html')
  
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/tweets')
        else:
            return render_template('/login')
    else:
        return render_template('login.html')
    
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')