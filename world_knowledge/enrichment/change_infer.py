import hashlib
from typing import Optional

from world_knowledge.schema import ChangeDemand, ObservationCandidate, ObjectCard
from world_knowledge.profile import EnvironmentProfile


class CandidateInferencer:
    """
    Only ChangeDemand from system can generate observation candidates.
    External knowledge cannot trigger this path directly.
    """

    def infer(
        self, demand: ChangeDemand, card: ObjectCard, profile: EnvironmentProfile
    ) -> Optional[ObservationCandidate]:
        ot = demand.constraints.get("object_type")
        if ot and ot != card.object_type:
            return None

        if demand.demand_type not in card.change_types:
            return None

        key = f"{demand.demand_type}:{card.object_type}:{profile.scene}"
        cid = hashlib.md5(key.encode()).hexdigest()[:10]
        strategy = {
            "observe": "state",
            "freq": "high" if "safety_critical" in card.tags else "normal",
        }
        conf = 0.8 if card.trust_level in ("trusted", "curated") else 0.4

        return ObservationCandidate(
            candidate_id=cid,
            demand=demand,
            object_type=card.object_type,
            strategy_hint=strategy,
            confidence=conf,
            evidence=[{"trust_level": card.trust_level, "scene": profile.scene}],
        )
