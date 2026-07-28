from airport_ai.storage.database import Database
from airport_ai.storage.repository import EventRepository

class DashboardDatabase:
    def __init__(self, repository, alert_repository):
        self.repository = repository
        self.alert_repository = alert_repository
    
    def recent_events(self, camera_id=None, limit=100):
        return self.repository.get_recent(camera_id, limit)
    
    def active_alerts(self):
        return self.alert_repository.get_active_alerts()
