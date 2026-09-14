# -*- coding: utf-8 -*-
"""
链级问题分析：输入 RequestTraceChain，输出 RequestTraceIssue + RequestTraceDiagnosticSummary。

规则化归因与检查点；无自动修复、无大模型、不改主链。
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_diagnostic_summary import RequestTraceDiagnosticSummary
from capabilities.voice.observations.request_trace_issue import (
    ISSUE_NONE,
    ISSUE_OBSERVATION_GAP,
    ISSUE_OUTPUT_DELIVERY_FAILURE,
    ISSUE_PLAYBACK_FAILURE,
    ISSUE_PROVIDER_CHAIN_FAILURE,
    ISSUE_PROVIDER_UNAVAILABLE,
    ISSUE_REQUEST_SUPPRESSED,
    ISSUE_UNKNOWN,
    SEVERITY_CRITICAL,
    SEVERITY_DEGRADED,
    SEVERITY_ERROR,
    SEVERITY_INFO,
    SEVERITY_WARNING,
    RequestTraceIssue,
)
from capabilities.voice.observations.request_trace_summary import build_request_trace_summary

CHECKPOINTS: dict[str, List[str]] = {
    ISSUE_NONE: ["无需额外排查（链级成功）"],
    ISSUE_PROVIDER_UNAVAILABLE: [
        "检查 primary provider 可执行文件路径与权限",
        "检查模型文件完整性（分片、checksum）",
        "检查 voice_tts_config.yaml 中 local_runtime 与 timeouts",
        "检查 voice_presets / 预设与 active_provider 是否一致",
    ],
    ISSUE_PROVIDER_CHAIN_FAILURE: [
        "检查 provider_order 与 active_provider",
        "检查 fallback 与 fallback_provider 配置",
        "检查各 provider 的 failure_type 与日志",
        "检查 legacy_fallback 与 cutover.rollback_on_provider_chain_failure",
        "检查 legacy 播报路径是否可用",
    ],
    ISSUE_REQUEST_SUPPRESSED: [
        "检查 dedup / cooldown / speech_gate 状态",
        "检查 output_category 与 priority",
        "检查当前是否为 restricted_device 等运行态",
    ],
    ISSUE_PLAYBACK_FAILURE: [
        "检查 audio_worker 是否收到任务与执行结果",
        "检查 playback 路径与 legacy 提交是否成功",
        "检查音频字节是否合法（长度、格式）",
        "检查 speech_gate 最终放行与场景冷却",
    ],
    ISSUE_OUTPUT_DELIVERY_FAILURE: [
        "检查 provider_chain_ok 与 final_execution_mode 组合",
        "检查 legacy_submit 返回值与 failed_no_output 成因",
        "检查 cutover 与 legacy_fallback.enabled",
    ],
    ISSUE_OBSERVATION_GAP: [
        "检查 SpeechRequest / 关键阶段是否落盘到日志",
        "检查抽链脚本是否覆盖当前日志格式",
    ],
    ISSUE_UNKNOWN: [
        "对照完整 RequestTraceChain.stages 与 errors",
        "检查 chain_type 与 final_execution_mode 是否冲突",
    ],
}


def _checkpoints_for(issue_type: str) -> List[str]:
    return list(CHECKPOINTS.get(issue_type, CHECKPOINTS[ISSUE_UNKNOWN]))


def _failed_stage_name(chain: RequestTraceChain) -> Optional[str]:
    for s in chain.stages:
        if s.status in ("fail",) or (s.stage_name == "provider_execution" and s.key_fields.get("provider_chain_ok") is False):
            return s.stage_name
    if chain.errors:
        return chain.errors[0].stage_name
    return None


def _playback_failure(chain: RequestTraceChain) -> bool:
    for e in chain.errors:
        if e.stage_name == "playback_result":
            return True
        et = (e.error_type or "").lower()
        if "playback" in et:
            return True
    for s in chain.stages:
        if s.stage_name == "playback_result" and s.status == "fail":
            return True
    return False


def _execution_succeeded_audio_chain(chain: RequestTraceChain) -> bool:
    """provider 侧已合成成功（用于区分 playback 失败）。"""
    for s in chain.stages:
        if s.stage_name == "provider_execution" and s.status == "ok":
            return True
    return chain.final_execution_mode == "provider_chain" and not any(
        s.stage_name == "provider_execution" and s.status == "fail" for s in chain.stages
    )


def _summary_text(
    request_id: str,
    issue_type: str,
    final_status: str,
    final_mode: Optional[str],
    short_reason: str,
) -> str:
    fm = final_mode or "unknown"
    templates = {
        ISSUE_NONE: f"[{request_id}] status={final_status}; mode={fm}; no chain-level issue.",
        ISSUE_PROVIDER_UNAVAILABLE: f"[{request_id}] status={final_status}; mode={fm}; primary provider failed; fallback delivered output. {short_reason}",
        ISSUE_PROVIDER_CHAIN_FAILURE: f"[{request_id}] status={final_status}; mode={fm}; provider chain failed; legacy rollback path. {short_reason}",
        ISSUE_REQUEST_SUPPRESSED: f"[{request_id}] status={final_status}; request suppressed before provider execution. {short_reason}",
        ISSUE_PLAYBACK_FAILURE: f"[{request_id}] status={final_status}; mode={fm}; audio produced but playback/delivery did not complete. {short_reason}",
        ISSUE_OUTPUT_DELIVERY_FAILURE: f"[{request_id}] status={final_status}; mode={fm}; no valid output path completed. {short_reason}",
        ISSUE_OBSERVATION_GAP: f"[{request_id}] status={final_status}; observation coverage gap; triage logging. {short_reason}",
        ISSUE_UNKNOWN: f"[{request_id}] status={final_status}; mode={fm}; issue not classified. {short_reason}",
    }
    return templates.get(issue_type, templates[ISSUE_UNKNOWN])


def analyze_request_trace_issue(
    chain: RequestTraceChain,
) -> Tuple[RequestTraceIssue, RequestTraceDiagnosticSummary]:
    sm = build_request_trace_summary(chain)
    fm = chain.final_execution_mode
    ct = chain.chain_type
    rid = chain.request_id
    failed_st = _failed_stage_name(chain)

    # 默认
    issue_type = ISSUE_UNKNOWN
    reason = "Unclassified chain outcome; inspect stages and errors."
    final_status = "unknown"
    severity = SEVERITY_INFO
    sec_type: Optional[str] = None
    sec_reason: Optional[str] = None

    # 1) 抑制
    if chain.status == "suppressed" or ct == "suppressed_chain":
        issue_type = ISSUE_REQUEST_SUPPRESSED
        reason = "Request blocked by routing, gate, cooldown, or dedup before provider execution."
        final_status = "suppressed"
        severity = SEVERITY_WARNING
    # 2) 播放失败（链上显式）
    elif _playback_failure(chain):
        issue_type = ISSUE_PLAYBACK_FAILURE
        reason = "Output was expected but playback or final delivery did not complete."
        final_status = "failed"
        severity = SEVERITY_CRITICAL
    # 3) failed_no_output：区分「纯交付失败」与「可判定为 playback」
    elif fm == "failed_no_output" and chain.status == "failed":
        if _execution_succeeded_audio_chain(chain):
            issue_type = ISSUE_PLAYBACK_FAILURE
            reason = "Provider chain reported success but final mode is failed_no_output; treat as delivery/playback path failure."
            final_status = "failed"
            severity = SEVERITY_CRITICAL
        else:
            issue_type = ISSUE_OUTPUT_DELIVERY_FAILURE
            reason = "No valid audio path completed; provider chain or legacy did not yield output."
            final_status = "failed"
            severity = SEVERITY_CRITICAL
    # 4) rollback 成功
    elif ct == "legacy_rollback_chain" and fm == "legacy_fallback" and chain.status == "ok":
        issue_type = ISSUE_PROVIDER_CHAIN_FAILURE
        reason = "All providers in configured chain failed; system rolled back to legacy and completed."
        final_status = "rollback_success"
        severity = SEVERITY_WARNING
        if sm.has_fallback:
            sec_type = "fallback_exhausted_or_invalid"
            sec_reason = "Fallback observation present; verify fallback output_valid and subsequent rollback trigger."
    # 5) fallback 成功（降级成功）
    elif ct == "provider_fallback_chain" and fm == "provider_chain" and chain.status == "ok":
        issue_type = ISSUE_PROVIDER_UNAVAILABLE
        reason = "Primary provider failed; fallback provider produced valid output."
        final_status = "degraded_success"
        severity = SEVERITY_DEGRADED
    # 6) 纯成功
    elif ct == "success_chain" and fm == "provider_chain" and chain.status == "ok":
        issue_type = ISSUE_NONE
        reason = "No issue detected on chain-level view."
        final_status = "success"
        severity = SEVERITY_INFO
    # 7) failed_chain 其他
    elif ct == "failed_chain":
        issue_type = ISSUE_OUTPUT_DELIVERY_FAILURE
        reason = "Chain marked failed; see errors and final_execution_mode."
        final_status = "failed"
        severity = SEVERITY_ERROR
    # 8) 观测缺口（大量 not_connected / missing，且非成功链）
    else:
        missing_like = sum(
            1
            for s in chain.stages
            if s.status in ("missing", "not_connected") and s.stage_name != "message_preparation"
        )
        prep_nc = any(s.stage_name == "message_preparation" and s.status == "not_connected" for s in chain.stages)
        if missing_like > 1 or (prep_nc and ct == "unknown"):
            issue_type = ISSUE_OBSERVATION_GAP
            reason = "Multiple stages missing or not connected; logging coverage insufficient for full diagnosis."
            final_status = "unknown"
            severity = SEVERITY_WARNING
        elif ct == "provider_fallback_chain":
            issue_type = ISSUE_PROVIDER_UNAVAILABLE
            reason = "Primary provider failed; fallback path used (verify final mode matches expectations)."
            final_status = "degraded_success" if chain.status == "ok" else "unknown"
            severity = SEVERITY_DEGRADED
        elif ct == "legacy_rollback_chain":
            issue_type = ISSUE_PROVIDER_CHAIN_FAILURE
            reason = "Rollback path; verify legacy outcome from final_execution_mode and status."
            final_status = "rollback_success" if fm == "legacy_fallback" and chain.status == "ok" else "failed"
            severity = SEVERITY_WARNING if final_status == "rollback_success" else SEVERITY_ERROR

    notes: List[str] = []
    if chain.notes:
        notes.extend(chain.notes)

    issue = RequestTraceIssue(
        request_id=rid,
        trace_id=chain.trace_id,
        chain_type=ct,
        provider_name=chain.provider_name,
        final_execution_mode=fm,
        final_status=final_status,
        primary_issue_type=issue_type,
        primary_issue_reason=reason,
        secondary_issue_type=sec_type,
        secondary_issue_reason=sec_reason,
        failed_stage=failed_st,
        severity=severity,
        has_fallback=sm.has_fallback,
        has_rollback=sm.has_rollback,
        recommended_checkpoints=_checkpoints_for(issue_type),
        notes=notes,
    )

    diag = RequestTraceDiagnosticSummary(
        request_id=rid,
        chain_type=ct,
        provider_name=chain.provider_name,
        final_execution_mode=fm,
        final_status=final_status,
        primary_issue_type=issue_type,
        primary_issue_reason=reason,
        failed_stage=failed_st,
        severity=severity,
        summary_text=_summary_text(rid, issue_type, final_status, fm, reason[:120]),
        recommended_checkpoints=list(issue.recommended_checkpoints),
    )

    return issue, diag
