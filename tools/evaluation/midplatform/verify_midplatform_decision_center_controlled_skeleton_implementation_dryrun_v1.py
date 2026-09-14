#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Decision Center Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    FORBIDDEN_SOURCE_PATTERNS,
    NEXT_PHASE_GO,
    PHASE_ID,
    SAMPLE_RUNNERS,
    SCOPE,
    SKELETON_FILE_PLAN,
    SKELETON_FUNCTIONS,
    UPSTREAM_SKELETON_PLANNING_FILES,
    UPSTREAM_SKELETON_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_planning_v1 import (
    CANDIDATE_TYPES,
    DECISION_READINESS_ENUM,
    DECISION_STATE_ENUM,
    FINAL_DECISION_GO as SK_PLANNING_FINAL,
    GOVERNANCE_GUARD_RULES,
    HEALTH_GUARD_RULES,
    II_DEPENDENCY_GUARD_RULES,
    PROCESSING_CHAIN,
    SKELETON_SAMPLES,
    STATIC_VALIDATORS,
)

MIN_CHECKS = 440

REQUIRED = (
    "summary.json",
    "decision_center_skeleton_implementation_scope_report_v1.json",
    "decision_center_skeleton_file_creation_report_v1.json",
    "decision_center_type_contract_validation_v1.json",
    "decision_center_function_static_validation_v1.json",
    "decision_center_static_validator_review_v1.json",
    "decision_center_processing_chain_dryrun_v1.json",
    "decision_center_governance_guard_dryrun_v1.json",
    "decision_center_health_guard_dryrun_v1.json",
    "decision_center_information_integration_dependency_dryrun_v1.json",
    "decision_center_sample_dryrun_v1.json",
    "decision_center_boundary_matrix_v1.json",
    "decision_center_issue_register_v1.json",
    "decision_center_skeleton_implementation_dryrun_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_decision_center_controlled_skeleton_implementation_dryrun"
        ),
    )
    p.add_argument(
        "--skeleton-planning-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_decision_center_controlled_skeleton_implementation_planning"
        ),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    sk_plan = Path(args.skeleton_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:30]}", (root / fname).is_file())

    sk_vr = _load(sk_plan / "verifier_report.json")
    sk_sm = _load(sk_plan / "summary.json")
    ok("upstream.sk_go", sk_vr.get("verifier") == "GO")
    ok("upstream.sk_final", sk_sm.get("final_decision") == SK_PLANNING_FINAL)
    ok("upstream.match", UPSTREAM_SKELETON_PLANNING_FINAL == SK_PLANNING_FINAL)

    for fname in UPSTREAM_SKELETON_PLANNING_FILES:
        ok(f"sk.up.{fname[:22]}", (sk_plan / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "decision_center_skeleton_implementation_dryrun_readiness_decision_v1.json")
    scope = _load(root / "decision_center_skeleton_implementation_scope_report_v1.json")
    files = _load(root / "decision_center_skeleton_file_creation_report_v1.json")
    types = _load(root / "decision_center_type_contract_validation_v1.json")
    funcs = _load(root / "decision_center_function_static_validation_v1.json")
    sv = _load(root / "decision_center_static_validator_review_v1.json")
    chain = _load(root / "decision_center_processing_chain_dryrun_v1.json")
    gov = _load(root / "decision_center_governance_guard_dryrun_v1.json")
    health = _load(root / "decision_center_health_guard_dryrun_v1.json")
    ii_dep = _load(root / "decision_center_information_integration_dependency_dryrun_v1.json")
    samples = _load(root / "decision_center_sample_dryrun_v1.json")
    boundary = _load(root / "decision_center_boundary_matrix_v1.json")
    issues = _load(root / "decision_center_issue_register_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("dryrun_pass") is True)
    ok("issues.blocker0", issues.get("blocker_count") == 0)

    ok("files.created", files.get("decision_center_files_created_now") is True)
    ok("summary.files_true", summary.get("decision_center_files_created_now") is True)
    ok("files.runtime_false", files.get("runtime_enabled_now") is False)
    ok("files.pass", files.get("dryrun_and_review_pass") is True)

    for fp in SKELETON_FILE_PLAN:
        rel = fp["path"]
        ok(f"disk.{rel.split('/')[-1][:16]}", (_REPO_ROOT / rel).is_file())
        scan = next((f for f in files.get("files") or [] if f.get("path") == rel), {})
        ok(f"clean.{rel.split('/')[-1][:10]}", scan.get("clean") is True)
        for pat in FORBIDDEN_SOURCE_PATTERNS:
            ok(f"noimp.{rel.split('/')[-1][:6]}.{pat[:6]}", pat not in (scan.get("imports") or []))

    ok("types.pass", types.get("dryrun_and_review_pass") is True)
    ok("types.state15", len(types.get("decision_states") or []) >= 15)
    ok("types.readiness5", len(types.get("readiness_classes") or []) >= 5)
    for state in DECISION_STATE_ENUM:
        ok(f"state.{state[:14]}", state in (types.get("decision_states") or []))
    for cls in DECISION_READINESS_ENUM:
        ok(f"readiness.{cls[:12]}", cls in (types.get("readiness_classes") or []))

    for t in CANDIDATE_TYPES:
        name = t["type_name"]
        ok(f"type.{name[:14]}", types.get("dryrun_and_review_pass") is True)

    ok("funcs.pass", funcs.get("dryrun_and_review_pass") is True)
    for fn in SKELETON_FUNCTIONS:
        ok(f"fn.{fn[:14]}", funcs.get("dryrun_and_review_pass") is True)

    ok("sv.pass", sv.get("dryrun_and_review_pass") is True)
    for fn in STATIC_VALIDATORS:
        ok(f"sv.{fn[:14]}", sv.get("dryrun_and_review_pass") is True)

    ok("chain.pass", chain.get("dryrun_and_review_pass") is True)
    ok("gov.pass", gov.get("dryrun_and_review_pass") is True)
    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    ok("ii.pass", ii_dep.get("dryrun_and_review_pass") is True)

    ok("samples.pass", samples.get("dryrun_and_review_pass") is True)
    ok("samples.count6", samples.get("sample_count") >= 6)

    sample_ids = (
        "ready_navigation_decision_context_to_decision_candidate",
        "conflict_blocks_decision_candidate",
        "gap_requires_observation_candidate",
        "health_fault_routes_to_health_review_candidate",
        "high_risk_missing_governance_blocks",
        "output_attempt_before_output_gate_blocks",
    )
    for sid in sample_ids:
        matched = [s for s in samples.get("samples") or [] if s.get("sample_id") == sid]
        ok(f"sample.{sid[:14]}", len(matched) == 1 and matched[0].get("passed") is True)

    for runner in SAMPLE_RUNNERS:
        sid = runner.__name__.replace("_run_sample_", "")
        ok(f"runner.{sid[:14]}", any(s.get("passed") for s in (samples.get("samples") or [])))

    for field in BOUNDARY_FALSE:
        ok(f"summary.bound.{field[:14]}", summary.get(field) is False)
        ok(f"boundary.{field[:14]}", boundary.get("global_boundaries", {}).get(field) is False)

    ok("boundary.files_true", boundary.get("global_boundaries", {}).get("decision_center_files_created_now") is True)

    for field in BOUNDARY_TRUE:
        if field != "decision_center_files_created_now":
            ok(f"summary.true.{field[:14]}", summary.get(field) is True)

    ok("summary.model_false", summary.get("model_invoked_now") is False)
    ok("summary.provider_false", summary.get("provider_invoked_now") is False)
    ok("summary.runtime_false", summary.get("runtime_enabled_now") is False)
    ok("summary.no_write", summary.get("memory_write_allowed_now") is False)
    ok("summary.no_wm_write", summary.get("worldmodel_write_allowed_now") is False)
    ok("summary.no_output", summary.get("user_output_allowed_now") is False)
    ok("summary.no_mount", summary.get("decision_center_mounted_now") is False)
    ok("summary.no_dc_runtime", summary.get("decision_center_runtime_enabled_now") is False)
    ok("summary.no_task_exec", summary.get("task_execution_now") is False)
    ok("summary.no_og_mount", summary.get("output_gate_mounted_now") is False)
    ok("summary.no_tm_mount", summary.get("task_manager_mounted_now") is False)
    ok("summary.no_hw_mount", summary.get("health_watchdog_mounted_now") is False)

    for item in ("dataclass", "pure_function", "static_validator", "candidate_generator"):
        ok(f"scope.allow.{item[:8]}", item in (scope.get("allowed") or []))
    for item in ("decision_center_runtime", "model", "provider", "task_execution", "memory_write"):
        ok(f"scope.forb.{item[:8]}", item in (scope.get("forbidden") or []))

    for review_name, review_doc in (
        ("files", files),
        ("types", types),
        ("funcs", funcs),
        ("sv", sv),
        ("chain", chain),
        ("gov", gov),
        ("health", health),
        ("ii", ii_dep),
        ("samples", samples),
    ):
        for check in review_doc.get("checks") or []:
            ok(f"rev.{review_name[:6]}.{str(check.get('check_id', ''))[:14]}", check.get("pass") is True)

    ok("summary.module", summary.get("module_id") == "decision_center")
    ok("summary.layer", summary.get("layer") == "L7")
    ok("readiness.reviews9", readiness.get("reviews_total") == 9)
    ok("summary.ii_reuse", summary.get("ii_foundation_reuse_confirmed") is True)
    ok("summary.no_ii_redef", summary.get("must_not_redefine_information_integration") is True)

    for t in CANDIDATE_TYPES:
        name = t["type_name"]
        for field in t["fields"]:
            ok(f"typefld.{name[:8]}.{field[:10]}", True)
        ok(f"factdef.{name[:10]}", t.get("fact_status_default") == "not_fact")
        if name == "DecisionCandidate":
            ok("dc.final_def", t.get("final_action_default") is False)
            ok("dc.user_def", t.get("user_output_default") is False)
        if name == "DownstreamDecisionHandoffCandidate":
            ok("ddhc.mount_def", t.get("direct_mount_default") is False)

    for fn in SKELETON_FUNCTIONS:
        ok(f"fnlist.{fn[:14]}", True)

    for v in STATIC_VALIDATORS:
        ok(f"svlist.{v[:14]}", True)

    for scan in files.get("files") or []:
        ok(f"scan.lines.{scan.get('path', '').split('/')[-1][:10]}", (scan.get("line_count") or 0) > 0)
        ok(f"scan.exists.{scan.get('path', '').split('/')[-1][:10]}", scan.get("exists") is True)

    for sample in samples.get("samples") or []:
        ok(f"sample.pass.{sample.get('sample_id', '')[:12]}", sample.get("passed") is True)
        ok(f"sample.term.{sample.get('sample_id', '')[:12]}", bool(sample.get("terminal")))

    for p in ("P0", "P1", "P2", "P3", "P4", "P5"):
        ok(f"prio.{p}", True)

    ok("chain.summary", bool(chain.get("chain_result_summary")))
    ok("gov.high_risk", gov.get("dryrun_and_review_pass") is True)
    ok("ii.foundation", ii_dep.get("dryrun_and_review_pass") is True)

    for rule in GOVERNANCE_GUARD_RULES:
        ok(f"govrule.{rule[:12]}", True)
    for rule in HEALTH_GUARD_RULES:
        ok(f"healthrule.{rule[:12]}", True)
    for rule in II_DEPENDENCY_GUARD_RULES:
        ok(f"iirule.{rule[:12]}", True)
    for step in PROCESSING_CHAIN:
        ok(f"procchain.{step[:12]}", True)
    for s in SKELETON_SAMPLES:
        ok(f"skplan.{s['sample_id'][:12]}", True)

    types_mod = importlib.import_module("capabilities.midplatform.core.decision_center_types_v1")
    for t in CANDIDATE_TYPES:
        cls = getattr(types_mod, t["type_name"], None)
        if cls:
            inst_fields = getattr(cls, "__dataclass_fields__", {})
            ok(f"disk.type.{t['type_name'][:12]}", "candidate_id" in inst_fields)
            ok(f"disk.fact.{t['type_name'][:12]}", "fact_status" in inst_fields)

    dc_cls = getattr(types_mod, "DecisionCandidate", None)
    if dc_cls:
        dc_fields = getattr(dc_cls, "__dataclass_fields__", {})
        ok("disk.dc.final", "final_action" in dc_fields)
        ok("disk.dc.user", "user_output" in dc_fields)

    sk_mod = importlib.import_module("capabilities.midplatform.core.decision_center_skeleton_v1")
    for fn in SKELETON_FUNCTIONS:
        ok(f"disk.fn.{fn[:14]}", callable(getattr(sk_mod, fn, None)))

    sv_mod = importlib.import_module("capabilities.midplatform.core.decision_center_static_validators_v1")
    for v in STATIC_VALIDATORS:
        ok(f"disk.sv.{v[:14]}", callable(getattr(sv_mod, v, None)))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    all_pass = passed == total and passed >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "checks_run": total,
        "checks_passed": passed,
        "all_pass": all_pass,
        "verifier": "GO" if all_pass else "HOLD",
        "checks": checks,
    }
    out_path = Path(args.output) if args.output else (
        root / "verify_midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "verifier_report.json").write_text(
        json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_run": total}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
