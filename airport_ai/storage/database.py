import sqlite3
from airport_ai.config import config

class Database:
    """
    SQLite database connection manager.
    """
    def __init__(self):
        self.database_path = config.get("database")["path"]

    def connect(self):
        return sqlite3.connect(self.database_path)