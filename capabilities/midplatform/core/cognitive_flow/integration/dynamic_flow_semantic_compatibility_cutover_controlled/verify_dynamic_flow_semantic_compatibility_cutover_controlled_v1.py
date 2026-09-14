"""Static/source verifier for the Dynamic Flow compatibility cutover."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

VERIFIER_PATH = Path(__file__).resolve()
for _candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.dynamic_flow_semantic_compatibility_cutover_controlled.dynamic_flow_semantic_compatibility_fixture_v1 import build_compatibility_run_v1  # noqa: E402
from capabilities.midplatform.core.cognitive_flow.integration.dynamic_flow_semantic_compatibility_cutover_controlled.dynamic_flow_semantic_compatibility_registry_v1 import PHASE, negative_guards  # noqa: E402


PACKAGE_DIR = Path(__file__).resolve().parent
EXPECTED_SOURCE_SET = {
    "__init__.py",
    "dynamic_flow_semantic_compatibility_engine_v1.py",
    "dynamic_flow_semantic_compatibility_fixture_v1.py",
    "dynamic_flow_semantic_compatibility_registry_v1.py",
    "dynamic_flow_semantic_compatibility_types_v1.py",
    "run_dynamic_flow_semantic_compatibility_cutover_controlled_v1.py",
    "verify_dynamic_flow_semantic_compatibility_cutover_controlled_v1.py",
}

DOC_NAMES = (
    "a_semantic_interpretation_cutover_v1.md",
    "change_manifest.md",
    "direct_caller_inventory_v1.md",
    "dynamic_flow_compatibility_output_v1.md",
    "implementation_overview_v1.md",
    "legacy_field_retention_v1.md",
    "multi_loop_dependency_v1.md",
    "negative_guards_v1.md",
    "phase_contract.md",
    "real_capability_single_invocation_contract_preservation_v1.md",
    "real_input_adapter_cutover_v1.md",
    "regression_checkpoint_note_v1.md",
    "scenario_mapping_v1.json",
)


def _jsonable(value):
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_jsonable(item) for item in value)
    return value


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "docs").is_dir() and (parent / "capabilities").is_dir():
            return parent
    return Path(__file__).resolve().parents[6]


def _contains(path: Path, *needles: str) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return all(needle in text for needle in needles)


def _source_names() -> set[str]:
    """Return implementation sources only; ignore __pycache__ and artifacts."""
    return {
        item.name
        for item in PACKAGE_DIR.iterdir()
        if item.is_file() and item.suffix == ".py"
    }


def _source_set_check() -> dict[str, object]:
    actual = _source_names()
    expected = set(EXPECTED_SOURCE_SET)
    return {
        "actual": sorted(actual),
        "expected": sorted(expected),
        "actual_only": sorted(actual - expected),
        "expected_only": sorted(expected - actual),
        "passed": actual == expected,
    }


def _engine_content_diagnostic(path: Path) -> dict[str, bool]:
    """Check the engine's contract surface, not a non-contractual field spelling."""
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    predicates = {
        "compatibility_output_builder": "def build_compatibility_output(" in text,
        "compatibility_output_type": "DynamicFlowCompatibilityOutputV1(" in text,
        "a_interpretation_adapter": "def interpret_for_a(" in text,
        "verified_a_wrapper": "wrap_dynamic_flow_output(" in text,
        "compatibility_source_owner": "source_owner_ref=SOURCE_OWNER" in text,
    }
    return {**predicates, "passed": all(predicates.values())}


