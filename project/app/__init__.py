from flask import Flask
from .database import init_db



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    #======データベース======#
    with app.app_context():
        init_db()
    #======データベース 終わり======#
    
    # Blueprintを登録
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
