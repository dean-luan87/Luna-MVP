def is_cpa_invalidated(
    prev_closing_speed: float,
    curr_closing_speed: float,
    prev_ttc: float,
    curr_ttc: float,
) -> bool:
    if curr_ttc > prev_ttc and abs(curr_closing_speed) < abs(prev_closing_speed):
        return True
    return False
