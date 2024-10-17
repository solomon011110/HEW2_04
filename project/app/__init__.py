from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config
from app.models import db
from app.routes import bp




def create_app():
    app = Flask(__name__)
    
    # 設定ファイルの読み込み
    app.config.from_object(Config)

    # データベースの初期化
    db.init_app(app)
    app.register_blueprint(bp)
  
    return app
    


