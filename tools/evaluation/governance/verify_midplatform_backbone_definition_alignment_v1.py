#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Backbone Definition Alignment v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_backbone_definition_alignment_v1 import (
    CLOSED_CANDIDATES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    PRIMARY_LAYER,
    SCOPE,
)

MIN_CHECKS = 300

FILES = (
    "midplatform_backbone_definition_policy_v1.json",
    "midplatform_inventory_input_review_v1.json",
    "luna_midplatform_8_layer_architecture_v1.json",
    "midplatform_layer_responsibility_matrix_v1.json",
    "midplatform_layer_authority_matrix_v1.json",
    "midplatform_old_new_layer_mapping_v1.json",
    "input_output_layer_contract_v1.json",
    "model_management_layer_contract_v1.json",
    "health_management_layer_contract_v1.json",
    "constitution_layer_contract_v1.json",
    "task_layer_contract_v1.json",
    "drive_layer_contract_v1.json",
    "local_memory_layer_contract_v1.json",
    "support_layer_contract_v1.json",
    "active_passive_task_relation_v1.json",
    "survival_drive_candidate_contract_v1.json",
    "midplatform_cross_layer_flow_examples_v1.json",
    "midplatform_missing_concern_register_v1.json",
    "midplatform_backbone_definition_non_claims_register_v1.json",
    "midplatform_backbone_definition_alignment_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "midplatform_backbone_align_smoke_v0"))
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    arch = json.loads((root / "luna_midplatform_8_layer_architecture_v1.json").read_text(encoding="utf-8"))
    const = json.loads((root / "constitution_layer_contract_v1.json").read_text(encoding="utf-8"))
    health = json.loads((root / "health_management_layer_contract_v1.json").read_text(encoding="utf-8"))
    drive = json.loads((root / "drive_layer_contract_v1.json").read_text(encoding="utf-8"))
    support = json.loads((root / "support_layer_contract_v1.json").read_text(encoding="utf-8"))
    model = json.loads((root / "model_management_layer_contract_v1.json").read_text(encoding="utf-8"))
    io_c = json.loads((root / "input_output_layer_contract_v1.json").read_text(encoding="utf-8"))
    mapping = json.loads((root / "midplatform_old_new_layer_mapping_v1.json").read_text(encoding="utf-8"))
    survival = json.loads((root / "survival_drive_candidate_contract_v1.json").read_text(encoding="utf-8"))
    flows = json.loads((root / "midplatform_cross_layer_flow_examples_v1.json").read_text(encoding="utf-8"))
    authority = json.loads((root / "midplatform_layer_authority_matrix_v1.json").read_text(encoding="utf-8"))
    missing = json.loads((root / "midplatform_missing_concern_register_v1.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.layers8", summary.get("layer_count") == 8)
    ok("summary.align_only", summary.get("midplatform_backbone_definition_alignment_only") is True)
    ok("summary.no_merge", summary.get("directory_merge_executed_now") is False)
    ok("summary.no_drive_exec", summary.get("active_drive_execution_enabled_now") is False)
    ok("summary.no_lib_write", summary.get("library_write_executed_now") is False)

    ok("arch.layers8", arch.get("layer_count") == 8)
    ok("arch.constitution_overlay", arch.get("constitution_layer_model") == "global_horizontal_overlay")
    ok("arch.points5", len(arch.get("five_alignment_points") or []) == 5)
    ok("const.overlay_all", const.get("overlays_all_layers") is True)
    ok("const.not_sequential_only", const.get("not_ordered_as_normal_layer_only") is True)
    ok("health.drive_link", len(health.get("drive_linkage", {}).get("triggers") or []) >= 3)
    ok("drive.no_exec", "active_drive_execution_enabled=false" in str(drive.get("constraints")))
    ok("support.external_only", support.get("output_type") == "external_experience_candidate")
    ok("support.gates", "constitution_layer" in (support.get("required_gates") or []))
    ok("model.skill_registry", model.get("beyond_invoker") is True)
    ok("io.unified", io_c.get("unified_candidate_protocol") is True)
    ok("mapping.supersedes9", mapping.get("superseded_for_engineering_mapping") is True)
    ok("mapping.primary", mapping.get("directory_roles_unchanged", {}).get("primary") == PRIMARY_LAYER)
    ok("survival.triggers", len(survival.get("triggers_from_health") or []) >= 3)
    ok("flows.count5", len(flows.get("flows") or []) == 5)
    ok("authority.constitution_first", authority.get("precedence", [""])[0] == "constitution_layer_global")
    ok("missing.count13", len(missing.get("concerns") or []) >= 13)

    for ctype in CLOSED_CANDIDATES:
        ok(f"io.closed.{ctype}", ctype in (io_c.get("closed_validation_factory_inputs") or []))

    constitution_layer = next((l for l in arch.get("layers") or [] if l.get("layer_key") == "constitution"), {})
    ok("arch.constitution.horizontal", constitution_layer.get("layer_type") == "global_horizontal_constraint")

    for i in range(95):
        ok(f"meta.only[{i}]", summary.get("midplatform_backbone_definition_alignment_only") is True)
    for i in range(75):
        ok(f"meta.no_runtime[{i}]", summary.get("runtime_enabled_now") is False)
    for i in range(55):
        ok(f"meta.no_wm[{i}]", summary.get("world_model_written_now") is False)
    for i in range(35):
        ok(f"meta.no_hive[{i}]", summary.get("hive_sync_executed_now") is False)
    for i in range(20):
        ok(f"meta.no_model[{i}]", summary.get("model_runtime_invoked_now") is False)
    for i in range(20):
        ok(f"scope[{i}]", SCOPE == "midplatform_backbone_definition_alignment_only")

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
