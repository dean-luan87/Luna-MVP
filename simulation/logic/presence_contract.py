# -*- coding: utf-8 -*-
"""
Weight-Only Replay Contract (Presence-Only).
仅约束 decision / pal_lookahead_m 的 presence，禁止任何 baseline 数值注入。
"""
import json
from typing import Dict, Optional


def is_weights_only_patch(patch: Optional[dict]) -> bool:
    """
    判定 patch 是否可应用合同：空 patch 或所有 key 以 weights. 开头。
    True 仅表示“可应用合同”；合同只对 candidate 生效（baseline 不应用）。
    """
    if not patch:
        return True
    return all(k.startswith("weights.") for k in patch.keys())


def build_presence_map(baseline_replay_path: str) -> Dict[str, Dict[int, bool]]:
    """
    从 baseline 的 replay_output.jsonl 构建 presence map（只存布尔）。
    返回 {"has_decision": {seq: bool}, "has_lookahead": {seq: bool}}。
    has_lookahead 仅在 has_decision=True 时才有意义。
    """
    has_decision: Dict[int, bool] = {}
    has_lookahead: Dict[int, bool] = {}
    try:
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
                if seq is None:
                    continue
                seq = int(seq)
                dec = rec.get("decision")
                dec_present = "decision" in rec and dec is not None
                has_decision[seq] = dec_present
                has_lookahead[seq] = dec_present and isinstance(dec, dict) and "pal_lookahead_m" in dec
    except OSError:
        pass
    return {"has_decision": has_decision, "has_lookahead": has_lookahead}
