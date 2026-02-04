# -*- coding: utf-8 -*-
import time
from typing import Optional
from .config import C3Config
from .store import C3Store


def prune_pending(store: C3Store, cfg: C3Config, *, now: Optional[float] = None) -> int:
    if now is None:
        now = time.time()
    ttl_s = cfg.pending_ttl_days * 86400
    removed = 0
    for belief_id, pb in list(store.pending.items()):
        if now - pb.last_updated_ts > ttl_s and pb.evidence_count < cfg.min_evidence:
            store.pending.pop(belief_id, None)
            removed += 1
    return removed


def decay_beliefs(store: C3Store, cfg: C3Config, *, now: Optional[float] = None) -> int:
    if now is None:
        now = time.time()
    decay_start_s = cfg.decay_start_days * 86400
    decayed = 0
    for belief_id, belief in store.beliefs.items():
        age_s = now - belief.last_triggered_ts
        if age_s <= decay_start_s:
            continue
        days = age_s / 86400
        belief.confidence *= cfg.decay_rate_per_day ** days
        belief.last_updated_ts = now
        store.beliefs[belief_id] = belief
        decayed += 1
    return decayed


def c3_maintenance(store: C3Store, cfg: C3Config, *, now: Optional[float] = None) -> None:
    if not cfg.enabled:
        return
    prune_pending(store, cfg, now=now)
    decay_beliefs(store, cfg, now=now)
