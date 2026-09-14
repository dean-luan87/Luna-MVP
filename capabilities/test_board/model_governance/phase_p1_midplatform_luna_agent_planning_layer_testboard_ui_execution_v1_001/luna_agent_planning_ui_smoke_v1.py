# -*- coding: utf-8
"""Luna Agent Planning Layer — TestBoard UI execution smoke v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.agent_planning.luna_agent_planning_dryrun_adapter_v1 import (
    run_agent_planning_dryrun,
)
from capabilities.midplatform.agent_planning.luna_agent_planning_ui_payload_v1 import (
    FORBIDDEN_UI_COPY,
    audit_ui_copy,
    build_ui_payload_from_agent_planning_dryrun,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    dryrun_case_a_shopfront,
    dryrun_case_d_user_goal_override,
    run_all_dryrun_cases,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_model_dryrun_v1_001.luna_situation_understanding_dryrun_fixtures_v1 import (
    fixture_unknown_scene_low_evidence,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_TESTBOARD_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_TESTBOARD_UI_EXECUTION_BLOCKED"

STATIC_REL = Path("capabilities/midplatform/model_test_lens/static_site")
JS_FILES = (
    STATIC_REL / "luna_agent_planning_copy_v1.js",
    STATIC_REL / "luna_agent_planning_state_v1.js",
    STATIC_REL / "luna_agent_planning_panel_v1.js",
    STATIC_REL / "luna_agent_planning_summary_v1.js",
    STATIC_REL / "luna_agent_planning_trace_view_v1.js",
)


def _active(payload: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in (payload.get("tool_plan") or {}).get("active", [])]


def _noop(payload: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in (payload.get("tool_plan") or {}).get("noop", [])]


def _selected_goal(payload: Dict[str, Any]) -> str:
    return (payload.get("selected_plan") or {}).get("goal_type", "")


def _selected_card(payload: Dict[str, Any]) -> Dict[str, Any]:
    for c in payload.get("plan_competition_cards") or []:
        if c.get("status") == "selected":
            return c
    return {}


def _payload_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False)


def smoke_case_a_shopfront_ui() -> Dict[str, Any]:
    """Case A: shopfront → OCR plan selected · SLAM noop."""
    dryrun = dryrun_case_a_shopfront()["result"]
    payload = build_ui_payload_from_agent_planning_dryrun(dryrun)
    text = _payload_text(payload)
    scene = (payload.get("situation_summary") or {}).get("scene_type")
    goal = _selected_goal(payload)
    active = _active(payload)
    noops = _noop(payload)
    selected = _selected_card(payload)
    chain = [s.get("stage") for s in payload.get("chain_trace") or []]
    passed = (
        scene == "shopfront_sign"
        and goal in ("identify_place", "read_text")
        and "ocr" in active
        and "slam" in noops
        and "tracking" in noops
        and "depth" in noops
        and selected.get("status") == "selected"
        and len(payload.get("plan_competition_cards") or []) >= 2
        and len(payload.get("goal_candidates") or []) >= 1
        and payload.get("selection_reason", {}).get("final_label")
        and "L2_PlanCompetition" in chain
        and "L3_ToolOSHandoff" in chain
        and (payload.get("tool_os_handoff") or {}).get("not_executed") is True
        and payload.get("candidate_only") is True
        and payload.get("not_fact") is True
        and not audit_ui_copy(text)
    )
    return {
        "case_id": "case_a_shopfront_ocr_selected_ui",
        "passed": passed,
        "ui_payload": payload,
        "assertions": {
            "scene_shopfront": scene == "shopfront_sign",
            "ocr_selected": "ocr" in active and goal in ("identify_place", "read_text"),
            "slam_noop": "slam" in noops,
        },
    }


def smoke_case_b_user_nav_override_ui() -> Dict[str, Any]:
    """Case B: user find-entrance overrides shopfront OCR-default → Navigation selected."""
    dryrun = dryrun_case_d_user_goal_override()["result"]
    payload = build_ui_payload_from_agent_planning_dryrun(dryrun)
    scene = (payload.get("situation_summary") or {}).get("scene_type")
    goal = _selected_goal(payload)
    active = _active(payload)
    cards = payload.get("plan_competition_cards") or []
    nav_card = next((c for c in cards if c.get("goal_type") == "navigate"), {})
    ocr_card = next(
        (c for c in cards if c.get("goal_type") in ("identify_place", "read_text")),
        {},
    )
    nav_score = float(nav_card.get("score") or 0)
    ocr_score = float(ocr_card.get("score") or 0)
    ocr_first = goal in ("read_text", "identify_place") and active == ["ocr"]
    passed = (
        scene == "shopfront_sign"
        and goal == "navigate"
        and ("detection" in active or "depth" in active)
        and not ocr_first
        and nav_score >= ocr_score
        and _selected_card(payload).get("goal_type") == "navigate"
        and payload.get("not_fact") is True
    )
    return {
        "case_id": "case_b_user_nav_override_ui",
        "passed": passed,
        "ui_payload": payload,
        "assertions": {
            "user_goal_overrides_visual_default": goal == "navigate" and scene == "shopfront_sign",
            "navigation_score_ge_ocr": nav_score >= ocr_score,
            "not_ocr_first": not ocr_first,
        },
    }


def smoke_case_c_unknown_ask_user_ui() -> Dict[str, Any]:
    """Case C: unknown_scene → Ask user · no blanket model activation."""
    dryrun = run_agent_planning_dryrun(fixture_unknown_scene_low_evidence())
    payload = build_ui_payload_from_agent_planning_dryrun(dryrun)
    scene = (payload.get("situation_summary") or {}).get("scene_type")
    goal = _selected_goal(payload)
    active = _active(payload)
    cards = payload.get("plan_competition_cards") or []
    ask_selected = _selected_card(payload).get("goal_type") == "ask_user"
    # Must not activate slam/detection/tracking/depth/ocr as blanket tools
    blanket = {"slam", "detection", "tracking", "depth", "ocr"}
    active_set = set(active)
    passed = (
        scene == "unknown_scene"
        and goal == "ask_user"
        and ask_selected
        and not (active_set & blanket)  # no perception blanket
        and (not active or active_set <= {"vlm"})  # optional VLM advisor only
        and payload.get("selection_reason", {}).get("final_label")
        and payload.get("candidate_only") is True
        and len(cards) >= 1
    )
    return {
        "case_id": "case_c_unknown_ask_user_ui",
        "passed": passed,
        "ui_payload": payload,
        "assertions": {
            "ask_user_selected": goal == "ask_user",
            "no_blanket_activation": not (active_set & blanket),
            "vlm_advisor_optional_only": active_set <= {"vlm"},
        },
    }


def smoke_case_d_static_audit(repo_root: Path) -> Dict[str, Any]:
    case_id = "case_d_ui_static_audit"
    failed: List[str] = []
    for js in JS_FILES:
        p = repo_root / js
        if not p.is_file():
            failed.append(f"missing:{js}")

    app = (repo_root / STATIC_REL / "app.js").read_text(encoding="utf-8") if (repo_root / STATIC_REL / "app.js").is_file() else ""
    index = (repo_root / STATIC_REL / "index.html").read_text(encoding="utf-8") if (repo_root / STATIC_REL / "index.html").is_file() else ""
    compact = (
        (repo_root / STATIC_REL / "luna_observation_compact_ui_v1.js").read_text(encoding="utf-8")
        if (repo_root / STATIC_REL / "luna_observation_compact_ui_v1.js").is_file()
        else ""
    )
    styles = (repo_root / STATIC_REL / "styles.css").read_text(encoding="utf-8") if (repo_root / STATIC_REL / "styles.css").is_file() else ""
    payload_py = (
        (repo_root / "capabilities/midplatform/agent_planning/luna_agent_planning_ui_payload_v1.py").read_text(encoding="utf-8")
        if (repo_root / "capabilities/midplatform/agent_planning/luna_agent_planning_ui_payload_v1.py").is_file()
        else ""
    )

    panel_files = [
        repo_root / STATIC_REL / "luna_agent_planning_panel_v1.js",
        repo_root / STATIC_REL / "luna_agent_planning_summary_v1.js",
        repo_root / STATIC_REL / "luna_agent_planning_trace_view_v1.js",
    ]
    # copy.js lists forbiddenParts for runtime guard — exclude that file from phrase scan
    user_facing = " ".join(p.read_text(encoding="utf-8") for p in panel_files if p.is_file())
    copy_path = repo_root / STATIC_REL / "luna_agent_planning_copy_v1.js"
    if copy_path.is_file():
        copy_text = copy_path.read_text(encoding="utf-8")
        # Only scan display strings outside forbiddenParts array
        cut = copy_text.find("forbiddenParts")
        user_facing += " " + (copy_text[:cut] if cut >= 0 else copy_text)
    forbidden_in_ui = [f for f in FORBIDDEN_UI_COPY if f in user_facing]

    js_bundle = " ".join(
        (repo_root / f).read_text(encoding="utf-8") for f in JS_FILES if (repo_root / f).is_file()
    )

    checks = {
        "js_files_exist": not any(f.startswith("missing:") for f in failed),
        "ui_payload_builder_present": "build_ui_payload_from_agent_planning_dryrun" in payload_py,
        "app_wired": "buildAgentPlanningPackage" in app and "agentPlanningPkg" in app,
        "index_wired": "luna_agent_planning_panel_v1.js" in index,
        "compact_wired": (
            "lol-right-agent-planning-host" in compact
            and "LunaAgentPlanningPanel" in compact
            and "LunaAgentPlanningSummary" in compact
        ),
        "styles_present": ".lap-panel" in styles and ".lap-plan-card" in styles,
        "no_node_global": "require(" not in js_bundle and "process." not in js_bundle,
        "no_network_fetch": "fetch(" not in js_bundle and "XMLHttpRequest" not in js_bundle,
        "no_forbidden_copy": not forbidden_in_ui,
        "candidate_governance": "candidate_only" in user_facing and "selected_plan_candidate" in user_facing,
        "explainable_chain": "L1" in user_facing or "PlanCompetition" in js_bundle or "决策链" in user_facing,
    }
    for k, v in checks.items():
        if not v:
            failed.append(k)
    return {"case_id": case_id, "passed": not failed, "failed_checks": failed, "audit_checks": checks}


def run_smoke_cases(repo_root: Path | None = None) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    cases = [
        smoke_case_a_shopfront_ui(),
        smoke_case_b_user_nav_override_ui(),
        smoke_case_c_unknown_ask_user_ui(),
        smoke_case_d_static_audit(root),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    job_a = next((c for c in cases if c.get("case_id") == "case_a_shopfront_ocr_selected_ui"), {})
    payload_a = job_a.get("ui_payload") or {}
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-TestBoard-UI-Execution-v1-001",
        "ui_execution_only": True,
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "job_564f1aa93983_ui_result": {
            "scene_type": (payload_a.get("situation_summary") or {}).get("scene_type"),
            "selected_goal": _selected_goal(payload_a),
            "active_tools": _active(payload_a),
            "noop_tools": _noop(payload_a),
            "competition_slots": len(payload_a.get("plan_competition_cards") or []),
            "handoff_not_executed": (payload_a.get("tool_os_handoff") or {}).get("not_executed"),
        },
        "dryrun_upstream_passed": run_all_dryrun_cases().get("final_decision", "").endswith("_GO"),
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
