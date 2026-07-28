import sqlite3

class Database:
    """
    SQLite database connection manager.
    """
    def __init__(self, database_path):
        self.database_path = database_path

    def connect(self):
        return sqlite3.connect(self.database_path)