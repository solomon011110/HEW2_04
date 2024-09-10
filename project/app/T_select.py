import sqlite3

dbpath = "mydatabase.db"
conn = sqlite3.connect(dbpath)
cur = conn.cursor()

cur.execute("""\
  INSERT INTO T_item
  (F_id, F_name, F_description, F_imgPass)
  VALUES ('00001', 'テストプロジェクト', '00001.txt', 'apple.jpg');\
""")
print(1)

cur.execute('SELECT * FROM T_item;')
for row in cur:
    print(row)

conn.close()