from time import perf_counter

class Timer:
    """
    Simple high-resolution timer for measuring execution time.
    """
    def __init__(self):
        self.start_time = None
    
    def start(self):
        self.start_time = perf_counter()

    def stop(self):
        if self.start_time is None:
            return 0
        elapsed = perf_counter() - self.start_time
        self.start_time = None
        return elapsed