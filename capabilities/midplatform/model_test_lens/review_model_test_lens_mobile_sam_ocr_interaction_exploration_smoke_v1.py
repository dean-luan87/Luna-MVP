# -*- coding: utf-8 -*-
"""MobileSAM → OCR route exploration smoke review v1."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


PHASE_ID = "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Exploration-Smoke-v1-001"
SMOKE_REL = (
    "capabilities/midplatform/model_test_lens/single_model_interaction_validation/"
    "mobile_sam_ocr_interaction_smoke_v1.py"
)
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"
UPSTREAM_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_UI_EXECUTION_GO"

FINAL_GO = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    SMOKE_REL,
    f"{_PKG}/run_mobile_sam_ocr_interaction_exploration_smoke_v1.py",
    f"{STATIC_REL}/multi_model_collaboration_panel_v1.js",
    f"{STATIC_REL}/multi_model_collaboration_copy_v1.js",
    f"{STATIC_REL}/multi_model_collaboration_state_v1.js",
    f"{_PKG}/review_model_test_lens_mobile_sam_ocr_interaction_exploration_smoke_v1.py",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bexecute_ocr\b|\bexecuteOcr\b", "ocr_runner_call"),
    (r"已识别文字|OCR结果|发现路牌|读取成功", "forbidden_ui_copy"),
    (r'"type"\s*:\s*"sign"', "sign_fact_label"),
    (r'"text"\s*:\s*"[^"]{2,}"', "text_fact_generation"),
)

NEGATIVE_GUARDS: Tuple[Tuple[str, str], ...] = (
    ("A", "no_ocr_runner_call"),
    ("B", "no_ocr_execution"),
    ("C", "no_fact_write"),
    ("D", "no_text_fact_generation"),
    ("E", "no_mobile_sam_direct_to_ocr"),
    ("F", "no_bypass_midplatform"),
    ("G", "ocr_task_requires_route_candidate"),
    ("H", "ocr_task_traceable_to_region"),
    ("I", "candidate_only_preserved"),
    ("J", "human_correction_not_ground_truth"),
    ("K", "case_a_passes"),
    ("L", "case_b_passes"),
    ("M", "case_c_passes"),
    ("N", "smoke_processor_defined"),
    ("O", "ui_collaboration_wired"),
    ("P", "upstream_ui_execution_go"),
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _run_smoke() -> Dict[str, Any]:
    script = _detect_repo_root() / _PKG / "run_mobile_sam_ocr_interaction_exploration_smoke_v1.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(_detect_repo_root()),
    )
    path = (
        _detect_repo_root()
        / "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_interaction_exploration_smoke_v0"
        / "mobile_sam_ocr_interaction_exploration_smoke_v1.json"
    )
    data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    data["exit_code"] = proc.returncode
    return data


def _audit(smoke: Dict[str, Any]) -> Dict[str, bool]:
    processor = _read(SMOKE_REL)
    panel = _read(f"{STATIC_REL}/multi_model_collaboration_panel_v1.js")
    app = _read(f"{STATIC_REL}/app.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    index = _read(f"{STATIC_REL}/index.html")

    upstream = _load_json(
        "_tmp_eval_out/p1_midplatform_single_model_interaction_validation_ui_execution_v1_smoke_v0/"
        "p1_midplatform_single_model_interaction_validation_ui_execution_review_v1.json"
    )

    case_a = smoke.get("case_a") or {}
    case_b = smoke.get("case_b") or {}
    case_c = smoke.get("case_c") or {}
    task_a = case_a.get("ocr_task_candidate") or {}

    return {
        "smoke_processor_defined": "process_segmentation_envelope_for_ocr_route" in processor,
        "no_ocr_runner_call": "ocr_runner_forbidden" in processor and "no_ocr_execution" in processor,
        "no_ocr_execution": case_c.get("no_ocr_execution") is True and case_a.get("no_ocr_execution") is True,
        "no_fact_write": "not_fact" in processor and "needs_fact_admission" in processor,
        "no_text_fact_generation": "no_text_fact_generation" in processor,
        "no_mobile_sam_direct_to_ocr": "midplatform_schedules_not_pipeline" not in processor
        or "evaluate_text_likely_region" in processor,
        "no_bypass_midplatform": "Midplatform Analysis" in processor or "midplatform_analysis_record" in processor,
        "ocr_task_requires_route_candidate": (
            case_a.get("followup_model_route_candidate") is not None
            and case_a.get("ocr_task_candidate") is not None
        ),
        "ocr_task_traceable_to_region": bool(
            task_a.get("source_region_id")
            and task_a.get("source_result_candidate_id")
            and task_a.get("source_analysis_record_id")
        ),
        "candidate_only_preserved": smoke.get("checks", {}).get("candidate_only_preserved", False),
        "human_correction_not_ground_truth": "human_correction_not_ground_truth" in processor,
        "case_a_passes": smoke.get("checks", {}).get("case_a_ocr_route", False),
        "case_b_passes": smoke.get("checks", {}).get("case_b_no_ocr_task", False),
        "case_c_passes": smoke.get("checks", {}).get("case_c_priority_signal", False),
        "ui_collaboration_wired": (
            "MultiModelCollaborationPanel" in compact
            and "lol-right-collaboration-host" in compact
            and "buildCollaborationPackage" in app
            and "multi_model_collaboration_panel_v1.js" in index
        ),
        "upstream_ui_execution_go": upstream.get("final_decision") == UPSTREAM_UI_GO,
    }


def review(*, write_file: bool = True) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    smoke = _run_smoke()
    bundle = _read(SMOKE_REL)
    violations = [pid for pat, pid in FORBIDDEN if pid not in ("forbidden_ui_copy",) and re.search(pat, bundle, re.I)]

    flags = _audit(smoke)
    guards = []
    for gid, key in NEGATIVE_GUARDS:
        passed = bool(flags.get(key, False))
        guards.append({"guard_id": gid, "key": key, "passed": passed})
        if not passed:
            failed.append(f"guard.{gid}.fail={key}")

    if smoke.get("final_decision") != FINAL_GO:
        failed.append("smoke.final_decision_not_go")
    if smoke.get("exit_code", 1) != 0:
        failed.append("smoke.exit_code_nonzero")

    ng_passed = sum(1 for g in guards if g["passed"])
    decision = FINAL_GO if not failed and not violations else FINAL_BLOCKED

    out_dir = _detect_repo_root() / "_tmp_eval_out" / "p1_midplatform_mobile_sam_ocr_interaction_exploration_smoke_v0"
    out_dir.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "exploration_smoke": True,
        "ocr_runner_forbidden": True,
        "smoke_report": smoke,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": ng_passed,
        "negative_guard_count": len(guards),
        "forbidden_violations": violations,
        "failed_checks": failed + [f"forbidden.{v}" for v in violations],
        "blocker_count": len(failed) + len(violations),
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }

    if write_file:
        rp = out_dir / "mobile_sam_ocr_interaction_exploration_smoke_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    return result


def main() -> int:
    r = review()
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
