import sqlite3

DB_FILE = 'ibratdebatebot/database.db'

def create_table():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            active  INTEGER DEFAULT (1) 
        );
    """)
    connection.commit()
    connection.close()
create_table()
def user_exists(user_id):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    connection.close()
    return bool(result)

def add_user(user_id):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
    connection.commit()
    connection.close()
    return cursor.rowcount > 0  # Returns True if a row was added

def set_active(user_id, active):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id,))
    connection.commit()
    connection.close()
    return cursor.rowcount > 0  # Returns True if a row was updated

def get_users():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    users = cursor.execute("SELECT user_id, active FROM users").fetchall()
    connection.close()
    return users  # Consider processing this result into a more usable format if needed