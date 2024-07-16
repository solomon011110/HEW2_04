from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

app.config.from_object('config.Config')

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)

from app.routes import auth, project
app.register_blueprint(auth.bp)
app.register_blueprint(project.bp)