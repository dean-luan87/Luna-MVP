#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unified env shadow 对照观察（V1）

比较 metadata 中 unified_env_summary_shadow_v1（或由主线同源逻辑即时计算）与
当前 shadow 输入所命中的垂直 summary 的语义一致率；导出统计与样本。

不改主线行为；本脚本仅分析。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _resolve_output_dir(explicit: Optional[str]) -> Path:
    """
    默认写入 ROOT/logs；若 logs 为只读或外链无权限，则回退到
    ROOT/logs_analyze_unified_shadow_v1。
    可通过 --output-dir 或环境变量 LUNA_UNIFIED_SHADOW_ANALYZE_OUT 覆盖。
    """
    if explicit:
        p = Path(explicit).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p
    envp = os.getenv("LUNA_UNIFIED_SHADOW_ANALYZE_OUT", "").strip()
    if envp:
        p = Path(envp).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p
    for candidate in (ROOT / "logs", ROOT / "logs_analyze_unified_shadow_v1"):
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write_probe_unified_shadow_analyze"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return candidate
        except OSError:
            continue
    fallback = Path.cwd() / "analyze_unified_env_shadow_out"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


from capabilities.cross_domain.context.unified_env_summary_v1 import (  # noqa: E402
    build_unified_env_summary_v1,
)
from capabilities.voice.runtime.voice_final_text_dispatcher import (  # noqa: E402
    _maybe_attach_unified_env_shadow_v1,
    _unified_shadow_raw_inputs_v1,
)
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402

VerticalSourceV1 = Literal["retail", "sidewalk", "none"]


def _vertical_source_tag_v1(md: Dict[str, Any], *, event: VoiceInputEvent) -> VerticalSourceV1:
    """与 voice_final_text_dispatcher._unified_shadow_raw_inputs_v1 分支一致，仅返回命中来源。"""
    sw = md.get("sidewalk_env_summary_v1")
    rt = md.get("retail_env_summary_v1")
    sw = sw if isinstance(sw, dict) else None
    rt = rt if isinstance(rt, dict) else None

    rt_scene = ""
    if rt:
        rt_scene = str(rt.get("scene_type_candidate") or rt.get("scene_type") or "").strip().lower()
    retail_like = rt_scene in ("retail_shelf", "retail_aisle") or (
        bool(rt_scene) and rt_scene.startswith("retail_")
    )

    if rt and retail_like:
        return "retail"
    if sw:
        return "sidewalk"
    if rt:
        return "retail"
    return "none"


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def _vertical_expected_family_v1(source: VerticalSourceV1, md: Dict[str, Any]) -> str:
    """
    仅从「命中」的垂直 dict 推导期望 scene_family（walkway / retail / unknown），
     deliberately 比 unified 分类器更保守，用于暴露错配；不读取 unified 输出。
    """
    if source == "retail":
        rt = md.get("retail_env_summary_v1")
        if not isinstance(rt, dict):
            return "unknown"
        st = _norm(str(rt.get("scene_type_candidate") or rt.get("scene_type") or ""))
        if st in ("retail_shelf", "retail_aisle"):
            return "retail"
        if st.startswith("retail_"):
            return "retail"
        return "unknown"

    if source == "sidewalk":
        sw = md.get("sidewalk_env_summary_v1")
        if not isinstance(sw, dict):
            return "unknown"
        cand = _norm(str(sw.get("scene_candidate") or ""))
        markers = ("outdoor_walkway", "walkway", "sidewalk", "pedestrian", "path_outdoor")
        if any(m in cand for m in markers) or cand == "outdoor":
            return "walkway"
        return "unknown"

    return "unknown"


def _vertical_freshness_v1(source: VerticalSourceV1, md: Dict[str, Any]) -> Optional[str]:
    if source == "retail":
        rt = md.get("retail_env_summary_v1")
        if isinstance(rt, dict):
            v = rt.get("summary_freshness")
            return str(v) if v is not None else None
    if source == "sidewalk":
        sw = md.get("sidewalk_env_summary_v1")
        if isinstance(sw, dict):
            v = sw.get("summary_freshness")
            return str(v) if v is not None else None
    return None


def _vertical_weak_or_missing_schema_v1(source: VerticalSourceV1, md: Dict[str, Any]) -> bool:
    if source == "retail":
        rt = md.get("retail_env_summary_v1")
        if not isinstance(rt, dict):
            return True
        return not str(rt.get("summary_schema_version") or "").strip()
    if source == "sidewalk":
        sw = md.get("sidewalk_env_summary_v1")
        if not isinstance(sw, dict):
            return True
        return not str(sw.get("summary_schema_version") or "").strip()
    return True


