import sqlite3
from airport_ai.config import config

class Database:
    """
    SQLite database connection manager.
    """
    def __init__(self, database_path="airport_monitor.db"):
        self.database_path = database_path

    def connect(self):
        return sqlite3.connect(self.database_path)