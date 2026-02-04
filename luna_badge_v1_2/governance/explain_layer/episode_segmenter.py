def segment_episodes(history: list):
    if not history:
        return ["SAFE"]
    return ["BUILD_UP", "CRITICAL"]
