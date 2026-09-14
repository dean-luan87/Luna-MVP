# -*- coding: utf-8 -*-
"""
Phase 3.3-D0: 问题量化系统。只做统计，不改参数。
禁止 import: runtime / intervention / a3 / main / external
"""
import json
import os
import statistics
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

ENGINE_VERSION = "runtime_v1.1"


def _load_jsonl(path: str) -> List[Dict[str, Any]]:
    out = []
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


def _pearson(x: List[float], y: List[float]) -> Optional[float]:
    """Pearson correlation; returns None if insufficient or zero variance."""
    n = len(x)
    if n != len(y) or n < 2:
        return None
    try:
        mx = statistics.mean(x)
        my = statistics.mean(y)
        sx = statistics.stdev(x)
        sy = statistics.stdev(y)
    except statistics.StatisticsError:
        return None
    if sx == 0 or sy == 0:
        return None
    r = sum((a - mx) * (b - my) for a, b in zip(x, y)) / (n * sx * sy)
    return round(r, 3)


class AutoTuneAnalyzer:
    """D0: 只读 outputs/ 与 annotations/，生成统计报告。不写 library_store，不改参数。"""

    def __init__(self, base_dir: str, version_tag: str, out_dir: Optional[str] = None) -> None:
        self.base_dir = base_dir.rstrip("/")
        self.version_tag = version_tag
        self.out_dir = (out_dir or os.path.join("outputs", version_tag)).rstrip("/")
        self.annotations_dir = os.path.join("annotations", version_tag)
        self._summaries: List[Dict[str, Any]] = []
        self._explanations: List[Dict[str, Any]] = []
        self._answers_by_episode: Dict[str, List[Dict[str, Any]]] = {}
        self._merged: List[Dict[str, Any]] = []

    def load_data(self) -> int:
        """加载 summaries、explanations、可选 answers。按 episode_id 合并。返回 episode 数。"""
        self._summaries = _load_jsonl(os.path.join(self.out_dir, "episode_summaries.jsonl"))
        self._explanations = _load_jsonl(os.path.join(self.out_dir, "episode_explanations.jsonl"))
        answers_path = os.path.join(self.annotations_dir, "answers.jsonl")
        answers = _load_jsonl(answers_path) if os.path.isfile(answers_path) else []
        self._answers_by_episode = {}
        for a in answers:
            eid = (a.get("episode_id") or "").strip()
            if eid:
                self._answers_by_episode.setdefault(eid, []).append(a)

        # 以 explanations 为主（有 field_deltas/completeness），缺的用 summary 补
        by_ep = {s.get("episode_id"): s for s in self._summaries if s.get("episode_id")}
        self._merged = []
        for ex in self._explanations:
            eid = ex.get("episode_id") or ""
            rec = {"episode_id": eid, "trigger_type": (ex.get("trigger_type") or "").strip()}
            rec["summary"] = by_ep.get(eid) or {}
            rec["explanation"] = ex
            rec["answers"] = self._answers_by_episode.get(eid, [])
            se = (ex.get("structured_explain") or {})
            risk = se.get("risk_analysis") or {}
            dec = se.get("decision_analysis") or {}
            eng = se.get("engagement_analysis") or {}
            rec["safety_level"] = dec.get("safety_level")
            rec["control_mode"] = eng.get("control_mode") or dec.get("control_mode")
            rec["pal"] = risk.get("pal")
            rec["complexity"] = risk.get("complexity")
            fd = ex.get("field_deltas") or {}
            rec["complexity_delta"] = fd.get("complexity_delta")
            rec["pal_delta"] = fd.get("pal_delta")
            rec["completeness_score"] = ex.get("completeness_score")
            rec["control_mode_path"] = (rec["summary"].get("control_mode_path") or [])
            self._merged.append(rec)
        return len(self._merged)

    def analyze_safety_changes(self) -> Dict[str, Any]:
        """safety_change 统计。"""
        n = len(self._merged)
        safety_count = sum(1 for r in self._merged if (r.get("trigger_type") or "").upper() == "SAFETY_CHANGE")
        ratio = round(safety_count / n, 3) if n else 0.0
        comp_deltas = [r["complexity_delta"] for r in self._merged if r.get("complexity_delta") is not None]
        pal_deltas = [r["pal_delta"] for r in self._merged if r.get("pal_delta") is not None]
        avg_comp = round(statistics.mean(comp_deltas), 3) if comp_deltas else 0.0
        avg_pal = round(statistics.mean(pal_deltas), 3) if pal_deltas else 0.0
        dist = Counter(r.get("safety_level") for r in self._merged if r.get("safety_level"))
        safety_distribution = dict(dist)
        return {
            "episode_count": n,
            "safety_change_count": safety_count,
            "ratio": ratio,
            "avg_complexity_delta": avg_comp,
            "avg_pal_delta": avg_pal,
            "safety_distribution": safety_distribution,
        }

    def analyze_control_mode_switch(self) -> Dict[str, Any]:
        """control_mode 切换统计。"""
        switches = []
        for r in self._merged:
            path = r.get("control_mode_path") or []
            switches.append(max(0, len(path) - 1))
        dist = Counter(r.get("control_mode") for r in self._merged if r.get("control_mode"))
        return {
            "avg_switch_per_episode": round(statistics.mean(switches), 3) if switches else 0.0,
            "max_switch": max(switches) if switches else 0,
            "distribution": dict(dist),
        }

    def analyze_pal_complexity_correlation(self) -> Dict[str, Any]:
        """pal/complexity 相关性；与 safety_change 的相关。"""
        pals = []
        comps = []
        comp_deltas = []
        pal_deltas = []
        safety_binary = []  # 1 if SAFETY_CHANGE trigger else 0
        for r in self._merged:
            p, c = r.get("pal"), r.get("complexity")
            if p is not None and c is not None:
                try:
                    pals.append(float(p))
                    comps.append(float(c))
                except (TypeError, ValueError):
                    pass
            cd = r.get("complexity_delta")
            pd = r.get("pal_delta")
            if cd is not None:
                comp_deltas.append(float(cd))
            else:
                comp_deltas.append(0.0)
            if pd is not None:
                pal_deltas.append(float(pd))
            else:
                pal_deltas.append(0.0)
            safety_binary.append(1 if (r.get("trigger_type") or "").upper() == "SAFETY_CHANGE" else 0)
        pal_complexity_corr = _pearson(pals, comps) if len(pals) >= 2 else None
        complexity_delta_vs_safety = _pearson(comp_deltas, safety_binary) if len(comp_deltas) >= 2 else None
        pal_delta_vs_safety = _pearson(pal_deltas, safety_binary) if len(pal_deltas) >= 2 else None
        return {
            "pal_complexity_corr": pal_complexity_corr,
            "complexity_delta_vs_safety": complexity_delta_vs_safety,
            "pal_delta_vs_safety": pal_delta_vs_safety,
        }

    def generate_report(self) -> Dict[str, Any]:
        """生成完整报告 dict，含 recommendation_candidates（仅文字）。"""
        safety = self.analyze_safety_changes()
        control = self.analyze_control_mode_switch()
        corr = self.analyze_pal_complexity_correlation()
        candidates: List[Dict[str, str]] = []
        n = safety["episode_count"]
        if n >= 1:
            if safety["ratio"] > 0.3 and safety["avg_complexity_delta"] < 0.2:
                candidates.append({
                    "hypothesis": "complexity threshold might be too sensitive",
                    "evidence": "avg_complexity_delta low but safety_change ratio high",
                    "suggested_direction": "increase threshold slightly",
                })
            if control["avg_switch_per_episode"] > 1.5:
                candidates.append({
                    "hypothesis": "control_mode may be switching too often",
                    "evidence": "high avg_switch_per_episode",
                    "suggested_direction": "consider hysteresis or debounce",
                })
            if not candidates:
                candidates.append({
                    "hypothesis": "no strong anomaly from D0 metrics",
                    "evidence": "safety and control stats within typical range",
                    "suggested_direction": "collect more episodes or add human labels",
                })
        return {
            "version": "D0",
            "engine_version": ENGINE_VERSION,
            "episode_count": n,
            "safety_change_stats": safety,
            "control_mode_stats": control,
            "risk_signal_correlation": corr,
            "recommendation_candidates": candidates,
        }
