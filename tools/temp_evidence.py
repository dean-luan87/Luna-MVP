# tools/temp_evidence.py
# TEMP ONLY — for v0.5 video regression without YOLO
"""
Temporary heuristic evidence for Gate activation.
This MUST NOT be used in production.

This is a minimal implementation to allow Gate to enter ACTIVE state
during v0.5 video regression testing without YOLO integration.

Usage:
    temp_evidence = TempEvidence(min_stable_frames=10, min_visibility=0.6)
    evidence_ok = temp_evidence.update(stability_score=0.8, visibility_score=0.7)
"""

from typing import Optional


class TempEvidence:
    """
    Temporary heuristic evidence for Gate activation.
    This MUST NOT be used in production.
    
    Design:
    - Based on visibility_score + consecutive stable frames
    - Only determines: "Is current view stable enough to allow Gate ACTIVE?"
    - Does NOT judge risks, events, or output decisions
    """

    def __init__(self, min_stable_frames: int = 10, min_visibility: float = 0.6):
        """
        :param min_stable_frames: Minimum consecutive stable frames required
        :param min_visibility: Minimum visibility score required
        """
        self.min_stable_frames = min_stable_frames
        self.min_visibility = min_visibility
        self._stable_count = 0

    def update(self, stability_score: Optional[float], visibility_score: float) -> bool:
        """
        Update evidence state based on stability and visibility.
        
        :param stability_score: Current stability score (0-1)
        :param visibility_score: Current visibility score (0-1)
        :return: evidence_ok (bool) - True if evidence is sufficient
        """
        if stability_score is None:
            self._stable_count = 0
            return False

        if stability_score >= 0.6 and visibility_score >= self.min_visibility:
            self._stable_count += 1
        else:
            self._stable_count = 0

        return self._stable_count >= self.min_stable_frames

    def snapshot(self) -> dict:
        """
        Get current evidence state snapshot.
        
        :return: Dictionary with evidence metadata
        """
        return {
            "type": "TEMP_HEURISTIC",
            "stable_count": self._stable_count,
            "min_required": self.min_stable_frames,
        }
