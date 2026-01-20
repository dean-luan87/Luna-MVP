from typing import Any, Dict, List


def diagnose_overreaction(timeline: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = {
        "OVERREACT_NO_RISK_CHANGE": 0,
        "OVERREACT_RISK_NONE": 0,
        "UNDERREACT_RISK_HIGH_NO_DROP": 0,
    }
    examples = {key: [] for key in counts}

    for event in events:
        if event["type"] == "AUTH_DROP":
            before_risk = event["before"].get("risk_level", "NONE")
            after_risk = event["after"].get("risk_level", "NONE")
            if before_risk == after_risk:
                counts["OVERREACT_NO_RISK_CHANGE"] += 1
                if len(examples["OVERREACT_NO_RISK_CHANGE"]) < 5:
                    examples["OVERREACT_NO_RISK_CHANGE"].append(event["event_id"])
            if after_risk == "NONE":
                counts["OVERREACT_RISK_NONE"] += 1
                if len(examples["OVERREACT_RISK_NONE"]) < 5:
                    examples["OVERREACT_RISK_NONE"].append(event["event_id"])
        if event["type"] == "RISK_RISE":
            after_risk = event["after"].get("risk_level", "NONE")
            if after_risk == "HIGH":
                counts["UNDERREACT_RISK_HIGH_NO_DROP"] += 1
                if len(examples["UNDERREACT_RISK_HIGH_NO_DROP"]) < 5:
                    examples["UNDERREACT_RISK_HIGH_NO_DROP"].append(event["event_id"])

    total_events = max(len(events), 1)
    rate = (counts["OVERREACT_NO_RISK_CHANGE"] + counts["OVERREACT_RISK_NONE"]) / total_events

    return {"rate": round(rate, 4), "counts": counts, "top_examples": examples}