def _vertical_missing_freshness_v1(source: VerticalSourceV1, md: Dict[str, Any]) -> bool:
    return _vertical_freshness_v1(source, md) is None


def _build_shadow_dict(md: Dict[str, Any], event: VoiceInputEvent) -> Dict[str, Any]:
    cand, conf, evt_ts, now = _unified_shadow_raw_inputs_v1(md, event=event)
    return build_unified_env_summary_v1(
        raw_scene_candidate=cand,
        raw_environment_confidence=conf,
        event_timestamp=evt_ts,
        now=now,
        source="unified_env_shadow_v1",
    )


@dataclass
class RowResult:
    fixture_id: str
    vertical_source: str
    unified_family: str
    expected_family: str
    unified_candidate: str
    shadow_input_candidate: str
    candidate_match: bool
    family_match: bool
    unified_freshness: str
    vertical_freshness: Optional[str]
    freshness_bucket: str
    unified_unknown_vertical_confident: bool
    unified_fresh_vertical_ambiguous: bool
    unified_helpful_fill: bool
    notes: str


def _analyze_one(
    fixture_id: str,
    metadata: Dict[str, Any],
    *,
    event: VoiceInputEvent,
    use_dispatcher_attach: bool,
) -> RowResult:
    md = dict(metadata)
    src = _vertical_source_tag_v1(md, event=event)
    exp_fam = _vertical_expected_family_v1(src, md)
    cand_in, _conf, _ets, _now = _unified_shadow_raw_inputs_v1(md, event=event)

    if use_dispatcher_attach:
        os.environ["LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1"] = "1"
        ctx = VoiceRuntimeContext(metadata=md)
        out = _maybe_attach_unified_env_shadow_v1(event, ctx)
        uni = (out.metadata or {}).get("unified_env_summary_shadow_v1") or {}
    else:
        uni = _build_shadow_dict(md, event)

    if not isinstance(uni, dict):
        uni = {}

    u_fam = str(uni.get("scene_family") or "unknown")
    u_cand = str(uni.get("scene_candidate") or "")
    u_fresh = str(uni.get("summary_freshness") or "")
    v_fresh = _vertical_freshness_v1(src, md)

    cand_match = _norm(u_cand) == _norm(cand_in)
    fam_match = u_fam == exp_fam

    if v_fresh is None:
        fb = "vertical_missing_freshness"
    elif v_fresh == u_fresh:
        fb = "equal"
    else:
        fb = "divergent"

    vconf = 0.0
    if src == "sidewalk":
        sw = md.get("sidewalk_env_summary_v1")
        if isinstance(sw, dict):
            vconf = float(sw.get("path_confidence") or 0.0)
    elif src == "retail":
        rt = md.get("retail_env_summary_v1")
        if isinstance(rt, dict):
            vconf = float(rt.get("retail_context_confidence") or 0.0)

    unified_unknown_vc = u_fam == "unknown" and vconf >= 0.55
    unified_fresh_va = u_fresh == "fresh" and v_fresh == "ambiguous"

    helpful = bool(
        src != "none"
        and uni.get("summary_schema_version")
        and u_fresh
        and (_vertical_weak_or_missing_schema_v1(src, md) or _vertical_missing_freshness_v1(src, md))
    )

    note = ""
    if not fam_match:
        note = f"family:unified={u_fam},vertical_expected={exp_fam},source={src}"
    elif not cand_match:
        note = f"candidate:unified={u_cand!r},input={cand_in!r}"

    return RowResult(
        fixture_id=fixture_id,
        vertical_source=src,
        unified_family=u_fam,
        expected_family=exp_fam,
        unified_candidate=u_cand,
        shadow_input_candidate=cand_in,
        candidate_match=cand_match,
        family_match=fam_match,
        unified_freshness=u_fresh,
        vertical_freshness=v_fresh,
        freshness_bucket=fb,
        unified_unknown_vertical_confident=unified_unknown_vc,
        unified_fresh_vertical_ambiguous=unified_fresh_va,
        unified_helpful_fill=helpful,
        notes=note,
    )


