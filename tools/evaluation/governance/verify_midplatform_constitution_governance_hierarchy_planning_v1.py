#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Constitution Governance Hierarchy Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    FINAL_DECISION_GO as AUTH_EXT_FINAL,
    NEXT_PHASE_GO as AUTH_EXT_NEXT,
    TEN_STANDARDS,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID as FACTORY_STANDARD_ID,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_planning_v1 import (
    BOUNDARY_FALSE,
    DEFERRED_PHASES,
    DESIGN_PRINCIPLES,
    DOMAIN_CONSTITUTIONS,
    DOMAIN_STANDARD_CATEGORIES,
    FINAL_DECISION_GO,
    GOVERNANCE_LAYERS,
    HIERARCHY_ANALOGY,
    LUNA_GENERAL_CONSTITUTION_ARTICLES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
    PHASE_ID,
    RULE_CLASSIFICATION_QUESTIONS,
    SCOPE,
)

MIN_CHECKS = 70

REQUIRED = (
    "midplatform_constitution_governance_hierarchy_planning_policy_v1.json",
    "upstream_factory_standards_input_review_v1.json",
    "luna_constitution_layer_outline_v1.json",
    "luna_general_constitution_plan_v1.json",
    "domain_constitution_registry_plan_v1.json",
    "domain_standard_registry_plan_v1.json",
    "capability_factory_constitution_reposition_plan_v1.json",
    "factory_authorization_standard_reposition_plan_v1.json",
    "controlled_provider_readiness_harness_reposition_plan_v1.json",
    "validation_factory_reposition_plan_v1.json",
    "ocr_domain_constitution_reposition_plan_v1.json",
    "vision_voice_future_constitution_reposition_plan_v1.json",
    "governance_hierarchy_decision_tree_v1.json",
    "rule_fragmentation_prevention_policy_v1.json",
    "deferred_phases_register_v1.json",
    "hierarchy_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "hierarchy_planning_decision_v1.json",
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
            "midplatform_constitution_governance_hierarchy_planning"
        ),
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "capability_factory_authorization_standard_extension_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    auth_ext_root = Path(args.capability_factory_authorization_standard_extension_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(
        root / "midplatform_constitution_governance_hierarchy_planning_policy_v1.json"
    )
    upstream = _load(root / "upstream_factory_standards_input_review_v1.json")
    outline = _load(root / "luna_constitution_layer_outline_v1.json")
    general = _load(root / "luna_general_constitution_plan_v1.json")
    domain_const = _load(root / "domain_constitution_registry_plan_v1.json")
    domain_std = _load(root / "domain_standard_registry_plan_v1.json")
    factory_repo = _load(root / "capability_factory_constitution_reposition_plan_v1.json")
    auth_repo = _load(root / "factory_authorization_standard_reposition_plan_v1.json")
    harness_repo = _load(root / "controlled_provider_readiness_harness_reposition_plan_v1.json")
    vf_repo = _load(root / "validation_factory_reposition_plan_v1.json")
    ocr_repo = _load(root / "ocr_domain_constitution_reposition_plan_v1.json")
    vv_repo = _load(root / "vision_voice_future_constitution_reposition_plan_v1.json")
    tree = _load(root / "governance_hierarchy_decision_tree_v1.json")
    frag = _load(root / "rule_fragmentation_prevention_policy_v1.json")
    deferred = _load(root / "deferred_phases_register_v1.json")
    dryrun = _load(root / "hierarchy_dryrun_plan_v1.json")
    decision = _load(root / "hierarchy_planning_decision_v1.json")

    auth_ext_vr = _load(auth_ext_root / "verifier_report.json")
    auth_ext_sm = _load(auth_ext_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.analogy", summary.get("hierarchy_analogy") == HIERARCHY_ANALOGY)

    ok("upstream.auth_ext_go", auth_ext_vr.get("verifier") == "GO")
    ok("upstream.auth_ext_final", auth_ext_sm.get("final_decision") == AUTH_EXT_FINAL)
    ok("upstream.pass", upstream.get("review_pass") is True)

    ok("outline.analogy", outline.get("hierarchy_analogy") == HIERARCHY_ANALOGY)
    ok("outline.layers4", len(outline.get("layers") or []) == len(GOVERNANCE_LAYERS))
    ok("policy.phase", policy.get("phase") == PHASE_ID)
    ok("policy.scope", policy.get("scope") == SCOPE)
    ok("policy.analogy", policy.get("hierarchy_analogy") == HIERARCHY_ANALOGY)
    ok("factory.std_id", any(
        e.get("artifact_id") == FACTORY_STANDARD_ID for e in (factory_repo.get("entries") or [])
    ))
    ok("auth.ten_standards", len(TEN_STANDARDS) == 10)
    ok("deferred.ocr_plan", any(
        d.get("phase_id")
        == "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Authorization-Standard-Planning-v1-001"
        for d in (deferred.get("deferred_phases") or [])
    ))
    ok("deferred.ocr_dr", any(
        d.get("phase_id")
        == "Phase-OCR-Provider-Real-Dependency-Check-Authorization-DryRunAndReview-v1-001"
        for d in (deferred.get("deferred_phases") or [])
    ))
    ok("vf.check_only", "not rule author" in (vf_repo.get("role") or ""))
    ok("general.articles6", general.get("article_count") == len(LUNA_GENERAL_CONSTITUTION_ARTICLES))
    ok("domain.const8", domain_const.get("domain_count") == len(DOMAIN_CONSTITUTIONS))
    ok("domain.std10", domain_std.get("category_count") == len(DOMAIN_STANDARD_CATEGORIES))

    ok("factory.repo", len(factory_repo.get("entries") or []) >= 1)
    ok("factory.no_delete", all(e.get("physical_delete") is False for e in (factory_repo.get("entries") or [])))

    ok("auth.repo", auth_repo.get("supersedes_duplicate_auth_in_ocr_phases") is True)
    auth_entries = auth_repo.get("entries") or []
    ok("auth.std", any(e.get("artifact_id") == AUTHORIZATION_STANDARD_ID for e in auth_entries))

    ok("harness.repo", len(harness_repo.get("entries") or []) >= 1)
    ok("vf.repo", len(vf_repo.get("entries") or []) >= 1)

    ocr_entries = ocr_repo.get("entries") or []
    ok("ocr.repo5", len(ocr_entries) >= 5)
    ok("ocr.chain", ocr_repo.get("future_authorization_chain") == OCR_REAL_DEP_AUTHORIZATION_CHAIN)

    ok("vv.planned", vv_repo.get("status") == "planned_not_instantiated")

    ok("tree.questions4", len(tree.get("questions") or []) == len(RULE_CLASSIFICATION_QUESTIONS))
    ok("tree.principles5", len(tree.get("design_principles") or []) == len(DESIGN_PRINCIPLES))

    ok("frag.forbidden", len(frag.get("forbidden_patterns") or []) >= 1)
    ok("deferred.count3", len(deferred.get("deferred_phases") or []) == len(DEFERRED_PHASES))
    ok("deferred.ext", any(
        d.get("phase_id") == "Phase-Capability-Factory-Authorization-Standard-Extension-DryRunAndReview-v1-001"
        for d in (deferred.get("deferred_phases") or [])
    ))

    ok("dryrun.merged", dryrun.get("dryrun_and_review_merged") is True)
    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.chain", decision.get("ocr_real_dep_authorization_chain") == OCR_REAL_DEP_AUTHORIZATION_CHAIN)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    ok("auth_ext.next_deferred", AUTH_EXT_NEXT.startswith("Phase-Capability-Factory-Authorization"))

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
