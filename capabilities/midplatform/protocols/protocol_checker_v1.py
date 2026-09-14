# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Checker v1 — pure checker flow, no runtime side effects."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.protocols.protocol_execution_result_v1 import (
    ProtocolError,
    ProtocolExecutionResult,
    build_protocol_execution_result,
)
from capabilities.midplatform.protocols.protocol_types_v1 import (
    ProtocolExecutionOutcome,
    ProtocolHealthStatus,
)


def check_constitution_execution(
    *,
    protocol_id: str,
    violations: Optional[List[str]] = None,
) -> ProtocolExecutionResult:
    errors: List[ProtocolError] = []
    for idx, violation in enumerate(violations or [], start=1):
        errors.append(
            ProtocolError(
                error_code=f"{protocol_id}::CONST-{idx:03d}",
                error_class="constitutional_violation",
                severity="blocker",
                detected_by="checker",
                phase_id="",
                artifact_ref="",
                field_path=violation,
                expected=True,
                actual=False,
            )
        )
    outcome = ProtocolExecutionOutcome.PASS.value if not errors else ProtocolExecutionOutcome.FAIL.value
    return build_protocol_execution_result(
        protocol_id,
        constitution_execution_result=outcome,
        overall_result=outcome,
        errors=errors,
        next_action="BLOCK" if errors else "READY_FOR_NEXT_PHASE",
    )


def check_process_execution(
    *,
    protocol_id: str,
    artifacts_complete: bool = True,
    upstream_go: bool = True,
    evidence_chain_complete: bool = True,
) -> str:
    if artifacts_complete and upstream_go and evidence_chain_complete:
        return ProtocolExecutionOutcome.PASS.value
    return ProtocolExecutionOutcome.FAIL.value


def check_interface_execution(
    *,
    protocol_id: str,
    schema_valid: bool = True,
    naming_valid: bool = True,
) -> str:
    if schema_valid and naming_valid:
        return ProtocolExecutionOutcome.PASS.value
    return ProtocolExecutionOutcome.FAIL.value


def check_assimilation_health(
    *,
    protocol_id: str,
    drift_detected: bool = False,
    semantic_drift: bool = False,
) -> str:
    if drift_detected or semantic_drift:
        return ProtocolHealthStatus.DRIFT_DETECTED.value
    return ProtocolHealthStatus.HEALTHY.value


def check_whitebox_binding(
    *,
    protocol_id: str,
    trace_ref: str = "",
    diagnostic_ref: str = "",
) -> str:
    if trace_ref and diagnostic_ref:
        return ProtocolExecutionOutcome.PASS.value
    return ProtocolExecutionOutcome.FAIL.value


def run_protocol_checker_flow(
    *,
    protocol_id: str,
    constitution_violations: Optional[List[str]] = None,
    artifacts_complete: bool = True,
    upstream_go: bool = True,
    evidence_chain_complete: bool = True,
    schema_valid: bool = True,
    naming_valid: bool = True,
    drift_detected: bool = False,
    whitebox_trace_ref: str = "",
    whitebox_diagnostic_ref: str = "",
) -> Dict[str, Any]:
    const_result = check_constitution_execution(
        protocol_id=protocol_id,
        violations=constitution_violations,
    )
    process = check_process_execution(
        protocol_id=protocol_id,
        artifacts_complete=artifacts_complete,
        upstream_go=upstream_go,
        evidence_chain_complete=evidence_chain_complete,
    )
    interface = check_interface_execution(
        protocol_id=protocol_id,
        schema_valid=schema_valid,
        naming_valid=naming_valid,
    )
    assimilation = check_assimilation_health(
        protocol_id=protocol_id,
        drift_detected=drift_detected,
    )
    whitebox = check_whitebox_binding(
        protocol_id=protocol_id,
        trace_ref=whitebox_trace_ref,
        diagnostic_ref=whitebox_diagnostic_ref,
    )
    overall = ProtocolExecutionOutcome.PASS.value
    if any(
        v == ProtocolExecutionOutcome.FAIL.value
        for v in (const_result.constitution_execution_result, process, interface, whitebox)
    ):
        overall = ProtocolExecutionOutcome.FAIL.value
    if assimilation != ProtocolHealthStatus.HEALTHY.value:
        overall = ProtocolExecutionOutcome.FAIL.value
    return build_protocol_execution_result(
        protocol_id,
        overall_result=overall,
        constitution_execution_result=const_result.constitution_execution_result,
        process_execution_result=process,
        interface_execution_result=interface,
        assimilation_health_result=assimilation,
        whitebox_binding_result=whitebox,
        errors=const_result.errors,
    ).to_dict()
