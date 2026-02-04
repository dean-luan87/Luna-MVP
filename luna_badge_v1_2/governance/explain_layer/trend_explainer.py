def explain_trend(phase3: dict):
    tags = []
    if phase3.get("acceleration") == "INCREASING":
        tags.append("RISK_ACCELERATION_PERSISTENT")
    if phase3.get("curvature") == "TOWARD_RISK":
        tags.append("CURVATURE_TOWARD_RISK")
    if phase3.get("irreversibility") == "LIKELY_IRREVERSIBLE":
        tags.append("IRREVERSIBILITY_HIGH")

    return tags[:3], "HIGH" if tags else "LOW"
