from typing import Any, Dict, List, Optional


_AUTH_ORDER = {"A1": 1, "A2": 2, "A3": 3, "A4": 4, "A5": 5}


def _percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = int(round((len(values) - 1) * pct))
    return values[idx]


def _pearson(x: List[float], y: List[float]) -> float:
    if not x or not y or len(x) != len(y):
        return 0.0
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    num = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
    den_x = sum((a - mean_x) ** 2 for a in x)
    den_y = sum((b - mean_y) ** 2 for b in y)
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / ((den_x * den_y) ** 0.5)


def compute_metrics(timeline: List[Dict[str, Any]]) -> Dict[str, float]:
    if not timeline:
        return {
            "risk_to_authority_lag_ms_p50": 0.0,
            "authority_overreaction_rate": 0.0,
            "envelope_boundary_alignment": 0.0,
        }

    risk_change_times = []
    for idx in range(1, len(timeline)):
        if timeline[idx]["risk_level"] != timeline[idx - 1]["risk_level"]:
            risk_change_times.append((idx, timeline[idx]["ts"]))

    authority_change_times = []
    for idx in range(1, len(timeline)):
        if timeline[idx]["authority_effective"] != timeline[idx - 1]["authority_effective"]:
            authority_change_times.append((idx, timeline[idx]["ts"]))

    lag_values = []
    for _, risk_ts in risk_change_times:
        next_authority = next((ts for _, ts in authority_change_times if ts >= risk_ts), None)
        if next_authority is not None:
            lag_values.append((next_authority - risk_ts) * 1000.0)

    auth_to_risk_lags = []
    for _, auth_ts in authority_change_times:
        next_risk = next((ts for _, ts in risk_change_times if ts >= auth_ts), None)
        if next_risk is not None:
            auth_to_risk_lags.append((next_risk - auth_ts) * 1000.0)

    overreaction = 0
    for idx, _ in authority_change_times:
        if idx == 0:
            continue
        if timeline[idx]["risk_level"] == timeline[idx - 1]["risk_level"]:
            overreaction += 1
    authority_overreaction_rate = overreaction / max(len(authority_change_times), 1)

    boundary_events = 0
    aligned = 0
    for entry in timeline:
        if entry["envelope_status"] in {"ADMISSIBLE", "UNACCEPTABLE"}:
            boundary_events += 1
            auth_rank = _AUTH_ORDER.get(entry["authority_effective"], 1)
            if auth_rank >= 3:
                aligned += 1
    envelope_boundary_alignment = aligned / max(boundary_events, 1)

    # Correlations (descriptive)
    risk_rank_map = {"NONE": 1, "LOW": 2, "MEDIUM": 3, "HIGH": 4}
    auth_rank_map = {"A1": 1, "A2": 2, "A3": 3, "A4": 4, "A5": 5}
    risk_numeric = [risk_rank_map.get(item.get("risk_level"), 0) for item in timeline]
    auth_numeric = [auth_rank_map.get(item.get("authority_effective"), 0) for item in timeline]
    gate_numeric = [1 if item.get("gate") == "BLOCK" else 0 for item in timeline]
    auth_drop = [
        1 if idx > 0 and auth_numeric[idx] > auth_numeric[idx - 1] else 0 for idx in range(len(auth_numeric))
    ]
    distortion_numeric = [1 if item.get("distortion_distorted") else 0 for item in timeline]
    blocked_recovery = [
        1 if item.get("authority_blocked_by") in {"HYSTERESIS", "RISK", "DISTORTION"} else 0
        for item in timeline
    ]

    return {
        "risk_to_authority_lag_ms_p10": round(_percentile(lag_values, 0.1), 4),
        "risk_to_authority_lag_ms_p50": round(_percentile(lag_values, 0.5), 4),
        "risk_to_authority_lag_ms_p90": round(_percentile(lag_values, 0.9), 4),
        "auth_to_risk_lag_ms_p10": round(_percentile(auth_to_risk_lags, 0.1), 4),
        "auth_to_risk_lag_ms_p50": round(_percentile(auth_to_risk_lags, 0.5), 4),
        "auth_to_risk_lag_ms_p90": round(_percentile(auth_to_risk_lags, 0.9), 4),
        "authority_overreaction_rate": round(authority_overreaction_rate, 4),
        "envelope_boundary_alignment": round(envelope_boundary_alignment, 4),
        "corr_risk_level_vs_authority_level": round(_pearson(risk_numeric, auth_numeric), 4),
        "corr_gate_blocked_vs_authority_drop": round(_pearson(gate_numeric, auth_drop), 4),
        "corr_distortion_vs_authority_blocked_recovery": round(_pearson(distortion_numeric, blocked_recovery), 4),
    }
