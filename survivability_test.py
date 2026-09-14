import time
from enum import Enum, auto

# =====================
# Enums
# =====================

class GateResult(Enum):
    ALLOW = auto()
    BLOCK = auto()

class ExecStatus(Enum):
    EXECUTED = auto()
    NOT_ATTEMPTED = auto()
    FAILED = auto()

class SystemMode(Enum):
    RUNTIME = auto()
    FAIL_SAFE = auto()

class Health(Enum):
    GREEN = auto()
    YELLOW = auto()
    RED = auto()

# =====================
# Mock Runtime Gate
# =====================

def runtime_gate(perception_ok, calibrated):
    if not perception_ok:
        return GateResult.BLOCK
    if not calibrated:
        return GateResult.BLOCK
    return GateResult.ALLOW

# =====================
# Mock Execution
# =====================

def execute(gate, force_fail=False):
    if gate != GateResult.ALLOW:
        return ExecStatus.NOT_ATTEMPTED
    if force_fail:
        return ExecStatus.FAILED
    return ExecStatus.EXECUTED

# =====================
# B Collaboration Tracker
# =====================

class BTracker:
    def __init__(self):
        self.fail = 0
        self.ok = 0

    def update(self, status):
        if status == ExecStatus.FAILED:
            self.fail += 1
        if status == ExecStatus.EXECUTED:
            self.ok += 1

    def health(self):
        if self.fail >= 2:
            return Health.RED
        if self.fail == 1:
            return Health.YELLOW
        return Health.GREEN

# =====================
# Auto Fail-Safe Policy
# =====================

class Policy:
    def __init__(self):
        self.yellow = 0

    def decide(self, health):
        if health == Health.RED:
            return True
        if health == Health.YELLOW:
            self.yellow += 1
            if self.yellow >= 2:
                return True
        else:
            self.yellow = 0
        return False

# =====================
# Assertion Helper
# =====================

def check(cond, msg):
    if not cond:
        raise AssertionError(msg)

# =====================
# Test Cases
# =====================

def T1_perception_unstable():
    g = runtime_gate(False, True)
    s = execute(g)
    check(s == ExecStatus.NOT_ATTEMPTED,
          "T1 failed: executed under unstable perception")

def T2_no_calibration():
    g = runtime_gate(True, False)
    s = execute(g)
    check(s == ExecStatus.NOT_ATTEMPTED,
          "T2 failed: executed without calibration")

def T3_exec_fail_triggers_failsafe():
    t = BTracker()
    p = Policy()
    mode = SystemMode.RUNTIME

    for _ in range(3):
        g = runtime_gate(True, True)
        s = execute(g, force_fail=True)
        t.update(s)
        if p.decide(t.health()):
            mode = SystemMode.FAIL_SAFE
            break

    check(mode == SystemMode.FAIL_SAFE,
          "T3 failed: FAIL_SAFE not triggered")

def T4_gate_block_not_failsafe():
    t = BTracker()
    p = Policy()
    mode = SystemMode.RUNTIME

    for _ in range(5):
        g = runtime_gate(False, True)
        s = execute(g)
        t.update(s)
        if p.decide(t.health()):
            mode = SystemMode.FAIL_SAFE

    check(mode == SystemMode.RUNTIME,
          "T4 failed: false FAIL_SAFE on gate block")

def T5_recovery_path():
    t = BTracker()
    p = Policy()
    mode = SystemMode.RUNTIME

    # enter fail-safe
    for _ in range(2):
        s = execute(runtime_gate(True, True), force_fail=True)
        t.update(s)

    if p.decide(t.health()):
        mode = SystemMode.FAIL_SAFE

    check(mode == SystemMode.FAIL_SAFE,
          "T5 failed: did not enter FAIL_SAFE")

    # recovery evidence
    t.fail = 0
    for _ in range(3):
        t.update(execute(runtime_gate(True, True)))

    check(t.health() == Health.GREEN,
          "T5 failed: recovery not GREEN")

# =====================
# Run All
# =====================

if __name__ == "__main__":
    print("Running Phase-1 Survivability Tests")

    T1_perception_unstable()
    print("✓ T1 perception unstable")

    T2_no_calibration()
    print("✓ T2 calibration missing")

    T3_exec_fail_triggers_failsafe()
    print("✓ T3 execution failure → FAIL_SAFE")

    T4_gate_block_not_failsafe()
    print("✓ T4 gate block safe")

    T5_recovery_path()
    print("✓ T5 recovery path")

    print("ALL TESTS PASSED")
