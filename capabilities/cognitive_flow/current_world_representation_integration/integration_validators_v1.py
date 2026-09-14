"""Pure contract and static validators for CWR integration DryRun v1."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable, Mapping, Tuple

from .integration_types_v1 import CurrentWorldRepresentationIntegrationDryRunResultV1


_BANNED_IMPORTS_V1 = {"requests", "httpx", "sqlite3", "sqlalchemy", "pymongo", "redis", "random", "uuid"}
_BANNED_TIME_CALLS_V1 = {"now", "utcnow", "today", "time"}


def validate_result_v1(result: CurrentWorldRepresentationIntegrationDryRunResultV1) -> Tuple[str, ...]:
    """Return stable failed-check names; an empty tuple means result validity."""

    failed = []
    if result.runtime_executed:
        failed.append("runtime_executed_must_be_false")
    if not result.simulation_only:
        failed.append("simulation_only_must_be_true")
    for name in (
        "reference_chain_valid", "version_chain_valid", "mutation_authority_valid",
        "readonly_boundary_valid", "unknown_preservation_valid", "context_isolation_valid",
        "cognitive_writeback_absent",
    ):
        if not getattr(result, name):
            failed.append(name)
    if result.active_context_ref not in result.context_refs:
        failed.append("active_context_ref_not_resolvable")
    if result.case_id == "case_05_context_insufficient" and result.analysis_boundary_admission:
        failed.append("insufficient_context_entered_analysis_boundary")
    if result.case_id == "case_06_evidence_revoked" and "evidence_revoked" not in result.failure_codes:
        failed.append("revoked_evidence_not_preserved")
    return tuple(failed)


def validate_all_results_v1(results: Iterable[CurrentWorldRepresentationIntegrationDryRunResultV1]) -> Mapping[str, Tuple[str, ...]]:
    return {result.case_id: validate_result_v1(result) for result in results}


def static_negative_guard_results_v1(source_root: Path) -> Tuple[str, ...]:
    """Inspect code AST only; documentation policy words are intentionally excluded."""

    failures = []
    for path in sorted(source_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name.split(".")[0] for alias in node.names]
                for name in names:
                    if name in _BANNED_IMPORTS_V1:
                        failures.append(f"banned_import:{name}:{path.name}")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in _BANNED_TIME_CALLS_V1:
                    failures.append(f"banned_time_call:{node.func.attr}:{path.name}")
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                lowered = node.name.lower()
                if "mutate" in lowered or "write_field_state" in lowered:
                    failures.append(f"direct_state_mutation_helper:{node.name}:{path.name}")
            if isinstance(node, ast.ClassDef):
                lowered = node.name.lower()
                if "hypothesis" in lowered or "decision" in lowered or "experience" in lowered:
                    failures.append(f"forbidden_output_type:{node.name}:{path.name}")
    return tuple(failures)
