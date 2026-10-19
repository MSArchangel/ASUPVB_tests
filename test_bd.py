import sqlite3
user_id = [None]

db_path = 'database_logins.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
name_from_edit, password_from_edit = 'aaasdasdaasdsdaasdasdasdadaaafaa', 'fffffffffffffffffffff'
cursor.execute("INSERT INTO loggins (login, password, results) VALUES (?, ?, ?)",(name_from_edit, password_from_edit, ""))
connection.commit()
user_id = [x for x in cursor.execute(f'SELECT id FROM loggins WHERE login = "{name_from_edit}" AND password = "{password_from_edit}"').fetchall()][0][0]
print(user_id)