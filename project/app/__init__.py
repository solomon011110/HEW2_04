from flask import Flask
from flask_login import LoginManager
from .database import init_db




app = Flask(__name__)
app.config.from_object('config.Config')
login = LoginManager(app) 
 
with app.app_context():
    init_db()
   
    
    
from .routes import bp as main_bp
app.register_blueprint(main_bp)
    

