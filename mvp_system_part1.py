# =====================================================
# mvp_system_part1.py
# Core Runtime: Decision -> D2RG -> RuntimeGate -> Execution
# =====================================================

import time
from enum import Enum, auto
from dataclasses import dataclass

# =========================
# Enums
# =========================

class IntentType(Enum):
    NONE = auto()
    NOTIFY = auto()
    WARNING = auto()
    ACTION = auto()

class DecisionMode(Enum):
    RUNTIME = auto()
    SHADOW = auto()
    FAIL_SAFE = auto()

class GateResult(Enum):
    ALLOW = auto()
    BLOCK = auto()
    FAIL_SAFE = auto()

class ExecutionStatus(Enum):
    NOT_ATTEMPTED = auto()
    EXECUTED = auto()
    FAILED = auto()
    TIMEOUT = auto()
    SKIPPED = auto()

class PerceptionState(Enum):
    STABLE = auto()
    UNSTABLE = auto()

class CalibrationState(Enum):
    CALIBRATED = auto()
    UNCALIBRATED = auto()

class SystemMode(Enum):
    BOOT = auto()
    SHADOW = auto()
    RUNTIME_STABLE = auto()
    FAIL_SAFE = auto()

# =========================
# Abstract Decision
# =========================

@dataclass
class AbstractDecision:
    decision_id: int
    intent: IntentType
    decision_mode: DecisionMode
    reference_id: int
    calibration_version: int

# =========================
# D2RG Adapter
# =========================

@dataclass
class GateCandidate:
    reference_id: int
    calibration_version: int
    policy: GateResult

def adapt_to_gate(decision: AbstractDecision) -> GateCandidate:
    if decision.decision_mode == DecisionMode.SHADOW:
        return GateCandidate(decision.reference_id, decision.calibration_version, GateResult.BLOCK)
    if decision.decision_mode == DecisionMode.FAIL_SAFE:
        return GateCandidate(decision.reference_id, decision.calibration_version, GateResult.FAIL_SAFE)
    if decision.intent == IntentType.NONE:
        return GateCandidate(decision.reference_id, decision.calibration_version, GateResult.BLOCK)
    return GateCandidate(decision.reference_id, decision.calibration_version, GateResult.ALLOW)

# =========================
# Runtime Gate (BCP-RG)
# =========================

@dataclass
class SystemRuntimeState:
    perception: PerceptionState
    calibration: CalibrationState
    mode: SystemMode
    reference_id: int
    calibration_version: int

class RuntimeGate:
    def validate(self, cand: GateCandidate, state: SystemRuntimeState) -> GateResult:
        if state.mode != SystemMode.RUNTIME_STABLE:
            return GateResult.BLOCK
        if state.perception != PerceptionState.STABLE:
            return GateResult.BLOCK
        if state.calibration != CalibrationState.CALIBRATED:
            return GateResult.BLOCK
        if cand.reference_id != state.reference_id:
            return GateResult.BLOCK
        if cand.calibration_version != state.calibration_version:
            return GateResult.BLOCK
        return cand.policy

# =========================
# Execution Receipt
# =========================

@dataclass
class ExecutionReceipt:
    receipt_id: int
    decision_id: int
    reference_id: int
    calibration_version: int
    gate_result: GateResult
    status: ExecutionStatus
    latency_ms: int

# =========================
# Execution Chain (MVP)
# =========================

def execute(decision: AbstractDecision, gate_result: GateResult) -> ExecutionReceipt:
    start_ms = int(time.time() * 1000)

    if gate_result != GateResult.ALLOW:
        return ExecutionReceipt(
            receipt_id=start_ms,
            decision_id=decision.decision_id,
            reference_id=decision.reference_id,
            calibration_version=decision.calibration_version,
            gate_result=gate_result,
            status=ExecutionStatus.NOT_ATTEMPTED,
            latency_ms=0
        )

    # MVP: assume execution success
    time.sleep(0.01)
    end_ms = int(time.time() * 1000)

    return ExecutionReceipt(
        receipt_id=end_ms,
        decision_id=decision.decision_id,
        reference_id=decision.reference_id,
        calibration_version=decision.calibration_version,
        gate_result=gate_result,
        status=ExecutionStatus.EXECUTED,
        latency_ms=end_ms - start_ms
    )
