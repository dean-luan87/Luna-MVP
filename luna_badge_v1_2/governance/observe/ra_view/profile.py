from typing import Dict


_STABILITY = {"calm", "oscillating", "degraded_like"}
_MARGIN = {"wide", "moderate", "tight"}
_RECOVERY = {"fast", "delayed", "blocked_often"}


def build_profile(metrics: Dict[str, float]) -> Dict[str, str]:
    oscillation = metrics.get("authority_overreaction_rate", 0.0)
    alignment = metrics.get("envelope_boundary_alignment", 0.0)
    lag = metrics.get("risk_to_authority_lag_ms_p50", 0.0)

    if oscillation >= 0.25:
        stability_profile = "oscillating"
    elif alignment < 0.4:
        stability_profile = "degraded_like"
    else:
        stability_profile = "calm"

    if alignment >= 0.8:
        safety_margin_profile = "wide"
    elif alignment >= 0.5:
        safety_margin_profile = "moderate"
    else:
        safety_margin_profile = "tight"

    if lag <= 200:
        recovery_profile = "fast"
    elif lag <= 800:
        recovery_profile = "delayed"
    else:
        recovery_profile = "blocked_often"

    return {
        "stability_profile": stability_profile,
        "safety_margin_profile": safety_margin_profile,
        "recovery_profile": recovery_profile,
    }
