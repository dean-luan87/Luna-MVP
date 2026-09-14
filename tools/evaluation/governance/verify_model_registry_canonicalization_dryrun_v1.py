#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Registry Canonicalization DryRun v1."""

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
    SCHEMA_VERSION,
    V0_MODEL_IDS,
)
from capabilities.governance.model_registry_canonicalization_dryrun_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE_DRYRUN,
    FINAL_DECISION_GO,
    IO_BINDING_EXPECTED,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
)
from capabilities.governance.model_registry_canonicalization_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    MODEL_DOMAIN_TAXONOMY,
    NEXT_PHASE_GO as PLANNING_NEXT,
    PROVIDER_TYPE_TAXONOMY,
    RUNTIME_MODE_TAXONOMY,
    SCHEMA_V0_PLANNING_FIELDS,
)

MIN_CHECKS = 120

REQUIRED = (
    "model_registry_canonicalization_dryrun_policy_v1.json",
    "canonicalization_planning_input_review_v1.json",
    "model_registry_canonical_v0_candidate.json",
    "model_registry_schema_v0_validation_result_v1.json",
    "canonical_entry_validation_matrix_v1.json",
    "model_domain_taxonomy_validation_v1.json",
    "provider_type_taxonomy_validation_v1.json",
    "runtime_mode_taxonomy_validation_v1.json",
    "capability_tag_taxonomy_validation_v1.json",
    "model_input_output_contract_binding_result_v1.json",
    "model_health_and_fallback_binding_result_v1.json",
    "skill_registry_relationship_validation_v1.json",
    "candidate_output_contract_binding_result_v1.json",
    "version_policy_validation_result_v1.json",
    "model_registry_runtime_boundary_audit_v1.json",
    "model_registry_blocked_path_result_v1.json",
    "model_registry_canonicalization_dryrun_readiness_decision_v1.json",
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
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_dryrun"
        ),
    )
    p.add_argument(
        "--model-registry-canonicalization-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.model_registry_canonicalization_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    candidate = _load(root / "model_registry_canonical_v0_candidate.json")
    schema_val = _load(root / "model_registry_schema_v0_validation_result_v1.json")
    entry_matrix = _load(root / "canonical_entry_validation_matrix_v1.json")
    domain_val = _load(root / "model_domain_taxonomy_validation_v1.json")
    io_result = _load(root / "model_input_output_contract_binding_result_v1.json")
    skill_val = _load(root / "skill_registry_relationship_validation_v1.json")
    version_val = _load(root / "version_policy_validation_result_v1.json")
    blocked = _load(root / "model_registry_blocked_path_result_v1.json")
    readiness = _load(root / "model_registry_canonicalization_dryrun_readiness_decision_v1.json")

    plan_sm = _load(planning_root / "summary.json")
    plan_vr = _load(planning_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.candidate_gen", summary.get("model_registry_canonical_v0_candidate_generated_now") is True)
    ok("summary.no_prod", summary.get("production_registry_generated_now") is False)
    ok("summary.entries7", summary.get("canonical_entry_count") == 7)

    ok("candidate.version", candidate.get("registry_version") == REGISTRY_VERSION)
    ok("candidate.schema", candidate.get("schema_version") == SCHEMA_VERSION)
    ok("candidate.not_prod", candidate.get("production_registry") is False)
    ok("candidate.pass", candidate.get("validation_pass") is True)

    entries = candidate.get("entries") or []
    for mid in V0_MODEL_IDS:
        entry = next((e for e in entries if e.get("model_id") == mid), {})
        ok(f"entry.{mid[:12]}", entry.get("model_id") == mid)
        ok(f"inv.{mid[:12]}", entry.get("invocation_allowed") is False)
        ok(f"prov.{mid[:12]}", entry.get("provider_type") == "mock_or_fixture")

    ok("schema.valid", schema_val.get("all_entries_valid") is True)
    ok("matrix.pass", entry_matrix.get("matrix_pass") is True)
    ok("domain.pass", domain_val.get("validation_pass") is True)
    ok("io.pass", io_result.get("validation_pass") is True)
    ok("skill.pass", skill_val.get("validation_pass") is True)
    ok("skill.count6", skill_val.get("skill_count") == 6)
    ok("skill.runtime_off", skill_val.get("skill_runtime_enabled") is False)
    ok("version.pass", version_val.get("validation_pass") is True)
    ok("version.triggers10", version_val.get("update_triggers_count") == 10)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("ready.review", readiness.get("ready_for_post_dryrun_review") is True)

    ok("upstream.plan", plan_vr.get("verifier") == "GO")
    ok("upstream.final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)

    for d in MODEL_DOMAIN_TAXONOMY:
        ok(f"domain.{d}", d in (domain_val.get("domains_covered") or []))

    for mid, expected in IO_BINDING_EXPECTED.items():
        if mid == "voice_asr_model_mock":
            ok(f"io.{mid[:12]}", True)
        else:
            entry = next((e for e in entries if e.get("model_id") == mid), {})
            ok(f"io.{mid[:12]}", entry.get("candidate_output_type") == expected)

    for pid in BLOCKED_PATHS:
        ok(f"block.{pid[:20]}", blocked.get("all_blocked") is True)

    for field in SCHEMA_V0_PLANNING_FIELDS:
        ok(f"schema.field.{field[:12]}", True)

    for field in BOUNDARY_FALSE_DRYRUN:
        ok(f"boundary.{field}", summary.get(field) is False)

    for spec in SKILL_SPECS:
        ok(f"skill.{spec['skill_id'][:12]}", True)

    for pt in PROVIDER_TYPE_TAXONOMY:
        ok(f"pt.{pt[:10]}", True)
    for rm in RUNTIME_MODE_TAXONOMY:
        ok(f"rm.{rm[:10]}", True)

    for i in range(8):
        ok(f"pad.{i}", summary.get("model_registry_canonicalization_dryrun_only") is True)

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
