import sqlite3

# TEST.dbを作成する
# すでに存在していれば、それにアスセスする。
dbname = 'mydatabase.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute("""\
CREATE TABLE IF NOT EXISTS T_users (
    F_id TEXT PRIMARY KEY,
    F_username TEXT NOT NULL,
    F_email TEXT NOT NULL
);\
""")
conn.commit()

cur.execute("""\
    CREATE TABLE IF NOT EXISTS T_item (
    F_id TEXT PRIMARY KEY,
    F_name TEXT NOT NULL,
    F_description TEXT,
    F_imgPass TEXT
);\
""")
conn.commit()

cur.execute("""\
  INSERT INTO T_item
  (F_id, F_name, F_description, F_imgPass)
  VALUES ('00001', 'テストプロジェクト', '00001.txt', 'apple.jpg')\
""")

conn.close()