def _default_fixtures() -> List[Tuple[str, Dict[str, Any], float]]:
    """(id, metadata, event_timestamp) 内置对照集。"""
    ts = 1_700_000_000.0
    out: List[Tuple[str, Dict[str, Any], float]] = []

    out.append(
        (
            "sw_walkway_fresh",
            {
                "sidewalk_env_summary_v1": {
                    "scene_candidate": "outdoor_walkway",
                    "path_confidence": 0.85,
                    "is_outdoor": True,
                    "summary_schema_version": "sidewalk_env_summary_v1/1",
                    "summary_freshness": "fresh",
                    "event_timestamp": ts,
                },
            },
            ts,
        )
    )

    out.append(
        (
            "rt_retail_fresh",
            {
                "retail_env_summary_v1": {
                    "scene_type": "retail_shelf",
                    "scene_type_candidate": "retail_shelf",
                    "retail_context_confidence": 0.72,
                    "shelf_visible": True,
                    "summary_schema_version": "retail_env_summary_v1/1",
                    "summary_freshness": "fresh",
                    "event_timestamp": ts,
                },
            },
            ts,
        )
    )

    out.append(
        (
            "both_retail_wins",
            {
                "sidewalk_env_summary_v1": {
                    "scene_candidate": "unknown",
                    "path_confidence": 0.3,
                    "is_outdoor": False,
                    "summary_schema_version": "sidewalk_env_summary_v1/1",
                    "summary_freshness": "ambiguous",
                    "event_timestamp": ts,
                },
                "retail_env_summary_v1": {
                    "scene_type_candidate": "retail_aisle",
                    "retail_context_confidence": 0.8,
                    "shelf_visible": True,
                    "summary_schema_version": "retail_env_summary_v1/1",
                    "summary_freshness": "fresh",
                    "event_timestamp": ts,
                },
            },
            ts,
        )
    )

    # 人行道 dict 内出现 retail 标签：垂直保守期望 unknown，unified 仍可能判 retail → 故意错配样本
    out.append(
        (
            "sw_dict_retail_string_mismatch",
            {
                "sidewalk_env_summary_v1": {
                    "scene_candidate": "retail_shelf",
                    "path_confidence": 0.75,
                    "is_outdoor": False,
                    "summary_schema_version": "sidewalk_env_summary_v1/1",
                    "summary_freshness": "fresh",
                    "event_timestamp": ts,
                },
            },
            ts,
        )
    )

    # 原始垂直缺 schema / freshness，unified 仍可产出结构化 shadow → 补缺候选
    out.append(
        (
            "sw_raw_weak_vertical",
            {
                "sidewalk_env_summary_v1": {
                    "scene_candidate": "sidewalk",
                    "path_confidence": 0.5,
                    "is_outdoor": True,
                    "event_timestamp": ts,
                },
            },
            ts,
        )
    )

    out.append(
        (
            "none_empty",
            {"risk_summary_v1": {"risk_level": "low", "risk_type": "none"}},
            ts,
        )
    )

    return out


