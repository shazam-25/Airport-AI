from airport_ai.alerts.models import Alert
from datetime import datetime

class AlertRepository:
    def __init__(self, database):
        self.database = database
    
    def save(self, alert: Alert):
        conn = self.database.connect()
        cur = conn.cursor()

        # Accept both datetime and ISO string
        if isinstance(alert.timestamp, datetime):
            timestamp = alert.timestamp.isoformat()
        else:
            timestamp = str(alert.timestamp)

        cur.execute(
            """
            INSERT INTO alerts(
                timestamp,
                camera_id,
                stream,
                track_id,
                object_type,
                event_type,
                severity,
                priority,
                message,
                status
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                timestamp,
                alert.camera_id,
                alert.stream,
                alert.track_id,
                alert.object_type,
                alert.event_type,
                alert.severity,
                alert.priority,
                alert.message,
                alert.status.value,
            ),
        )
        conn.commit()
        conn.close()

    def get_active_alerts(self, limit=100):
        conn = self.database.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                timestamp,
                camera_id,
                stream,
                priority,
                status,
                message
            FROM alerts
            WHERE status != 'RESOLVED'
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows