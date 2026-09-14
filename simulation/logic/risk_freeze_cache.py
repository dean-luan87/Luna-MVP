# -*- coding: utf-8 -*-
"""
Weight-Only Replay Contract：冻结 baseline 参考流，供 candidate 同构输出。
契约：当 patch 仅含 weights.* 时，candidate replay 的 decision/lookahead presence 与 baseline 一致。
"""
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# 执行包：FrozenFrame 签名固定
@dataclass(frozen=True)
class FrozenFrame:
    seq: int
    has_decision: bool
    has_lookahead: bool
    control_mode: Optional[str]
    safety_level: Optional[str]
    pal_lookahead_m: Optional[float]


def is_weights_only_patch(patch: Optional[Dict[str, Any]]) -> bool:
    """
    Patch 分类（写死）：空 {} → True；所有 key 必须以 weights. 开头（允许 meta. 但不参与 config）；其他 → False。
    """
    if patch is None or not isinstance(patch, dict):
        return True
    if len(patch) == 0:
        return True
    for k in patch.keys():
        if not isinstance(k, str):
            return False
        k = k.strip()
        if k.startswith("weights."):
            continue
        if k.startswith("meta."):
            continue
        return False
    return True


def _has_decision(rec: Dict[str, Any]) -> bool:
    """存在 decision 且含 control_mode / safety_level 非空。"""
    d = rec.get("decision") or {}
    sl = d.get("safety_level")
    cm = d.get("control_mode")
    return (
        sl is not None
        and (sl if isinstance(sl, str) else str(sl)).strip() != ""
        and cm is not None
        and str(cm).strip() != ""
    )


def _has_lookahead(rec: Dict[str, Any]) -> bool:
    """存在 decision.pal_lookahead_m 且为有效数值（>0 且非 null）。"""
    d = rec.get("decision") or {}
    v = d.get("pal_lookahead_m")
    if v is None:
        return False
    try:
        return float(v) > 0
    except (TypeError, ValueError):
        return False


def build_frozen_stream_from_baseline(baseline_replay_path: str, out_path: str) -> str:
    """
    从 baseline 的 replay_output.jsonl 逐行读取，解析 seq / decision presence / lookahead presence，
    输出 jsonl 每行：{"seq", "has_decision", "has_lookahead", "control_mode", "safety_level", "pal_lookahead_m"}（平铺）。
    """
    if not os.path.isfile(baseline_replay_path):
        return out_path
    seen_seq: set = set()
    lines: List[Dict[str, Any]] = []
    with open(baseline_replay_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            seq = rec.get("seq")
            if seq is None or seq in seen_seq:
                continue
            seen_seq.add(seq)
            d = rec.get("decision") or {}
            has_dec = _has_decision(rec)
            has_la = _has_lookahead(rec)
            lines.append({
                "seq": int(seq),
                "has_decision": has_dec,
                "has_lookahead": has_la,
                "control_mode": d.get("control_mode"),
                "safety_level": d.get("safety_level"),
                "pal_lookahead_m": d.get("pal_lookahead_m"),
            })
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for obj in lines:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    return out_path


def load_frozen_stream(path: str) -> Dict[int, FrozenFrame]:
    """加载 frozen_risk_stream.jsonl，key=seq，value=FrozenFrame。"""
    out: Dict[int, FrozenFrame] = {}
    if not path or not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            seq = obj.get("seq")
            if seq is None:
                continue
            try:
                ff = FrozenFrame(
                    seq=int(seq),
                    has_decision=bool(obj.get("has_decision", False)),
                    has_lookahead=bool(obj.get("has_lookahead", False)),
                    control_mode=obj.get("control_mode"),
                    safety_level=obj.get("safety_level"),
                    pal_lookahead_m=obj.get("pal_lookahead_m") if obj.get("pal_lookahead_m") is not None else None,
                )
                out[ff.seq] = ff
            except (TypeError, ValueError):
                continue
    return out
