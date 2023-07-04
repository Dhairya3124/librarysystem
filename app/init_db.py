import sqlite3

connection = sqlite3.connect('database.db')


with open('app\schema.sql') as f:
    connection.executescript(f.read())

print("Database created")
cur = connection.cursor()

data = cur.execute("SELECT * FROM books")
print(data.fetchall())

connection.commit()
connection.close()