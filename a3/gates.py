def roi_gate(frame_quality: str, view_confidence: float) -> bool:
    if frame_quality != "GOOD":
        return False
    if view_confidence < 0.6:
        return False
    return True
