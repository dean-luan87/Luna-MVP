FORBIDDEN_FIELDS = {
    "decision",
    "authority",
    "abilities",
    "c_decision",
}


def read_phase3(risk_snapshot: dict) -> dict:
    for key in FORBIDDEN_FIELDS:
        if key in risk_snapshot:
            raise AssertionError(f"Explain read forbidden field: {key}")
    return {
        "acceleration": risk_snapshot.get("acceleration"),
        "curvature": risk_snapshot.get("curvature"),
        "irreversibility": risk_snapshot.get("irreversibility"),
    }
