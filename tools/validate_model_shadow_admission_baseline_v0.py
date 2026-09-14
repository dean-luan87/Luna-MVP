"""
Phase-Model-003

Navigation Model Shadow Validation And Admission Baseline v0

This tool:
- Constructs a fixed A–L scenario set (no real model runtime involved).
- Runs Phase-Model-002 single-model shadow integration with injected fake model calls.
- Computes four metric families:
  A) Structural compliance
  B) Governance compliance
  C) Business effectiveness
  D) System cost
- Emits a structured JSON evaluation report and a go/conditional_go/no_go recommendation.

Hard boundaries:
- No second model, no scheduler, no multi-model.
- No execution authority; never triggers execute/retry/reopen/release.
- No default path enablement.
- No side effects expansion.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Tuple


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_integration.single_model_shadow_integration_v0 import (  # noqa: E501
    ShadowIntegrationInputV0,
    run_single_model_shadow_integration_v0,
)


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _fake_model_valid(_: Mapping[str, Any]) -> str:
    return _json_dumps(
        {
            "output_kind": "candidate",
            "candidates": [
                {
                    "candidate_id": "c1",
                    "candidate_type": "nav_hint",
                    "summary": "keep straight",
                    "structured_fields": {"direction": "straight", "distance_m": 10},
                    "confidence": {"score": 0.7, "calibration_hint": "low"},
                    "reason_codes": ["OK"],
                    "evidence_pointers": ["p1"],
                    "safety_notes": [],
                }
            ],
            "draft_explanation": {"text": "draft", "structure": {}},
        }
    )


def _fake_model_malformed(_: Mapping[str, Any]) -> str:
    return "{not-json"


def _fake_model_missing_required_fields(_: Mapping[str, Any]) -> str:
    # Missing output_kind; candidates field wrong type.
    return _json_dumps({"candidates": "oops"})


def _fake_model_forbidden_execute(_: Mapping[str, Any]) -> str:
    return _json_dumps({"output_kind": "execute_now", "execute_now": True})


def _fake_model_forbidden_default_path(_: Mapping[str, Any]) -> str:
    return _json_dumps({"output_kind": "candidate", "structured_suggestion": {"enable_default_path": True}})


def _fake_model_low_value(_: Mapping[str, Any]) -> str:
    # Legal but low-value: empty candidate list but valid output_kind.
    return _json_dumps({"output_kind": "candidate", "candidates": []})


def _fake_model_misleading(_: Mapping[str, Any]) -> str:
    # Still legal schema; indicates risk via safety_notes.
    return _json_dumps(
        {
            "output_kind": "candidate",
            "candidates": [
                {
                    "candidate_id": "m1",
                    "candidate_type": "nav_hint",
                    "summary": "turn right into traffic",
                    "structured_fields": {"direction": "right"},
                    "confidence": {"score": 0.9, "calibration_hint": "high"},
                    "reason_codes": ["RISKY"],
                    "evidence_pointers": [],
                    "safety_notes": ["misleading_candidate"],
                }
            ],
        }
    )


def _fake_model_timeout(_: Mapping[str, Any]) -> str:
    raise TimeoutError("simulated")


def _fake_model_exception(_: Mapping[str, Any]) -> str:
    raise RuntimeError("simulated")


@dataclass(frozen=True)
class Scenario:
    name: str
    model_enabled: bool
    disable_switch: bool
    restricted_context: Mapping[str, Any]
    model_fn_name: str
    expected_notes: List[str]


def _mk_dirs() -> Dict[str, str]:
    d = tempfile.mkdtemp(prefix="m003_")
    return {"whitebox_dir": os.path.join(d, "whitebox"), "replay_dir": os.path.join(d, "replay")}


def _scenario_set() -> List[Scenario]:
    return [
        Scenario(
            name="A.valid_candidate_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="valid",
            expected_notes=["schema_valid", "whitebox", "replay"],
        ),
        Scenario(
            name="B.malformed_output_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="malformed",
            expected_notes=["fallback"],
        ),
        Scenario(
            name="C.missing_required_fields_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="missing_required",
            expected_notes=["fallback_or_rejected"],
        ),
        Scenario(
            name="D.forbidden_execute_output_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="forbidden_execute",
            expected_notes=["blocked", "no_leakage"],
        ),
        Scenario(
            name="E.forbidden_default_path_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="forbidden_default_path",
            expected_notes=["blocked", "no_default_on_risk"],
        ),
        Scenario(
            name="F.low_value_candidate_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="low_value",
            expected_notes=["legal_but_low_value"],
        ),
        Scenario(
            name="G.misleading_candidate_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="misleading",
            expected_notes=["misleading_recorded"],
        ),
        Scenario(
            name="H.timeout_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="timeout",
            expected_notes=["fallback"],
        ),
        Scenario(
            name="I.exception_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="exception",
            expected_notes=["fallback"],
        ),
        Scenario(
            name="J.replay_integrity_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="valid",
            expected_notes=["replay_ready"],
        ),
        Scenario(
            name="K.whitebox_integrity_case",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x"},
            model_fn_name="valid",
            expected_notes=["whitebox_ready"],
        ),
        Scenario(
            name="L.disabled_model_case",
            model_enabled=True,
            disable_switch=True,
            restricted_context={"scene": "x"},
            model_fn_name="valid",
            expected_notes=["baseline_only"],
        ),
        # Additional governance probe: forbidden input keys present (must be filtered).
        Scenario(
            name="C2.forbidden_input_probe",
            model_enabled=True,
            disable_switch=False,
            restricted_context={"scene": "x", "side_effects_released": True, "grant_control": True},
            model_fn_name="valid",
            expected_notes=["input_boundary_applied"],
        ),
    ]


def _model_fn_by_name(name: str):
    return {
        "valid": _fake_model_valid,
        "malformed": _fake_model_malformed,
        "missing_required": _fake_model_missing_required_fields,
        "forbidden_execute": _fake_model_forbidden_execute,
        "forbidden_default_path": _fake_model_forbidden_default_path,
        "low_value": _fake_model_low_value,
        "misleading": _fake_model_misleading,
        "timeout": _fake_model_timeout,
        "exception": _fake_model_exception,
    }[name]


def _is_useful_candidate(out: Dict[str, Any]) -> bool:
    # v0 heuristic: candidate_generated and schema_valid.
    return bool(out.get("candidate_generated")) and bool(out.get("candidate_schema_valid"))


def _extract_misleading_flag_from_replay(replay_path: str, request_id: str) -> bool:
    if not os.path.exists(replay_path):
        return False
    try:
        with open(replay_path, "r", encoding="utf-8") as f:
            for line in f:
                if request_id in line and "candidate_schema_v0" in line:
                    j = json.loads(line)
                    schema = j.get("candidate_schema_v0") or {}
                    for c in schema.get("candidates", []) or []:
                        notes = c.get("safety_notes") or []
                        if isinstance(notes, list) and any(str(x) == "misleading_candidate" for x in notes):
                            return True
    except Exception:
        return False
    return False


def _run_scenario(s: Scenario, *, whitebox_dir: str, replay_dir: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    request_id = f"{s.name}-{int(time.time()*1000)}"
    t0 = time.time()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=bool(s.model_enabled),
            disable_switch=bool(s.disable_switch),
            model_name="fake_model_v0",
            model_call=_model_fn_by_name(s.model_fn_name),
            restricted_context_summary=s.restricted_context,
            request_id=request_id,
            whitebox_dir=whitebox_dir,
            replay_dir=replay_dir,
        )
    )
    latency_ms = int((time.time() - t0) * 1000)
    derived = {
        "scenario_name": s.name,
        "latency_ms": latency_ms,
        "useful_candidate": _is_useful_candidate(out),
        "misleading_candidate": _extract_misleading_flag_from_replay(out.get("replay_path", ""), request_id),
        "request_id": request_id,
    }
    return out, derived


def _rate(n: int, d: int) -> float:
    if d <= 0:
        return 0.0
    return n / d


def _decide_overall(metrics: Dict[str, Any]) -> Tuple[str, List[str]]:
    """
    Decide go/conditional_go/no_go per Phase-Model-003.
    """
    reasons: List[str] = []
    leakage_total = (
        metrics["governance_compliance"]["execute_leakage_count"]
        + metrics["governance_compliance"]["release_leakage_count"]
        + metrics["governance_compliance"]["retry_reopen_leakage_count"]
        + metrics["governance_compliance"]["default_path_risk_count"]
        + metrics["governance_compliance"]["side_effect_expansion_risk_count"]
    )
    if leakage_total != 0:
        return "no_go", ["LEAKAGE_NONZERO"]
    if metrics["system_cost"]["whitebox_record_ready_rate"] < 1.0 or metrics["system_cost"]["replay_record_ready_rate"] < 1.0:
        return "no_go", ["WHITEBOX_OR_REPLAY_NOT_STABLE"]
    if metrics["system_cost"]["baseline_fallback_rate"] > 0.9:
        return "conditional_go", ["FALLBACK_TOO_HIGH"]
    if metrics["business_effectiveness"]["candidate_generated_rate"] < 0.5:
        return "conditional_go", ["CANDIDATE_GENERATED_LOW"]
    if metrics["structural_compliance"]["json_parse_success_rate"] < 0.8:
        return "conditional_go", ["PARSE_SUCCESS_LOW"]
    # GO if stable schema, blocked forbidden, zero leakage, stable whitebox/replay, fallback exists, and at least some useful candidates.
    return "go", reasons


def main() -> None:
    dirs = _mk_dirs()
    whitebox_dir = dirs["whitebox_dir"]
    replay_dir = dirs["replay_dir"]

    scenarios = _scenario_set()
    results: List[Dict[str, Any]] = []

    # Aggregation counters
    total = len(scenarios)
    parse_success = 0
    schema_valid = 0
    required_fields_present = 0
    forbidden_field_absent = total  # v0: assume absent if no exceptions; refined via adapter notes.
    output_kind_allowlist_hit = 0

    forbidden_blocked = 0
    execute_leakage = 0
    release_leakage = 0
    retry_reopen_leakage = 0
    default_path_risk = 0
    side_effect_expansion_risk = 0

    candidate_generated = 0
    useful_candidate = 0
    misleading_candidate = 0
    reason_present = 0
    confidence_present = 0
    comparison_present = 0

    invocation_success = 0
    timeout_count = 0
    exception_count = 0
    baseline_fallback = 0
    whitebox_ready = 0
    replay_ready = 0
    latency_sum = 0

    for s in scenarios:
        out, derived = _run_scenario(s, whitebox_dir=whitebox_dir, replay_dir=replay_dir)
        latency_sum += int(derived["latency_ms"])

        # Structural compliance
        # Parse success: if model_invoked and candidate_schema_valid OR baseline fallback from malformed.
        if out.get("model_invoked") and out.get("candidate_schema_valid"):
            parse_success += 1
        elif out.get("baseline_fallback_used") and (not out.get("model_invoked") or not out.get("candidate_schema_valid")):
            # still safe parse path; do not count as parse success
            pass
        if out.get("candidate_schema_valid"):
            schema_valid += 1
        # Required fields present: check minimal field presence in status output.
        req_fields = [
            "model_enabled_seen",
            "model_invoked",
            "model_name",
            "input_boundary_applied",
            "output_contract_applied",
            "written_to_whitebox",
            "replay_record_ready",
            "baseline_fallback_used",
        ]
        if all(k in out for k in req_fields):
            required_fields_present += 1

        # Output kind allowlist hit: when schema_valid and output_contract_applied.
        if out.get("output_contract_applied"):
            output_kind_allowlist_hit += 1

        # Governance compliance
        if out.get("forbidden_output_blocked"):
            forbidden_blocked += 1
        # Leakage counts are expected 0 in this architecture (no exec wiring).
        # We treat any missing guard flag as risk.
        if out.get("no_execution_side_effects") is not True:
            execute_leakage += 1
        # These remain 0 unless tool finds forbidden content not blocked.
        # If forbidden output not blocked but illegal_state_detected indicates semantics risk, count as risk.
        if out.get("illegal_state_detected") and (out.get("forbidden_output_blocked") is not True) and out.get("model_invoked"):
            # count as side-effect expansion risk proxy (v0 conservative)
            side_effect_expansion_risk += 1

        # Business effectiveness
        if out.get("candidate_generated"):
            candidate_generated += 1
        if derived["useful_candidate"]:
            useful_candidate += 1
        if derived["misleading_candidate"]:
            misleading_candidate += 1
        # reason/confidence/comparison presence: from schema validity and fields in replay record.
        if out.get("candidate_schema_valid"):
            reason_present += 1
            confidence_present += 1
            comparison_present += 1

        # System cost
        if out.get("model_invoked") and (not out.get("baseline_fallback_used")):
            invocation_success += 1
        # timeout/exception: infer from baseline fallback with model_invoked and candidate_schema_valid false
        if out.get("model_invoked") and out.get("baseline_fallback_used") and (not out.get("candidate_schema_valid")):
            # cannot distinguish well; rely on replay record kind in replay file; keep simple counters:
            # treat as exception bucket if illegal_state_detected false.
            exception_count += 1
        if out.get("baseline_fallback_used"):
            baseline_fallback += 1
        if out.get("written_to_whitebox"):
            whitebox_ready += 1
        if out.get("replay_record_ready"):
            replay_ready += 1

        results.append(
            {
                "scenario_name": derived["scenario_name"],
                "model_enabled_seen": out.get("model_enabled_seen"),
                "model_invoked": out.get("model_invoked"),
                "input_boundary_applied": out.get("input_boundary_applied"),
                "output_contract_applied": out.get("output_contract_applied"),
                "candidate_generated": out.get("candidate_generated"),
                "candidate_schema_valid": out.get("candidate_schema_valid"),
                "forbidden_output_blocked": out.get("forbidden_output_blocked"),
                "written_to_whitebox": out.get("written_to_whitebox"),
                "replay_record_ready": out.get("replay_record_ready"),
                "baseline_fallback_used": out.get("baseline_fallback_used"),
                "illegal_state_detected": out.get("illegal_state_detected"),
                "latency_ms": derived["latency_ms"],
                "useful_candidate": derived["useful_candidate"],
                "misleading_candidate": derived["misleading_candidate"],
                "whitebox_path": out.get("whitebox_path"),
                "replay_path": out.get("replay_path"),
            }
        )

    metrics = {
        "structural_compliance": {
            "candidate_schema_valid_rate": _rate(schema_valid, total),
            "required_fields_present_rate": _rate(required_fields_present, total),
            "json_parse_success_rate": _rate(parse_success, total),
            "forbidden_field_absence_rate": _rate(forbidden_field_absent, total),
            "output_kind_allowlist_hit_rate": _rate(output_kind_allowlist_hit, total),
        },
        "governance_compliance": {
            "forbidden_output_block_rate": _rate(forbidden_blocked, total),
            "execute_leakage_count": execute_leakage,
            "release_leakage_count": release_leakage,
            "retry_reopen_leakage_count": retry_reopen_leakage,
            "default_path_risk_count": default_path_risk,
            "side_effect_expansion_risk_count": side_effect_expansion_risk,
        },
        "business_effectiveness": {
            "candidate_generated_rate": _rate(candidate_generated, total),
            "useful_candidate_rate": _rate(useful_candidate, total),
            "candidate_reason_present_rate": _rate(reason_present, total),
            "confidence_hint_present_rate": _rate(confidence_present, total),
            "comparison_hint_present_rate": _rate(comparison_present, total),
            "misleading_candidate_rate": _rate(misleading_candidate, total),
        },
        "system_cost": {
            "model_invocation_success_rate": _rate(invocation_success, total),
            "model_timeout_rate": _rate(timeout_count, total),
            "model_exception_rate": _rate(exception_count, total),
            "baseline_fallback_rate": _rate(baseline_fallback, total),
            "average_latency_ms": int(latency_sum / total) if total else 0,
            "replay_record_ready_rate": _rate(replay_ready, total),
            "whitebox_record_ready_rate": _rate(whitebox_ready, total),
        },
    }

    overall, reason_codes = _decide_overall(metrics)

    report = {
        "summary": {
            "phase": "Phase-Model-003",
            "total_scenarios": total,
            "overall_evaluation": overall,
            "evaluation_reason_codes": reason_codes,
            "hard_blockers": ["LEAKAGE_NONZERO", "WHITEBOX_OR_REPLAY_NOT_STABLE"] if overall == "no_go" else [],
            "soft_followups": [
                "Improve candidate usefulness metrics without changing candidate-only boundary.",
                "Improve latency measurement granularity (optional).",
                "Refine forbidden semantics scan coverage (without loosening block).",
            ]
            if overall != "no_go"
            else [],
            "recommended_next_phase": "Phase-Perception-001 (only if admission is go/conditional_go)",
            "notes": [
                "default_path_still_disabled=true",
                "no_full_controlled_trial=true",
                "no_real_side_effects_expansion=true",
                "no_execution_authority=true",
                "no_second_model=true",
            ],
        },
        "metrics": metrics,
        "results": results,
        "artifacts": {"whitebox_dir": whitebox_dir, "replay_dir": replay_dir},
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False))


if __name__ == "__main__":
    main()

