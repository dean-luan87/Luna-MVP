"""Core controlled PCN skeleton: reference -> candidate -> projection -> trace."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .personal_cognitive_activation_skeleton_v1 import (
    prepare_activation_candidate_from_fixture,
    prepare_activation_projection,
)
from .personal_cognitive_activation_types_v1 import ActivationRequest
from .personal_cognitive_growth_skeleton_v1 import prepare_growth_candidates
from .personal_cognitive_interaction_handoff_skeleton_v1 import (
    prepare_interaction_handoff_candidates,
)
from .personal_cognitive_link_types_v1 import (
    CognitiveLinkCandidate,
    TRUTH_UNVERIFIED_OR_SUBJECTIVE,
)
from .personal_cognitive_network_types_v1 import (
    CognitiveObjectReference,
    PCNContextReference,
    PCNVersion,
    SourceObjectReference,
)
from .personal_cognitive_projection_types_v1 import ActiveCognitiveProjectionCandidate
from .personal_cognitive_trace_types_v1 import PCNTraceCandidate


@dataclass(frozen=True)
class SkeletonRunResult:
    case_id: str
    link_candidates: Tuple[CognitiveLinkCandidate, ...]
    activation_candidate_id: str
    projection: ActiveCognitiveProjectionCandidate
    trace: PCNTraceCandidate
    growth_candidates: Dict[str, Tuple[object, ...]]
    skeleton_only: bool = True
    candidate_only: bool = True
    runtime_executed: bool = False
    source_mutation_executed: bool = False
    persistence_executed: bool = False
    causal_reasoning_executed: bool = False
    intent_generation_executed: bool = False
    decision_executed: bool = False


class PersonalCognitiveNetworkSkeletonV1:
    def __init__(self) -> None:
        self.version = PCNVersion(major=1, minor=0, patch=0)

    def _to_cognitive_refs(
        self, case: Dict[str, object]
    ) -> Tuple[CognitiveObjectReference, ...]:
        refs: List[CognitiveObjectReference] = []
        context_id = str(case.get("context_id", "ctx-unknown"))
        for index, ref_id in enumerate(case.get("source_refs", [])):
            source_ref = SourceObjectReference(
                owner="SOURCE_OWNER_REFERENCE_ONLY",
                object_id=str(ref_id),
                object_type="SOURCE_REFERENCE",
                version="candidate",
                reference_key=str(ref_id),
                provenance_reference=f"fixture:{context_id}",
            )
            refs.append(
                CognitiveObjectReference(
                    reference_id=f"cog-ref-{index}-{ref_id}",
                    source_ref=source_ref,
                    confidence="candidate",
                    uncertainty="preserved",
                )
            )
        return tuple(refs)

    def _build_link_candidates(
        self,
        case: Dict[str, object],
        context_ref: PCNContextReference,
        refs: Tuple[CognitiveObjectReference, ...],
    ) -> Tuple[CognitiveLinkCandidate, ...]:
        if len(refs) < 2:
            return ()
        link = CognitiveLinkCandidate(
            link_id=f"link-{case.get('case_id', 'unknown')}",
            source_refs=(refs[0], refs[1]),
            relation_type="SUBJECTIVE_RELATEDNESS",
            activation_state="ACTIVE",
            strength_state="STRONG" if case.get("subjective") else "MEDIUM",
            formation_source="synthetic_fixture",
            context_refs=(context_ref,),
            temporal_validity="CURRENT_CONTEXT_WINDOW",
            provenance=f"fixture:{case.get('case_id', 'unknown')}",
            confidence="candidate",
            uncertainty="preserved",
            subjective=bool(case.get("subjective", False)),
            truth_status=str(case.get("truth_status", TRUTH_UNVERIFIED_OR_SUBJECTIVE)),
            candidate_only=True,
        )
        return (link,)

    def run_case(self, case: Dict[str, object]) -> SkeletonRunResult:
        context_ref = PCNContextReference(
            context_id=str(case.get("context_id", "ctx-unknown")),
            context_version="candidate-v1",
            context_trace_ref=f"trace-{case.get('case_id', 'unknown')}",
        )
        refs = self._to_cognitive_refs(case)
        request = ActivationRequest(
            request_id=f"req-{case.get('case_id', 'unknown')}",
            context_ref=context_ref,
            source_refs=refs,
            resource_budget_label=str(case.get("resource_label", "LOW")),
            unknown_preserved=True,
        )
        links = self._build_link_candidates(case, context_ref, refs)
        interactions = prepare_interaction_handoff_candidates(case)
        activation = prepare_activation_candidate_from_fixture(request, refs)
        activation_projection = prepare_activation_projection(
            activation=activation,
            active_link_ids=tuple(link.link_id for link in links),
            unresolved_links=(),
            resource_constraint_ref=f"resource-{case.get('resource_label', 'LOW')}",
        )
        projection = ActiveCognitiveProjectionCandidate(
            projection_id=activation_projection.projection_id,
            active_reference_set=activation_projection.active_ref_ids,
            active_link_set=activation_projection.active_link_ids,
            related_context_refs=(context_ref.context_id,),
            unresolved_links=activation_projection.unresolved_links,
            interaction_refs=tuple(i.interaction_reference for i in interactions),
            activation_trace_ref=context_ref.context_trace_ref,
            confidence="candidate",
            uncertainty="preserved",
            resource_constraint_ref=activation_projection.resource_constraint_ref
            or "resource-unknown",
            provenance=f"fixture:{case.get('case_id', 'unknown')}",
            candidate_only=True,
            decision_output=False,
            causal_output=False,
            intent_output=False,
        )
        growth = prepare_growth_candidates(case)
        trace = PCNTraceCandidate(
            trace_id=context_ref.context_trace_ref,
            context_ref=context_ref.context_id,
            activation_request_ref=request.request_id,
            source_refs=tuple(ref.reference_id for ref in refs),
            link_refs=tuple(link.link_id for link in links),
            interaction_refs=tuple(i.interaction_reference for i in interactions),
            resource_refs=(projection.resource_constraint_ref,),
            assembly_steps=(
                "reference_intake",
                "candidate_link_build",
                "activation_candidate_build",
                "projection_candidate_build",
                "trace_assembly",
            ),
            projection_ref=projection.projection_id,
            unknowns=("unknown_preserved",),
            status="CANDIDATE",
            candidate_only=True,
        )
        return SkeletonRunResult(
            case_id=str(case.get("case_id", "unknown")),
            link_candidates=links,
            activation_candidate_id=activation.candidate_id,
            projection=projection,
            trace=trace,
            growth_candidates=growth,
            skeleton_only=True,
            candidate_only=True,
            runtime_executed=False,
            source_mutation_executed=False,
            persistence_executed=False,
            causal_reasoning_executed=False,
            intent_generation_executed=False,
            decision_executed=False,
        )
