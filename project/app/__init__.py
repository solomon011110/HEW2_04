from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from app.models import db, User
import os
import random

mail = Mail()


def create_app():
    app = Flask(__name__)

    # 設定ファイルの読み込み
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.urandom(24)

    # データベースの初期化
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # ログインの初期化
    login_manager = LoginManager()
    login_manager.init_app(app)  
    login_manager.login_view = "/login"

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

    # ユーザーのローディング
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
