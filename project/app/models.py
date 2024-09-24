from app import login
from flask_login import UserMixin

# UserMixinクラスを継承したUserクラスを定義
class User(UserMixin, db.Model):
    @login.user_loader
    def load_user(id):
    # usersテーブルから指定のidを持つレコードを取り出す
    # flask-loginがこの関数に引数として渡すidの値は文字列であるため、数値に変換する
    return User.query.get(int(id))