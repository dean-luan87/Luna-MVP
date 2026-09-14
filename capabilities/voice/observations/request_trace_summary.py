# -*- coding: utf-8 -*-
"""
单条 RequestTraceChain 的查询层摘要（快速浏览，不必展开完整链）。

查询层可对 chain_type / status 做最小规范化，不回写主链。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from capabilities.voice.observations.request_trace_chain import RequestTraceChain


def normalize_chain_type_for_query(raw: str) -> str:
    """与抽链器 chain_type 对齐的查询层短名。"""
    m = {
        "success_chain": "success",
        "provider_fallback_chain": "provider_fallback",
        "legacy_rollback_chain": "legacy_rollback",
        "failed_chain": "failed_chain",
        "suppressed_chain": "suppressed_chain",
        "unknown": "unknown",
    }
    return m.get(raw, raw)


def normalize_status_for_query(chain: RequestTraceChain, chain_type_n: str) -> str:
    """查询用 status：success / degraded_success / failed / suppressed / unknown。"""
    st = chain.status
    if st == "suppressed":
        return "suppressed"
    if st == "failed":
        return "failed"
    if st == "ok":
        if chain_type_n == "provider_fallback":
            return "degraded_success"
        return "success"
    if st == "partial":
        return "unknown"
    return "unknown"


def _infer_has_fallback(chain: RequestTraceChain, chain_type_n: str) -> bool:
    if chain_type_n == "provider_fallback":
        return True
    for s in chain.stages:
        if s.source_observation_type == "ProviderFallbackObservation":
            return True
        kf = s.key_fields or {}
        if "fallback_provider" in kf:
            return True
    return False


def _infer_has_rollback(chain: RequestTraceChain, chain_type_n: str) -> bool:
    if chain_type_n == "legacy_rollback":
        return True
    for s in chain.stages:
        if s.source_observation_type == "TTSRollbackObservation":
            return True
    return False


def _primary_failure(chain: RequestTraceChain) -> tuple[str, str]:
    if chain.errors:
        e = chain.errors[0]
        return e.error_type, e.error_reason
    for s in chain.stages:
        if s.status == "fail" and s.key_fields:
            ft = s.key_fields.get("failure_type")
            if ft is not None:
                return str(ft), str(s.key_fields.get("note") or "")
    return "", ""


def build_request_trace_summary(chain: RequestTraceChain) -> RequestTraceSummary:
    ct_raw = chain.chain_type
    ct_n = normalize_chain_type_for_query(ct_raw)
    st_n = normalize_status_for_query(chain, ct_n)
    pet, per = _primary_failure(chain)
    started = chain.started_at
    ended = chain.ended_at
    duration_ms: Optional[float] = None
    if started is not None and ended is not None:
        duration_ms = max(0.0, (ended - started) * 1000.0)

    return RequestTraceSummary(
        request_id=chain.request_id,
        trace_id=chain.trace_id,
        chain_type_raw=ct_raw,
        chain_type=ct_n,
        provider_name=chain.provider_name,
        final_execution_mode=chain.final_execution_mode,
        status_raw=chain.status,
        status=st_n,
        started_at=started,
        ended_at=ended,
        duration_ms=duration_ms,
        primary_error_type=pet or None,
        primary_error_reason=per or None,
        stage_count=len(chain.stages),
        has_fallback=_infer_has_fallback(chain, ct_n),
        has_rollback=_infer_has_rollback(chain, ct_n),
        notes=list(chain.notes),
        failure_type=pet or None,
    )


@dataclass
class RequestTraceSummary:
    request_id: str
    trace_id: Optional[str] = None
    chain_type_raw: str = ""
    chain_type: str = ""  # 规范化：success | provider_fallback | legacy_rollback | failed_chain | suppressed_chain | unknown
    provider_name: Optional[str] = None
    final_execution_mode: Optional[str] = None
    status_raw: str = ""
    status: str = ""  # success | degraded_success | failed | suppressed | unknown
    started_at: Optional[float] = None
    ended_at: Optional[float] = None
    duration_ms: Optional[float] = None
    primary_error_type: Optional[str] = None
    primary_error_reason: Optional[str] = None
    stage_count: int = 0
    has_fallback: bool = False
    has_rollback: bool = False
    notes: List[str] = field(default_factory=list)
    failure_type: Optional[str] = None  # 与 primary_error_type 对齐，便于按 failure_type 过滤

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "chain_type_raw": self.chain_type_raw,
            "chain_type": self.chain_type,
            "provider_name": self.provider_name,
            "final_execution_mode": self.final_execution_mode,
            "status_raw": self.status_raw,
            "status": self.status,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_ms": self.duration_ms,
            "primary_error_type": self.primary_error_type,
            "primary_error_reason": self.primary_error_reason,
            "stage_count": self.stage_count,
            "has_fallback": self.has_fallback,
            "has_rollback": self.has_rollback,
            "notes": list(self.notes),
            "failure_type": self.failure_type,
        }
