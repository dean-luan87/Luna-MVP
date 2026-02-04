# vision_pipeline/b2/v03/factors.py

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Any


# =========================
# 因子类型（可扩展）
# =========================
class FactorType(str, Enum):
    PATH = "path"
    ENV = "env"
    PEOPLE = "people"
    EVENT = "event"


# =========================
# 因子证据
# =========================
@dataclass
class FactorEvidence:
    factor: FactorType
    score: float          # 0~1
    changed: bool
    reason: str


# =========================
# 核心函数
# =========================
def build_factor_evidences(
    future_states: List[Dict[str, Any]]
) -> Dict[FactorType, FactorEvidence]:
    """
    future_states: [
        {
            "ts": float,
            "perception": perception_dict
        },
        ...
    ]
    """

    evidences: Dict[FactorType, FactorEvidence] = {}

    # ========= PATH =========
    path_score = 0.0
    path_hits = 0

    for s in future_states:
        p = s["perception"].get("path")
        if not p:
            continue

        surface = p.get("surface", "unknown")
        has_path = p.get("has_path", True)

        if surface in ("gravel", "stairs"):
            path_score += 0.6
            path_hits += 1

        if has_path is False:
            path_score += 0.8
            path_hits += 1

    if path_hits > 0:
        evidences[FactorType.PATH] = FactorEvidence(
            factor=FactorType.PATH,
            score=min(1.0, path_score / path_hits),
            changed=True,
            reason="path surface or continuity changed"
        )

    # ========= ENV =========
    env_score = 0.0
    env_hits = 0

    for s in future_states:
        e = s["perception"].get("env")
        if not e:
            continue

        scene = e.get("scene")
        density = e.get("density")
        indoor = e.get("indoor")

        if scene in ("market", "indoor", "plaza"):
            env_score += 0.6
            env_hits += 1

        if density == "high":
            env_score += 0.4
            env_hits += 1

        if indoor is True:
            env_score += 0.5
            env_hits += 1

    if env_hits > 0:
        evidences[FactorType.ENV] = FactorEvidence(
            factor=FactorType.ENV,
            score=min(1.0, env_score / env_hits),
            changed=True,
            reason="environment scene or density changed"
        )

    # ========= PEOPLE =========
    people_score = 0.0
    people_hits = 0

    for s in future_states:
        ppl = s["perception"].get("people")
        if not ppl:
            continue

        count = ppl.get("count", 0)
        moving = ppl.get("moving", False)

        if count >= 5:
            people_score += 0.4
            people_hits += 1

        if moving:
            people_score += 0.3
            people_hits += 1

    if people_hits > 0:
        evidences[FactorType.PEOPLE] = FactorEvidence(
            factor=FactorType.PEOPLE,
            score=min(1.0, people_score / people_hits),
            changed=True,
            reason="people density or movement increased"
        )

    # ========= EVENT（强打断） =========
    for s in future_states:
        events = s["perception"].get("events", [])
        if not events:
            continue

        evidences[FactorType.EVENT] = FactorEvidence(
            factor=FactorType.EVENT,
            score=1.0,
            changed=True,
            reason="sudden blocking or dangerous event detected"
        )
        break  # 一个就够了

    return evidences
