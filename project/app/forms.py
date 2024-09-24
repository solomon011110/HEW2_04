# flask_wtfからFlaskFormをimport
from flask_wtf import FlaskForm
# wtformからフォームに必要なフィールドをimport
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# wtformからフォームのバリデーションに必要な機能をimport
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
# モデルファイルからUserクラスをimport
from app.models import User
# ...
# FlaskFormクラスを継承するRegistrationFormを定義
class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
      'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  # このアプリケーションではusernameがuniqueの設定なので、
  # そのusenameが他のユーザーに使われていないか確認する
  def validate_username(self, username):
    # usersテーブルから入力されたusenameを持つレコードを検索
    user = User.query.filter_by(username=username.data).one_or_none()
    # usersテーブルに入力されたものと同じusernameをもつレコードが存在する場合
    if user is not None:
      # バリデーションエラーを返す
      raise ValidationError('Please use a different username.')

  # emailがuniqueの設定なので、
  # そのemailが他のユーザーに使われていないか確認する
  def validate_email(self, email):
    # usersテーブルから入力されたemailを持つレコードを検索
    user = User.query.filter_by(email=email.data).one_or_none()
    # usersテーブルに入力されたものと同じemailをもつレコードが存在する場合
    if user is not None:
      # バリデーションエラーを返す
      raise ValidationError('Please use a different email address.')