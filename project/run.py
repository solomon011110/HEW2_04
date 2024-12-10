# run.py
from app import create_app, socketio

app = create_app()  # Flaskアプリケーションのインスタンスを作成

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)  # Flask-SocketIOを使ってアプリを起動
