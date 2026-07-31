import sqlite3
import time
import cv2
import numpy as np

class RuntimeStore:
    def __init__(self, path="data/database/runtime.db"):
        self.path = path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS frames(
            camera_id TEXT PRIMARY KEY,
            timestamp REAL,
            image BLOB
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id TEXT,
            event_type TEXT,
            severity TEXT,
            message TEXT,
            timestamp REAL
        )
        """)
        conn.commit()
        conn.close()
    
    def save_frame(
        self,
        camera_id,
        frame
    ):
        _, buffer = cv2.imencode(
            ".jpg",
            frame
        )
        blob = buffer.tobytes()
        conn = sqlite3.connect(self.path)
        conn.execute(
            """
            INSERT OR REPLACE INTO frames
            VALUES(?,?,?)
            """,
            (
                camera_id,
                time.time(),
                blob
            )
        )
        conn.commit()
        conn.close()

    def get_frame(
        self,
        camera_id
    ):
        conn = sqlite3.connect(self.path)
        row = conn.execute(
            """
            SELECT image
            FROM frames
            WHERE camera_id=?
            """,
            (camera_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        image = np.frombuffer(
            row[0],
            dtype=np.uint8
        )
        return cv2.imdecode(
            image,
            cv2.IMREAD_COLOR
        )

    def save_event(
        self,
        event
    ):
        conn = sqlite3.connect(self.path)
        conn.execute(
            """
            INSERT INTO events
            (
            camera_id,
            event_type,
            severity,
            message,
            timestamp
            )
            VALUES(?,?,?,?,?)
            """,
            (
                event.camera_id,
                event.event_type,
                event.severity,
                event.message,
                time.time()
            )
        )
        conn.commit()
        conn.close()
    
    def get_events(
        self,
        limit=50
    ):
        conn = sqlite3.connect(self.path)
        rows = conn.execute(
            """
            SELECT *
            FROM events
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()
        conn.close()
        return rows

    # Get latest events
    def get_latest_event_by_severity(self, severity):
        conn = sqlite3.connect(self.path)
        row = conn.execute(
            """
            SELECT *
            FROM events
            WHERE severity=?
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (severity,)
        ).fetchone()
        conn.close()
        return row

    # Get event count
    def get_event_counts(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT severity, COUNT(*)
            FROM events
            GROUP BY severity
        """)
        rows = cursor.fetchall()
        conn.close()
        counts = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        total = 0
        for severity, count in rows:
            counts[severity.upper()] = count
            total += count
        counts["TOTAL"] = total
        return counts

    # Get Severity Distribution
    def get_severity_distribution(self):
        conn = sqlite3.connect(self.path)
        rows = conn.execute("""
            SELECT severity,
                COUNT(*)
            FROM events
            GROUP BY severity
        """).fetchall()
        conn.close()
        return rows
    