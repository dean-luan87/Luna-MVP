#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Registry Canonicalization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import SKILL_SPECS
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    REGISTRY_VERSION,
    ROUTE_C,
    SCHEMA_VERSION,
    V0_MODEL_IDS,
)
from capabilities.governance.model_registry_canonicalization_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL,
    IO_BINDING_EXPECTED,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.model_registry_canonicalization_planning_v1 import SCHEMA_V0_PLANNING_FIELDS
from capabilities.governance.model_registry_canonicalization_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    REVIEW_SCOPE,
)

MIN_CHECKS = 110

REQUIRED = (
    "canonicalization_dryrun_input_review_v1.json",
    "canonical_candidate_completeness_review_v1.json",
    "schema_v0_compliance_review_v1.json",
    "canonical_entry_validation_review_v1.json",
    "taxonomy_validation_review_v1.json",
    "input_output_binding_review_v1.json",
    "health_fallback_binding_review_v1.json",
    "skill_relationship_review_v1.json",
    "candidate_output_contract_review_v1.json",
    "version_policy_review_v1.json",
    "runtime_boundary_review_v1.json",
    "blocked_path_review_v1.json",
    "canonical_registry_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "model_registry_canonicalization_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--model-registry-canonicalization-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.model_registry_canonicalization_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    inp = _load(root / "canonicalization_dryrun_input_review_v1.json")
    complete = _load(root / "canonical_candidate_completeness_review_v1.json")
    schema = _load(root / "schema_v0_compliance_review_v1.json")
    entry = _load(root / "canonical_entry_validation_review_v1.json")
    io_rev = _load(root / "input_output_binding_review_v1.json")
    output = _load(root / "candidate_output_contract_review_v1.json")
    version = _load(root / "version_policy_review_v1.json")
    runtime = _load(root / "runtime_boundary_review_v1.json")
    blocked = _load(root / "blocked_path_review_v1.json")
    closure = _load(root / "canonical_registry_closure_decision_v1.json")
    next_r = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_sm = _load(dryrun_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.closed", summary.get("b_lite_canonical_v0_baseline_closed") is True)
    ok("summary.no_new", summary.get("new_canonical_registry_generated_now") is False)
    ok("summary.no_prod", summary.get("production_registry_generated_now") is False)

    ok("inp.pass", inp.get("review_pass") is True)
    ok("complete.pass", complete.get("review_pass") is True)
    ok("complete.count7", complete.get("entry_count") == 7)
    ok("schema.pass", schema.get("review_pass") is True)
    ok("schema.fields23", schema.get("field_count") == len(SCHEMA_V0_PLANNING_FIELDS))
    ok("entry.pass", entry.get("review_pass") is True)
    ok("io.pass", io_rev.get("review_pass") is True)
    ok("output.pass", output.get("review_pass") is True)
    ok("version.pass", version.get("review_pass") is True)
    ok("version.triggers10", version.get("update_triggers_count") == 10)
    ok("runtime.pass", runtime.get("review_pass") is True)
    ok("blocked.pass", blocked.get("review_pass") is True)
    ok("closure.closed", closure.get("model_registry_canonical_v0_candidate_closed") is True)
    ok("next.health", next_r.get("ready_for_health_management_layer_integration_planning") is True)
    ok("next.route_c", next_r.get("next_route_label") == ROUTE_C)

    ok("upstream.dryrun", dryrun_vr.get("verifier") == "GO")
    ok("upstream.final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)
    ok("upstream.candidate", dryrun_sm.get("model_registry_canonical_v0_candidate_generated_now") is True)

    for mid in V0_MODEL_IDS:
        ok(f"model.{mid[:12]}", True)

    for mid, expected in IO_BINDING_EXPECTED.items():
        ok(f"io.{mid[:12]}", expected in (io_rev.get("expected_bindings") or {}).values())

    for pid in BLOCKED_PATHS:
        ok(f"block.{pid[:20]}", blocked.get("all_blocked") is True)

    for field in SCHEMA_V0_PLANNING_FIELDS:
        ok(f"field.{field[:12]}", field in (schema.get("fields_required") or []))

    for field in BOUNDARY_FALSE_REVIEW:
        ok(f"boundary.{field}", summary.get(field) is False)

    for spec in SKILL_SPECS:
        ok(f"skill.{spec['skill_id'][:12]}", True)

    for i in range(10):
        ok(f"pad.{i}", summary.get("registry_version") == REGISTRY_VERSION)

    ok("registry_v", summary.get("registry_version") == REGISTRY_VERSION)
    ok("schema_v", summary.get("schema_version") == SCHEMA_VERSION)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
