from flask import Flask, request, make_response, render_template, redirect
from flask_socketio import SocketIO, emit
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions
socketio = SocketIO(app)
db = SQLAlchemy(app)

# DBモデル
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)  # 投稿ID
    device_id = db.Column(db.String(100), nullable=False)  # 投稿者の一意ID
    content = db.Column(db.Text, nullable=False)  # 投稿内容
    timestamp = db.Column(db.DateTime, default=datetime.now)  # 投稿日時

# DB初期化
with app.app_context():
    db.create_all()

# Cookieに一意のIDを設定
@app.after_request
def assign_device_id(response):
    if 'device_id' not in request.cookies:
        unique_id = str(uuid.uuid4())
        response.set_cookie('device_id', unique_id)
    return response

# ソケットイベント：新しいメッセージを受信した場合
@socketio.on('new_message')
def handle_new_message(data):
    print("New message received: ", data)
    emit('message_received', data, to=None)  # すべてのクライアントに送信

# メインページ（掲示板）
@app.route('/board', methods=['GET'])
def board():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('board.html', posts=posts)

# 投稿を受け取るルート
@app.route('/post', methods=['POST'])
def post_message():
    device_id = request.cookies.get('device_id')
    content = request.form.get('content')
    if content and device_id:
        new_post = Post(device_id=device_id, content=content)
        db.session.add(new_post)
        db.session.commit()
        # 新しい投稿をSocketIOでクライアントに送信
        socketio.emit('new_message', {
            'content': content,
            'timestamp': new_post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'device_id': device_id
        }, to=None)  # broadcastの代わりにto=Noneを使用
    return redirect('/board')

# アプリ起動
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
