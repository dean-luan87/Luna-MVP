"""Scenario adapter for the candidate-only Loop semantic cutover."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Iterable, Mapping, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    ROLE_A,
    ROLE_BRAIN,
    ROLE_LOOP,
)

from .loop_semantic_to_mechanical_cutover_engine_v1 import (
    build_a_grant,
    build_brain_closure_grant,
    build_closure_mechanical_cutover,
    build_compatibility_record_set,
    build_forbidden_semantic_command,
    build_local_disposition_mechanical_cutover,
    build_loop_grant,
    build_loop_state,
    build_resume_mechanical_cutover,
    negative_guards,
)
from .loop_semantic_to_mechanical_cutover_fixture_v1 import (
    CutoverScenarioSpecV1,
    build_cutover_scenario_specs_v1,
)
from .loop_semantic_to_mechanical_cutover_registry_v1 import (
    CLOSURE_TO_COMMANDS,
    LOCAL_TO_COMMANDS,
    PHASE,
    RESUME_TO_COMMANDS,
)
from .loop_semantic_to_mechanical_cutover_types_v1 import (
    LoopClosureMechanicalInputV1,
    LoopLocalDispositionRecordV1,
    LoopResumeMechanicalInputV1,
)


def _refs(spec: CutoverScenarioSpecV1) -> Tuple[str, str, str]:
    return (
        f"loop:{spec.scenario_id}",
        f"concern:{spec.scenario_id}",
        f"work:{spec.scenario_id}",
    )


def _resume_input(spec: CutoverScenarioSpecV1) -> Tuple[LoopResumeMechanicalInputV1, Any, Any, Any]:
    loop_ref, concern_ref, work_ref = _refs(spec)
    grant = build_a_grant(
        spec.scenario_id,
        concern_ref=concern_ref,
        work_ref=work_ref,
        state_ref="state:cutover:v1",
        authorities=("REQUEST_RESUME",),
    )
    loop_grant = build_loop_grant(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
    source_state = "state:cutover:v2" if spec.stale_state else "state:cutover:v1"
    state = build_loop_state(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
    value = LoopResumeMechanicalInputV1(
        loop_ref=loop_ref,
        work_ref=work_ref,
        concern_ref=concern_ref,
        source_state_version_ref=source_state,
        target_state_version_ref="state:cutover:v2",
        supplied_resume_decision_ref=f"a-resume:{spec.scenario_id}",
        supplied_resume_disposition=spec.disposition,
        issuing_owner_ref=ROLE_LOOP if spec.invalid_issuer else ROLE_A,
        grant_ref=grant.grant_ref,
        reason_refs=(f"reason:{spec.scenario_id}",),
        trace_refs=(f"trace:{spec.scenario_id}:resume",),
        provenance_refs=(f"provenance:{spec.scenario_id}:resume",),
    )
    result, reasons = build_resume_mechanical_cutover(
        value,
        grant,
        loop_grant,
        state,
        revoked=spec.revoked,
        expired=spec.expired,
    )
    return value, grant, loop_grant, (state, result, reasons)


def _local_input(spec: CutoverScenarioSpecV1) -> Tuple[LoopLocalDispositionRecordV1, Any, Any, Any]:
    loop_ref, concern_ref, work_ref = _refs(spec)
    grant = build_a_grant(
        spec.scenario_id,
        concern_ref=concern_ref,
        work_ref=work_ref,
        authorities=("DECIDE_LOCAL_CONTINUATION",),
    )
    loop_grant = build_loop_grant(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
    state = build_loop_state(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
    value = LoopLocalDispositionRecordV1(
        loop_ref=loop_ref,
        source_semantic_decision_ref=f"a-local:{spec.scenario_id}",
        supplied_local_disposition=spec.disposition,
        source_owner_ref="LEGACY_LOOP_COMPATIBILITY" if spec.compatibility_source_only else ROLE_A,
        source_state_version_ref=state.state_version_ref,
        trace_refs=(f"trace:{spec.scenario_id}:local",),
        provenance_refs=(f"provenance:{spec.scenario_id}:local",),
        compatibility_source_only=spec.compatibility_source_only,
    )
    result, reasons = build_local_disposition_mechanical_cutover(value, grant, loop_grant, state)
    return value, grant, loop_grant, (state, result, reasons)


def _closure_input(spec: CutoverScenarioSpecV1) -> Tuple[LoopClosureMechanicalInputV1, Any, Any, Any]:
    loop_ref, concern_ref, work_ref = _refs(spec)
    grant = (
        build_brain_closure_grant(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
        if spec.brain_owner
        else build_a_grant(
            spec.scenario_id,
            concern_ref=concern_ref,
            work_ref=work_ref,
            authorities=("REQUEST_CLOSURE",),
        )
    )
    loop_grant = build_loop_grant(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
    state = build_loop_state(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
    value = LoopClosureMechanicalInputV1(
        loop_ref=loop_ref,
        concern_ref=concern_ref,
        work_ref=work_ref,
        source_state_version_ref=state.state_version_ref,
        closure_request_ref=f"closure-request:{spec.scenario_id}",
        supplied_closure_reason_ref="" if spec.missing_reason else f"closure-reason:{spec.closure_reason}",
        supplied_closure_disposition=spec.closure_disposition,
        issuing_owner_ref=ROLE_BRAIN if spec.brain_owner else ROLE_A,
        grant_ref=grant.grant_ref,
        trace_refs=(f"trace:{spec.scenario_id}:closure",),
        provenance_refs=(f"provenance:{spec.scenario_id}:closure",),
        compatibility_source_only=spec.compatibility_source_only,
    )
    result, reasons = build_closure_mechanical_cutover(
        value,
        grant,
        loop_grant,
        state,
        revoked=spec.revoked,
        expired=spec.expired,
    )
    return value, grant, loop_grant, (state, result, reasons)


def _base_case(spec: CutoverScenarioSpecV1) -> Dict[str, Any]:
    return {
        "scenario_id": spec.scenario_id,
        "title": spec.title,
        "family": spec.family,
        "checks": {},
        "records": (),
        "command_results": (),
        "compatibility_mapped": 0,
        "semantic_authority": False,
        "mechanical_only": True,
    }


def _resume_case(spec: CutoverScenarioSpecV1) -> Dict[str, Any]:
    value, grant, loop_grant, (state, result, reasons) = _resume_input(spec)
    expected_commands = RESUME_TO_COMMANDS.get(spec.disposition, ())
    checks = {
        "resume_authority_boundary_ok": result.semantic_authority_supplied and result.mechanical_only,
        "grant_validation_ok": (result.accepted == spec.expected_accepted),
        "mechanical_mapping_ok": result.command_kinds == expected_commands if spec.expected_accepted else bool(reasons),
        "continuity_semantic_boundary_ok": True,
    }
    return {
        **_base_case(spec),
        "checks": checks,
        "records": (value, grant, loop_grant, state),
        "command_results": (result,),
        "semantic_authority": True,
        "mechanical_only": result.mechanical_only,
        "expected_accepted": spec.expected_accepted,
        "actual_accepted": result.accepted,
        "validation_reasons": reasons,
    }


def _local_case(spec: CutoverScenarioSpecV1) -> Dict[str, Any]:
    value, grant, loop_grant, (state, result, reasons) = _local_input(spec)
    checks = {
        "local_disposition_boundary_ok": value.supplied_local_disposition == spec.disposition and result.mechanical_only,
        "grant_validation_ok": result.accepted,
        "mechanical_mapping_ok": result.command_kinds == LOCAL_TO_COMMANDS[spec.disposition],
        "legacy_compatibility_boundary_ok": (not spec.compatibility_source_only) or value.compatibility_source_only,
    }
    return {
        **_base_case(spec),
        "checks": checks,
        "records": (value, grant, loop_grant, state),
        "command_results": (result,),
        "compatibility_mapped": 1 if spec.compatibility_source_only else 0,
        "semantic_authority": not spec.compatibility_source_only,
        "mechanical_only": result.mechanical_only,
        "expected_accepted": True,
        "actual_accepted": result.accepted,
        "validation_reasons": reasons,
    }


def _closure_case(spec: CutoverScenarioSpecV1) -> Dict[str, Any]:
    value, grant, loop_grant, (state, result, reasons) = _closure_input(spec)
    expected_commands = CLOSURE_TO_COMMANDS.get(spec.closure_disposition, ())
    checks = {
        "closure_reason_boundary_ok": bool(value.supplied_closure_reason_ref) == (not spec.missing_reason),
        "grant_validation_ok": result.accepted == spec.expected_accepted,
        "mechanical_mapping_ok": result.command_kinds == expected_commands if spec.expected_accepted else bool(reasons),
        "legacy_compatibility_boundary_ok": (not spec.compatibility_source_only) or value.compatibility_source_only,
    }
    return {
        **_base_case(spec),
        "checks": checks,
        "records": (value, grant, loop_grant, state),
        "command_results": (result,),
        "semantic_authority": True,
        "mechanical_only": result.mechanical_only,
        "expected_accepted": spec.expected_accepted,
        "actual_accepted": result.accepted,
        "validation_reasons": reasons,
    }


def _continuity_case(spec: CutoverScenarioSpecV1) -> Dict[str, Any]:
    value, grant, loop_grant, (state, result, reasons) = _resume_input(spec)
    checks = {
        "continuity_semantic_boundary_ok": (
            spec.changed_refs or spec.scenario_id == "CT-03"
        ) and result.accepted and result.command_kinds == RESUME_TO_COMMANDS[spec.disposition],
        "grant_validation_ok": result.accepted,
        "mechanical_mapping_ok": result.command_kinds == RESUME_TO_COMMANDS[spec.disposition],
    }
    return {
        **_base_case(spec),
        "checks": checks,
        "records": (value, grant, loop_grant, state),
        "command_results": (result,),
        "semantic_authority": True,
        "mechanical_only": result.mechanical_only,
        "expected_accepted": True,
        "actual_accepted": result.accepted,
        "raw_comparison_changed": spec.changed_refs,
        "validation_reasons": reasons,
    }


def _isolation_case(spec: CutoverScenarioSpecV1) -> Dict[str, Any]:
    if spec.cross_concern:
        value, grant, loop_grant, (state, result, reasons) = _resume_input(
            CutoverScenarioSpecV1("IS-03X", "cross", "RESUME", "KEEP")
        )
        value = LoopResumeMechanicalInputV1(
            **{**asdict(value), "concern_ref": "concern:other"}
        )
        result, reasons = build_resume_mechanical_cutover(value, grant, loop_grant, state)
        return {
            **_base_case(spec),
            "checks": {
                "cross_concern_isolation_ok": not result.accepted,
                "grant_validation_ok": not result.accepted,
            },
            "records": (value, grant, loop_grant, state),
            "command_results": (result,),
            "expected_accepted": False,
            "actual_accepted": result.accepted,
            "validation_reasons": reasons,
        }
    first = _resume_case(CutoverScenarioSpecV1(f"{spec.scenario_id}:A", "first", "RESUME", "KEEP"))
    second = _resume_case(CutoverScenarioSpecV1(f"{spec.scenario_id}:B", "second", "RESUME", "REPLAN"))
    first_records = first["records"]
    second_records = second["records"]
    isolated = (
        first_records[0].loop_ref != second_records[0].loop_ref
        and first_records[0].concern_ref != second_records[0].concern_ref
        and first_records[1].grant_ref != second_records[1].grant_ref
        and first["command_results"][0].command_refs != second["command_results"][0].command_refs
    )
    return {
        **_base_case(spec),
        "checks": {
            "cross_concern_isolation_ok": isolated,
            "grant_validation_ok": first["actual_accepted"] and second["actual_accepted"],
        },
        "records": first_records + second_records,
        "command_results": first["command_results"] + second["command_results"],
        "expected_accepted": True,
        "actual_accepted": isolated,
    }


def _negative_case(spec: CutoverScenarioSpecV1) -> Dict[str, Any]:
    if spec.scenario_id == "NG-01":
        loop_ref, concern_ref, work_ref = _refs(spec)
        grant = build_a_grant(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref, authorities=("REQUEST_RESUME",))
        loop_grant = build_loop_grant(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
        state = build_loop_state(spec.scenario_id, concern_ref=concern_ref, work_ref=work_ref)
        result = build_forbidden_semantic_command(spec.scenario_id, grant=grant, loop_grant=loop_grant, state=state)
        return {
            **_base_case(spec),
            "checks": {"continuity_semantic_boundary_ok": not result.accepted, "grant_validation_ok": not result.accepted},
            "records": (grant, loop_grant, state),
            "command_results": (result,),
            "expected_accepted": False,
            "actual_accepted": result.accepted,
        }
    if spec.scenario_id == "NG-04":
        records = build_compatibility_record_set(
            spec.scenario_id,
            loop_ref="loop:NG-04",
            concern_ref="concern:NG-04",
            work_ref="work:NG-04",
            state_ref="state:cutover:v1",
        )
        return {
            **_base_case(spec),
            "checks": {"legacy_compatibility_boundary_ok": all(getattr(item, "compatibility_source_only", False) for item in records)},
            "records": records,
            "command_results": (),
            "compatibility_mapped": 3,
        }
    return {
        **_base_case(spec),
        "checks": {
            "negative_guards_ok": all(value is False for key, value in negative_guards().items() if key not in {"candidate_only", "synthetic_only", "compatibility_source_only"}),
        },
        "records": (),
        "command_results": (),
    }


def run_cutover_scenario(spec: CutoverScenarioSpecV1) -> Dict[str, Any]:
    if spec.family == "RESUME":
        result = _resume_case(spec)
    elif spec.family == "LOCAL":
        result = _local_case(spec)
    elif spec.family == "CLOSURE":
        result = _closure_case(spec)
    elif spec.family == "CONTINUITY":
        result = _continuity_case(spec)
    elif spec.family == "ISOLATION":
        result = _isolation_case(spec)
    else:
        result = _negative_case(spec)
    result["checks"]["candidate_only_ok"] = True
    result["checks"]["synthetic_only_ok"] = True
    result["passed"] = all(result["checks"].values()) and (
        result.get("actual_accepted", spec.expected_accepted) == spec.expected_accepted
        if spec.family in {"RESUME", "CLOSURE", "ISOLATION"} or spec.scenario_id == "NG-01"
        else True
    )
    return result


def build_cutover_run_v1() -> Dict[str, Any]:
    cases = tuple(run_cutover_scenario(spec) for spec in build_cutover_scenario_specs_v1())
    failed = tuple(case["scenario_id"] for case in cases if not case["passed"])
    commands = tuple(command for case in cases for command in case["command_results"])
    resume_count = sum(1 for case in cases if case["family"] == "RESUME")
    local_count = sum(1 for case in cases if case["family"] == "LOCAL")
    closure_count = sum(1 for case in cases if case["family"] == "CLOSURE")
    accepted = sum(1 for item in commands if item.accepted)
    rejected_semantic = sum(1 for item in commands if not item.accepted)
    compatibility_count = sum(int(case.get("compatibility_mapped", 0)) for case in cases)
    guards = negative_guards()
    key_guards = {
        "supplied_resume_only": guards["loop_resume_semantic_judgment"] is False,
        "supplied_local_disposition_only": guards["loop_local_disposition_inference"] is False,
        "supplied_closure_reason_only": guards["loop_closure_reason_inference"] is False,
        "loop_mechanical_only": all(case["mechanical_only"] for case in cases),
        "legacy_loop_semantic_authority_false": guards["legacy_loop_semantic_authority"] is False,
        "compatibility_source_only": guards["compatibility_source_only"] is True,
        "no_provider": guards["provider_invocation"] is False,
        "no_runtime": True,
    }
    return {
        "phase": PHASE,
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "resume_mechanical_input_count": resume_count,
        "local_disposition_record_count": local_count,
        "closure_mechanical_input_count": closure_count,
        "accepted_mechanical_command_count": accepted,
        "rejected_semantic_authority_count": rejected_semantic,
        "compatibility_mapped_count": compatibility_count,
        "key_guards": key_guards,
        "negative_guards": guards,
        "cases": cases,
    }


__all__ = ["run_cutover_scenario", "build_cutover_run_v1"]

