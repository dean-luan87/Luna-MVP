from dataclasses import dataclass
from typing import List

from world_knowledge.schema import ObjectCard, ObservationSignal
from world_knowledge.profile import EnvironmentProfile


@dataclass(frozen=True)
class VerificationResult:
    accepted: bool
    new_trust_level: str
    reasons: List[str]


class VerificationGate:
    """
    The only path from external signals to curated knowledge.
    """

    def verify(
        self,
        signals: List[ObservationSignal],
        draft_card: ObjectCard,
        profile: EnvironmentProfile,
    ) -> VerificationResult:
        providers = {s.provider for s in signals}
        if len(providers) >= 2:
            return VerificationResult(True, "curated", ["multi_provider_agreement"])
        return VerificationResult(False, draft_card.trust_level, ["insufficient_evidence"])
