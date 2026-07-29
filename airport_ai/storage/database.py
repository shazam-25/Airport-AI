import sqlite3
from airport_ai.config import config
from pathlib import Path

class Database:
    """
    SQLite database connection manager.
    """
    def __init__(self, database_path="database/airport_monitor.db"):
        PROJECT_ROOT = Path(__file__).resolve().parents[2]
        path = Path(database_path)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        # Create parent folders if missing
        path.parent.mkdir(parents=True, exist_ok=True)

        self.database_path = str(path.resolve())
        print("Database:",self.database_path)
        self.initialize()

    def connect(self):
        return sqlite3.connect(self.database_path)

    def initialize(self):
        connection = self.connect()
        cursor = connection.cursor()
        # ================
        # Events
        # ================
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                camera_id TEXT NOT NULL,
                timestamp TEXT,
                stream TEXT,
                track_id INTEGER,
                object_type TEXT,
                event_type TEXT,
                severity TEXT,
                message TEXT
            )
            """
        )
        # ==========================
        # Alerts
        # ==========================
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                camera_id TEXT NOT NULL,
                stream TEXT NOT NULL,
                track_id INTEGER,
                object_type TEXT,
                event_type TEXT,
                severity TEXT,
                priority TEXT,
                message TEXT,
                status TEXT
            )
            """
        )
        connection.commit()
        connection.close()