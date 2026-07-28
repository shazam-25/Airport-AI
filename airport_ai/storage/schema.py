class DatabaseSchema:
    def __init__(self, database):
        self.database = database
    def create_tables(self):
        connection = self.database.connect()
        cursor = connection.cursor()
        # Create 'events' table
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
        # Create 'alerts' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        camera_id TEXT,
        stream TEXT NOT NULL,
        track_id INTEGER,
        object_type TEXT,
        event_type TEXT,
        severity TEXT,
        priority TEXT
        message TEXT,
        status TEXT
        )
        """)

        connection.commit()
        connection.close()