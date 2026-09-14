# =====================================================
# mvp_system_part2.py
# Autonomy Heartbeat + ASR Reporting + Demo main
# =====================================================

import time
import json
from enum import Enum, auto
from dataclasses import dataclass, asdict
from typing import List
from collections import deque

# ======= imports from part1 (if split files) =======
from mvp_system_part1 import (
    AbstractDecision, IntentType, DecisionMode,
    SystemRuntimeState, PerceptionState, CalibrationState, SystemMode,
    adapt_to_gate, RuntimeGate, execute
)

# =====================================================
# Autonomy Heartbeat Monitor (minimal)
# =====================================================

@dataclass
class RuntimeSignal:
    tick: int
    last_active_ms: int

class AutonomyHeartbeatMonitor:
    def check(self, signal: RuntimeSignal) -> List[str]:
        now_ms = int(time.time() * 1000)
        issues = []
        if now_ms - signal.last_active_ms > 2000:
            issues.append("B-PROC-HB-001")  # no response
        return issues

# =====================================================
# B Autonomy Core (minimal)
# =====================================================

class B_InternalProcessState(Enum):
    OK = auto()
    DEGRADED = auto()
    FAILED = auto()

class B_OutputQualityState(Enum):
    OK = auto()
    SUSPICIOUS = auto()
    INVALID = auto()

class B_CollaborationState(Enum):
    COLLAB_OK = auto()
    COLLAB_DEGRADED = auto()
    COLLAB_SUSPENDED = auto()

class B_OverallState(Enum):
    HEALTHY = auto()
    DEGRADED = auto()
    SUSPENDED = auto()
    UNAVAILABLE = auto()

@dataclass
class B_Issue:
    code: str  # e.g. B-PROC-HB-001
    level: str  # WARNING / ERROR / CRITICAL

class B_AutonomyAggregator:
    def __init__(self):
        self.proc = B_InternalProcessState.OK
        self.out = B_OutputQualityState.OK
        self.collab = B_CollaborationState.COLLAB_OK

    def update_by_issues(self, issues: List[B_Issue]):
        self.proc = B_InternalProcessState.OK
        self.out = B_OutputQualityState.OK
        self.collab = B_CollaborationState.COLLAB_OK

        for issue in issues:
            if issue.code.startswith("B-PROC"):
                if issue.level == "CRITICAL":
                    self.proc = B_InternalProcessState.FAILED
                else:
                    self.proc = B_InternalProcessState.DEGRADED

            if issue.code.startswith("B-OUT"):
                self.out = B_OutputQualityState.INVALID

            if issue.code.startswith("B-COLLAB"):
                self.collab = B_CollaborationState.COLLAB_SUSPENDED

    def overall_state(self) -> B_OverallState:
        if self.proc == B_InternalProcessState.FAILED:
            return B_OverallState.SUSPENDED
        if self.out == B_OutputQualityState.INVALID:
            return B_OverallState.SUSPENDED
        if self.collab == B_CollaborationState.COLLAB_SUSPENDED:
            return B_OverallState.SUSPENDED
        if self.proc == B_InternalProcessState.DEGRADED:
            return B_OverallState.DEGRADED
        return B_OverallState.HEALTHY

class B_Runtime:
    def __init__(self):
        self.tick = 0
        self.last_active_ms = int(time.time() * 1000)

    def step(self):
        self.tick += 1
        self.last_active_ms = int(time.time() * 1000)

    def signal(self) -> RuntimeSignal:
        return RuntimeSignal(
            tick=self.tick,
            last_active_ms=self.last_active_ms
        )

# =====================================================
# B Execution Collaboration Tracker (minimal)
# =====================================================

@dataclass
class ExecEvent:
    ts_ms: int
    status: str
    gate: str

class B_ExecCollabTracker:
    def __init__(self, window_ms=10000):
        self.window_ms = window_ms
        self.events = deque()

    def add_receipt(self, receipt):
        self.events.append(ExecEvent(
            ts_ms=int(time.time() * 1000),
            status=receipt.status.name,
            gate=receipt.gate_result.name
        ))
        self._gc()

    def _gc(self):
        now = int(time.time() * 1000)
        while self.events and now - self.events[0].ts_ms > self.window_ms:
            self.events.popleft()

    def summary(self):
        cnt = {"EXECUTED": 0, "FAILED": 0, "TIMEOUT": 0, "SKIPPED": 0, "BLOCK": 0}
        for e in self.events:
            if e.status in cnt:
                cnt[e.status] += 1
            if e.gate == "BLOCK":
                cnt["BLOCK"] += 1
        return cnt

