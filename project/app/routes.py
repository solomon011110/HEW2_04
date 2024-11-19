from flask import Flask, Blueprint, redirect, render_template, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from app.models import db, User
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import random
from app import mail

bp = Blueprint('main', __name__)

def generate_verification_code():
    return str(random.randint(100000, 999999))

@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@bp.route('/create_project')
@login_required
def create_project():
    return render_template('create_project.html')

@bp.route('/project_list')
@login_required
def project_list():
    return render_template('project_list.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # Userテーブルからemailに一致するユーザを取得
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/tweets')  # 適切なリダイレクト先に変更
        else:
            flash('ユーザー名またはパスワードが間違っています。')
            return render_template('login.html')
    else:
        return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # 認証コード生成
        verification_code = generate_verification_code()
        
        # セッションに認証コードを保存
        session['verification_code'] = verification_code
        session['email'] = email
        session['password'] = password
        
        # 認証コードをメールで送信
        msg = Message('Your Verification Code', sender='hewgroup040@gmail.com', recipients=[email])
        msg.body = f'Your verification code is: {verification_code}'
        mail.send(msg)
        
        flash('認証コードがメールに送信されました。')
        return redirect(url_for('main.verify'))
    
    return render_template('register.html')

@bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        input_code = request.form['verification_code']
        stored_code = session.get('verification_code')
        
        if input_code == stored_code:
            flash('認証に成功しました！登録が完了しました。')
            email = session.get('email')
            password = session.get('password')
            # Userのインスタンスを作成
            user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()
            return redirect("login")
        else:
            flash('認証コードが正しくありません。再試行してください。')
    
    return render_template('verify.html')


@bp.route('/resetpass')
def resetpass():
    return render_template('resetpass.html')