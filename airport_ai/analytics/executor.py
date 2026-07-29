from concurrent.futures import ThreadPoolExecutor

class AnalyticsExecutor:
    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def evaluate(
        self,
        tracks,
        turnaround,
        ppe,
        fod,
    ):
        safety_events = self.executor.submit(turnaround.evaluate, tracks)
        ppe_events = self.executor.submit(ppe.evaluate, tracks)
        fod_events = self.executor.submit(fod.evaluate, tracks)

        return (
            safety_events.result(),
            ppe_events.result(),
            fod_events.result(),
        )

    def shutdown(self):
        self.executor.shutdown(wait=True)
        