def issues_from_receipt_summary(summary):
    issues = []

    if summary["FAILED"] > 0:
        issues.append(("B-COLLAB-EXEC-FAILED", "ERROR"))
    if summary["TIMEOUT"] > 0:
        issues.append(("B-COLLAB-EXEC-TIMEOUT", "ERROR"))

    if summary["SKIPPED"] >= 3:
        issues.append(("B-COLLAB-EXEC-SKIPPED", "WARNING"))

    if summary["BLOCK"] >= 3:
        issues.append(("B-COLLAB-GATE-BLOCKED", "WARNING"))

    return issues

def maybe_recover_collab(summary, b_issues):
    if summary["EXECUTED"] >= 3 and summary["FAILED"] == 0 and summary["TIMEOUT"] == 0:
        b_issues[:] = [i for i in b_issues if not i.code.startswith("B-COLLAB")]

def build_collab_window_stats(tracker):
    summary = tracker.summary()
    return {
        "executed": summary.get("EXECUTED", 0),
        "failed": summary.get("FAILED", 0),
        "timeout": summary.get("TIMEOUT", 0),
        "skipped": summary.get("SKIPPED", 0),
        "gate_blocked": summary.get("BLOCK", 0),
        "window_ms": tracker.window_ms
    }

# =====================================================
# System Snapshot Builder
# =====================================================

def build_system_snapshot(system_state, b_snapshot: dict) -> dict:
    if b_snapshot["collab_health"] == "SUSPENDED":
        system_health = "RED"
        recommended = "ENTER_FAIL_SAFE"
    elif b_snapshot["collab_health"] == "DEGRADED":
        system_health = "YELLOW"
        recommended = "DEGRADE"
    else:
        system_health = "GREEN"
        recommended = "CONTINUE"

    return {
        "system_mode": system_state.mode.name,
        "perception_state": system_state.perception.name,
        "calibration_state": system_state.calibration.name,
        "reference_id": system_state.reference_id,
        "calibration_version": system_state.calibration_version,
        "modules": {
            "B": b_snapshot
        },
        "system_health": system_health,
        "recommended_action": recommended,
        "ts": int(time.time() * 1000)
    }

# =====================================================
# Policy Layer: Auto Fail-Safe Controller
# =====================================================

class PolicyState(Enum):
    NORMAL = auto()
    PENDING_FAIL_SAFE = auto()
    FAIL_SAFE_ACTIVE = auto()

class AutoFailSafePolicy:
    def __init__(self, yellow_threshold=3):
        self.state = PolicyState.NORMAL
        self.yellow_count = 0
        self.yellow_threshold = yellow_threshold

    def evaluate(self, system_snapshot: dict):
        health = system_snapshot["system_health"]

        if health == "RED":
            self.state = PolicyState.FAIL_SAFE_ACTIVE
            return "ENTER_FAIL_SAFE"

        if health == "YELLOW":
            self.yellow_count += 1
            if self.yellow_count >= self.yellow_threshold:
                self.state = PolicyState.FAIL_SAFE_ACTIVE
                return "ENTER_FAIL_SAFE"
            self.state = PolicyState.PENDING_FAIL_SAFE
            return "WAIT"

        self.yellow_count = 0
        self.state = PolicyState.NORMAL
        return "CONTINUE"

def apply_system_mode(system_state, action: str):
    if action == "ENTER_FAIL_SAFE":
        system_state.mode = SystemMode.FAIL_SAFE

def report_policy_decision(system_snapshot, action):
    report_snapshot({
        "module": "POLICY",
        "system_health": system_snapshot["system_health"],
        "recommended_action": system_snapshot["recommended_action"],
        "policy_action": action,
        "ts": int(time.time() * 1000)
    })

# =====================================================
# Decision Capability Limiter (driven by B autonomy)
# =====================================================

class DecisionCapability(Enum):
    FULL = auto()        # 原始能力
    LIMITED = auto()     # 降级能力
    MINIMAL = auto()     # 最小能力（几乎不作为）

def capability_from_b_state(b_state) -> DecisionCapability:
    if b_state.name == "HEALTHY":
        return DecisionCapability.FULL
    if b_state.name == "DEGRADED":
        return DecisionCapability.LIMITED
    if b_state.name in ["SUSPENDED", "UNAVAILABLE"]:
        return DecisionCapability.MINIMAL
    return DecisionCapability.MINIMAL

def apply_b_capability(decision: AbstractDecision,
                       capability: DecisionCapability) -> AbstractDecision:
    if capability == DecisionCapability.FULL:
        return decision

    if capability == DecisionCapability.LIMITED:
        if decision.intent == IntentType.ACTION:
            return AbstractDecision(
                decision_id=decision.decision_id,
                intent=IntentType.WARNING,
                decision_mode=decision.decision_mode,
                reference_id=decision.reference_id,
                calibration_version=decision.calibration_version
            )
        return decision

    if capability == DecisionCapability.MINIMAL:
        return AbstractDecision(
            decision_id=decision.decision_id,
            intent=IntentType.NONE,
            decision_mode=DecisionMode.FAIL_SAFE,
            reference_id=decision.reference_id,
            calibration_version=decision.calibration_version
        )

    return decision

