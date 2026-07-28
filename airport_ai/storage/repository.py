class EventRepository:
    def __init__(self, database):
        self.database = database
    
    def save(self, stream, event):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO events(
                timestamp,
                stream,
                track_id,
                object_type,
                event_type,
                severity,
                message
            )
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.timestamp.isoformat(),
                stream,
                event.track_id,
                event.object_type,
                event.event_type,
                event.severity,
                event.message
            ),
        )
        connection.commit()
        connection.close()

    def get_recent(self, limit=100): # Retrieve Recent Events
        connection = self.database.connect()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                timestamp,
                stream,
                track_id,
                object_type,
                event_type,
                severity,
                message
            FROM events
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        connection.close()
        return rows