import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        db = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        g.db = db
    return g.db

def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # 既存のテーブルを確認してからスキーマを作成する
    with current_app.open_resource('schema.sql') as f:
        # テーブルの存在を確認し、存在しない場合のみスキーマを作成
        try:
            db.execute("SELECT 1 FROM users LIMIT 1;")
        except sqlite3.DatabaseError:
            db.executescript(f.read().decode('utf8'))
