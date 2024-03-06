import sqlite3

# class Database:
#     def __init__(self, db_file):
#         self.connection = sqlite3.connect(db_file)
#         self.cursor = self.connection.cursor()
    
#     def user_exists(self, user_id):
#         with self.connection:
#             result = self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchmany(1)
#             return bool(len(result))

#     def add_user(self, user_id):
#         with self.connection:
#             return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

#     def set_active(self, user_id, active):
#         with self.connection:
#             return self.cursor.execute("UPDATE 'users' SET 'active' = ? WHERE 'user_id' = ?", (active, user_id))
        
#     def get_users(self):
#         with self.connection:
#             return self.cursor.execute("SELECT 'user_id', 'active' FROM 'users'").fetchall()

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE
                                NOT NULL,
                active  INTEGER DEFAULT (1) 
        );
        """)
        self.connection.commit()
    
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(result)

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            return self.cursor.rowcount > 0  # Returns True if a row was added

    def set_active(self, user_id, active):
        with self.connection:
            self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id,))
            return self.cursor.rowcount > 0  # Returns True if a row was updated
        
    def get_users(self):
        with self.connection:
            users = self.cursor.execute("SELECT user_id, active FROM users").fetchall()
            return users  # Consider processing this result into a more usable format if needed