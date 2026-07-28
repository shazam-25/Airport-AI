from airport_ai.storage.database import Database
from airport_ai.storage.repository import EventRepository

class DashboardDatabase:
    def __init__(self, database_path):
        database = Database(database_path)
        self.repository = EventRepository(database)
    
    def recent_events(self, limit=100):
        return self.repository.get_recent(limit)
