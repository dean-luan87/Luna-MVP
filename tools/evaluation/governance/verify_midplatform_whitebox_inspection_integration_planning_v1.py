#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Whitebox Inspection Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_whitebox_inspection_integration_planning_v1 import (
    BOUNDARY_FALSE,
    CHV_MAPPING,
    EVIDENCE_TRACE_MAPPING,
    FACTORY_AUTH_MAPPING,
    FINAL_DECISION_GO,
    GLOBAL_TO_LOCAL_PRINCIPLES,
    INSPECTION_LAYERS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_AUTH_EXT_DR_FINAL,
    UPSTREAM_CONSTITUTION_DR_FINAL,
    UPSTREAM_VALIDATION_SEP_DR_FINAL,
    VALIDATION_ABSORPTION,
    WHITEBOX_VISIBILITY_DOMAINS,
)

MIN_CHECKS = 90

REQUIRED = (
    "whitebox_inspection_integration_planning_policy_v1.json",
    "existing_detection_chain_input_review_v1.json",
    "whitebox_engineering_role_definition_v1.json",
    "validation_engineering_absorption_mapping_v1.json",
    "constitution_health_validation_whitebox_mapping_v1.json",
    "factory_authorization_whitebox_mapping_v1.json",
    "evidence_boundary_traceback_whitebox_mapping_v1.json",
    "global_to_local_inspection_principle_v1.json",
    "whitebox_inspection_layer_model_v1.json",
    "whitebox_drilldown_policy_v1.json",
    "ocr_real_dep_as_local_evidence_mapping_v1.json",
    "no_parallel_whitebox_policy_v1.json",
    "whitebox_integration_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "whitebox_inspection_integration_planning_decision_v1.json",
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
            "midplatform_whitebox_inspection_integration_planning"
        ),
    )
    p.add_argument(
        "--ocr-execution-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_real_minimal_controlled_execution"
        ),
    )
    p.add_argument(
        "--validation-separation-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_validation_engineering_separation_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    ocr_root = Path(args.ocr_execution_root)
    val_root = Path(args.validation_separation_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    ocr_vr = _load(ocr_root / "verifier_report.json")
    ocr_sm = _load(ocr_root / "summary.json")
    val_vr = _load(val_root / "verifier_report.json")
    val_sm = _load(val_root / "summary.json")
    summary = _load(root / "summary.json")
    role = _load(root / "whitebox_engineering_role_definition_v1.json")
    val_abs = _load(root / "validation_engineering_absorption_mapping_v1.json")
    chv = _load(root / "constitution_health_validation_whitebox_mapping_v1.json")
    factory = _load(root / "factory_authorization_whitebox_mapping_v1.json")
    evidence = _load(root / "evidence_boundary_traceback_whitebox_mapping_v1.json")
    global_local = _load(root / "global_to_local_inspection_principle_v1.json")
    layers = _load(root / "whitebox_inspection_layer_model_v1.json")
    ocr_local = _load(root / "ocr_real_dep_as_local_evidence_mapping_v1.json")
    no_parallel = _load(root / "no_parallel_whitebox_policy_v1.json")
    dryrun = _load(root / "whitebox_integration_dryrun_plan_v1.json")

    ok("upstream.ocr_go", ocr_vr.get("verifier") == "GO")
    ok("upstream.ocr_boundary", ocr_sm.get("boundary_ok") is True)
    ok("upstream.ocr_completed", ocr_sm.get("execution_completed") is True)
    ok("upstream.val_go", val_vr.get("verifier") == "GO")
    ok("upstream.val_final", val_sm.get("final_decision") == UPSTREAM_VALIDATION_SEP_DR_FINAL)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_only", summary.get("whitebox_inspection_integration_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.no_runtime", summary.get("whitebox_runtime_enabled_now") is False)
    ok("summary.no_parallel", summary.get("new_parallel_whitebox_system_created_now") is False)
    ok("summary.not_invalidated", summary.get("existing_detection_chain_invalidated_now") is False)

    ok("role.no_replace_val", role.get("whitebox_does_not_replace_validation_engineering") is True)
    ok("role.no_constitution", role.get("whitebox_does_not_redraft_constitution") is True)
    ok("role.no_provider", role.get("whitebox_does_not_execute_provider_directly") is True)
    ok("role.domains10", len(role.get("visibility_domains") or []) == 10)

    for domain in WHITEBOX_VISIBILITY_DOMAINS:
        ok(f"domain.{domain[:15]}", domain in (role.get("visibility_domains") or []))

    ok("val.absorbed8", len(val_abs.get("mappings") or []) == 8)
    for m in VALIDATION_ABSORPTION:
        ok(f"absorb.{m['component'][:12]}", any(
            x.get("component") == m["component"] for x in (val_abs.get("mappings") or [])
        ))

    ok("chv.count4", len(chv.get("mappings") or []) == 4)
    ok("factory.count5", len(factory.get("mappings") or []) == 5)
    ok("evidence.count8", len(evidence.get("mappings") or []) == 8)

    for principle in GLOBAL_TO_LOCAL_PRINCIPLES:
        ok(f"principle.{principle[:20]}", principle in (global_local.get("hard_principles") or []))

    ok("layers.count5", len(layers.get("layers") or []) == 5)
    ok("layers.default1", layers.get("default_start_level") == 1)
    ok("layers.node_drill", layers.get("node_level_requires_upstream_signal") is True)

    for layer in INSPECTION_LAYERS:
        ok(f"layer.{layer['layer_id'][:12]}", any(
            l.get("layer_id") == layer["layer_id"] for l in (layers.get("layers") or [])
        ))

    ok("ocr.local", ocr_local.get("evidence_level") == "node_level_whitebox")
    ok("ocr.not_main_chain", ocr_local.get("must_not_expand_as_main_detection_chain") is True)
    ok("ocr.read_only", ocr_local.get("read_only_evidence_source") is True)
    ok("ocr.no_auto_fix", ocr_local.get("failure_does_not_trigger_install_download_repair") is True)

    ok("no_parallel.true", no_parallel.get("no_new_parallel_whitebox_system") is True)
    ok("no_parallel.preserved", no_parallel.get("historical_detection_artifacts_preserved") is True)
    ok("no_parallel.not_invalid", no_parallel.get("previous_work_not_invalidated") is True)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("planning_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "integration_not_rebuild": True,
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