# =====================================================
# ASR (Snapshot / Issue / Receipt Reporting)
# =====================================================

def _append_json(path: str, obj: dict):
    with open(path, "a") as f:
        f.write(json.dumps(obj, default=str) + "\n")

def report_snapshot(snapshot: dict, path="snapshot.log"):
    _append_json(path, snapshot)

def report_issue(issue: dict, path="issue.log"):
    _append_json(path, issue)

def report_receipt(receipt, path="receipt.log"):
    _append_json(path, asdict(receipt))

# =====================================================
# Demo Main (MVP Run)
# =====================================================

if __name__ == "__main__":
    # --- system runtime state ---
    system_state = SystemRuntimeState(
        perception=PerceptionState.STABLE,
        calibration=CalibrationState.CALIBRATED,
        mode=SystemMode.RUNTIME_STABLE,
        reference_id=1,
        calibration_version=1
    )

    # --- abstract decision ---
    decision = AbstractDecision(
        decision_id=1,
        intent=IntentType.NOTIFY,
        decision_mode=DecisionMode.RUNTIME,
        reference_id=1,
        calibration_version=1
    )

    # --- B autonomy (minimal integration) ---
    b_runtime = B_Runtime()
    b_aggregator = B_AutonomyAggregator()
    ahm = AutonomyHeartbeatMonitor()
    b_exec_tracker = B_ExecCollabTracker(window_ms=10000)
    policy = AutoFailSafePolicy(yellow_threshold=3)

    b_runtime.step()
    hb_issues = ahm.check(b_runtime.signal())
    b_issues: List[B_Issue] = []

    for code in hb_issues:
        b_issues.append(B_Issue(code=code, level="CRITICAL"))

    b_aggregator.update_by_issues(b_issues)
    b_state = b_aggregator.overall_state()

    # --- B -> Decision influence (insert before D2RG) ---
    capability = capability_from_b_state(b_state)
    decision = apply_b_capability(decision, capability)

    # --- D2RG ---
    gate_candidate = adapt_to_gate(decision)

    # --- runtime gate ---
    gate = RuntimeGate()
    gate_result = gate.validate(gate_candidate, system_state)

    # --- execution ---
    receipt = execute(decision, gate_result)
    report_receipt(receipt)

    # --- B <- ExecutionReceipt integration ---
    b_exec_tracker.add_receipt(receipt)
    summary = b_exec_tracker.summary()
    new_issues = issues_from_receipt_summary(summary)

    for code, level in new_issues:
        b_issues.append(B_Issue(code=code, level=level))

    maybe_recover_collab(summary, b_issues)

    b_aggregator.update_by_issues(b_issues)
    b_state = b_aggregator.overall_state()

    for code, level in new_issues:
        report_issue({
            "issue_code": code,
            "level": level,
            "window": summary,
            "ts": int(time.time() * 1000)
        })

    if b_state in [B_OverallState.SUSPENDED, B_OverallState.UNAVAILABLE]:
        report_issue({
            "issue_code": "B-AUTO-SUSPENDED",
            "state": b_state.name,
            "ts": int(time.time() * 1000)
        })

    collab_stats = build_collab_window_stats(b_exec_tracker)
    collab_health = (
        "OK" if b_aggregator.collab.name == "COLLAB_OK" else
        "DEGRADED" if b_aggregator.collab.name == "COLLAB_DEGRADED" else
        "SUSPENDED"
    )
    report_snapshot({
        "module": "B",
        "proc": b_aggregator.proc.name,
        "out": b_aggregator.out.name,
        "collab": b_aggregator.collab.name,
        "overall": b_state.name,
        "collab_health": collab_health,
        "collab_window_stats": collab_stats,
        "ts": int(time.time() * 1000)
    })

    system_snapshot = build_system_snapshot(
        system_state=system_state,
        b_snapshot={
            "overall": b_state.name,
            "collab_health": collab_health,
            "collab_window_stats": collab_stats
        }
    )
    report_snapshot({
        "module": "SYSTEM",
        **system_snapshot
    })

    policy_action = policy.evaluate(system_snapshot)
    report_policy_decision(system_snapshot, policy_action)
    apply_system_mode(system_state, policy_action)

    # --- snapshot (decision/execution) ---
    report_snapshot({
        "decision_id": decision.decision_id,
        "gate_result": gate_result.name,
        "execution_status": receipt.status.name,
        "ts": int(time.time() * 1000)
    })

    print("MVP run completed.")
