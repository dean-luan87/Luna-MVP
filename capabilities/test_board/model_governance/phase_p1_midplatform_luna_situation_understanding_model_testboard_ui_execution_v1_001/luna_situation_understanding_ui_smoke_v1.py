# -*- coding: utf-8
"""Luna Situation Understanding — TestBoard UI execution smoke v1."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.situation_understanding.luna_situation_understanding_ui_payload_v1 import (
    FORBIDDEN_UI_COPY,
    audit_ui_copy,
    build_ui_payload_from_dryrun_result,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_model_dryrun_v1_001.luna_situation_understanding_dryrun_fixtures_v1 import (
    dryrun_case_a_job_564f1aa93983,
    dryrun_case_b_subway,
    dryrun_case_c_street,
    dryrun_case_d_corridor,
    dryrun_case_e_unknown,
    run_all_dryrun_cases,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_TESTBOARD_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_TESTBOARD_UI_EXECUTION_BLOCKED"

STATIC_REL = Path("capabilities/midplatform/model_test_lens/static_site")
JS_FILES = (
    STATIC_REL / "luna_situation_understanding_copy_v1.js",
    STATIC_REL / "luna_situation_understanding_state_v1.js",
    STATIC_REL / "luna_situation_understanding_panel_v1.js",
    STATIC_REL / "luna_situation_understanding_summary_v1.js",
    STATIC_REL / "luna_situation_understanding_trace_view_v1.js",
)


def _caps(payload: Dict[str, Any], bucket: str) -> List[str]:
    return payload.get("model_need_hint_summary", {}).get(bucket, [])


def _task_types(payload: Dict[str, Any]) -> List[str]:
    return [c["task_type"] for c in payload.get("task_clue_candidates", [])]


def _payload_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False)


def smoke_case_a_shopfront_ui() -> Dict[str, Any]:
    dryrun = dryrun_case_a_job_564f1aa93983()["dryrun"]
    payload = build_ui_payload_from_dryrun_result(dryrun)
    text = _payload_text(payload)
    passed = (
        payload["scene_profile_candidate"]["scene_type"] == "shopfront_sign"
        and payload["runner_scene_hint_evidence"].get("value") == "unknown_scene"
        and any(t.get("stage") == "runner_scene_hint_conflict" for t in payload.get("conflict_trace", []))
        and "read_text" in _task_types(payload)
        and "identify_place" in _task_types(payload)
        and "ocr" in _caps(payload, "likely_needed")
        and "slam" in _caps(payload, "not_needed")
        and "tracking" in _caps(payload, "not_needed")
        and "depth" in _caps(payload, "not_needed")
        and not audit_ui_copy(text)
        and payload.get("no_runner_invocation") is True
    )
    return {"case_id": "case_a_job_564f1aa93983_ui", "passed": passed, "ui_payload": payload}


def smoke_case_b_subway_ui() -> Dict[str, Any]:
    payload = build_ui_payload_from_dryrun_result(dryrun_case_b_subway()["dryrun"])
    passed = (
        payload["scene_profile_candidate"]["scene_type"] == "subway_platform"
        and "find_direction" in _task_types(payload)
        and "read_text" in _task_types(payload)
        and "ocr" in _caps(payload, "likely_needed")
        and "slam" in _caps(payload, "not_needed")
        and payload["not_fact"] is True
    )
    return {"case_id": "case_b_subway_ui", "passed": passed, "ui_payload": payload}


def smoke_case_c_street_ui() -> Dict[str, Any]:
    payload = build_ui_payload_from_dryrun_result(dryrun_case_c_street()["dryrun"])
    likely = _caps(payload, "likely_needed")
    passed = (
        payload["scene_profile_candidate"]["scene_type"] == "street_crossing"
        and "detection" in likely
        and "depth" in likely
        and "tracking" in likely
        and "ocr" not in likely
    )
    return {"case_id": "case_c_street_ui", "passed": passed, "ui_payload": payload}


def smoke_case_d_corridor_ui() -> Dict[str, Any]:
    payload = build_ui_payload_from_dryrun_result(dryrun_case_d_corridor()["dryrun"])
    passed = (
        payload["scene_profile_candidate"]["scene_type"] == "corridor"
        and "depth" in _caps(payload, "likely_needed")
        and "slam" in _caps(payload, "likely_needed")
        and "ocr" in _caps(payload, "not_needed")
    )
    return {"case_id": "case_d_corridor_ui", "passed": passed, "ui_payload": payload}


def smoke_case_e_unknown_ui() -> Dict[str, Any]:
    payload = build_ui_payload_from_dryrun_result(dryrun_case_e_unknown()["dryrun"])
    u = payload.get("uncertainty", {})
    passed = (
        payload["scene_profile_candidate"]["scene_type"] == "unknown_scene"
        and (u.get("needs_manual_review") or "ask_user" in u.get("fallback_suggestion", ""))
        and len(_caps(payload, "likely_needed")) == 0
    )
    return {"case_id": "case_e_unknown_ui", "passed": passed, "ui_payload": payload}


def smoke_case_f_static_audit(repo_root: Path) -> Dict[str, Any]:
    case_id = "case_f_ui_static_audit"
    failed: List[str] = []
    for js in JS_FILES:
        p = repo_root / js
        if not p.is_file():
            failed.append(f"missing:{js}")
    app = (repo_root / STATIC_REL / "app.js").read_text(encoding="utf-8") if (repo_root / STATIC_REL / "app.js").is_file() else ""
    index = (repo_root / STATIC_REL / "index.html").read_text(encoding="utf-8") if (repo_root / STATIC_REL / "index.html").is_file() else ""
    compact = (repo_root / STATIC_REL / "luna_observation_compact_ui_v1.js").read_text(encoding="utf-8") if (repo_root / STATIC_REL / "luna_observation_compact_ui_v1.js").is_file() else ""
    runner = ""
    runner_path = repo_root / "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    if runner_path.is_file():
        runner = runner_path.read_text(encoding="utf-8")

    panel_files = [
        repo_root / STATIC_REL / "luna_situation_understanding_panel_v1.js",
        repo_root / STATIC_REL / "luna_situation_understanding_summary_v1.js",
        repo_root / STATIC_REL / "luna_situation_understanding_trace_view_v1.js",
    ]
    user_facing = " ".join(p.read_text(encoding="utf-8") for p in panel_files if p.is_file())
    forbidden_in_ui = [f for f in FORBIDDEN_UI_COPY if f not in ("confirmed", "fact", "导航到") and f in user_facing]

    checks = {
        "js_files_exist": not any(f.startswith("missing:") for f in failed),
        "app_wired": "buildSituationPackage" in app and "situationPkg" in app,
        "index_wired": "luna_situation_understanding_panel_v1.js" in index,
        "compact_wired": "lol-right-situation-host" in compact and "LunaSituationUnderstandingPanel" in compact,
        "no_node_global": "require(" not in app and "process." not in " ".join(
            (repo_root / f).read_text(encoding="utf-8") for f in JS_FILES if (repo_root / f).is_file()
        ),
        "no_runner_mutation": "situation_understanding" not in runner,
        "no_boundary_clone": "cloneBoundary" not in user_facing,
        "no_forbidden_copy": not forbidden_in_ui,
    }
    for k, v in checks.items():
        if not v:
            failed.append(k)
    return {"case_id": case_id, "passed": not failed, "failed_checks": failed, "audit_checks": checks}


def run_smoke_cases(repo_root: Path | None = None) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    cases = [
        smoke_case_a_shopfront_ui(),
        smoke_case_b_subway_ui(),
        smoke_case_c_street_ui(),
        smoke_case_d_corridor_ui(),
        smoke_case_e_unknown_ui(),
        smoke_case_f_static_audit(root),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    job_a = next((c for c in cases if c.get("case_id") == "case_a_job_564f1aa93983_ui"), {})
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-TestBoard-UI-Execution-v1-001",
        "ui_execution_only": True,
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "job_564f1aa93983_ui_result": {
            "scene_type": job_a.get("ui_payload", {}).get("scene_profile_candidate", {}).get("scene_type"),
            "runner_hint": (job_a.get("ui_payload", {}) or {}).get("runner_scene_hint_evidence", {}).get("value"),
            "likely_needed": _caps(job_a.get("ui_payload", {}), "likely_needed"),
            "not_needed": _caps(job_a.get("ui_payload", {}), "not_needed"),
        },
        "dryrun_upstream_passed": run_all_dryrun_cases().get("final_decision", "").endswith("_GO"),
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
