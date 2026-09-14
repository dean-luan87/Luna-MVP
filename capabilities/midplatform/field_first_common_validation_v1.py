# -*- coding: utf-8 -*-
"""Field-First common validation baseline for evaluation verifiers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)


@dataclass
class CommonValidationConfig:
    repo_root: Path
    output_root: Path
    summary: Dict[str, Any]
    report: Dict[str, Any]
    file_size_review: Dict[str, Any]
    phase_id: str
    scope: str
    final_decision_go: str
    selected_next_phase: str
    go_conditions_keys: Tuple[str, ...]
    artifacts: Tuple[str, ...]
    docs: Tuple[str, ...]
    phase_python_files: Tuple[str, ...]
    whitelist_files: Tuple[str, ...]
    upstream_summary: Optional[Dict[str, Any]] = None
    upstream_verifier: Optional[Dict[str, Any]] = None
    upstream_final_go: Optional[str] = None
    upstream_pass_flag: Optional[str] = None
    upstream_min_checks: int = 360
    pass_flag_key: str = ""
    md_report_name: str = ""


def _add(checks: List[Dict[str, Any]], category: str, check_id: str, ok: bool) -> None:
    checks.append({"category": category, "check_id": check_id, "passed": bool(ok)})


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        import json
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except Exception:
        return {}


def run_project_common_validation(cfg: CommonValidationConfig) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    for name in cfg.artifacts:
        if name in ("verifier_report.json", "common_validation_reuse_report_v1.json"):
            continue
        _add(checks, "project_common", f"art.{name[:24]}", (cfg.output_root / name).is_file() and bool(_read_json(cfg.output_root / name)))
    for doc in cfg.docs:
        _add(checks, "project_common", f"doc.{doc.split('/')[-1][:20]}", (cfg.repo_root / doc).is_file())
    if cfg.upstream_summary and cfg.upstream_final_go:
        _add(checks, "project_common", "up.final", cfg.upstream_summary.get("final_decision") == cfg.upstream_final_go)
    if cfg.upstream_verifier:
        _add(checks, "project_common", "up.verifier", cfg.upstream_verifier.get("verifier") == "GO")
        _add(checks, "project_common", "up.checks", int(cfg.upstream_verifier.get("passed_checks", 0)) >= cfg.upstream_min_checks)
    if cfg.upstream_pass_flag and cfg.upstream_summary:
        _add(checks, "project_common", "up.pass_flag", cfg.upstream_summary.get(cfg.upstream_pass_flag) is True)
    _add(checks, "project_common", "sum.phase", cfg.summary.get("phase") == cfg.phase_id)
    _add(checks, "project_common", "sum.scope", cfg.summary.get("scope") == cfg.scope)
    _add(checks, "project_common", "sum.final", cfg.summary.get("final_decision") == cfg.final_decision_go)
    _add(checks, "project_common", "sum.next", cfg.summary.get("recommended_next_phase") == cfg.selected_next_phase)
    _add(checks, "project_common", "sum.blocker0", cfg.summary.get("blocker_count") == 0)
    if cfg.pass_flag_key:
        _add(checks, "project_common", "sum.pass_flag", cfg.summary.get(cfg.pass_flag_key) is True)
    if cfg.md_report_name:
        _add(checks, "project_common", "md.exists", (cfg.output_root / cfg.md_report_name).is_file())
    _add(checks, "project_common", "report.final", cfg.report.get("final_decision") == cfg.final_decision_go)
    for k in cfg.go_conditions_keys:
        _add(checks, "project_common", f"go.{k[:20]}", cfg.summary.get(k) is True)
    return checks


def run_field_first_common_validation(cfg: CommonValidationConfig) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    ff_keys = (
        "field_first_route_preserved", "continuity_before_tracking", "tracking_depends_on_continuity",
        "midplatform_still_has_remaining_work", "foundation_consolidation_not_final_midplatform_completion",
        "no_fragmentary_phase_expansion", "integration_test_executed",
    )
    for k in ff_keys:
        if k in cfg.summary:
            _add(checks, "field_first_common", f"ff.{k[:18]}", cfg.summary.get(k) is (False if k == "integration_test_executed" else True))
    chain = cfg.summary.get("chain_trace_nodes") or []
    _add(checks, "field_first_common", "chain.len", len(chain) >= 5)
    for idx, k in enumerate(ABSENCE_KEYS):
        if k in cfg.summary:
            _add(checks, "field_first_common", f"abs.{idx}", cfg.summary.get(k) is True)
    return checks


def run_candidate_boundary_validation(cfg: CommonValidationConfig) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    boundary_keys = (
        "candidate_only_outputs", "no_world_model_fact_creation", "no_persistent_memory_write",
        "tracker_id_is_hint_not_fact",
    )
    for k in boundary_keys:
        if k in cfg.summary:
            _add(checks, "candidate_boundary", f"cand.{k[:18]}", cfg.summary.get(k) is True)
    _add(checks, "candidate_boundary", "runtime.not_enabled", cfg.summary.get("runtime_status") == "not_enabled" or cfg.report.get("runtime_status") == "not_enabled")
    return checks


def run_non_execution_boundary_validation(cfg: CommonValidationConfig) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    guard_keys = (
        "non_execution_boundary_ok", "no_model_download", "no_weight_download", "no_real_inference_execution",
        "no_runtime_execution", "no_integration_test", "no_real_tracking_execution", "no_trajectory_prediction",
        "no_task_simulation", "no_task_execution", "no_field_simulation", "no_semantic_attachment",
        "no_final_action_output",
    )
    for k in guard_keys:
        if k in cfg.summary:
            _add(checks, "non_execution_boundary", f"guard.{k[:18]}", cfg.summary.get(k) is True)
    return checks


def run_file_size_governance_validation(cfg: CommonValidationConfig) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    fs = cfg.file_size_review
    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, "file_size_governance", f"fs.{k[:18]}", cfg.summary.get(k) is True or fs.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, "file_size_governance", f"fsr.{k[:18]}", fs.get(k) is True)
    for rel in cfg.whitelist_files:
        _add(checks, "file_size_governance", f"wl.{rel.split('/')[-1][:14]}", (cfg.repo_root / rel).is_file())
    for rel in cfg.phase_python_files:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, "file_size_governance", f"pf.{rel.split('/')[-1][:14]}", row.get("tier") == "ok")
    return checks


def run_all_common_validations(cfg: CommonValidationConfig) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    categories = (
        run_project_common_validation(cfg),
        run_field_first_common_validation(cfg),
        run_candidate_boundary_validation(cfg),
        run_non_execution_boundary_validation(cfg),
        run_file_size_governance_validation(cfg),
    )
    checks: List[Dict[str, Any]] = []
    for group in categories:
        checks.extend(group)
    by_category: Dict[str, Dict[str, Any]] = {}
    for cat in ("project_common", "field_first_common", "candidate_boundary", "non_execution_boundary", "file_size_governance"):
        cat_checks = [c for c in checks if c["category"] == cat]
        by_category[cat] = {
            "count": len(cat_checks),
            "passed": sum(1 for c in cat_checks if c["passed"]),
            "failed": sum(1 for c in cat_checks if not c["passed"]),
        }
    report = {
        "report_id": "common_validation_reuse_report_v1",
        "common_validation_reuse_ok": all(c["passed"] for c in checks),
        "categories": by_category,
        "total_checks": len(checks),
        "total_passed": sum(1 for c in checks if c["passed"]),
        "reused_modules": (
            "field_first_common_validation_v1",
            "file_size_module_split_governance_rule_v1",
            "task_manager_foundation_handoff_absence_keys",
        ),
    }
    return checks, report


def flatten_checks(checks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{"check_id": f"{c['category']}.{c['check_id']}", "passed": c["passed"]} for c in checks]
