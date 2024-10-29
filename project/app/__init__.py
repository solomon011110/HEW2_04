from flask import Flask, redirect, render_template, request

from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from app.config import Config
from app.models import db, User
from app.routes import bp
import os



def create_app():
    app = Flask(__name__)
    
    # 設定ファイルの読み込み
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.urandom(24)
    # データベースの初期化
    db.init_app(app)
    app.register_blueprint(bp)
    with app.app_context():
        db.create_all()
    #ログイン
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
    


