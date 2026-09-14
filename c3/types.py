# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
import time
import uuid


@dataclass
class EnvTag:
    safety: str
    control: str
    complexity_bucket: str  # LOW / MID / HIGH


@dataclass
class PendingBelief:
    belief_id: str
    pattern: str
    tendency: str
    env_tag: EnvTag
    evidence_count: int = 0
    counter_evidence: int = 0
    first_seen_ts: float = field(default_factory=time.time)
    last_updated_ts: float = field(default_factory=time.time)
    last_triggered_ts: float = field(default_factory=time.time)


@dataclass
class Belief:
    belief_id: str
    pattern: str
    tendency: str
    env_tag: EnvTag
    evidence_count: int
    counter_evidence: int
    confidence: float
    last_updated_ts: float
    last_triggered_ts: float
