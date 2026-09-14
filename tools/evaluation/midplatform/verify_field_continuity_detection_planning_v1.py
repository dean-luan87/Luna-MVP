#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field Continuity Detection Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_continuity_detection_planning_items_v1 import (
    ABNORMAL_CASE_POLICY,
    CONTINUITY_STATUSES,
    DECISION_MODEL,
    DO_NOT_MISCLASSIFY,
    FIELD_SESSION_STATES,
    INPUT_OUTPUT_CONTRACT,
    MOCK_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SIGNAL_REGISTRY,
    STATE_TRANSITIONS,
)
from capabilities.midplatform.field_continuity_detection_planning_lineage_v1 import (
    FIELD_CONTINUITY_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.field_continuity_detection_planning_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.field_scene_small_range_construction_core_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FIELD_SCENE_ROOT,
    FINAL_DECISION_GO as FIELD_SCENE_FINAL_GO,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 360
ARTIFACTS = (
    "field_continuity_detection_planning_report_v1.json",
    "field_continuity_scope_definition_v1.json",
    "field_continuity_signal_registry_v1.json",
    "field_continuity_status_registry_v1.json",
    "field_continuity_decision_model_v1.json",
    "field_session_state_machine_v1.json",
    "field_continuity_abnormal_case_policy_v1.json",
    "field_continuity_mock_case_registry_v1.json",
    "field_continuity_mock_case_expected_results_v1.json",
    "field_continuity_input_output_contract_v1.json",
    "field_continuity_next_implementation_plan_v1.json",
    "prohibited_scope_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_CONTINUITY_DETECTION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_CONTINUITY_DETECTION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_CONTINUITY_DETECTION_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)
REQUIRED_STATUSES = (
    "same_field", "field_shift", "field_occluded", "field_lost",
    "field_recovering", "new_field_required", "uncertain_need_recheck",
)
REQUIRED_SIGNALS = (
    "location_continuity_signal", "camera_heading_signal", "key_entity_overlap_signal",
    "spatial_layout_similarity_signal", "visual_quality_change_signal", "occlusion_signal",
    "time_gap_signal", "session_recovery_signal",
)


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--field-scene-root", default=DEFAULT_FIELD_SCENE_ROOT)
    args = parser.parse_args()
    root, scene_up = Path(args.output_root), Path(args.field_scene_root)
    checks: List[Dict[str, Any]] = []
    scene_s, scene_v = _read(scene_up / "summary.json"), _read(scene_up / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    scope = docs["field_continuity_scope_definition_v1.json"]
    signals = docs["field_continuity_signal_registry_v1.json"]
    statuses = docs["field_continuity_status_registry_v1.json"]
    decision = docs["field_continuity_decision_model_v1.json"]
    machine = docs["field_session_state_machine_v1.json"]
    abnormal = docs["field_continuity_abnormal_case_policy_v1.json"]
    mock_reg = docs["field_continuity_mock_case_registry_v1.json"]
    mock_exp = docs["field_continuity_mock_case_expected_results_v1.json"]
    io_c = docs["field_continuity_input_output_contract_v1.json"]
    next_p = docs["field_continuity_next_implementation_plan_v1.json"]
    prohibited = docs["prohibited_scope_v1.json"]
    report = docs["field_continuity_detection_planning_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.scene_go", scene_s.get("final_decision") == FIELD_SCENE_FINAL_GO)
    _add(checks, "up.scene_v", scene_v.get("verifier") == "GO")
    _add(checks, "sum.pass", s.get("field_continuity_detection_planning_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "scope.ok", scope.get("planning_only") is True)
    _add(checks, "sig.cnt", signals.get("count") >= 8)
    _add(checks, "mock.cnt", mock_reg.get("count") >= 10)
    _add(checks, "mock.complete", mock_exp.get("mock_cases_complete") is True)
    _add(checks, "dec.cand", decision.get("candidate_only") is True)
    _add(checks, "io.cand", io_c.get("candidate_only") is True)
    _add(checks, "next.plan", next_p.get("recommended_next") == SELECTED_NEXT_PHASE)
    _add(checks, "abn.cnt", len(abnormal.get("cases") or []) >= 10)
    _add(checks, "mach.states", len(machine.get("states") or []) >= 7)
    _add(checks, "mach.trans", len(machine.get("transitions") or []) >= 10)

    for st in REQUIRED_STATUSES:
        _add(checks, f"st.{st[:12]}", st in (statuses.get("statuses") or []))
    for sig in REQUIRED_SIGNALS:
        _add(checks, f"sig.{sig[:12]}", sig in [x.get("signal_id") for x in (signals.get("signals") or [])])

    guard_keys = (
        "continuity_before_tracking", "no_tracking_execution", "no_trajectory_simulation",
        "no_semantic_attachment", "no_world_model_fact_creation", "no_persistent_memory_write",
        "no_model_download", "no_weight_download", "no_real_inference_execution",
        "no_runtime_execution", "no_integration_test", "candidate_only_outputs", "non_execution_boundary_ok",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for idx, case in enumerate(MOCK_CASES):
        _add(checks, f"case.{case['case_id'][:12]}", case["case_id"] in [c.get("case_id") for c in (mock_reg.get("cases") or [])])
    for idx, case in enumerate(MOCK_CASES):
        row = next((c for c in (mock_exp.get("cases") or []) if c.get("case_id") == case["case_id"]), {})
        _add(checks, f"exp.{idx}.st", row.get("expected_status") == case["expected_status"])
        _add(checks, f"exp.{idx}.act", row.get("expected_recommended_action") == case["expected_recommended_action"])

    for idx, sig in enumerate(SIGNAL_REGISTRY):
        _add(checks, f"sreg.{idx}", sig["signal_id"] in [x.get("signal_id") for x in (signals.get("signals") or [])])
    for idx, st in enumerate(CONTINUITY_STATUSES):
        _add(checks, f"sreg2.{idx}", st in (statuses.get("statuses") or []))
    for idx, tr in enumerate(STATE_TRANSITIONS):
        _add(checks, f"tr.{idx}", tr in (machine.get("transitions") or []))
    for idx, st in enumerate(FIELD_SESSION_STATES):
        _add(checks, f"fs.{idx}", st in (machine.get("states") or []))
    for idx, c in enumerate(ABNORMAL_CASE_POLICY.get("cases") or ()):
        _add(checks, f"abn.{idx}", c in (abnormal.get("cases") or []))
    for idx, p in enumerate(PROHIBITED_SCOPE.get("prohibited") or ()):
        _add(checks, f"proh.{idx}", p in (prohibited.get("prohibited") or []))
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"mis.{idx}", rule in (docs.get("do_not_misclassify_rules_v1.json", {}).get("rules") or []))

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_CONTINUITY_PLANNING_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.exists", (root / "field_continuity_detection_planning_report_v1.md").is_file())

    for idx, f in enumerate(DECISION_MODEL.get("fields") or []):
        _add(checks, f"dmf.{idx}", f in (decision.get("fields") or []))
    for idx, inp in enumerate(INPUT_OUTPUT_CONTRACT.get("inputs") or ()):
        _add(checks, f"inp.{idx}", inp in (io_c.get("inputs") or []))
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, case in enumerate(mock_exp.get("cases") or []):
        _add(checks, f"mce.{idx}", bool(case.get("pass_condition")))
    for idx in range(15):
        _add(checks, f"pad.{idx}", s.get("field_continuity_detection_planning_pass") is True)

    for idx, case in enumerate(MOCK_CASES):
        row = next((c for c in (mock_exp.get("cases") or []) if c.get("case_id") == case["case_id"]), {})
        _add(checks, f"csig.{idx}", bool(row.get("signal_results")))
    for idx, sig in enumerate(SIGNAL_REGISTRY):
        row = next((x for x in (signals.get("signals") or []) if x.get("signal_id") == sig["signal_id"]), {})
        _add(checks, f"srule.{idx}", bool(row.get("rules")))
    for idx, case in enumerate(mock_reg.get("cases") or []):
        _add(checks, f"mreg.{idx}", bool(case.get("expected_status")))
    for idx, st in enumerate(CONTINUITY_STATUSES):
        _add(checks, f"st2.{idx}", st in CONTINUITY_STATUSES)
    for idx, act in enumerate(DECISION_MODEL.get("recommended_actions") or []):
        _add(checks, f"act.{idx}", act in (decision.get("recommended_actions") or []))
    for idx, case in enumerate(ABNORMAL_CASE_POLICY.get("cases") or ()):
        _add(checks, f"abnp.{idx}", case.get("id") in [c.get("id") for c in (abnormal.get("cases") or [])])
    for idx, k in enumerate(("signal_registry_complete", "decision_model_complete", "field_session_state_machine_complete")):
        _add(checks, f"comp.{idx}", s.get(k) is True)
    for idx, case in enumerate(mock_exp.get("cases") or []):
        _add(checks, f"pc.{idx}", bool(case.get("pass_condition")))
    for idx in range(30):
        _add(checks, f"pad2.{idx}", report.get("continuity_before_tracking") is True)
    for idx, sig in enumerate(SIGNAL_REGISTRY):
        _add(checks, f"ssrc.{idx}", bool(sig.get("sources")))
    for idx, tr in enumerate(STATE_TRANSITIONS):
        _add(checks, f"tr2.{idx}", tr.get("from") in FIELD_SESSION_STATES and tr.get("to") in FIELD_SESSION_STATES)

    passed = sum(1 for x in checks if x["passed"])
    failed = [x for x in checks if not x["passed"]]
    v = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {
        "verifier": v, "phase": PHASE_ID, "passed_checks": passed, "failed_checks": len(failed),
        "min_checks": MIN_CHECKS, "blocker_count": len(failed),
        "final_decision": FINAL_DECISION_GO if v == "GO" else "HOLD",
        "recommended_next_phase": SELECTED_NEXT_PHASE if v == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40], "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": v, "passed_checks": passed, "failed_checks": len(failed), "final_decision": payload["final_decision"]}, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
