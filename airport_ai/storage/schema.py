class DatabaseSchema:
    def __init__(self, database):
        self.database = database
    def create_tables(self):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        camera_id TEXT,
        timestamp TEXT NOT NULL,
        stream TEXT NOT NULL,
        track_id INTEGER,
        object_type TEXT,
        event_type TEXT,
        severity TEXT,
        message TEXT
        )
        """)

        connection.commit()
        connection.close()