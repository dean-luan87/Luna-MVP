"""Independent serialized-output verifier for A3 Translation Validation Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Tuple


_PHASE_V1 = "Phase-A3-Evidence-Context-Translation-Layer-Validation-Closure-Execution-v1-001"
_SCHEMA_V1 = "luna.cognitive_analysis.translation_validation_closure.v1"
_CONTRACT_V1 = "LUNA-A3-EVIDENCE-CONTEXT-TRANSLATION-CONTRACT-V1"
_CASES_V1 = {
    "case_1_ocr_translation": ("ocr", "semantic_candidate", "exit_related_candidate"),
    "case_2_vision_translation": ("vision", "entity_candidate", "human_candidate"),
    "case_3_spatial_translation": ("spatial", "spatial_candidate", "location_related_candidate"),
    "case_4_audio_translation": ("audio", "semantic_candidate", "speaker_related_candidate"),
    "case_5_provenance_trace": ("provenance_trace", "temporal_candidate", "trace_preserving_candidate"),
}
_GUARDS_V1 = {
    "Guard-1-evidence-to-fact-forbidden",
    "Guard-2-evidence-to-decision-forbidden",
    "Guard-3-provenance-required",
    "Guard-4-external-model-identity-not-cognitive-entity",
    "Guard-5-context-snapshot-field-state-mutation-forbidden",
}
_JSON_FILES_V1 = (
    "translation_validation_result_v1.json",
    "semantic_boundary_result_v1.json",
    "provenance_closure_result_v1.json",
    "negative_guard_result_v1.json",
    "deterministic_result_v1.json",
)


def _canonical_json_v1(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _read_json_v1(path: Path) -> Tuple[Dict[str, Any], bool]:
    if not path.is_file():
        return {}, False
    raw = path.read_text(encoding="utf-8")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return {}, False
    return value, raw == _canonical_json_v1(value)


def verify_cognitive_translation_validation_closure_v1(
    output_dir: Path,
    comparison_dir: Path | None = None,
) -> Dict[str, Any]:
    """Read serialized closure evidence only; never imports Runner or Translation Skeleton."""
    payloads = {}
    canonical_checks = []
    for filename in _JSON_FILES_V1:
        payload, canonical = _read_json_v1(output_dir / filename)
        payloads[filename] = payload
        canonical_checks.append(canonical)
    result = payloads["translation_validation_result_v1.json"]
    semantic = payloads["semantic_boundary_result_v1.json"]
    provenance = payloads["provenance_closure_result_v1.json"]
    guards = payloads["negative_guard_result_v1.json"]
    deterministic = payloads["deterministic_result_v1.json"]
    flags = result.get("validation_flags", {})
    checks = [
        all(canonical_checks),
        result.get("phase") == _PHASE_V1,
        result.get("schema_version") == _SCHEMA_V1,
        result.get("contract_ref") == _CONTRACT_V1,
        result.get("case_count") == len(_CASES_V1),
        result.get("all_cases_passed") is True,
        result.get("blocker_count") == 0,
        flags.get("validation_executed") is True,
        all(flags.get(name) is False for name in (
            "runtime_executed", "model_invoked", "external_call", "state_writeback",
            "fact_created", "decision_created", "action_created", "memory_updated",
        )),
        semantic.get("passed") is True,
        provenance.get("passed") is True,
        guards.get("passed") is True,
        set(guards.get("required_guard_ids", ())) == _GUARDS_V1,
        deterministic.get("passed") is True,
        deterministic.get("run1_equals_run2") is True,
        deterministic.get("canonical_json") is True,
        deterministic.get("random_id_present") is False,
        deterministic.get("timestamp_drift_present") is False,
        deterministic.get("environment_path_drift_present") is False,
    ]
    observed = set()
    for case in result.get("case_results", ()):
        case_id = case.get("case_id")
        observed.add(case_id)
        expected = _CASES_V1.get(case_id)
        envelope = case.get("translation_candidate_envelope", {})
        candidate = envelope.get("cognitive_primitive_candidate", {})
        request = case.get("request", {})
        case_guards = case.get("negative_guard_results", {})
        checks.extend((
            expected is not None,
            case.get("fixture_kind") == (expected[0] if expected else None),
            case.get("expected_primitive_type") == (expected[1] if expected else None),
            case.get("expected_candidate_label") == (expected[2] if expected else None),
            case.get("contract_valid") is True,
            case.get("semantic_boundary_passed") is True,
            case.get("provenance_closure_passed") is True,
            case.get("case_passed") is True,
            candidate.get("candidate_only") is True,
            candidate.get("fact_status") == "not_fact",
            candidate.get("candidate_status") == "translation_not_executed",
            candidate.get("primitive_type") == (expected[1] if expected else None),
            candidate.get("source_refs") == request.get("evidence_refs"),
            candidate.get("context_refs") == request.get("context_refs"),
            candidate.get("trace_ref") == request.get("trace_ref"),
            set(case_guards) == _GUARDS_V1 and all(case_guards.values()),
        ))
    checks.append(observed == set(_CASES_V1))
    comparison_ok = True
    if comparison_dir is not None:
        for filename in _JSON_FILES_V1:
            comparison_payload, comparison_canonical = _read_json_v1(comparison_dir / filename)
            comparison_ok = comparison_ok and comparison_canonical and (
                payloads[filename] == comparison_payload
            )
        checks.append(comparison_ok)
    failed_checks = sum(not check for check in checks)
    return {
        "verifier_id": "a3_translation_layer_validation_closure_verifier_v1",
        "source_directory": output_dir.name,
        "passed_checks": len(checks) - failed_checks,
        "failed_checks": failed_checks,
        "case_count": len(result.get("case_results", ())),
        "verifier_invoked_runner": False,
        "verifier_invoked_translation_skeleton": False,
        "verifier_invoked_dryrun_runner": False,
        "comparison_run_checked": comparison_dir is not None,
        "comparison_run_equal": comparison_ok if comparison_dir is not None else None,
        "blocker_count": failed_checks,
        "warning_count": int(result.get("warning_count", 0)),
        "final_candidate_decision": (
            "TRANSLATION_VALIDATION_CLOSURE_VERIFICATION_CANDIDATE_PASS"
            if failed_checks == 0
            else "TRANSLATION_VALIDATION_CLOSURE_VERIFICATION_CANDIDATE_BLOCKED"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--comparison-dir")
    args = parser.parse_args()
    comparison_dir = Path(args.comparison_dir) if args.comparison_dir else None
    print(_canonical_json_v1(
        verify_cognitive_translation_validation_closure_v1(
            Path(args.output_dir), comparison_dir
        )
    ))


if __name__ == "__main__":
    main()
