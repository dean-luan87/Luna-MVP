# -*- coding: utf-8 -*-
"""
单条语音请求白盒抽链结果（结构化，供脚本导出与后续后台展示）。

无业务逻辑，仅数据模型与序列化。
字段语义见 docs/architecture/voice/LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TraceStageRecord:
    """流程上的一段观测快照。"""

    stage_name: str
    status: str  # ok | missing | partial | skipped | reserved | not_connected | fail
    timestamp: Optional[float] = None
    key_fields: Dict[str, Any] = field(default_factory=dict)
    source_observation_type: str = ""
    source_ref: str = ""  # 如 file:line 或 inline

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage_name": self.stage_name,
            "status": self.status,
            "timestamp": self.timestamp,
            "key_fields": dict(self.key_fields),
            "source_observation_type": self.source_observation_type,
            "source_ref": self.source_ref,
        }


@dataclass
class TraceErrorRecord:
    """错误节点（阶段化，不是裸字符串）。"""

    stage_name: str
    error_type: str
    error_reason: str
    severity: str = "info"  # info | warning | error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage_name": self.stage_name,
            "error_type": self.error_type,
            "error_reason": self.error_reason,
            "severity": self.severity,
        }


@dataclass
class RequestTraceChain:
    """单条 request 的完整抽链结果。"""

    request_id: str
    trace_id: Optional[str] = None
    session_id: Optional[str] = None
    task_context_id: Optional[str] = None
    chain_type: str = "unknown"  # success_chain | provider_fallback_chain | legacy_rollback_chain | failed_chain | suppressed_chain | unknown
    final_execution_mode: Optional[str] = None
    provider_name: Optional[str] = None
    started_at: Optional[float] = None
    ended_at: Optional[float] = None
    status: str = "partial"  # ok | partial | failed | suppressed
    stages: List[TraceStageRecord] = field(default_factory=list)
    errors: List[TraceErrorRecord] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    raw_observation_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "session_id": self.session_id,
            "task_context_id": self.task_context_id,
            "chain_type": self.chain_type,
            "final_execution_mode": self.final_execution_mode,
            "provider_name": self.provider_name,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "status": self.status,
            "stages": [s.to_dict() for s in self.stages],
            "errors": [e.to_dict() for e in self.errors],
            "notes": list(self.notes),
            "raw_observation_refs": list(self.raw_observation_refs),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> RequestTraceChain:
        """从抽链脚本导出的 JSON 反序列化（仅结构化字段，不做校验）。"""
        stages_in = d.get("stages") or []
        stages: List[TraceStageRecord] = []
        for s in stages_in if isinstance(stages_in, list) else []:
            if not isinstance(s, dict):
                continue
            stages.append(
                TraceStageRecord(
                    stage_name=str(s.get("stage_name", "")),
                    status=str(s.get("status", "")),
                    timestamp=s.get("timestamp") if isinstance(s.get("timestamp"), (int, float)) else None,
                    key_fields=dict(s.get("key_fields") or {}) if isinstance(s.get("key_fields"), dict) else {},
                    source_observation_type=str(s.get("source_observation_type", "")),
                    source_ref=str(s.get("source_ref", "")),
                )
            )
        errs_in = d.get("errors") or []
        errors: List[TraceErrorRecord] = []
        for e in errs_in if isinstance(errs_in, list) else []:
            if not isinstance(e, dict):
                continue
            errors.append(
                TraceErrorRecord(
                    stage_name=str(e.get("stage_name", "")),
                    error_type=str(e.get("error_type", "")),
                    error_reason=str(e.get("error_reason", "")),
                    severity=str(e.get("severity", "info")),
                )
            )
        return cls(
            request_id=str(d.get("request_id", "")),
            trace_id=d.get("trace_id"),
            session_id=d.get("session_id"),
            task_context_id=d.get("task_context_id"),
            chain_type=str(d.get("chain_type", "unknown")),
            final_execution_mode=d.get("final_execution_mode"),
            provider_name=d.get("provider_name"),
            started_at=float(d["started_at"]) if isinstance(d.get("started_at"), (int, float)) else None,
            ended_at=float(d["ended_at"]) if isinstance(d.get("ended_at"), (int, float)) else None,
            status=str(d.get("status", "partial")),
            stages=stages,
            errors=errors,
            notes=list(d.get("notes") or []) if isinstance(d.get("notes"), list) else [],
            raw_observation_refs=list(d.get("raw_observation_refs") or [])
            if isinstance(d.get("raw_observation_refs"), list)
            else [],
        )
