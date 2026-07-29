import numpy as np

class OverlayCache:
    def __init__(self):
        self.overlay = None
        self.frame_shape = None
        self.cache_hits = 0
        self.cache_misses = 0

    # --- Cache Status ---
    def has_overlay(self):
        return self.overlay is not None

    # --- Store Overlay ---
    def store(self, overlay, frame_shape):
        self.overlay = overlay.copy()
        self.frame_shape = frame_shape
        self.cache_misses += 1

    # --- Retrieve Overlay ---
    def get(self):
        if self.overlay is None:
            return None
        self.cache_hits += 1
        return self.overlay
    
    # --- Invalidate Cache ---
    def invalidate(self):
        self.overlay = None
        self.frame_shape = None

    # --- Auto Resize Check ---
    def needs_refresh(self,frame,):
        """
        Returns True if overlay needs rebuilding.
        """
        if self.overlay is None:
            return True
        return frame.shape != self.frame_shape

    # --- Create Blank Overlay ---
    def create_blank(
        self,
        frame,
    ):
        """
        Create an empty overlay matching the frame.
        """
        return np.zeros_like(frame)
    
    # --- Cache Statistics ---
    def statistics(self):
        total = self.cache_hits + self.cache_misses
        if total == 0:
            hit_rate = 0.0
        else:
            hit_rate = self.cache_hits / total
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": hit_rate,
        }
    
    # --- Reset Statistics ---
    def reset_statistics(self):
        self.cache_hits = 0
        self.cache_misses = 0

