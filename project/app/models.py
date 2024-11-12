from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True) 
	email = db.Column(db.String(50),  unique=True, nullable=False)
	password = db.Column(db.String(25))
	name = db.Column(db.String(25), nullable=False)


class PJenre(db.Model):
	Jid = db.Column(db.Integer, primary_key=True)
	Jenre = db.Column(db.String(20))
	
class Project(db.Model):
	Pid = db.Column(db.Integer, primary_key=True)
	Jid = db.Column(db.ForeignKey('PJenre.Jid'), nullable=False)
	creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False )
	Pname = db.Column(db.String(50))
	Funding_target = db.Column(db.Integer)
	current_funding = db.Column(db.Integer)
	overview = db.Column(db.String(100))
	image = db.Column(db.String(100))
	start_date = db.Column(db.Date, nullable=False)
	end_date = db.Column(db.Date, nullable=False)


#DB内容物要検討 リレーションシップの追加推奨
