"""Pure fixture-only CWR integration DryRun execution v1."""

from __future__ import annotations

from typing import Tuple

from .integration_fixture_v1 import (
    IntegrationCaseFixtureV1,
    build_integration_fixtures_v1,
    context_reference_v1,
)
from .integration_types_v1 import (
    INTEGRATION_SCHEMA_VERSION_V1,
    CurrentWorldRepresentationIntegrationDryRunResultV1,
)


def _context_isolation_valid(fixture: IntegrationCaseFixtureV1) -> bool:
    refs = tuple(context_reference_v1(context) for context in fixture.contexts)
    snapshots = {context.snapshot_ref for context in fixture.contexts}
    selected_sets = {context.selected_field_unit_refs for context in fixture.contexts}
    if fixture.case_id == "case_03_snapshot_refresh":
        return bool(
            len(fixture.contexts) == 2
            and len(snapshots) == 2
            and fixture.contexts[-1].previous_context_ref == context_reference_v1(fixture.contexts[0])
            and fixture.contexts[-1].context_version != fixture.contexts[0].context_version
        )
    gap_sets = {tuple(gap.gap_id for gap in context.information_gaps) for context in fixture.contexts}
    exclusion_targets = {record.excluded_object_ref for context in fixture.contexts for record in context.exclusion_records}
    return bool(
        len(refs) == len(set(refs))
        and len(snapshots) == 1
        and (len(fixture.contexts) < 2 or len(selected_sets) == len(fixture.contexts))
        and (len(fixture.contexts) < 2 or len(gap_sets) == len(fixture.contexts))
        and (len(fixture.contexts) < 2 or len(exclusion_targets) == len(fixture.contexts))
    )


def _reference_chain_valid(fixture: IntegrationCaseFixtureV1) -> bool:
    event = fixture.admitted_event
    return bool(
        event.get("admission_status") == "admitted_event"
        and event.get("reducer_eligible") is True
        and fixture.reducer_output.runtime_executed is False
        and fixture.reducer_output.state_mutation_executed is False
        and fixture.field_state.produced_by == "field_state_reducer"
        and fixture.state_versions[0].field_state_ref == fixture.field_state.state_id
        and fixture.transitions[0].target_state_version == fixture.state_versions[0].state_version_id
        and fixture.read_model_result.runtime_executed is False
        and fixture.envelope.snapshot_ref == fixture.snapshot.snapshot_id
    )


def _version_chain_valid(fixture: IntegrationCaseFixtureV1) -> bool:
    context_version_ok = all(context.context_version for context in fixture.contexts)
    active_ok = fixture.active_context_ref in tuple(context_reference_v1(context) for context in fixture.contexts)
    if fixture.case_id == "case_03_snapshot_refresh":
        context_v2 = fixture.contexts[-1]
        return bool(context_v2.previous_context_ref == context_reference_v1(fixture.contexts[0]) and context_v2.context_version == "v2" and context_v2.snapshot_ref == fixture.snapshot.snapshot_id and active_ok)
    return bool(fixture.state_versions and context_version_ok and active_ok)


def _readonly_boundary_valid(fixture: IntegrationCaseFixtureV1) -> bool:
    return bool(
        fixture.field_state.state_mutation_executed is False
        and fixture.snapshot.state_store_write_executed is False
        and fixture.history_projection.state_mutation_executed is False
        and fixture.envelope.read_only is True
        and fixture.envelope.state_mutation_executed is False
        and all(context.field_state_mutation_executed is False for context in fixture.contexts)
        and fixture.read_model_result.boundary_flags.get("read_only", False) is True
    )


def _unknown_preservation_valid(fixture: IntegrationCaseFixtureV1) -> bool:
    if fixture.case_id != "case_02_unknown_time":
        return True
    return bool(
        fixture.state_versions[0].valid_from is None
        and fixture.state_versions[0].temporal_uncertainty.get("valid_from_status") == "unknown"
        and fixture.transitions[0].transition_time is None
        and fixture.transitions[0].transition_time_status == "unknown"
        and fixture.envelope.representation_status == "incomplete"
    )


def _mutation_authority_valid(fixture: IntegrationCaseFixtureV1) -> bool:
    return bool(
        fixture.reducer_output.mutation_allowed_only_by_reducer is True
        and fixture.reducer_output.state_mutation_executed is False
        and fixture.field_state.produced_by == "field_state_reducer"
    )


def _result_from_fixture(fixture: IntegrationCaseFixtureV1) -> CurrentWorldRepresentationIntegrationDryRunResultV1:
    input_refs = (fixture.admitted_event["event_ref"], fixture.field_identity.field_id, fixture.snapshot.snapshot_id)
    return CurrentWorldRepresentationIntegrationDryRunResultV1(
        schema_version=INTEGRATION_SCHEMA_VERSION_V1,
        dryrun_id="dryrun:current_world_representation_integration:v1",
        case_id=fixture.case_id,
        case_name=fixture.case_name,
        execution_scope="fixed_fixture_contract_integration_only",
        runtime_executed=False,
        simulation_only=True,
        input_refs=input_refs,
        admitted_event_ref=str(fixture.admitted_event["event_ref"]),
        reducer_output_ref=f"reducer_output:{fixture.case_id}",
        field_state_ref=fixture.field_state.state_id,
        state_version_refs=tuple(version.state_version_id for version in fixture.state_versions),
        transition_record_refs=tuple(record.transition_id for record in fixture.transitions),
        history_projection_ref=f"history:{fixture.case_id}",
        snapshot_ref=fixture.snapshot.snapshot_id,
        read_model_result_ref=fixture.read_model_result.query_id,
        context_refs=tuple(context_reference_v1(context) for context in fixture.contexts),
        active_context_ref=fixture.active_context_ref,
        envelope_ref=fixture.envelope.representation_id,
        reference_chain_valid=_reference_chain_valid(fixture),
        version_chain_valid=_version_chain_valid(fixture),
        mutation_authority_valid=_mutation_authority_valid(fixture),
        readonly_boundary_valid=_readonly_boundary_valid(fixture),
        unknown_preservation_valid=_unknown_preservation_valid(fixture),
        context_isolation_valid=_context_isolation_valid(fixture),
        cognitive_writeback_absent=True,
        analysis_boundary_admission=fixture.expected_analysis_boundary_admission,
        failure_codes=fixture.expected_failure_codes,
        warning_codes=fixture.expected_warning_codes,
        provenance={"fixture_only": True, "case_id": fixture.case_id},
        trace=f"trace:{fixture.case_id}",
    )


def run_controlled_integration_dryrun_v1() -> Tuple[CurrentWorldRepresentationIntegrationDryRunResultV1, ...]:
    """Run six fixed in-memory fixtures without external effects or runtimes."""

    return tuple(_result_from_fixture(fixture) for fixture in build_integration_fixtures_v1())
