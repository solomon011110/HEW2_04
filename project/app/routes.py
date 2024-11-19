from flask import Flask, Blueprint, redirect, render_template, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from app.models import db, User, Inventory
from flask_login import current_user, LoginManager, UserMixin, login_user, logout_user, login_required
from functools import wraps
from app import mail

bp = Blueprint('main', __name__)

admin_credentials = {
    'username': '1@1',
    'password': '1'
}

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in as an admin to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_verification_code():
    return str(1)

@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', email=current_user.email)
    

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # Userテーブルからemailに一致するユーザを取得
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/profile')  # 適切なリダイレクト先に変更
        else:
            flash('ユーザー名またはパスワードが間違っています。')
            return render_template('login.html')
    else:
        return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
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

@bp.route('/verify', methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        input_code = request.form['verification_code']
        stored_code = session.get('verification_code')
        
        if input_code == stored_code:
            flash('認証に成功しました！登録が完了しました。')
            id = session.get('id')
            email = session.get('email')
            password = session.get('password')
            # Userのインスタンスを作成
            user = User(id=id, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect("login")
        else:
            flash('認証コードが正しくありません。再試行してください。')
    
    return render_template('verify.html')

@bp.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        text = request.form['text']

        contact = Contact(email=email, name=name, text=text)
        db.session.add(contact)
        db.session.commit()

        flash('お問い合わせが送信されました。')
        return redirect(url_for('home.html'))
    return render_template('contact.html')

@bp.route('/main_market',  methods=['GET','POST'])
def main_market():
    return render_template('main_market')




@bp.route('/project_info')
@login_required
def project_info():
    return render_template('project_info.html')

@bp.route('/create_project')
@login_required
def create_project():
    return render_template('create_project.html')

@bp.route('/project_list')
@login_required
def project_list():
    return render_template('project_list.html')


@bp.route('/cart')
def cart():
    return render_template('cart.html')


@bp.route('/purchase')
@login_required
def purchase():
    return render_template('purchase.html')



@bp.route('/purchasecon')
@login_required
def purchasecon():
    return render_template('purchasecon.html')












@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 認証チェック
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            session['admin_logged_in'] = True  # セッションにログイン状態を保持
            login_user(User.query.filter_by(email=username).first())
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid username or password')  # 誤ったログイン情報でフラッシュメッセージ

    return render_template('admin_login.html')




@bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    # ユーザーと在庫データを取得
    users = User.query.all()
    inventories = Inventory.query.all()
    return render_template('admin_dashboard.html', name=current_user.email, users=users, inventories=inventories)

@bp.route('/update_inventory/<int:inventory_id>', methods=['POST'])
@login_required
def update_inventory(inventory_id):
    if current_user.email != "1@1":  # 管理者のみアクセス許可
        return "アクセス権がありません", 403
    # 在庫数の更新
    inventory = Inventory.query.get_or_404(inventory_id)
    new_quantity = request.form.get('quantity', type=int)
    if new_quantity is not None:
        inventory.quantity = new_quantity
        db.session.commit()
        flash('在庫数を更新しました！', 'success')
    else:
        flash('更新に失敗しました。', 'danger')
    return redirect(url_for('main.admin_dashboard'))

@bp.route('/delete_inventory/<int:inventory_id>', methods=['POST'])
@login_required
def delete_inventory(inventory_id):
    if current_user.email != "1@1":  # 管理者のみアクセス許可
        return "アクセス権がありません", 403
    # 在庫データの削除
    inventory = Inventory.query.get_or_404(inventory_id)
    db.session.delete(inventory)
    db.session.commit()
    flash('在庫データを削除しました。', 'success')
    return redirect(url_for('main.admin_dashboard'))


@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.email != "1@1":  # 管理者のみアクセス許可
        return "アクセス権がありません", 403

    user = User.query.get(user_id)
    if user and user_id != 3:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main.admin_dashboard'))
    return "ユーザーが見つかりません", 404