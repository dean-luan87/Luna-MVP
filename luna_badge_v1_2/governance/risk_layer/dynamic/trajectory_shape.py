def estimate_curvature(
    heading_prev: float,
    heading_curr: float,
    dt: float,
) -> float:
    if dt <= 0:
        return 0.0
    delta = abs(heading_curr - heading_prev)
    return delta / dt
