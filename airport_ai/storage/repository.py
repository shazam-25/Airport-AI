class EventRepository:
    def __init__(self, database):
        self.database = database
    
    def save(self, camera_id, stream, event):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO events(
                camera_id,
                timestamp,
                stream,
                track_id,
                object_type,
                event_type,
                severity,
                message
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                camera_id,
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

    def get_recent(self, camera_id=None, limit=100): # Retrieve Recent Events
        connection = self.database.connect()
        cursor = connection.cursor()
        if camera_id is None:
            cursor.execute(
                """
                SELECT 
                    camera_id,
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
        else:
            cursor.execute(
                """
                SELECT 
                    camera_id,
                    timestamp,
                    stream,
                    track_id,
                    object_type,
                    event_type,
                    severity,
                    message
                FROM events
                WHERE camera_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (camera_id, limit,),
            )
        rows = cursor.fetchall()
        connection.close()
        return rows