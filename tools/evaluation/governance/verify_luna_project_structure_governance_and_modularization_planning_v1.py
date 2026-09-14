#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Project Structure Governance and Modularization Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Luna-Project-Structure-Governance-and-Modularization-Planning-v1-001"
FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_READY_FOR_STRUCTURE_MAP_DRYRUN"
NEXT_PHASE = "Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(
            repo_root
            / "_eval_out"
            / "luna_project_structure_governance_and_modularization_planning_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    # Required outputs
    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    policy = _load_json(root / "luna_project_structure_governance_planning_policy.json")
    audit = _load_json(root / "current_project_structure_audit.json")
    target_model = _load_json(root / "target_project_structure_model.json")
    domain_taxonomy = _load_json(root / "module_domain_taxonomy.json")
    versioning_policy = _load_json(root / "module_versioning_and_changelog_policy.json")
    doc_policy = _load_json(root / "document_reorganization_policy.json")
    organ_model = _load_json(root / "midplatform_organ_system_model.json")
    dev_backend_plan = _load_json(root / "developer_backend_extraction_plan.json")
    hardware_plan = _load_json(root / "hardware_management_consolidation_plan.json")
    future_plan = _load_json(root / "future_module_placeholder_plan.json")
    consolidation = _load_json(root / "module_consolidation_candidate_register.json")
    client_boundary = _load_json(root / "client_boundary_policy.json")
    debt = _load_json(root / "project_governance_debt_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")
    no_action = _load_json(root / "no_action_boundary_report.json")
    no_file_op = _load_json(root / "no_file_operation_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}

    ok("input.row_count", input_root_matrix.get("row_count") == len(rows), input_root_matrix.get("row_count"))

    # Required intakes must be loaded
    required_intakes = (
        "gate_taxonomy_planning",
        "post_file_stat_roadmap_decision",
        "file_stat_guarded_closure",
        "file_existence_check_guarded_closure",
        "file_metadata_boundary_closure",
        "controlled_frame_sample_closure",
        "controlled_frame_input_closure",
        "crossing_decision_closure",
        "safety_constitution",
    )
    for intake_id in required_intakes:
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)
        ok(f"input.{intake_id}.required", idx.get(intake_id, {}).get("required") is True)
        ok(f"input.{intake_id}.status=loaded", idx.get(intake_id, {}).get("status") == "loaded", idx.get(intake_id, {}).get("status"))

    # Optional intakes: allow loaded or optional_missing
    for intake_id in (
        "basic_navigation_loop_vision_strengthening_closure",
        "map_location_readonly_context",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        status = idx.get(intake_id, {}).get("status")
        ok(f"input.{intake_id}.optional", status in {"loaded", "optional_missing"}, status)

    ok("summary.phase", summary.get("phase") == PHASE_ID, summary.get("phase"))
    ok(
        "summary.planning_scope",
        summary.get("planning_scope") == "luna_project_structure_governance_and_modularization_planning_only",
        summary.get("planning_scope"),
    )

    # Required true summary keys (planning artifacts generated)
    required_true = (
        "gate_taxonomy_input_loaded",
        "post_file_stat_roadmap_input_loaded",
        "file_stat_guarded_closure_input_loaded",
        "file_existence_check_guarded_closure_input_loaded",
        "file_metadata_boundary_closure_input_loaded",
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "crossing_decision_closure_input_loaded",
        "safety_constitution_input_loaded",
        "current_project_structure_audit_generated",
        "target_project_structure_model_generated",
        "module_domain_taxonomy_generated",
        "module_versioning_policy_generated",
        "document_reorganization_policy_generated",
        "midplatform_organ_system_model_generated",
        "developer_backend_extraction_plan_generated",
        "hardware_management_consolidation_plan_generated",
        "future_module_placeholder_plan_generated",
        "module_consolidation_candidate_register_generated",
        "client_boundary_policy_generated",
        "project_governance_debt_register_generated",
        "developer_backend_not_client",
        "whitebox_not_client_runtime",
        "test_center_not_client_runtime",
        "simulation_lab_not_client_runtime",
        "evaluation_not_client_runtime",
        "hardware_monitoring_owned_by_midplatform",
        "hardware_runtime_execution_deferred",
        "module_versioning_required",
        "module_changelog_required",
        "module_interface_contract_required",
        "module_non_claims_required",
        "docs_reorganization_planned",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    )
    for k in required_true:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    # Required false summary keys (hard boundaries)
    required_false = (
        "actual_file_move_executed",
        "actual_module_merge_executed",
        "runtime_enabled",
        "existing_behavior_changed",
        "existing_phase_result_changed",
        "file_operation_invoked",
        "stat_invoked",
        "exists_invoked",
        "file_opened",
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "navigation_action_triggered",
        "speech_gate_invoked",
        "tts_invoked",
    )
    for k in required_false:
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION, summary.get("final_decision"))
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE, summary.get("recommended_next_phase"))

    # Next phase recommendation must mirror summary
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION, next_phase.get("final_decision"))
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE, next_phase.get("recommended_next_phase"))

    # Policy must reference expected filenames
    ok("policy.planning_scope", policy.get("planning_scope") == summary.get("planning_scope"), policy.get("planning_scope"))
    for ref_key, expected in (
        ("current_project_structure_audit_ref", "current_project_structure_audit.json"),
        ("target_project_structure_model_ref", "target_project_structure_model.json"),
        ("module_domain_taxonomy_ref", "module_domain_taxonomy.json"),
        ("module_versioning_policy_ref", "module_versioning_and_changelog_policy.json"),
        ("document_reorganization_policy_ref", "document_reorganization_policy.json"),
        ("developer_backend_extraction_plan_ref", "developer_backend_extraction_plan.json"),
        ("midplatform_modularization_plan_ref", "midplatform_organ_system_model.json"),
        ("future_module_placeholder_plan_ref", "future_module_placeholder_plan.json"),
        ("governance_debt_register_ref", "project_governance_debt_register.json"),
        ("no_runtime_boundary_ref", "no_runtime_boundary_report.json"),
    ):
        ok(f"policy.{ref_key}", policy.get(ref_key) == expected, policy.get(ref_key))

    # Audit checks (non-fact)
    ok("audit.fact_status", audit.get("fact_status") == "not_fact", audit.get("fact_status"))
    ok("audit.write_allowed=false", audit.get("write_allowed") is False, audit.get("write_allowed"))
    ok("audit.audit_sections.list", isinstance(audit.get("audit_sections"), list), type(audit.get("audit_sections")).__name__)
    sections = audit.get("audit_sections", [])
    ok("audit.audit_sections.count>=8", len(sections) >= 8, len(sections))

    # Each audit section must have counts keys and be not_fact
    required_count_keys = ("visited_dir_count", "file_count", "md_count", "py_count", "json_count", "sample_paths", "truncated")
    for i, s in enumerate(sections[:30]):
        ok(f"audit.section[{i}].section_id", bool(s.get("section_id")), s.get("section_id"))
        counts = (s.get("counts") or {})
        for ck in required_count_keys:
            ok(f"audit.section[{i}].counts.{ck}.present", ck in counts, list(counts.keys()))
        ok(f"audit.section[{i}].counts.not_fact", counts.get("fact_status") == "not_fact", counts.get("fact_status"))
        ok(f"audit.section[{i}].counts.write_allowed=false", counts.get("write_allowed") is False, counts.get("write_allowed"))
        # Sample paths must be bounded
        sp = counts.get("sample_paths") or []
        ok(f"audit.section[{i}].counts.sample_paths<=20", isinstance(sp, list) and len(sp) <= 20, len(sp) if isinstance(sp, list) else type(sp).__name__)

    ok("audit.current_doc_count>=0", isinstance(audit.get("current_doc_count"), int) and audit.get("current_doc_count") >= 0, audit.get("current_doc_count"))
    ok("audit.current_eval_phase_count>=0", isinstance(audit.get("current_eval_phase_count"), int) and audit.get("current_eval_phase_count") >= 0, audit.get("current_eval_phase_count"))
    ok("audit.current_closure_count>=0", isinstance(audit.get("current_closure_count"), int) and audit.get("current_closure_count") >= 0, audit.get("current_closure_count"))

    # Target model checks
    ok("target_model.not_fact", target_model.get("fact_status") == "not_fact", target_model.get("fact_status"))
    tlm = target_model.get("target_top_level_model") or []
    ok("target_model.target_top_level_model.list", isinstance(tlm, list), type(tlm).__name__)
    ok("target_model.target_top_level_model.len>=6", len(tlm) >= 6, len(tlm))

    # Domain taxonomy checks
    ok("domain_taxonomy.not_fact", domain_taxonomy.get("fact_status") == "not_fact", domain_taxonomy.get("fact_status"))
    domains = domain_taxonomy.get("domains") or []
    ok("domain_taxonomy.domains.list", isinstance(domains, list), type(domains).__name__)
    ok("domain_taxonomy.domain_count==len(domains)", domain_taxonomy.get("domain_count") == len(domains), domain_taxonomy.get("domain_count"))
    ok("domain_taxonomy.domain_count>=10", len(domains) >= 10, len(domains))
    for i, d in enumerate(domains[:40]):
        for k in ("domain_id", "domain_name", "owner_layer"):
            ok(f"domain[{i}].{k}.present", bool(d.get(k)), d.get(k))
        ok(f"domain[{i}].current_status", d.get("current_status") == "planning_only", d.get("current_status"))
        ok(f"domain[{i}].runtime_status=false", d.get("runtime_status") is False, d.get("runtime_status"))
        ok(f"domain[{i}].write_status=false", d.get("write_status") is False, d.get("write_status"))
        ok(f"domain[{i}].versioning_required=true", d.get("versioning_required") is True, d.get("versioning_required"))
        ok(f"domain[{i}].documentation_required=true", d.get("documentation_required") is True, d.get("documentation_required"))

    # Versioning policy checks
    ok("versioning_policy.not_fact", versioning_policy.get("fact_status") == "not_fact", versioning_policy.get("fact_status"))
    ok("versioning_policy.module_versioning_required", versioning_policy.get("module_versioning_required") is True, versioning_policy.get("module_versioning_required"))
    required_files = versioning_policy.get("required_files") or []
    ok("versioning_policy.required_files.list", isinstance(required_files, list), type(required_files).__name__)
    ok("versioning_policy.required_files.len>=8", len(required_files) >= 8, len(required_files))
    maturity_levels = versioning_policy.get("maturity_levels") or []
    ok("versioning_policy.maturity_levels.list", isinstance(maturity_levels, list), type(maturity_levels).__name__)
    ok("versioning_policy.maturity_levels.len>=6", len(maturity_levels) >= 6, len(maturity_levels))

    # Doc policy checks
    ok("doc_policy.not_fact", doc_policy.get("fact_status") == "not_fact", doc_policy.get("fact_status"))
    ok("doc_policy.docs_reorganization_planned", doc_policy.get("docs_reorganization_planned") is True, doc_policy.get("docs_reorganization_planned"))
    ok("doc_policy.mapping_plan_only", doc_policy.get("mapping_plan_only") is True, doc_policy.get("mapping_plan_only"))
    ok("doc_policy.proposed_structure.list", isinstance(doc_policy.get("proposed_structure"), list), type(doc_policy.get("proposed_structure")).__name__)

    # Midplatform organ system model checks
    ok("organ_model.not_fact", organ_model.get("fact_status") == "not_fact", organ_model.get("fact_status"))
    subsystems = organ_model.get("subsystems") or []
    ok("organ_model.subsystems.list", isinstance(subsystems, list), type(subsystems).__name__)
    ok("organ_model.subsystem_count==len(subsystems)", organ_model.get("subsystem_count") == len(subsystems), organ_model.get("subsystem_count"))
    ok("organ_model.subsystem_count>=8", len(subsystems) >= 8, len(subsystems))
    for i, s in enumerate(subsystems[:60]):
        ok(f"subsystem[{i}].subsystem_id.present", bool(s.get("subsystem_id")), s.get("subsystem_id"))
        ok(f"subsystem[{i}].runtime_status=false", s.get("runtime_status") is False, s.get("runtime_status"))
        ok(f"subsystem[{i}].versioning_required=true", s.get("versioning_required") is True, s.get("versioning_required"))

    # Developer backend plan checks
    ok("dev_backend_plan.not_fact", dev_backend_plan.get("fact_status") == "not_fact", dev_backend_plan.get("fact_status"))
    for k in (
        "developer_backend_not_client",
        "whitebox_not_client_runtime",
        "test_center_not_client_runtime",
        "simulation_lab_not_client_runtime",
        "evaluation_not_client_runtime",
        "production_client_excludes_developer_backend",
    ):
        ok(f"dev_backend_plan.{k}", dev_backend_plan.get(k) is True, dev_backend_plan.get(k))
    ok("dev_backend_plan.components.list", isinstance(dev_backend_plan.get("components"), list), type(dev_backend_plan.get("components")).__name__)
    ok("dev_backend_plan.components.len>=6", len(dev_backend_plan.get("components") or []) >= 6, len(dev_backend_plan.get("components") or []))

    # Hardware plan checks
    ok("hardware_plan.not_fact", hardware_plan.get("fact_status") == "not_fact", hardware_plan.get("fact_status"))
    ok("hardware_plan.hardware_monitoring_owned_by_midplatform", hardware_plan.get("hardware_monitoring_owned_by_midplatform") is True, hardware_plan.get("hardware_monitoring_owned_by_midplatform"))
    ok("hardware_plan.hardware_runtime_execution_deferred", hardware_plan.get("hardware_runtime_execution_deferred") is True, hardware_plan.get("hardware_runtime_execution_deferred"))
    ok("hardware_plan.coverage.list", isinstance(hardware_plan.get("coverage"), list), type(hardware_plan.get("coverage")).__name__)

    # Future placeholder plan checks
    ok("future_plan.not_fact", future_plan.get("fact_status") == "not_fact", future_plan.get("fact_status"))
    futures = future_plan.get("future_modules") or []
    ok("future_plan.future_modules.list", isinstance(futures, list), type(futures).__name__)
    ok("future_plan.count==len", future_plan.get("future_placeholder_module_count") == len(futures), future_plan.get("future_placeholder_module_count"))
    ok("future_plan.count>=8", len(futures) >= 8, len(futures))
    for i, f in enumerate(futures[:80]):
        ok(f"future[{i}].future_module_id.present", bool(f.get("future_module_id")), f.get("future_module_id"))
        ok(f"future[{i}].current_status=placeholder_only", f.get("current_status") == "placeholder_only", f.get("current_status"))
        ok(f"future[{i}].runtime_status=false", f.get("runtime_status") is False, f.get("runtime_status"))
        ok(f"future[{i}].write_status=false", f.get("write_status") is False, f.get("write_status"))

    # Consolidation candidates
    ok("consolidation.not_fact", consolidation.get("fact_status") == "not_fact", consolidation.get("fact_status"))
    candidates = consolidation.get("candidates") or []
    ok("consolidation.candidates.list", isinstance(candidates, list), type(candidates).__name__)
    ok("consolidation.count==len", consolidation.get("consolidation_candidate_count") == len(candidates), consolidation.get("consolidation_candidate_count"))
    ok("consolidation.count>=6", len(candidates) >= 6, len(candidates))
    for i, c in enumerate(candidates[:60]):
        ok(f"candidate[{i}].id.present", bool(c.get("consolidation_candidate_id")), c.get("consolidation_candidate_id"))
        ok(f"candidate[{i}].planning_only=true", c.get("planning_only") is True, c.get("planning_only"))
        ok(f"candidate[{i}].should_merge_now=false", c.get("should_merge_now") is False, c.get("should_merge_now"))

    # Client boundary policy
    ok("client_boundary.not_fact", client_boundary.get("fact_status") == "not_fact", client_boundary.get("fact_status"))
    ok("client_boundary.developer_backend_excluded.list", isinstance(client_boundary.get("developer_backend_excluded"), list), type(client_boundary.get("developer_backend_excluded")).__name__)
    ok("client_boundary.client_allowed_candidates.list", isinstance(client_boundary.get("client_allowed_candidates"), list), type(client_boundary.get("client_allowed_candidates")).__name__)

    # Governance debt register
    ok("debt.not_fact", debt.get("fact_status") == "not_fact", debt.get("fact_status"))
    ok("debt.topic_count==len(topics)", debt.get("topic_count") == len(debt.get("topics") or []), debt.get("topic_count"))
    ok("debt.topic_count>=8", len(debt.get("topics") or []) >= 8, len(debt.get("topics") or []))

    # Boundary reports must be conservative and identical in key booleans
    for name, rep in (
        ("no_runtime", no_runtime),
        ("no_write", no_write),
        ("no_action", no_action),
        ("no_file_operation", no_file_op),
    ):
        ok(f"{name}.planning_only", rep.get("planning_only") is True, rep.get("planning_only"))
        ok(f"{name}.runtime_enabled=false", rep.get("runtime_enabled") is False, rep.get("runtime_enabled"))
        ok(f"{name}.file_operation_invoked=false", rep.get("file_operation_invoked") is False, rep.get("file_operation_invoked"))
        ok(f"{name}.stat_invoked=false", rep.get("stat_invoked") is False, rep.get("stat_invoked"))
        ok(f"{name}.exists_invoked=false", rep.get("exists_invoked") is False, rep.get("exists_invoked"))
        ok(f"{name}.file_opened=false", rep.get("file_opened") is False, rep.get("file_opened"))
        ok(f"{name}.file_content_read=false", rep.get("file_content_read") is False, rep.get("file_content_read"))
        ok(f"{name}.image_content_read=false", rep.get("image_content_read") is False, rep.get("image_content_read"))
        ok(f"{name}.video_content_read=false", rep.get("video_content_read") is False, rep.get("video_content_read"))
        ok(f"{name}.real_file_hash_computed=false", rep.get("real_file_hash_computed") is False, rep.get("real_file_hash_computed"))
        ok(f"{name}.perceptual_hash_computed=false", rep.get("perceptual_hash_computed") is False, rep.get("perceptual_hash_computed"))
        ok(f"{name}.camera_invoked=false", rep.get("camera_invoked") is False, rep.get("camera_invoked"))
        ok(f"{name}.visual_model_invoked=false", rep.get("visual_model_invoked") is False, rep.get("visual_model_invoked"))
        ok(f"{name}.ocr_provider_invoked=false", rep.get("ocr_provider_invoked") is False, rep.get("ocr_provider_invoked"))
        ok(f"{name}.tracking_runtime_invoked=false", rep.get("tracking_runtime_invoked") is False, rep.get("tracking_runtime_invoked"))
        ok(f"{name}.crossing_runtime_invoked=false", rep.get("crossing_runtime_invoked") is False, rep.get("crossing_runtime_invoked"))
        ok(f"{name}.navigation_action_triggered=false", rep.get("navigation_action_triggered") is False, rep.get("navigation_action_triggered"))
        ok(f"{name}.world_model_written=false", rep.get("world_model_written") is False, rep.get("world_model_written"))
        ok(f"{name}.memory_written=false", rep.get("memory_written") is False, rep.get("memory_written"))
        ok(f"{name}.library_written=false", rep.get("library_written") is False, rep.get("library_written"))
        ok(f"{name}.fact_written=false", rep.get("fact_written") is False, rep.get("fact_written"))
        ok(f"{name}.boundary_ok=true", rep.get("boundary_ok") is True, rep.get("boundary_ok"))
        ok(f"{name}.violations.list", isinstance(rep.get("violations"), list), type(rep.get("violations")).__name__)

    # Sanity: check_count >= baseline and >= MIN_CHECKS
    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "passed": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())

