# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Execution Result v1 — pure schema / helper, no runtime side effects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from capabilities.midplatform.protocols.protocol_types_v1 import (
    ProtocolExecutionOutcome,
    ProtocolHealthStatus,
)

REQUIRED_RESULT_KEYS: tuple[str, ...] = (
    "protocol_id",
    "overall_result",
    "constitution_execution_result",
    "process_execution_result",
    "interface_execution_result",
    "assimilation_health_result",
    "whitebox_binding_result",
    "errors",
    "warnings",
    "next_action",
)


@dataclass
class ProtocolError:
    error_code: str
    error_class: str
    severity: str
    detected_by: str
    phase_id: str
    artifact_ref: str
    field_path: str
    expected: Any
    actual: Any
    whitebox_trace_ref: str = ""
    diagnostic_node_ref: str = ""
    recommended_action: str = "block_and_quarantine"
    notification_required: bool = True
    owner_operator_notification_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_code": self.error_code,
            "error_class": self.error_class,
            "severity": self.severity,
            "detected_by": self.detected_by,
            "phase_id": self.phase_id,
            "artifact_ref": self.artifact_ref,
            "field_path": self.field_path,
            "expected": self.expected,
            "actual": self.actual,
            "whitebox_trace_ref": self.whitebox_trace_ref,
            "diagnostic_node_ref": self.diagnostic_node_ref,
            "recommended_action": self.recommended_action,
            "notification_required": self.notification_required,
            "owner_operator_notification_required": self.owner_operator_notification_required,
        }


@dataclass
class ProtocolExecutionResult:
    protocol_id: str
    overall_result: str = ProtocolExecutionOutcome.PASS.value
    constitution_execution_result: str = ProtocolExecutionOutcome.PASS.value
    process_execution_result: str = ProtocolExecutionOutcome.PASS.value
    interface_execution_result: str = ProtocolExecutionOutcome.PASS.value
    assimilation_health_result: str = ProtocolHealthStatus.HEALTHY.value
    whitebox_binding_result: str = ProtocolExecutionOutcome.PASS.value
    errors: List[ProtocolError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    next_action: str = "READY_FOR_NEXT_PHASE"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "protocol_execution_result": {
                "protocol_id": self.protocol_id,
                "overall_result": self.overall_result,
                "constitution_execution_result": self.constitution_execution_result,
                "process_execution_result": self.process_execution_result,
                "interface_execution_result": self.interface_execution_result,
                "assimilation_health_result": self.assimilation_health_result,
                "whitebox_binding_result": self.whitebox_binding_result,
                "errors": [e.to_dict() for e in self.errors],
                "warnings": list(self.warnings),
                "next_action": self.next_action,
            }
        }


def build_protocol_execution_result(
    protocol_id: str,
    *,
    overall_result: str = ProtocolExecutionOutcome.PASS.value,
    constitution_execution_result: str = ProtocolExecutionOutcome.PASS.value,
    process_execution_result: str = ProtocolExecutionOutcome.PASS.value,
    interface_execution_result: str = ProtocolExecutionOutcome.PASS.value,
    assimilation_health_result: str = ProtocolHealthStatus.HEALTHY.value,
    whitebox_binding_result: str = ProtocolExecutionOutcome.PASS.value,
    errors: Optional[List[ProtocolError]] = None,
    warnings: Optional[List[str]] = None,
    next_action: str = "READY_FOR_NEXT_PHASE",
) -> ProtocolExecutionResult:
    return ProtocolExecutionResult(
        protocol_id=protocol_id,
        overall_result=overall_result,
        constitution_execution_result=constitution_execution_result,
        process_execution_result=process_execution_result,
        interface_execution_result=interface_execution_result,
        assimilation_health_result=assimilation_health_result,
        whitebox_binding_result=whitebox_binding_result,
        errors=errors or [],
        warnings=warnings or [],
        next_action=next_action,
    )


def validate_protocol_execution_result(result: Dict[str, Any]) -> bool:
    inner = result.get("protocol_execution_result")
    if not isinstance(inner, dict):
        return False
    return all(key in inner for key in REQUIRED_RESULT_KEYS)
