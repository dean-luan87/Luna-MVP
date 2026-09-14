"""
Phase-EngineeringFlow-003

SceneContext Gates Minimal Offline Runtime v0.

Hard boundaries:
- Offline evaluation only (phone_local controlled capture).
- Produces gate results + gated perception candidates only.
- Does NOT produce task/fusion/output candidates.
- Never enables execute/default-on/side effects; allows_execute_now must be false.
- Evidence boundary must be preserved (evidence_type unchanged; controlled_live_stream remains false).
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


FORBIDDEN_TOKENS_V0: Tuple[str, ...] = (
    "execute_now",
    "walk_now",
    "turn_now",
    "cross_now",
    "force_action",
    "release_side_effects",
    "retry_now",
    "reopen_now",
    "enable_default_path",
    "override_governance",
    "final_navigation_instruction",
    "actual_tts",
)


def _now_ts() -> float:
    return float(time.time())


def _forbidden_scan(obj: Any) -> Dict[str, Any]:
    try:
        hay = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    except Exception:
        hay = repr(obj)
    low = hay.lower()
    hits: List[str] = []
    for tok in FORBIDDEN_TOKENS_V0:
        pat = re.compile(rf"(^|[^a-z0-9_]){re.escape(tok)}([^a-z0-9_]|$)")
        if pat.search(low) is not None:
            hits.append(tok)
    return {"pass": len(hits) == 0, "hits": hits}


@dataclass(frozen=True)
class OfflineSceneContextGateConfigV0:
    gate_version: str = "v0"
    # v0 is minimal; allow optional test hint injection via per-sample metadata
    allow_test_hints: bool = True


def visual_medium_gate_v0(*, sample: Dict[str, Any], cfg: OfflineSceneContextGateConfigV0) -> Dict[str, Any]:
    """
    Minimal Visual Medium / Depicted Scene gate.
    v0 behavior:
    - Defaults to no medium detected (since no OCR/medium detector wired).
    - If a test hint is provided, blocks macro transitions + task triggers.
    """
    ts = _now_ts()
    reason: List[str] = ["visual_medium_gate_v0", "candidate_only"]

    hint = None
    if cfg.allow_test_hints:
        hint = (sample.get("scene_context_test_hint") or {}).get("visual_medium_type")

    detected = False
    medium_type = "unknown"
    depicted_blocked = False
    task_trigger_allowed = True
    macro_transition_allowed = True
    depicted_scene_candidate = None

    if isinstance(hint, str) and hint in {"poster", "screen", "ad", "photo", "mirror", "glass_reflection", "book_cover"}:
        detected = True
        medium_type = hint
        depicted_blocked = True
        task_trigger_allowed = False
        macro_transition_allowed = False
        depicted_scene_candidate = {"status": "depicted_scene", "medium_type": hint}
        reason.append("depicted_scene_blocked")
    else:
        reason.append("no_medium_signal_available_v0")

    return {
        "gate_status": "ok",
        "visual_medium_detected": detected,
        "visual_medium_type": medium_type,
        "depicted_scene_candidate": depicted_scene_candidate,
        "depicted_scene_blocked": depicted_blocked,
        "task_trigger_allowed": task_trigger_allowed,
        "macro_scene_transition_allowed": macro_transition_allowed,
        "reason_codes": reason,
        "ts": ts,
    }


def physics_consistency_gate_v0(*, sample: Dict[str, Any], cfg: OfflineSceneContextGateConfigV0) -> Dict[str, Any]:
    """
    Minimal physics gate. Since no depth/motion/tracking is wired in v0, must be conservative:
    - depth_status=not_available
    - motion_status=not_available
    - collision_risk_status=not_confirmed
    - physical_plausibility=uncertain
    """
    ts = _now_ts()
    reason = ["physics_consistency_gate_v0", "candidate_only", "depth_not_available", "motion_not_available"]
    return {
        "gate_status": "ok",
        "physical_plausibility": "uncertain",
        "consistency_level": "not_available",
        "depth_status": "not_available",
        "motion_status": "not_available",
        "passability_geometry_status": "not_available",
        "collision_risk_status": "not_confirmed",
        "conflict_detected": False,
        "conflict_type": "none",
        "recommended_handling": "degrade_or_collect_more_evidence",
        "reason_codes": reason,
        "ts": ts,
    }


def scene_continuity_zone_gate_v0(
    *,
    sample: Dict[str, Any],
    prev: Optional[Dict[str, Any]],
    visual_medium_gate: Dict[str, Any],
    physics_gate: Dict[str, Any],
    cfg: OfflineSceneContextGateConfigV0,
) -> Dict[str, Any]:
    """
    Minimal continuity/zone reasoning:
    - Does not confirm macro_scene unless sufficient evidence (v0: never confirms).
    - Uses conservative candidates: outdoor_sidewalk + sidewalk_path when compatible.
    - If depicted_scene blocked, do NOT allow macro transition.
    """
    ts = _now_ts()
    reason = ["scene_continuity_zone_gate_v0", "candidate_only"]

    prev_macro = "unknown"
    if isinstance(prev, dict):
        prev_macro = str(prev.get("macro_scene_confirmed") or prev.get("previous_macro_scene") or "unknown")

    evidence_type = str(sample.get("evidence_type") or "unknown")
    controlled_live = bool(sample.get("controlled_live_stream") is True)
    depicted_blocked = bool(visual_medium_gate.get("depicted_scene_blocked") is True)

    macro_candidate = "unknown"
    zone_candidate = "unknown"
    if (evidence_type == "phone_local_controlled_capture") and (not controlled_live):
        macro_candidate = "outdoor_sidewalk"
        zone_candidate = "sidewalk_path"
        reason.append("phone_local_outdoor_sidewalk_candidate")

    transition_allowed = bool(visual_medium_gate.get("macro_scene_transition_allowed") is True)
    if depicted_blocked:
        transition_allowed = False
        reason.append("depicted_scene_blocks_transition")

    degraded = True  # v0 conservative default
    requires_more = True

    return {
        "gate_status": "ok",
        "previous_macro_scene": prev_macro,
        "macro_scene_candidate": macro_candidate,
        "macro_scene_confirmed": False,
        "zone_type_candidate": zone_candidate,
        "zone_update_allowed": True if zone_candidate != "unknown" else False,
        "macro_scene_transition_state": "blocked" if not transition_allowed else "not_confirmed_v0",
        "requires_more_evidence": requires_more,
        "degraded_or_uncertain": degraded,
        "reason_codes": reason,
        "ts": ts,
    }


def run_offline_scene_context_gates_v0(
    *,
    perception_sample: Dict[str, Any],
    prev_scene_context: Optional[Dict[str, Any]],
    cfg: Optional[OfflineSceneContextGateConfigV0] = None,
) -> Dict[str, Any]:
    """
    Entry point: takes one PerceptionEval per-sample result dict and returns gate result + gated perception.
    """
    cfg = cfg or OfflineSceneContextGateConfigV0()
    ts0 = _now_ts()

    # Evidence boundary invariants (hard)
    hard_blockers: List[str] = []
    evidence_type = perception_sample.get("evidence_type")
    if evidence_type != "phone_local_controlled_capture":
        hard_blockers.append("evidence_type_mismatch")
    if perception_sample.get("controlled_live_stream") is not False:
        hard_blockers.append("controlled_live_stream_not_false")
    if perception_sample.get("phone_local_capture") is not True:
        hard_blockers.append("phone_local_capture_not_true")
    if perception_sample.get("pending_real_sidewalk_run") is not True:
        hard_blockers.append("pending_real_sidewalk_run_not_true")

    vm = visual_medium_gate_v0(sample=perception_sample, cfg=cfg)
    ph = physics_consistency_gate_v0(sample=perception_sample, cfg=cfg)
    sc = scene_continuity_zone_gate_v0(sample=perception_sample, prev=prev_scene_context, visual_medium_gate=vm, physics_gate=ph, cfg=cfg)

    # Gate result: v0 always candidate-only; never allows execute.
    gated_status = "ok" if not hard_blockers else "blocked"
    gated_allowed_downstream = (gated_status == "ok") and (vm.get("task_trigger_allowed") is True)

    overall = {
        "gated_result_status": gated_status,
        "scene_context_gate_required": True,
        "gated_perception_allowed_downstream": bool(gated_allowed_downstream),
        "candidate_only": True,
        "allows_execute_now": False,
        "hard_blockers": hard_blockers,
        "soft_followups": ["scene_context_minimal_v0"],
        "ts": ts0,
    }

    # Forbidden scan on emitted structure
    # Include test hints in scan payload to ensure execute-probe fixtures are blocked.
    test_hint = perception_sample.get("scene_context_test_hint") if cfg.allow_test_hints else None
    forb = _forbidden_scan(
        {
            "visual_medium_gate": vm,
            "physics_gate": ph,
            "scene_continuity_zone_gate": sc,
            "overall": overall,
            "scene_context_test_hint": test_hint,
        }
    )
    if not bool(forb.get("pass") is True):
        overall["gated_result_status"] = "blocked"
        overall["gated_perception_allowed_downstream"] = False
        overall["hard_blockers"] = list(overall.get("hard_blockers") or []) + ["forbidden_output_blocked"]

    gated_perception = {
        "source_policy_id": perception_sample.get("source_policy_id"),
        "source_selected": perception_sample.get("source_selected"),
        "signals": perception_sample.get("signals"),
        "signal_presence": perception_sample.get("signal_presence"),
        "candidate_only": True,
        "allows_execute_now": False,
        "real_tts_invoked": False,
    }

    return {
        "sample_id": perception_sample.get("sample_id"),
        "source_perception_result_id": perception_sample.get("sample_id"),
        "source_policy_id": perception_sample.get("source_policy_id"),
        "source_selected": perception_sample.get("source_selected"),
        "evidence_type": evidence_type,
        "controlled_live_stream": perception_sample.get("controlled_live_stream"),
        "phone_local_capture": perception_sample.get("phone_local_capture"),
        "pending_real_sidewalk_run": perception_sample.get("pending_real_sidewalk_run"),
        "scene_context_test_hint": test_hint,
        "visual_medium_gate": vm,
        "physics_consistency_gate": ph,
        "scene_continuity_zone_gate": sc,
        "overall_gate_result": overall,
        "forbidden_output_scan_result": forb,
        "gated_perception_result": gated_perception,
    }

