# -*- coding: utf-8 -*-
"""
从 JSON/JSONL 聚合 observation，按 request_id / trace_id 组装 RequestTraceChain。

最小实现：无 IO、无服务、无后台；仅纯函数 + 聚合。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from capabilities.voice.observations.request_trace_chain import (
    RequestTraceChain,
    TraceErrorRecord,
    TraceStageRecord,
)

# 链型（与文档 LUNA_VOICE_REQUEST_TRACE_EXTRACTION_RULES_V1 对齐）
CHAIN_SUCCESS = "success_chain"
CHAIN_FALLBACK = "provider_fallback_chain"
CHAIN_ROLLBACK = "legacy_rollback_chain"
CHAIN_FAILED = "failed_chain"
CHAIN_SUPPRESSED = "suppressed_chain"
CHAIN_UNKNOWN = "unknown"


def _stage(
    name: str,
    status: str,
    *,
    ts: Optional[float] = None,
    fields: Optional[Dict[str, Any]] = None,
    obs_type: str = "",
    ref: str = "",
) -> TraceStageRecord:
    return TraceStageRecord(
        stage_name=name,
        status=status,
        timestamp=ts,
        key_fields=dict(fields or {}),
        source_observation_type=obs_type,
        source_ref=ref,
    )


def _ts_from(d: Optional[Dict[str, Any]]) -> Optional[float]:
    if not d:
        return None
    t = d.get("timestamp")
    return float(t) if isinstance(t, (int, float)) else None


def _merge_dict(dst: Dict[str, Any], src: Dict[str, Any]) -> None:
    for k, v in src.items():
        if v is None:
            continue
        if k not in dst or dst[k] is None:
            dst[k] = v
            continue
        if isinstance(dst[k], dict) and isinstance(v, dict):
            _merge_dict(dst[k], v)


def _normalize_record(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    将 JSONL 信封或扁平行统一为：
    selection_observation / fallback_observation / cutover_observation / rollback_observation / playback_observation / playback_runtime_observation / output_decision_observation / submit_observation / request_runtime_observation
    以及顶层 request_id / trace_id / success / final_execution_mode 等。
    """
    out: Dict[str, Any] = {}
    for k in ("request_id", "trace_id", "session_id", "task_context_id"):
        if k in obj and obj[k] is not None:
            out[k] = obj[k]

    # JSONL envelope: {"type": "selection", "data": {...}}
    typ = obj.get("type")
    data = obj.get("data")
    if isinstance(typ, str) and isinstance(data, dict):
        key = {
            "selection": "selection_observation",
            "fallback": "fallback_observation",
            "cutover": "cutover_observation",
            "rollback": "rollback_observation",
            "playback": "playback_observation",
            "playback_runtime": "playback_runtime_observation",
            "output_decision": "output_decision_observation",
            "submit_invoked": "submit_observation",
            "request_runtime": "request_runtime_observation",
        }.get(typ)
        if key:
            out[key] = data

    # Flat row (validate_local_tts_runtime)
    for key in (
        "selection_observation",
        "fallback_observation",
        "cutover_observation",
        "rollback_observation",
        "playback_observation",
        "playback_runtime_observation",
        "output_decision_observation",
        "submit_observation",
        "request_runtime_observation",
    ):
        if key in obj and obj[key] is not None and isinstance(obj[key], dict):
            out[key] = obj[key]

    for k in ("success", "ok", "final_execution_mode", "provider_name", "provider_ok", "provider_failure_type"):
        if k in obj:
            out[k] = obj[k]

    md = obj.get("metadata")
    if isinstance(md, dict):
        out.setdefault("metadata", {}).update(md)
    return out