def build_verification_summary_v1() -> dict[str, object]:
    root = _repo_root()
    results = build_compatibility_run_v1()
    guards = negative_guards()
    package = PACKAGE_DIR
    docs_dir = root / "docs" / "architecture" / "phase_luna_dynamic_flow_semantic_compatibility_cutover_controlled_v1"
    engine_content_diagnostic = _engine_content_diagnostic(
        package / "dynamic_flow_semantic_compatibility_engine_v1.py"
    )
    source_content_checks = {
        "types": _contains(package / "dynamic_flow_semantic_compatibility_types_v1.py", "DynamicFlowCompatibilityOutputV1", "semantic_authority: bool = False"),
        "engine": engine_content_diagnostic["passed"],
        "fixture": _contains(package / "dynamic_flow_semantic_compatibility_fixture_v1.py", "build_compatibility_scenario_specs_v1", "DynamicCognitiveLoopOutputV1"),
        "runner": _contains(package / "run_dynamic_flow_semantic_compatibility_cutover_controlled_v1.py", "all_cases_passed", "failed_case_ids"),
        "verifier": _contains(package / "verify_dynamic_flow_semantic_compatibility_cutover_controlled_v1.py", "documentation_set_ok", "source_set_ok"),
    }
    source_set_check = _source_set_check()
    source_manifest_ok = bool(source_set_check["passed"])
    source_content_ok = all(source_content_checks.values())
    real_trial = root / "capabilities/midplatform/core/cognitive_flow/integration/dynamic_cognitive_flow_real_capability_single_invocation_trial"
    real_trial_text = "\n".join(path.read_text(encoding="utf-8") for path in real_trial.glob("*.py")) if real_trial.is_dir() else ""
    direct_cutover = all(item.direct_semantic_consumption_blocked and item.interpretation.a_decisions.compatibility_wrapper_only for item in results)
    checks = {
        "scenario_cases_ok": all(item.passed for item in results),
        "compatibility_output_boundary_ok": all(
            item.compatibility_output.compatibility_only and not item.compatibility_output.semantic_authority
            for item in results
        ),
        "a_need_authority_ok": all(item.interpretation.a_decisions.need_decision.decision_owner_ref == "A_REASONING_ROLE" for item in results),
        "a_sufficiency_authority_ok": all(item.interpretation.a_decisions.sufficiency_decision.decision_owner_ref == "A_REASONING_ROLE" for item in results),
        "a_reconsideration_authority_ok": all(item.interpretation.a_decisions.reconsideration_decision.decision_owner_ref == "A_REASONING_ROLE" for item in results),
        "a_next_step_authority_ok": all(item.interpretation.a_decisions.next_step_decision.decision_owner_ref == "A_REASONING_ROLE" for item in results),
        "direct_caller_cutover_ok": direct_cutover,
        "loop_boundary_ok": guards["loop_semantic_authority"] is False,
        "real_capability_single_invocation_contract_preserved": all(
            needle in real_trial_text
            for needle in ("real_provider_invocation_count", "<= 1", "provider_invocation")
        ),
        "legacy_compatibility_ok": all(
            needle in (root / "capabilities/midplatform/core/cognitive_flow/cognitive_dynamic_loop_types_v1.py").read_text(encoding="utf-8")
            for needle in ("current_minimum_need_ref", "final_disposition", "next_step_disposition", "reconsiderations")
        ),
        "computation_keep_boundary_ok": all(
            needle in (root / "capabilities/midplatform/core/cognitive_flow/cognitive_dynamic_loop_engine_v1.py").read_text(encoding="utf-8")
            for needle in ("state_versions", "trace_refs", "provenance_refs", "non_materialized_plan_refs")
        ),
        "negative_guards_ok": all(
            guards[key] == expected
            for key, expected in {
                "candidate_only": True,
                "synthetic_only": True,
                "dynamic_flow_semantic_authority": False,
                "dynamic_flow_direct_semantic_consumption": False,
                "a_need_authority": True,
                "a_sufficiency_authority": True,
                "a_reconsideration_authority": True,
                "a_next_step_authority": True,
                "provider_invocation": False,
                "brain_runtime": False,
            }.items()
        ),
        "source_set_ok": source_manifest_ok and source_content_ok,
        "documentation_set_ok": docs_dir.is_dir() and all((docs_dir / name).is_file() for name in DOC_NAMES),
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    failed_case_ids = [item.scenario_id for item in results if not item.passed]
    return {
        "phase": PHASE,
        "scenario_count": len(results),
        "all_checks_passed": not failed_checks,
        "failed_case_ids": failed_case_ids,
        "failed_checks": failed_checks,
        "source_set_diagnostic": {
            **source_set_check,
            "content_checks": source_content_checks,
            "engine_content_diagnostic": engine_content_diagnostic,
        },
        "source_manifest_ok": source_manifest_ok,
        "source_content_ok": source_content_ok,
        **checks,
    }


def main() -> int:
    summary = build_verification_summary_v1()
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
