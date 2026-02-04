# -*- coding: utf-8 -*-
import time
import uuid
from .types import PendingBelief, Belief, EnvTag
from .gates import env_allows_learning, bucket_complexity
from .config import C3Config
from .store import C3Store


class C3Learner:
    def __init__(self, cfg: C3Config, store: C3Store):
        self.cfg = cfg
        self.store = store

    def observe(self, *, env_mode, pattern: str, tendency: str, positive: bool = True) -> None:
        if not self.cfg.enabled:
            return
        if not env_allows_learning(env_mode, self.cfg):
            return

        env_tag = EnvTag(
            safety=env_mode.safety_level,
            control=env_mode.control_mode,
            complexity_bucket=bucket_complexity(env_mode.complexity_score),
        )

        belief_id = self._make_id(pattern, tendency, env_tag)
        belief = self.store.beliefs.get(belief_id)
        pb = self.store.pending.get(belief_id)
        now = time.time()

        if belief is not None:
            if positive:
                belief.evidence_count += 1
                belief.last_triggered_ts = now
            else:
                belief.counter_evidence = min(belief.counter_evidence + 1, belief.evidence_count)
            belief.confidence = self._confidence_counts(belief.evidence_count, belief.counter_evidence)
            belief.last_updated_ts = now
            self.store.beliefs[belief_id] = belief
            return

        if pb is None:
            pb = PendingBelief(
                belief_id=belief_id,
                pattern=pattern,
                tendency=tendency,
                env_tag=env_tag,
            )

        if positive:
            pb.evidence_count += 1
            pb.last_triggered_ts = now
        else:
            pb.counter_evidence = min(pb.counter_evidence + 1, pb.evidence_count)

        pb.last_updated_ts = now
        self.store.upsert_pending(pb)

        # 评估是否晋升
        if pb.evidence_count >= self.cfg.min_evidence:
            conf = self._confidence(pb)
            if conf >= self.cfg.min_confidence:
                belief = Belief(
                    belief_id=pb.belief_id,
                    pattern=pb.pattern,
                    tendency=pb.tendency,
                    env_tag=pb.env_tag,
                    evidence_count=pb.evidence_count,
                    counter_evidence=pb.counter_evidence,
                    confidence=conf,
                    last_updated_ts=now,
                    last_triggered_ts=now,
                )
                self.store.promote(belief)

    def _confidence(self, pb: PendingBelief) -> float:
        return self._confidence_counts(pb.evidence_count, pb.counter_evidence)

    def _confidence_counts(self, evidence_count: int, counter_evidence: int) -> float:
        total = evidence_count + counter_evidence
        if total == 0:
            return 0.0
        return evidence_count / total

    def _make_id(self, pattern: str, tendency: str, env_tag: EnvTag) -> str:
        key = f"{pattern}|{tendency}|{env_tag.safety}|{env_tag.control}|{env_tag.complexity_bucket}"
        return uuid.uuid5(uuid.NAMESPACE_OID, key).hex
