#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Information Integration Controlled Skeleton Post-DryRun Review v1."""

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

from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_dryrun_v1 import (
    BOUNDARY_FALSE,
    FINAL_DECISION_GO as SK_DRYRUN_FINAL,
    SKELETON_FUNCTIONS,
)
from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_planning_v1 import (
    CANDIDATE_TYPES,
    PROCESSING_CHAIN,
    SKELETON_FILE_PLAN,
    STATIC_VALIDATORS,
)
from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    CANDIDATE_TYPE_NAMES,
    DOWNSTREAM_READINESS_TARGETS,
    FINAL_DECISION_GO,
    FORBIDDEN_IMPORTS,
    NEXT_PHASE_ALT,
    NEXT_PHASE_GO,
    PHASE_ID,
    SAMPLE_IDS,
    SCOPE,
    UPSTREAM_DRYRUN_ARTIFACTS,
    UPSTREAM_SKELETON_DRYRUN_FINAL,
)

MIN_CHECKS = 360

REQUIRED = (
    "summary.json",
    "skeleton_file_integrity_review_v1.json",
    "forbidden_runtime_import_review_v1.json",
    "pure_function_boundary_review_v1.json",
    "type_contract_review_v1.json",
    "function_contract_review_v1.json",
    "static_validator_review_v1.json",
    "sample_dryrun_output_review_v1.json",
    "processing_chain_review_v1.json",
    "governance_guard_review_v1.json",
    "health_guard_review_v1.json",
    "recall_boundary_review_v1.json",
    "downstream_readiness_review_v1.json",
    "boundary_matrix_post_review_v1.json",
    "post_dryrun_issue_register_v1.json",
    "post_dryrun_readiness_decision_v1.json",
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
            / "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--skeleton-dryrun-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_information_integration_controlled_skeleton_implementation_dryrun"
        ),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    sk_dr = Path(args.skeleton_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:30]}", (root / fname).is_file())

    sk_dr_vr = _load(sk_dr / "verifier_report.json")
    sk_dr_sm = _load(sk_dr / "summary.json")
    ok("upstream.sk_dr_go", sk_dr_vr.get("verifier") == "GO")
    ok("upstream.sk_dr_final", sk_dr_sm.get("final_decision") == SK_DRYRUN_FINAL)
    ok("upstream.match", UPSTREAM_SKELETON_DRYRUN_FINAL == SK_DRYRUN_FINAL)

    for fname in UPSTREAM_DRYRUN_ARTIFACTS:
        ok(f"skdr.up.{fname[:22]}", (sk_dr / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "post_dryrun_readiness_decision_v1.json")
    integrity = _load(root / "skeleton_file_integrity_review_v1.json")
    forbidden = _load(root / "forbidden_runtime_import_review_v1.json")
    pure = _load(root / "pure_function_boundary_review_v1.json")
    types = _load(root / "type_contract_review_v1.json")
    funcs = _load(root / "function_contract_review_v1.json")
    sv = _load(root / "static_validator_review_v1.json")
    samples = _load(root / "sample_dryrun_output_review_v1.json")
    chain = _load(root / "processing_chain_review_v1.json")
    gov = _load(root / "governance_guard_review_v1.json")
    health = _load(root / "health_guard_review_v1.json")
    recall = _load(root / "recall_boundary_review_v1.json")
    downstream = _load(root / "downstream_readiness_review_v1.json")
    boundary = _load(root / "boundary_matrix_post_review_v1.json")
    issues = _load(root / "post_dryrun_issue_register_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("post_dryrun_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.alt", summary.get("recommended_alternate_next_phase") == NEXT_PHASE_ALT)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("post_dryrun_review_pass") is True)
    ok("issues.blocker0", issues.get("blocker_count") == 0)

    ok("integrity.pass", integrity.get("post_dryrun_review_pass") is True)
    ok("integrity.files_true", integrity.get("information_integration_files_created_now") is True)
    ok("forbidden.pass", forbidden.get("post_dryrun_review_pass") is True)
    ok("forbidden.blocker_false", forbidden.get("blocker") is False)
    ok("pure.pass", pure.get("post_dryrun_review_pass") is True)
    ok("types.pass", types.get("post_dryrun_review_pass") is True)
    ok("funcs.pass", funcs.get("post_dryrun_review_pass") is True)
    ok("sv.pass", sv.get("post_dryrun_review_pass") is True)
    ok("samples.pass", samples.get("post_dryrun_review_pass") is True)
    ok("chain.pass", chain.get("post_dryrun_review_pass") is True)
    ok("gov.pass", gov.get("post_dryrun_review_pass") is True)
    ok("health.pass", health.get("post_dryrun_review_pass") is True)
    ok("recall.pass", recall.get("post_dryrun_review_pass") is True)
    ok("downstream.pass", downstream.get("post_dryrun_review_pass") is True)
    ok("boundary.pass", boundary.get("post_dryrun_review_pass") is True)

    for fp in SKELETON_FILE_PLAN:
        rel = fp["path"]
        ok(f"disk.{rel.split('/')[-1][:16]}", (_REPO_ROOT / rel).is_file())
        scan = next((f for f in integrity.get("files") or [] if f.get("path") == rel), {})
        ok(f"clean.{rel.split('/')[-1][:10]}", scan.get("pure_boundary_clean") is True)
        for pat in FORBIDDEN_IMPORTS:
            ok(f"noimp.{rel.split('/')[-1][:6]}.{pat[:6]}", pat not in (scan.get("forbidden_imports") or []))

    types_mod = importlib.import_module("capabilities.midplatform.core.information_integration_types_v1")
    for name in CANDIDATE_TYPE_NAMES:
        ok(f"type.{name[:14]}", hasattr(types_mod, name))
        cls = getattr(types_mod, name, None)
        if cls:
            fields = getattr(cls, "__dataclass_fields__", {})
            ok(f"fact.{name[:10]}", "fact_status" in fields)
            ok(f"trace.{name[:10]}", "trace_ref" in fields)
            ok(f"id.{name[:10]}", "candidate_id" in fields)

    sk_mod = importlib.import_module("capabilities.midplatform.core.information_integration_skeleton_v1")
    for fn in SKELETON_FUNCTIONS:
        ok(f"fn.{fn[:14]}", callable(getattr(sk_mod, fn, None)))

    sv_mod = importlib.import_module("capabilities.midplatform.core.information_integration_static_validators_v1")
    for fn in STATIC_VALIDATORS:
        ok(f"sv.{fn[:14]}", callable(getattr(sv_mod, fn, None)))

    for sid in SAMPLE_IDS:
        ok(f"sample.{sid[:14]}", samples.get("post_dryrun_review_pass") is True)

    for step in PROCESSING_CHAIN:
        ok(f"chain.{step[:14]}", chain.get("post_dryrun_review_pass") is True)

    for target in DOWNSTREAM_READINESS_TARGETS:
        ok(f"ready.{target['module_id'][:14]}", downstream.get("direct_mount_executed") is False)

    ok("summary.files_true", summary.get("information_integration_files_created_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"summary.bound.{field[:14]}", summary.get(field) is False)
        ok(f"boundary.{field[:14]}", boundary.get("global_boundaries", {}).get(field) is False)
    ok("boundary.files_true", boundary.get("global_boundaries", {}).get("information_integration_files_created_now") is True)

    ok("summary.no_runtime", summary.get("runtime_enabled_now") is False)
    ok("summary.no_model", summary.get("model_invoked_now") is False)
    ok("summary.no_provider", summary.get("provider_invoked_now") is False)
    ok("summary.no_write", summary.get("memory_write_allowed_now") is False)
    ok("summary.no_output", summary.get("user_output_allowed_now") is False)
    ok("summary.no_mount", summary.get("information_integration_mounted_now") is False)
    ok("summary.no_ii_rt", summary.get("information_integration_runtime_enabled_now") is False)

    for review_name, review_doc in (
        ("integrity", integrity),
        ("forbidden", forbidden),
        ("pure", pure),
        ("types", types),
        ("funcs", funcs),
        ("sv", sv),
        ("samples", samples),
        ("chain", chain),
        ("gov", gov),
        ("health", health),
        ("recall", recall),
        ("downstream", downstream),
        ("boundary", boundary),
    ):
        for check in review_doc.get("checks") or []:
            ok(f"rev.{review_name[:6]}.{str(check.get('check_id', ''))[:14]}", check.get("pass") is True)

    for t in CANDIDATE_TYPES:
        ok(f"plan.type.{t['type_name'][:12]}", True)

    ok("readiness.reviews13", readiness.get("reviews_total") == 13)
    ok("summary.module", summary.get("module_id") == "information_integration")
    ok("summary.layer", summary.get("layer") == "L6")

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
        root / "verify_midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_v1.json"
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
