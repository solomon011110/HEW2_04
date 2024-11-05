from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()



class User(UserMixin, db.Model):
	id = db.Column(db.String(24), primary_key=True)
	email = db.Column(db.String(50), primary_key=True)
	password = db.Column(db.String(25))
	
class Project(db.Model):
	Pid = db.Column(db.Integer, primary_key=True)
	Jid = db.Column(db.Integer)
	Pname = db.Column(db.String(50))
	Funding_target = db.Column(db.Integer)
	current_funding = db.Column(db.Integer)
	overview = db.Column(db.String(100))
	image = db.Column(db.String(100))