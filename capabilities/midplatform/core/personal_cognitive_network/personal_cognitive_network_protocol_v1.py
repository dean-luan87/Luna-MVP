"""Protocol definitions for PCN controlled skeleton operations."""

from __future__ import annotations

from typing import Protocol, Tuple

from .personal_cognitive_activation_types_v1 import (
    ActivationCandidate,
    ActivationRequest,
)
from .personal_cognitive_growth_types_v1 import (
    DormancyCandidate,
    LinkGrowthCandidate,
    ReactivationCandidate,
)
from .personal_cognitive_link_types_v1 import CognitiveLinkCandidate
from .personal_cognitive_projection_types_v1 import ActiveCognitiveProjectionCandidate
from .personal_cognitive_trace_types_v1 import PCNTraceCandidate
from .personal_cognitive_network_types_v1 import SourceObjectReference


class PersonalCognitiveNetworkProtocolV1(Protocol):
    def validate_source_reference(self, source_ref: SourceObjectReference) -> bool: ...

    def validate_link_candidate(self, link: CognitiveLinkCandidate) -> bool: ...

    def prepare_activation_candidate(
        self, request: ActivationRequest
    ) -> ActivationCandidate: ...

    def prepare_projection_candidate(
        self,
        activation: ActivationCandidate,
        links: Tuple[CognitiveLinkCandidate, ...],
    ) -> ActiveCognitiveProjectionCandidate: ...

    def prepare_growth_candidate(
        self, fixture_case_id: str
    ) -> Tuple[LinkGrowthCandidate, ...]: ...

    def prepare_dormancy_candidate(
        self, fixture_case_id: str
    ) -> Tuple[DormancyCandidate, ...]: ...

    def prepare_reactivation_candidate(
        self, fixture_case_id: str
    ) -> Tuple[ReactivationCandidate, ...]: ...

    def create_trace(
        self, request: ActivationRequest, projection_id: str
    ) -> PCNTraceCandidate: ...
