# -*- coding: utf-8 -*-
"""
Phase 3.3-D0: SimRunner — 离线重跑器。
只读 library_store/.../records.jsonl + meta.json；只写 outputs/.../simulations/。
禁止使用真实时钟与 sleep；不导入 runtime / intervention / a3 / main / external。
D1 Presence-Only Contract：当 patch 仅含 weights.* 时，candidate 仅与 baseline 做 decision/lookahead presence 对齐，禁止复制任何数值。
"""
import json
import os
from typing import Any, Dict, List, Optional

from simulation.logic.presence_contract import build_presence_map, is_weights_only_patch
from simulation.logic.risk_freeze_cache import (
    build_frozen_stream_from_baseline,
)

ENGINE_VERSION = "runtime_v1.1"
OBS_V1 = "OBS_V1"
FROZEN_STREAM_FILENAME = "frozen_risk_stream.jsonl"
REPLAY_FILENAME = "replay_output.jsonl"


def _load_json(path: str) -> Optional[Dict[str, Any]]:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _load_jsonl(path: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def run_episode(
    base_dir: str,
    version_tag: str,
    episode_rel_path: str,
    patch_path: str,
    out_dir: str,
    bundle_episode_id: Optional[str] = None,
    baseline_bundle_path: Optional[str] = None,
    weights_only_contract: bool = True,
    mode: str = "replay",
) -> str:
    """
    离线重跑单 episode：读 records + patch，写出 replay。
    mode="replay"：decision 来自 record（统一宇宙）。
    mode="recompute"：baseline 与 candidate 均用 A3 Headless 重算，weights 不同；Presence Contract 保留。
    """
    base_dir = base_dir.rstrip("/")
    out_dir = out_dir.rstrip("/")
    episode_dir = os.path.join(base_dir, episode_rel_path.strip("/"))
    records_path = os.path.join(episode_dir, "records.jsonl")
    meta_path = os.path.join(episode_dir, "meta.json")

    records = _load_jsonl(records_path)
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    meta = _load_json(meta_path) or {}
    episode_id = meta.get("episode_id") or os.path.basename(episode_dir.rstrip("/"))
    bundle_id = bundle_episode_id if bundle_episode_id is not None else episode_id

    patch_config: Dict[str, Any] = {}
    if patch_path and os.path.isfile(patch_path):
        patch_config = _load_json(patch_path) or {}
    baseline_config: Dict[str, Any] = {}
    candidate = {**baseline_config, **patch_config}

    if not patch_path or not os.path.isfile(patch_path):
        patch_id = "baseline"
    else:
        patch_id = os.path.splitext(os.path.basename(patch_path))[0] or "baseline"
    # D2.3：blind_patch 对抗补丁在 replay 中模拟“把 CAUTION/DANGER 判成 SAFE、且无 GUARDED/短 lookahead”，供门禁 FAIL。
    is_blind_patch = (
        patch_id == "blind_patch"
        or "blind_patch" in (patch_config.get("patch_id") or "")
    )
    bundle_name = f"{bundle_id}_{patch_id}"
    bundle_dir = os.path.join(out_dir, bundle_name)
    os.makedirs(bundle_dir, exist_ok=True)

    # D2.3：baseline / empty_patch 使用确定性“参考风险”基线（按 seq 注入 CAUTION），使与 blind_patch 对比时能触发门禁。
    is_baseline_or_empty = (patch_id == "baseline" or patch_id == "empty_patch")
    # D1 Presence-Only Contract：candidate 仅与 baseline 做 decision/lookahead presence 对齐，禁止注入数值
    weights_only_candidate = (
        weights_only_contract
        and not is_baseline_or_empty
        and is_weights_only_patch(patch_config)
        and (baseline_bundle_path or "").strip() != ""
    )
    presence_map: Dict[str, Dict[int, bool]] = {"has_decision": {}, "has_lookahead": {}}
    baseline_replay_path = ""
    if weights_only_candidate and baseline_bundle_path:
        baseline_replay_path = os.path.join(baseline_bundle_path.rstrip("/"), REPLAY_FILENAME)
        if os.path.isfile(baseline_replay_path):
            presence_map = build_presence_map(baseline_replay_path)
        baseline_replay_path = os.path.abspath(baseline_replay_path) if baseline_replay_path else ""

    # Phase 2 recompute：weights.* 必选；thresholds.* 仅用于诊断/calibration probe，不进入 D1 候选空间
    a3_adapter = None
    if mode == "recompute":
        import simulation.logic.a3_headless_adapter as _a3_adapter_mod
        print("[SIM] using a3_headless_adapter from:", getattr(_a3_adapter_mod, "__file__", "?"))
        from simulation.logic.a3_headless_adapter import A3HeadlessAdapter
        a3_patch = {k: v for k, v in patch_config.items() if isinstance(k, str) and (k == "risk_scale_factor" or k.startswith("weights.") or k.startswith("thresholds.") or k.startswith("smoothing."))}
        a3_adapter = A3HeadlessAdapter(base_config={}, patch_config=a3_patch)
        a3_adapter.reset()

    def _apply_reference_risk(d: Dict[str, Any], seq: int) -> None:
        d["safety_level"] = "CAUTION" if seq % 7 == 0 else "SAFE"
        d["control_mode"] = "ASSISTED"
        d["pal_lookahead_m"] = 2.0

    # 用于 scorer early_gain：recompute 时写“决策用风险 + 阈值 + high_risk”，与 A3 口径一致
    replay_lines: List[Dict[str, Any]] = []
    for r in obs_v1:
        seq = r.get("seq", len(replay_lines))
        ts = r.get("ts", 0.0)
        decision: Dict[str, Any]
        risk_used_this_frame: Optional[float] = None
        threshold_this_frame: Optional[float] = None
        high_risk_this_frame: Optional[bool] = None
        if mode == "recompute" and a3_adapter is not None:
            out = a3_adapter.tick(r, virtual_ts=ts)
            decision = {
                "safety_level": out.get("safety_level"),
                "control_mode": out.get("control_mode"),
                "pal_lookahead_m": out.get("pal_lookahead_m"),
            }
            risk_used_this_frame = float(out.get("risk_used_for_decision") or out.get("complexity_score") or 0.0)
            threshold_this_frame = float(out.get("threshold_safe_to_caution", 0.38))
            high_risk_this_frame = risk_used_this_frame >= threshold_this_frame
        else:
            decision = (r.get("decision") or {}).copy()

        forced_decision_presence = False
        forced_lookahead_presence = False
        missing_presence = False
        if weights_only_candidate and presence_map["has_decision"]:
            hd = presence_map["has_decision"].get(seq)
            hl = presence_map["has_lookahead"].get(seq, False)
            if hd is None:
                missing_presence = True
                if mode != "recompute":
                    if not (decision.get("safety_level") or "").strip():
                        _apply_reference_risk(decision, seq)
                    decision["decision_source"] = "baseline_passthrough"
                else:
                    decision["decision_source"] = "recompute"
                rec_out = {
                    "seq": seq,
                    "ts": ts,
                    "decision": decision,
                    "explain_placeholder": True,
                    "replay_meta": {
                        "weights_only_contract_applied": True,
                        "frozen_stream_path": baseline_replay_path,
                        "forced_decision_presence": False,
                        "forced_lookahead_presence": False,
                        "missing_frozen": True,
                    },
                }
                if risk_used_this_frame is not None:
                    rec_out["risk_used_for_decision"] = risk_used_this_frame
                if threshold_this_frame is not None:
                    rec_out["threshold_safe_to_caution"] = threshold_this_frame
                if high_risk_this_frame is not None:
                    rec_out["high_risk"] = high_risk_this_frame
            else:
                # A) decision presence 对齐（禁止复制 baseline 数值）；cand_dec 来自 A3(recompute) 或 record(replay)
                cand_dec = decision if mode == "recompute" else (r.get("decision") or {}).copy()
                has_cand_decision = bool(cand_dec)
                if not hd:
                    decision = {}
                elif not has_cand_decision:
                    decision = {"decision_valid": False, "meta": {"forced_decision_presence": True}}
                    forced_decision_presence = True
                else:
                    decision = cand_dec
                    decision.setdefault("meta", {})["contract_applied"] = True
                # B) lookahead presence 对齐（只补字段存在性，值为 null，不填 baseline 数值）
                if hd and isinstance(decision, dict):
                    if not hl:
                        decision.pop("pal_lookahead_m", None)
                        if decision.get("meta") is not None:
                            decision["meta"]["forced_lookahead_presence"] = False
                    else:
                        if "pal_lookahead_m" not in decision:
                            decision["pal_lookahead_m"] = None
                            decision.setdefault("meta", {})["forced_lookahead_presence"] = True
                            forced_lookahead_presence = True
                rec_out = {
                    "seq": seq,
                    "ts": ts,
                    "decision": decision,
                    "explain_placeholder": True,
                    "replay_meta": {
                        "weights_only_contract_applied": True,
                        "frozen_stream_path": baseline_replay_path,
                        "forced_decision_presence": forced_decision_presence,
                        "forced_lookahead_presence": forced_lookahead_presence,
                        "missing_frozen": False,
                    },
                }
                if risk_used_this_frame is not None:
                    rec_out["risk_used_for_decision"] = risk_used_this_frame
                if threshold_this_frame is not None:
                    rec_out["threshold_safe_to_caution"] = threshold_this_frame
                if high_risk_this_frame is not None:
                    rec_out["high_risk"] = high_risk_this_frame
        else:
            # replay 模式才做 stub/blind_patch；recompute 已由 A3 产出
            if mode != "recompute":
                if not is_baseline_or_empty and not (decision.get("safety_level") or "").strip():
                    _apply_reference_risk(decision, seq)
                if is_blind_patch:
                    if not is_baseline_or_empty:
                        _apply_reference_risk(decision, seq)
                    level = (decision.get("safety_level") or "").strip().upper()
                    if level in ("CAUTION", "DANGER"):
                        decision["safety_level"] = "SAFE"
                        decision["decision_source"] = "blind_patch_simulated"
                    else:
                        decision["decision_source"] = "baseline_passthrough"
                else:
                    decision["decision_source"] = "baseline_passthrough"
            else:
                decision["decision_source"] = "recompute"
            rec_out = {
                "seq": seq,
                "ts": ts,
                "decision": decision,
                "explain_placeholder": mode != "recompute",
            }
            if risk_used_this_frame is not None:
                rec_out["risk_used_for_decision"] = risk_used_this_frame
            if threshold_this_frame is not None:
                rec_out["threshold_safe_to_caution"] = threshold_this_frame
            if high_risk_this_frame is not None:
                rec_out["high_risk"] = high_risk_this_frame
        replay_lines.append(rec_out)

    replay_path = os.path.join(bundle_dir, "replay_output.jsonl")
    with open(replay_path, "w", encoding="utf-8") as f:
        for rec in replay_lines:
            # 写 replay：decision/seq/ts；risk_used_for_decision/threshold_safe_to_caution/high_risk 供 scorer early_gain
            out_rec = {"seq": rec["seq"], "ts": rec["ts"], "decision": rec["decision"], "explain_placeholder": rec.get("explain_placeholder", True)}
            if "replay_meta" in rec:
                out_rec["replay_meta"] = rec["replay_meta"]
            if "risk_used_for_decision" in rec:
                out_rec["risk_used_for_decision"] = rec["risk_used_for_decision"]
            if "threshold_safe_to_caution" in rec:
                out_rec["threshold_safe_to_caution"] = rec["threshold_safe_to_caution"]
            if "high_risk" in rec:
                out_rec["high_risk"] = rec["high_risk"]
            if "complexity_delta" in rec:
                out_rec["complexity_delta"] = rec["complexity_delta"]
            f.write(json.dumps(out_rec, ensure_ascii=False) + "\n")

    # baseline 跑完后生成 frozen stream
    if is_baseline_or_empty:
        build_frozen_stream_from_baseline(
            replay_path,
            os.path.join(bundle_dir, FROZEN_STREAM_FILENAME),
        )

    created_at = meta.get("created_at") or "D0_replay"
    run_meta = {
        "episode_id": episode_id,
        "patch_id": patch_id,
        "created_at": created_at,
        "engine_version": "recompute_v1" if mode == "recompute" else ENGINE_VERSION,
        "record_count": len(replay_lines),
        "config_applied": candidate,
        "weights_only_contract_applied": weights_only_candidate,
        "frozen_stream_path": baseline_replay_path if weights_only_candidate else None,
        "recompute": mode == "recompute",
    }
    run_meta_path = os.path.join(bundle_dir, "run_meta.json")
    with open(run_meta_path, "w", encoding="utf-8") as f:
        json.dump(run_meta, f, ensure_ascii=False, indent=2)

    return bundle_dir
