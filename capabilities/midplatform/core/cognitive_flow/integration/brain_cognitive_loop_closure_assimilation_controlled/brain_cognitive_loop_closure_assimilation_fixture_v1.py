"""Two controlled replay inputs for Brain closure integration."""

from __future__ import annotations

from capabilities.midplatform.core.a_route_orchestration.controlled_replay_runtime_fixture_v1 import (
    build_minimum_sufficient_loop_replay_input_v1,
)


def build_case_a_replay_v1():
    return (
        build_minimum_sufficient_loop_replay_input_v1(
            case_id="brain-case-a-sufficient-stop",
            cycle_index=1,
            evidence_refs=("evidence:brain:case-a:target-identity",),
            available_information_refs=("information:target-identity", "information:target-location"),
        ),
    )


def build_case_b_cycle_1_replay_v1():
    return build_minimum_sufficient_loop_replay_input_v1(
        case_id="brain-case-b-gap-reobserve-revise-stop",
        cycle_index=1,
        evidence_refs=("evidence:brain:case-b:target-identity",),
        available_information_refs=("information:target-identity",),
    )


def build_case_b_cycle_2_replay_v1(proof):
    if proof is None:
        raise ValueError("case_b_cycle_2_requires_cycle_1_cognitive_proof")
    return build_minimum_sufficient_loop_replay_input_v1(
        case_id="brain-case-b-gap-reobserve-revise-stop",
        cycle_index=2,
        evidence_refs=("evidence:brain:case-b:target-location",),
        available_information_refs=("information:target-identity", "information:target-location"),
        prior_current_world_ref=proof.current_world_ref,
        prior_hypothesis_refs=proof.hypothesis_refs,
        prior_information_gap_ref=proof.information_gap_ref,
        prior_reobservation_ref=proof.reobservation_ref,
        prior_next_cycle_ingress_ref=proof.next_cycle_ingress_ref,
        prior_sufficiency_candidate=proof.sufficiency_candidate,
        prior_information_gap_candidate=proof.information_gap_candidate,
        prior_reobservation_candidate=proof.reobservation_candidate,
    )