def _load_jsonl(path: Path) -> List[Tuple[str, Dict[str, Any], float]]:
    rows: List[Tuple[str, Dict[str, Any], float]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        mid = str(obj.get("id") or f"line_{i}")
        md = obj.get("metadata")
        if not isinstance(md, dict):
            continue
        ets = obj.get("event_timestamp")
        try:
            ts = float(ets) if ets is not None else time.time()
        except (TypeError, ValueError):
            ts = time.time()
        rows.append((mid, md, ts))
    return rows


def _row_to_dict(r: RowResult) -> Dict[str, Any]:
    return {
        "fixture_id": r.fixture_id,
        "vertical_source": r.vertical_source,
        "unified_family": r.unified_family,
        "expected_family_from_vertical": r.expected_family,
        "unified_candidate": r.unified_candidate,
        "shadow_input_candidate": r.shadow_input_candidate,
        "candidate_match": r.candidate_match,
        "family_match": r.family_match,
        "unified_freshness": r.unified_freshness,
        "vertical_freshness": r.vertical_freshness,
        "freshness_bucket": r.freshness_bucket,
        "unified_unknown_but_vertical_confident": r.unified_unknown_vertical_confident,
        "unified_fresh_but_vertical_ambiguous": r.unified_fresh_vertical_ambiguous,
        "unified_helpful_fill": r.unified_helpful_fill,
        "notes": r.notes,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="unified env shadow 对照观察 V1")
    ap.add_argument(
        "--input-jsonl",
        type=str,
        default="",
        help="可选：每行 JSON，含 metadata、可选 event_timestamp、可选 id",
    )
    ap.add_argument(
        "--use-dispatcher-attach",
        action="store_true",
        help="通过 _maybe_attach_unified_env_shadow_v1 计算 shadow（需打开环境开关逻辑）",
    )
    ap.add_argument(
        "--output-dir",
        type=str,
        default="",
        help="报告输出目录（默认：logs/ 或可写回退目录；也可用 LUNA_UNIFIED_SHADOW_ANALYZE_OUT）",
    )
    args = ap.parse_args()

    utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = _resolve_output_dir(args.output_dir.strip() or None)
    jpath = log_dir / f"analyze_unified_env_shadow_v1_{utc}.json"
    mpath = log_dir / f"analyze_unified_env_shadow_v1_{utc}.md"

    if args.input_jsonl:
        fixtures = _load_jsonl(Path(args.input_jsonl))
    else:
        fixtures = _default_fixtures()

    rows: List[RowResult] = []
    for fid, md, ts in fixtures:
        ev = VoiceInputEvent(
            request_id=fid,
            session_id="analyze_session",
            timestamp=ts,
            raw_text="x",
            normalized_text="x",
            is_task_mode=True,
        )
        rows.append(
            _analyze_one(
                fid,
                md,
                event=ev,
                use_dispatcher_attach=bool(args.use_dispatcher_attach),
            )
        )

    n = max(len(rows), 1)
    fam_ok = sum(1 for r in rows if r.family_match)
    cand_ok = sum(1 for r in rows if r.candidate_match)
    fam_mm = sum(1 for r in rows if not r.family_match)
    cand_mm = sum(1 for r in rows if not r.candidate_match)

    fresh_buckets: Dict[str, int] = {}
    for r in rows:
        fresh_buckets[r.freshness_bucket] = fresh_buckets.get(r.freshness_bucket, 0) + 1

    helpful = sum(1 for r in rows if r.unified_helpful_fill)

    summary = {
        "generated_at_utc": utc,
        "fixture_count": len(rows),
        "scene_family_match_rate": round(fam_ok / n, 6),
        "scene_candidate_match_rate": round(cand_ok / n, 6),
        "freshness_alignment_summary": fresh_buckets,
        "family_mismatch_count": fam_mm,
        "candidate_mismatch_count": cand_mm,
        "unified_helpful_fill_count": helpful,
    }

    aligned = [_row_to_dict(r) for r in rows if r.family_match and r.candidate_match]
    mismatch = [_row_to_dict(r) for r in rows if not r.family_match or not r.candidate_match]
    suspicious = [
        _row_to_dict(r)
        for r in rows
        if r.unified_helpful_fill
        or r.unified_unknown_vertical_confident
        or r.unified_fresh_vertical_ambiguous
    ]

    payload = {
        **summary,
        "samples": {
            "aligned": aligned,
            "mismatch_or_divergent": mismatch,
            "helpful_or_suspicious": suspicious,
        },
    }

    jpath.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        f"# unified env shadow 对照观察（V1） {utc}",
        "",
        "## 汇总",
        "",
        f"- fixture_count: {summary['fixture_count']}",
        f"- scene_family_match_rate: {summary['scene_family_match_rate']}",
        f"- scene_candidate_match_rate: {summary['scene_candidate_match_rate']}",
        f"- family_mismatch_count: {summary['family_mismatch_count']}",
        f"- candidate_mismatch_count: {summary['candidate_mismatch_count']}",
        f"- unified_helpful_fill_count: {summary['unified_helpful_fill_count']}",
        f"- freshness_alignment_summary: `{json.dumps(fresh_buckets, ensure_ascii=False)}`",
        "",
        "## 一致样本（摘要）",
        "",
        f"- 条数: {len(aligned)}",
        "",
        "## 错配 / 候选不一致（摘要）",
        "",
        f"- 条数: {len(mismatch)}",
        "",
    ]
    for r in mismatch[:20]:
        md_lines.append(f"- **{r['fixture_id']}**: {r.get('notes') or json.dumps(r, ensure_ascii=False)[:200]}")
    md_lines.extend(
        [
            "",
            "## 补缺或可疑（摘要）",
            "",
            f"- 条数: {len(suspicious)}",
            "",
        ]
    )
    for r in suspicious[:20]:
        md_lines.append(f"- **{r['fixture_id']}**: helpful={r.get('unified_helpful_fill')} "
                        f"unk_vs_conf={r.get('unified_unknown_but_vertical_confident')} "
                        f"fresh_vs_amb={r.get('unified_fresh_but_vertical_ambiguous')}")
    md_lines.extend(
        [
            "",
            f"完整 JSON: `{jpath.name}`（目录 `{log_dir}`）",
            "",
            "## 一句话收束",
            "",
            "对照统计已落盘；是否进入最小接线实验应结合真实窗口 JSONL 重跑本脚本后再判断。",
        ]
    )
    mpath.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {jpath}")
    print(f"Wrote {mpath}")


if __name__ == "__main__":
    main()
