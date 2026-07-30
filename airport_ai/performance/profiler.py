"""
Used by:
    - CameraPipeline
    - Runtime Metrics
    - End-to-End Performance Validation
"""
import time
from collections import defaultdict

class PipelineProfiler:
    """
    Collects timing statistics for every stages of the Airport AI pipeline.
    """
    def __init__(self):
        # Stage timings (seconds)
        self.metrics = defaultdict(list)
        # Visualization statistics
        self.visualization = {
            "frames_rendered": 0,
            "frames_skipped": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }
        self.start_time = time.time()

    # --- Stage Timing ---
    def record(self, stage:str, elapsed: float):
        """
        Record elapsed time (seconds) for a pipeline stage.
        """
        self.metrics[stage].append(elapsed)
    
    # --- Visualization Metrics
    def visualization_rendered(self):
        self.visualization["frames_rendered"] += 1

    def visualization_skipped(self):
        self.visualization["frames_skipped"] += 1

    def visualization_cache_hit(self):
        self.visualization["cache_hits"] += 1

    def visualization_cache_miss(self):
        self.visualization["cache_misses"] += 1

    # --- Average Stage Time ---
    def average(self, stage: str):
        values = self.metrics.get(stage, [])
        if not values:
            return 0.0
        return sum(values) / len(values)

    # --- Frames Per Second ---
    def fps(self):
        runtime = time.time() - self.start_time
        if runtime <= 0:
            return 0.0
        frames = len(self.metrics.get("capture", []))
        return frames / runtime
    
    # --- Summary Report ---
    def summary(self):
        results = {}

        for stage, values in self.metrics.items():
            if not values: continue
            results[stage] = {
                "count": len(values),
                "avg_ms": (sum(values) / len(values)) * 1000,
                "min_ms": min(values) * 1000,
                "max_ms": max(values) * 1000,
            }
        results["runtime"] = {
            "seconds": round(time.time() - self.start_time, 2),
            "fps": round(self.fps(), 2)
        }
        results["visualization"] = {
            "frames_rendered": self.visualization["frames_rendered"],
            "frames_skipped": self.visualization["frames_skipped"],
            "cache_hits": self.visualization["cache_hits"],
            "cache_misses": self.visualization["cache_misses"],
            "cache_hit_rate": self.cache_hit_rate(),
        }
        return results
    
    # --- Cache Statistics ---
    def cache_hit_rate(self):
        total = (
            self.visualization["cache_hits"]
            + self.visualization["cache_misses"]
        )
        if total == 0:
            return 0.0
        return round(
            self.visualization["cache_hits"] / total,
            3,
        )
    
    # --- Pretty Console Report ---
    def print_summary(self):
        report = self.summary()
        print("\n========== PIPELINE PROFILER ==========\n")
        for stage, values in report.items():
            if stage in ("runtime", "visualization"):
                continue
            print(
                f"{stage:<25}"
                f"{values['avg_ms']:>8.2f} ms"
                f" | min {values['min_ms']:.2f}"
                f" | max {values['max_ms']:.2f}"
                f" | count {values['count']}"
            )
        print("\nRuntime")
        print(f"FPS: {report['runtime']['fps']}")
        print(f"Elapsed: {report['runtime']['seconds']} sec")

        print("\nVisualization")
        vis = report["visualization"]
        print(f"Rendered: {vis['frames_rendered']}")
        print(f"Skipped: {vis['frames_skipped']}")
        print(f"Cache Hits: {vis['cache_hits']}")
        print(f"Cache Misses: {vis['cache_misses']}")
        print(f"Hit Rate: {vis['cache_hit_rate'] * 100:.1f}%")
    
    # --- Reset Statistics ---
    def reset(self):
        self.metrics.clear()
        self.visualization = {
            "frames_rendered": 0,
            "frames_skipped": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }
        self.start_time = time.time()