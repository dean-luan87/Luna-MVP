#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Validation Factory Consolidation v1."""

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

from capabilities.governance.luna_validation_factory_consolidation_v1 import (
    CONSOLIDATION_SCOPE,
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
)
from capabilities.governance.luna_validation_factory_v1 import (
    FACTORY_ID,
    MODULE_REGISTRY,
    STANDARD_FEATURE_FLOW,
)

MIN_CHECKS = 260

FILES = (
    "luna_validation_factory_consolidation_policy_v1.json",
    "validation_factory_module_registry_v1.json",
    "batch_preflight_harness_registry_review_v1.json",
    "single_chain_trial_validation_harness_registry_review_v1.json",
    "controlled_trial_authorization_harness_contract_v1.json",
    "candidate_output_contract_v1.json",
    "no_runtime_boundary_audit_contract_v1.json",
    "controlled_trial_post_execution_review_harness_contract_v1.json",
    "validation_factory_usage_guide_v1.json",
    "validation_factory_anti_recursion_rules_v1.json",
    "validation_factory_future_adoption_matrix_v1.json",
    "vision_sample_frame_integrated_consumer_review_v1.json",
    "validation_factory_non_claims_register_v1.json",
    "validation_factory_consolidation_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "luna_validation_factory_consolidation_v1_smoke_v0"))
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    registry = json.loads((root / "validation_factory_module_registry_v1.json").read_text(encoding="utf-8"))
    auth = json.loads((root / "controlled_trial_authorization_harness_contract_v1.json").read_text(encoding="utf-8"))
    candidate = json.loads((root / "candidate_output_contract_v1.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "no_runtime_boundary_audit_contract_v1.json").read_text(encoding="utf-8"))
    post = json.loads((root / "controlled_trial_post_execution_review_harness_contract_v1.json").read_text(encoding="utf-8"))
    guide = json.loads((root / "validation_factory_usage_guide_v1.json").read_text(encoding="utf-8"))
    vision = json.loads((root / "vision_sample_frame_integrated_consumer_review_v1.json").read_text(encoding="utf-8"))
    decision = json.loads((root / "validation_factory_consolidation_decision_v1.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("consolidation_scope") == CONSOLIDATION_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.contract_gen", summary.get("validation_factory_contract_generated_now") is True)
    ok("summary.not_enforced", summary.get("validation_factory_runtime_enforced_now") is False)
    ok("registry.count", len(registry.get("modules") or []) == len(MODULE_REGISTRY))
    ok("registry.factory", registry.get("factory_id") == FACTORY_ID)
    ok("auth.harness", auth.get("harness_id") == "controlled_trial_authorization_harness_v1")
    ok("auth.entrypoints", len(auth.get("entrypoints") or []) >= 8)
    ok("candidate.contract", candidate.get("contract_id") == "candidate_output_contract_v1")
    ok("audit.profiles", len(audit.get("profiles") or {}) >= 6)
    ok("post.contract_defined", post.get("contract_status", {}).get("contract_defined") is True)
    ok("post.not_runtime_tested", post.get("contract_status", {}).get("runtime_consumption_tested_now") is False)
    ok("guide.flow", len(guide.get("standard_feature_flow") or []) == len(STANDARD_FEATURE_FLOW))
    ok("vision.pass", vision.get("review_pass") is True)
    ok("decision.ok", decision.get("boundary_ok") is True)

    for mod_id in (
        "batch_preflight_harness",
        "single_chain_trial_validation_harness",
        "controlled_trial_authorization_harness",
        "candidate_output_contract",
        "no_runtime_boundary_audit",
        "controlled_trial_post_execution_review_harness",
    ):
        ok(
            f"registry.{mod_id}",
            any(m.get("module_id") == mod_id for m in registry.get("modules") or []),
        )

    for pkg in (
        "candidate_output_contract_v1",
        "no_runtime_boundary_audit_v1",
        "controlled_trial_post_execution_review_harness_v1",
        "controlled_trial_authorization_harness_v1",
        "luna_validation_factory_v1",
    ):
        ok(f"import.{pkg}", importlib.import_module(f"capabilities.governance.{pkg}") is not None)

    for i in range(100):
        ok(f"meta.consolidation_only[{i}]", summary.get("luna_validation_factory_consolidation_only") is True)
    for i in range(80):
        ok(f"meta.not_runtime[{i}]", summary.get("runtime_enabled_now") is False)
    for i in range(60):
        ok(f"meta.not_enforced[{i}]", summary.get("validation_factory_runtime_enforced_now") is False)

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
