from flask import *
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from app.models import db, User, Product
import os,uuid
from werkzeug.security import generate_password_hash
from flask_socketio import *
mail = Mail()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    # SocketIOのインスタンスをアプリに結びつける
    socketio.init_app(app)
    # 設定ファイルの読み込み
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.urandom(24)

    # データベースの初期化
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # テストデータを挿入
        init_db()

    # ログインの初期化
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "/login"

    # user_loaderを設定
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    @app.before_request
    def assign_device_id():
        # Cookieに一意のIDがない場合、新規作成
        if 'device_id' not in request.cookies:
            unique_id = str(uuid.uuid4())
            response = make_response()
            response.set_cookie('device_id', unique_id)
            return response

    # メールの設定
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'hewgroup040@gmail.com'
    app.config['MAIL_PASSWORD'] = 'eeur oncr sfjz ssmc'  # アプリパスワードを使用
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'hewgroup040@gmail.com'
    mail.init_app(app)

    # ルーティングの設定
    from app.routes import bp
    app.register_blueprint(bp)

    return app

# テストデータ挿入の関数


def init_db():
    with db.session.begin():
        # Userデータの挿入
        if not User.query.filter_by(email='1@1').first():  # すでにユーザーが存在するか確認
            user = User(email='1@1', password=generate_password_hash(
                "1", method='pbkdf2:sha256'))
            db.session.add(user)

        # Productデータの挿入
        if not Product.query.filter_by(name='アップル').first():  # すでにアップルが存在するか確認
            apple = Product(name='アップル', sale_price=500, category="フルーツ")
            db.session.add(apple)

        if not Product.query.filter_by(name='バナナ').first():  # すでにバナナが存在するか確認
            banana = Product(name='バナナ', sale_price=200, category="フルーツ")
            db.session.add(banana)

        # 変更をコミットしてデータを保存
        db.session.commit()