def aggregate_records_for_request(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """合并同一 request 的多条记录（调用方已按 request_id/trace_id 筛过）。"""
    merged: Dict[str, Any] = {}
    for raw in records:
        norm = _normalize_record(raw)
        _merge_dict(merged, norm)
        # 扁平行顶层字段再覆盖一层（normalize 可能未含 ok/success）
        for k in ("success", "ok", "final_execution_mode", "provider_name", "provider_ok", "provider_failure_type"):
            if k in raw and raw[k] is not None:
                merged[k] = raw[k]
    return merged


def classify_chain_type(merged: Dict[str, Any]) -> str:
    cut = merged.get("cutover_observation") or {}
    fb = merged.get("fallback_observation")
    rb = merged.get("rollback_observation")
    fm = merged.get("final_execution_mode") or cut.get("final_execution_mode") or ""

    # 被抑制（占位：仅当显式标记或 output 拒绝且未进入 selector）
    if merged.get("suppressed") is True:
        return CHAIN_SUPPRESSED
    od = merged.get("output_decision_observation")
    if isinstance(od, dict) and od.get("accepted") is False and not cut.get("selector_hit"):
        return CHAIN_SUPPRESSED

    if fm == "failed_no_output":
        return CHAIN_FAILED

    if rb and fm == "legacy_fallback":
        return CHAIN_ROLLBACK

    if fb is not None and isinstance(fb, dict) and fm == "provider_chain":
        return CHAIN_FALLBACK

    if fm == "provider_chain" and merged.get("success") is not False and merged.get("ok") is not False:
        return CHAIN_SUCCESS

    if fm == "legacy_fallback" and not rb:
        # cutover 关闭等场景可能无 rollback observation
        return CHAIN_ROLLBACK

    if merged.get("success") is False or merged.get("ok") is False:
        return CHAIN_FAILED

    return CHAIN_UNKNOWN


def build_request_trace_chain(
    merged: Dict[str, Any],
    *,
    source_ref: str = "",
) -> RequestTraceChain:
    """从合并后的 observation 字典构造 RequestTraceChain。"""
    rid = merged.get("request_id") or ""
    if not rid:
        raise ValueError("merged 缺少 request_id")

    sel = merged.get("selection_observation") or {}
    fb = merged.get("fallback_observation")
    cut = merged.get("cutover_observation") or {}
    rb = merged.get("rollback_observation")
    pb = merged.get("playback_observation")
    pbr = merged.get("playback_runtime_observation")
    od = merged.get("output_decision_observation")
    sub = merged.get("submit_observation")
    rr = merged.get("request_runtime_observation")

    stages: List[TraceStageRecord] = []
    errors: List[TraceErrorRecord] = []
    notes: List[str] = []
    refs: List[str] = []
    if source_ref:
        refs.append(source_ref)

    # 1 request_ingress
    if cut:
        stages.append(
            _stage(
                "request_ingress",
                "ok",
                ts=_ts_from(cut),
                fields={
                    "request_id": rid,
                    "cutover_enabled": cut.get("cutover_enabled"),
                    "cutover_mode": cut.get("cutover_mode"),
                },
                obs_type="TTSCutoverObservation",
                ref=source_ref,
            )
        )
    else:
        stages.append(_stage("request_ingress", "missing", fields={"request_id": rid}))

    # 2 message_preparation
    stages.append(
        _stage(
            "message_preparation",
            "not_connected",
            fields={"note": "SpeechRequest 未在日志行中持久化；需主链显式落盘"},
            obs_type="SpeechRequest",
        )
    )

    # 2.1 request_runtime（V1：request_created/request_submitted/terminal 等）
    # 注意：本 V1 为最小实现，当前聚合器只会保留一个 request_runtime_observation（最后一次合并覆盖）。
    # 后续若需要完整序列，应按 event 聚合为列表；本轮先保证“至少能看到 submitted/terminal”。
    if isinstance(rr, dict):
        stages.append(
            _stage(
                "request_runtime",
                "ok" if rr.get("status") in (None, "", "ok") else ("partial" if rr.get("status") == "rejected" else "fail"),
                ts=_ts_from(rr),
                fields={
                    "event": rr.get("event"),
                    "status": rr.get("status"),
                    "reason": rr.get("reason"),
                    "terminal_mode": rr.get("terminal_mode"),
                },
                obs_type="RequestRuntimeObservation",
            )
        )
    else:
        stages.append(_stage("request_runtime", "missing", obs_type="RequestRuntimeObservation"))

    # 2.5 submit_invoked（最小闭环 V1：证明 submit 被调用）
    if isinstance(sub, dict):
        stages.append(
            _stage(
                "submit_invoked",
                "ok" if sub.get("accepted") is not False else "partial",
                ts=_ts_from(sub),
                fields={
                    "accepted": sub.get("accepted"),
                    "reason": sub.get("reason"),
                    "output_plane": sub.get("output_plane"),
                },
                obs_type="OutputSubmitObservation",
            )
        )
    else:
        stages.append(_stage("submit_invoked", "missing", obs_type="OutputSubmitObservation"))

    # 8 playback_result（speaking 真源锚点：playback executor 的事件）
    if isinstance(pbr, dict):
        ev = str(pbr.get("event") or "")
        st = str(pbr.get("status") or "ok")
        status = "ok"
        if st in ("fail",):
            status = "fail"
        elif st in ("cancelled", "canceled"):
            status = "partial"
        stages.append(
            _stage(
                "playback_result",
                status,
                ts=_ts_from(pbr),
                fields={
                    "event": ev,
                    "status": st,
                    "reason": pbr.get("reason"),
                },
                obs_type="PlaybackRuntimeObservation",
            )
        )
    else:
        stages.append(_stage("playback_result", "missing", obs_type="PlaybackRuntimeObservation"))

    # 3 bridge / routing（含 OutputDecision 若存在）
    bridge_fields: Dict[str, Any] = {}
    if cut:
        bridge_fields["selector_hit"] = cut.get("selector_hit")
    if isinstance(od, dict):
        bridge_fields["output_decision"] = {
            "accepted": od.get("accepted"),
            "reason": od.get("reason"),
        }
    if cut or od:
        stages.append(
            _stage(
                "bridge_or_routing_decision",
                "ok" if (cut and cut.get("selector_hit")) or (od and od.get("accepted") is not False) else "partial",
                ts=_ts_from(cut) or _ts_from(od),
                fields=bridge_fields,
                obs_type="TTSCutoverObservation" if cut else "OutputDecisionObservation",
            )
        )
    else:
        stages.append(_stage("bridge_or_routing_decision", "missing"))

    # 4 core_policy
    stages.append(
        _stage(
            "core_or_policy_handling",
            "reserved",
            fields={"note": "policy 结构化观测未接；非 not_connected 即 reserved"},
        )
    )

    # 5 provider_selection
    if sel:
        stages.append(
            _stage(
                "provider_selection",
                "ok",
                ts=_ts_from(sel),
                fields={
                    "chosen_provider": sel.get("chosen_provider"),
                    "provider_order": sel.get("provider_order"),
                    "selection_reason": sel.get("selection_reason"),
                    "preset_name": sel.get("preset_name"),
                },
                obs_type="ProviderSelectionObservation",
            )
        )
    else:
        stages.append(_stage("provider_selection", "missing"))

    # 6 provider_execution
    if cut.get("provider_chain_ok") is True:
        ex_fields: Dict[str, Any] = {
            "provider_chain_ok": True,
            "selected_provider": (cut.get("metadata") or {}).get("selected_provider"),
        }
        if merged.get("provider_name"):
            ex_fields["provider_name"] = merged["provider_name"]
        stages.append(
            _stage(
                "provider_execution",
                "ok",
                ts=_ts_from(cut),
                fields=ex_fields,
                obs_type="TTSProviderResult",
            )
        )
    elif cut.get("provider_chain_ok") is False:
        stages.append(
            _stage(
                "provider_execution",
                "fail",
                ts=_ts_from(cut),
                fields={
                    "provider_chain_ok": False,
                    "failure_type": (cut.get("metadata") or {}).get("failure_type"),
                },
                obs_type="TTSCutoverObservation",
            )
        )
        errors.append(
            TraceErrorRecord(
                stage_name="provider_execution",
                error_type="provider_chain_failure",
                error_reason=str((cut.get("metadata") or {}).get("failure_type") or "unknown"),
                severity="error",
            )
        )
    else:
        stages.append(_stage("provider_execution", "partial", fields={"note": "无 provider_chain_ok 字段"}))

    # 7 fallback / rollback
    if fb:
        stages.append(
            _stage(
                "fallback_or_rollback",
                "ok",
                ts=_ts_from(fb),
                fields={
                    "primary_provider": fb.get("primary_provider"),
                    "fallback_provider": fb.get("fallback_provider"),
                    "failure_type": fb.get("failure_type"),
                    "output_valid": fb.get("output_valid"),
                },
                obs_type="ProviderFallbackObservation",
            )
        )
    if rb:
        stages.append(
            _stage(
                "fallback_or_rollback",
                "ok",
                ts=_ts_from(rb),
                fields={
                    "rollback_trigger": rb.get("rollback_trigger"),
                    "rollback_reason": rb.get("rollback_reason"),
                    "provider_chain_status": rb.get("provider_chain_status"),
                },
                obs_type="TTSRollbackObservation",
            )
        )
    if not fb and not rb:
        stages.append(_stage("fallback_or_rollback", "skipped", fields={"note": "无 fallback / rollback 观测"}))

    # 8 playback
    if cut:
        fm = cut.get("final_execution_mode")
        stages.append(
            _stage(
                "playback_result",
                "ok" if fm == "provider_chain" else ("fail" if fm == "failed_no_output" else "partial"),
                ts=_ts_from(cut),
                fields={
                    "final_execution_mode": fm,
                    "final_executor": cut.get("final_executor"),
                },
                obs_type="TTSCutoverObservation",
            )
        )
        if fm == "failed_no_output":
            errors.append(
                TraceErrorRecord(
                    stage_name="playback_result",
                    error_type="failed_no_output",
                    error_reason="final_execution_mode=failed_no_output",
                    severity="error",
                )
            )
    elif pb:
        stages.append(
            _stage(
                "playback_result",
                "ok" if pb.get("finished") else "partial",
                ts=_ts_from(pb),
                fields={"started": pb.get("started"), "finished": pb.get("finished"), "error": pb.get("error")},
                obs_type="PlaybackObservation",
            )
        )
    else:
        stages.append(_stage("playback_result", "missing", obs_type="PlaybackObservation"))

    chain_type = classify_chain_type(merged)
    if chain_type == CHAIN_SUPPRESSED:
        notes.append("被抑制链：依赖 output_decision 或显式 suppressed 标记；当前样本可能不足。")

    final_mode = cut.get("final_execution_mode") or merged.get("final_execution_mode")
    provider_name = None
    if sel:
        provider_name = sel.get("chosen_provider")
    if not provider_name and fb and isinstance(fb, dict):
        provider_name = fb.get("final_provider_used") or fb.get("fallback_provider")
    if not provider_name:
        provider_name = (cut.get("metadata") or {}).get("selected_provider") or merged.get("provider_name")

    timestamps = [t for t in (_ts_from(sel), _ts_from(fb), _ts_from(cut), _ts_from(rb)) if t is not None]
    started = min(timestamps) if timestamps else _ts_from(cut)
    ended = max(timestamps) if timestamps else _ts_from(cut)

    status = "ok"
    if final_mode == "failed_no_output":
        status = "failed"
    elif merged.get("success") is False or merged.get("ok") is False:
        status = "failed"
    elif chain_type == CHAIN_UNKNOWN:
        status = "partial"
    if chain_type == CHAIN_SUPPRESSED:
        status = "suppressed"

    return RequestTraceChain(
        request_id=rid,
        trace_id=merged.get("trace_id"),
        session_id=merged.get("session_id"),
        task_context_id=merged.get("task_context_id"),
        chain_type=chain_type,
        final_execution_mode=final_mode,
        provider_name=provider_name,
        started_at=started,
        ended_at=ended,
        status=status,
        stages=stages,
        errors=errors,
        notes=notes,
        raw_observation_refs=refs,
    )


def iter_jsonl(path: Path) -> Iterator[Tuple[int, Dict[str, Any]]]:
    """逐行 JSONL，返回 (line_no, obj)。"""
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield i, json.loads(line)
            except json.JSONDecodeError:
                continue


def load_records_from_json_file(path: Path) -> List[Dict[str, Any]]:
    """加载 .json：支持 {results:[]}, {rows:[]}, 或顶层 list。"""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    out: List[Dict[str, Any]] = []
    if isinstance(data, list):
        for x in data:
            if isinstance(x, dict):
                out.append(x)
    elif isinstance(data, dict):
        for key in ("results", "rows", "items"):
            if isinstance(data.get(key), list):
                for x in data[key]:
                    if isinstance(x, dict):
                        out.append(x)
        if not out and "request_id" in data:
            out.append(data)
    return out


def load_all_records(paths: List[Path]) -> List[Dict[str, Any]]:
    """从多个 JSONL / JSON 文件加载所有记录（未归一化）。"""
    acc: List[Dict[str, Any]] = []
    for p in paths:
        if not p.exists():
            continue
        if p.suffix.lower() == ".jsonl":
            for line_no, obj in iter_jsonl(p):
                if isinstance(obj, dict):
                    obj = dict(obj)
                    obj["_file"] = str(p)
                    obj["_line"] = line_no
                    acc.append(obj)
        elif p.suffix.lower() == ".json":
            for row in load_records_from_json_file(p):
                row = dict(row)
                row["_file"] = str(p)
                acc.append(row)
    return acc


def filter_records_by_request(
    records: List[Dict[str, Any]],
    *,
    request_id: Optional[str] = None,
    trace_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """筛选可能相关的记录（宽松匹配）。"""
    out: List[Dict[str, Any]] = []
    for r in records:
        if request_id and r.get("request_id") == request_id:
            out.append(r)
            continue
        if trace_id and r.get("trace_id") == trace_id:
            out.append(r)
            continue
        # nested
        if request_id:
            data = r.get("data")
            if isinstance(data, dict) and data.get("request_id") == request_id:
                out.append(r)
    return out


def extract_trace_from_paths(
    paths: List[Path],
    *,
    request_id: Optional[str] = None,
    trace_id: Optional[str] = None,
) -> RequestTraceChain:
    """
    从文件列表加载并抽取一条链。
    request_id 与 trace_id 至少一个非空。
    """
    if not request_id and not trace_id:
        raise ValueError("需要 request_id 或 trace_id")

    all_recs = load_all_records(paths)
    filtered = filter_records_by_request(all_recs, request_id=request_id, trace_id=trace_id)
    if not filtered:
        # 空合并：仍返回带 missing 的链
        merged: Dict[str, Any] = {"request_id": request_id or ""}
        if trace_id:
            merged["trace_id"] = trace_id
        if request_id:
            merged["request_id"] = request_id
        chain = build_request_trace_chain(merged, source_ref="no_matching_records")
        chain.notes.append("未在日志中找到匹配记录；阶段多为 missing。")
        return chain

    merged = aggregate_records_for_request(filtered)
    if request_id:
        merged["request_id"] = request_id
    if trace_id:
        merged["trace_id"] = trace_id

    chain = build_request_trace_chain(merged, source_ref="")
    chain.raw_observation_refs = []
    for fr in filtered:
        fp = fr.get("_file")
        ln = fr.get("_line")
        if fp:
            chain.raw_observation_refs.append(f"{fp}:{ln}" if ln else str(fp))
    return chain
