# vision_pipeline/b2/v03/param_encoder.py
from __future__ import annotations
from typing import Dict, Any

from .param_schema import clamp
from .param_registry import PARAMS


def _onehot(val: str | None, target: str) -> float:
    return 1.0 if (val == target) else 0.0


def encode_params(factors: Dict[str, Any]) -> Dict[str, float]:
    """
    输入：EvidenceRecord 中的 factors（结构化事实）
    输出：参数向量（稀疏 dict）
    """
    env = factors.get("env") or {}
    people = factors.get("people") or {}
    path = factors.get("path") or {}
    motion = factors.get("motion") or {}
    event = factors.get("event") or {}

    out: Dict[str, float] = {}

    # env.scene_type
    scene_type = env.get("scene_type")
    out["env.scene_type.indoor"] = _onehot(scene_type, "indoor")
    out["env.scene_type.outdoor"] = _onehot(scene_type, "outdoor")

    # env.enclosure
    enclosure = (env.get("enclosure") or {}).get("type")
    out["env.enclosure.enclosed"] = _onehot(enclosure, "enclosed")

    # elevator
    vt = env.get("vertical_transport") or {}
    out["env.vertical_transport.is_elevator"] = 1.0 if vt.get("is_elevator") else 0.0
    st = vt.get("state")
    out["env.vertical_transport.state.entering"] = _onehot(st, "entering")
    out["env.vertical_transport.state.inside"] = _onehot(st, "inside")
    out["env.vertical_transport.state.exiting"] = _onehot(st, "exiting")

    # people
    count = people.get("count")
    if isinstance(count, (int, float)):
        out["people.count"] = clamp(float(count) / 50.0, 0.0, 1.0)  # 50人归一化阈值可调

    dens = people.get("density") or {}
    if isinstance(dens.get("value"), (int, float)):
        out["people.density.value"] = clamp(float(dens["value"]), 0.0, 1.0)
    if isinstance(dens.get("delta"), (int, float)):
        out["people.density.delta"] = clamp(float(dens["delta"]), -1.0, 1.0)

    mp = people.get("motion_pattern") or {}
    mp_t = mp.get("type")
    out["people.motion.bidirectional"] = _onehot(mp_t, "bidirectional")
    out["people.motion.crossing"] = _onehot(mp_t, "crossing")
    out["people.motion.chaotic"] = _onehot(mp_t, "chaotic")

    cs = people.get("crowd_scene") or {}
    out["people.crowd_scene.is_market"] = 1.0 if cs.get("is_market") else 0.0

    of = people.get("opposite_flow") or {}
    out["people.opposite_flow.detected"] = 1.0 if of.get("detected") else 0.0

    # path placeholder
    out["path.surface.changed"] = 1.0 if path.get("surface_changed") else 0.0

    # motion
    spd = motion.get("speed")
    if isinstance(spd, (int, float)):
        out["motion.speed"] = clamp(float(spd), 0.0, 1.0)

    mpt = motion.get("motion_pattern")
    out["motion.motion_pattern.vertical_shift"] = _onehot(mpt, "vertical_shift")

    # event
    et = event.get("type")
    out["event.near_miss"] = _onehot(et, "near_miss")
    out["event.collision_risk"] = _onehot(et, "collision_risk")
    sev = event.get("severity")
    if isinstance(sev, (int, float)):
        out["event.severity"] = clamp(float(sev), 0.0, 1.0)

    # 只输出注册表里出现过的 pid（保证稳定、避免脏字段）
    allowed = {p.pid for p in PARAMS}
    return {k: v for k, v in out.items() if k in allowed}

