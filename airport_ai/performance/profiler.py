from collections import defaultdict

class PipelineProfiler:
    """
    Collects timing statistics for different stages of the pipeline.
    """
    def __init__(self):
        self.metrics = defaultdict(list)

    def record(self, stage:str, elapsed: float):
        self.metrics[stage].append(elapsed)
    
    def average(self, stage: str):
        values = self.metrics.get(stage, [])
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    def summary(self):
        results = {}

        for stage, values in self.metrics.items():
            # values = self.metrics[stage]
            results[stage] = {
                "count": len(values),
                "average_ms": (sum(values) / len(values)) * 1000,
                "min_ms": min(values) * 1000,
                "max_ms": max(values) * 1000,
            }
        return results
    
    def reset(self):
        self.metrics.clear()