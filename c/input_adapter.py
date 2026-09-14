from typing import Any, Dict

from c.types import CInput


def build_c_input(system_snapshot: Dict[str, Any]) -> CInput:
    health = system_snapshot.get("health", {})
    perception_health = health.get("perception", "ok")

    facts = system_snapshot.get("perception_facts", {})
    navigation = system_snapshot.get("navigation_state", {})

    obstacle_distance_m = facts.get("obstacle_distance")
    human_proximity_m = facts.get("human_proximity_m")
    traffic_light = facts.get("traffic_light")
    crosswalk_signal = facts.get("crosswalk_signal")
    passage_state = navigation.get("passage_state")
    floor_state = navigation.get("floor_state")
    facility_state = navigation.get("facility_state")

    confidence = facts.get("confidence", {})
    device_state = system_snapshot.get("device_state", {})

    return CInput(
        perception_health=str(perception_health),
        obstacle_distance_m=obstacle_distance_m,
        human_proximity_m=human_proximity_m,
        traffic_light=traffic_light,
        crosswalk_signal=crosswalk_signal,
        passage_state=passage_state,
        floor_state=floor_state,
        facility_state=facility_state,
        confidence=dict(confidence) if isinstance(confidence, dict) else {},
        device_state=dict(device_state) if isinstance(device_state, dict) else {},
    )
