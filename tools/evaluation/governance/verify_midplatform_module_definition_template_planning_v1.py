#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Module Definition Template Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    FINAL_DECISION_GO as DC_MODULE_FINAL,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    FAILURE_TRACE_FIELDS,
    INPUT_CONTRACT_BASE_FIELDS,
    OUTPUT_CONTRACT_BASE_FIELDS,
    RUNTIME_BOUNDARY_FIELDS,
    SYSTEM_LAYERS,
    TEMPLATE_ID,
    TEMPLATE_PRINCIPLE,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)

MIN_CHECKS = 82

REQUIRED = (
    "midplatform_module_definition_template_policy_v1.json",
    "decision_center_module_planning_input_review_v1.json",
    "midplatform_module_definition_template_v1.json",
    "decision_center_module_full_definition_exemplar_v1.json",
    "template_adoption_requirement_v1.json",
    "non_claims_register_v1.json",
    "midplatform_module_definition_template_planning_decision_v1.json",
    "summary.json",
)

FINAL_DECISION_GO = "MIDPLATFORM_MODULE_DEFINITION_TEMPLATE_PLANNING_READY_FOR_ADOPTION"


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_module_definition_template_planning"
        ),
    )
    p.add_argument(
        "--decision-center-module-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_decision_center_module_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dc_root = Path(args.decision_center_module_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    dc_vr = _load(dc_root / "verifier_report.json")
    dc_sm = _load(dc_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "midplatform_module_definition_template_policy_v1.json")
    template = _load(root / "midplatform_module_definition_template_v1.json")
    exemplar = _load(root / "decision_center_module_full_definition_exemplar_v1.json")
    adoption = _load(root / "template_adoption_requirement_v1.json")
    decision = _load(root / "midplatform_module_definition_template_planning_decision_v1.json")

    ok("upstream.dc_go", dc_vr.get("verifier") == "GO")
    ok("upstream.dc_final", dc_sm.get("final_decision") == DC_MODULE_FINAL)

    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.template_only", summary.get("midplatform_module_definition_template_planning_only") is True)
    ok("summary.template_default", summary.get("template_established_as_default") is True)

    ok("policy.mandatory", policy.get("adoption_mandatory_for_future_modules") is True)
    ok("policy.sections10", len(policy.get("ten_section_structure") or []) == 10)
    ok("policy.principle", policy.get("template_principle") == TEMPLATE_PRINCIPLE)
    ok("policy.layers8", len(policy.get("system_layers") or []) == 8)

    ok("template.id", template.get("template_id") == TEMPLATE_ID)
    ok("template.sections10", len(template.get("required_sections") or []) == 10)
    for section in TEMPLATE_SECTIONS:
        ok(f"section.{section[:12]}", section in (template.get("required_sections") or []))

    for layer in SYSTEM_LAYERS:
        ok(f"layer.{layer}", layer in (template.get("system_layers") or SYSTEM_LAYERS))

    ok("exemplar.valid", exemplar.get("exemplar_valid") is True)
    ok("exemplar.module", exemplar.get("module_identity", {}).get("module_id") == "midplatform_decision_center_v1")
    ok("exemplar.layer", exemplar.get("module_identity", {}).get("system_layer") == "Decision")

    valid, issues = validate_module_definition(exemplar)
    ok("exemplar.validate", valid and len(issues) == 0)

    identity = exemplar.get("module_identity") or {}
    upstream = exemplar.get("upstream_sources") or {}
    downstream = exemplar.get("downstream_targets") or {}
    processing = exemplar.get("processing_scope") or {}
    output = exemplar.get("output_contract") or {}
    boundaries = exemplar.get("runtime_boundaries") or {}

    ok("exemplar.upstream7", len(upstream.get("upstream_modules") or []) >= 7)
    ok("exemplar.downstream_task", "task_response_candidate_integration" in (
        downstream.get("downstream_modules") or []
    ))
    ok("exemplar.forbid_user", "user_output_candidate" in (downstream.get("forbidden_outputs") or []))
    ok("exemplar.forbid_memory", "memory_fact" in (downstream.get("forbidden_outputs") or []))
    ok("exemplar.arbitration", processing.get("arbitration_allowed") is True)
    ok("exemplar.no_write", processing.get("write_allowed") is False)
    ok("exemplar.no_provider", processing.get("provider_invocation_allowed") is False)
    ok("exemplar.output_decision", output.get("output_object_type") == "decision_candidate")
    ok("exemplar.no_user_out", output.get("user_output_allowed") is False)

    for field in INPUT_CONTRACT_BASE_FIELDS:
        ok(f"input_base.{field[:12]}", field in (template.get("input_contract_base_fields") or []))
    for field in OUTPUT_CONTRACT_BASE_FIELDS:
        ok(f"output_base.{field[:12]}", field in (template.get("output_contract_base_fields") or []))
    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"runtime.{field[:12]}", boundaries.get(field) is False or field in (
            template.get("runtime_boundary_fields") or []
        ))
    for field in FAILURE_TRACE_FIELDS:
        ok(f"failure.{field[:12]}", field in (exemplar.get("failure_and_traceability") or {}))

    ok("adoption.mandatory", adoption.get("all_future_midplatform_modules_must_use_template") is True)
    ok("adoption.sections10", adoption.get("minimum_sections") == 10)
    ok("adoption.first_exemplar", adoption.get("first_exemplar_module_id") == "midplatform_decision_center_v1")

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.template", decision.get("template_established") is True)

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("planning_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": "Phase-Midplatform-Module-Definition-Template-Planning-v1-001",
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "template_id": TEMPLATE_ID,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
