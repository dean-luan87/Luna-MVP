# B2 v0.4 → v0.4.1 Code Changes

**Target:** Make code impossible to violate the 7 boundary assumptions.

---

## ✅ Required Code Changes

### 1️⃣ B Never Confirms Risk, Only Signals It

**Location:** `vision_pipeline/b2/v03/b2_v03.py`
- Method: `_summarize_world_change()`
- Method: `_build_message_to_c()`

**Mandatory Rules:**
```python
# ❌ FORBIDDEN: Any "confirmed / verified / must" semantics
# ✅ REQUIRED: Only suggestion / potential / may affect

# Example - CORRECT:
impact = ActionImpact.NEED_SLOW_DOWN  # Suggestion
message = {
    "action": "NEED_SLOW_DOWN",
    "reason": "potential path surface change",
    "confidence": 0.65
}

# Example - WRONG:
impact = ActionImpact.CONFIRMED_RISK  # ❌ FORBIDDEN
message = {
    "action": "MUST_STOP",
    "verified": True  # ❌ FORBIDDEN
}
```

**Implementation:**
- Remove any `confirmed_risk`, `verified_danger`, `must_*` fields
- Impact enum only represents behavior impact type
- All messages must be deniable suggestions

**Files to Modify:**
- `vision_pipeline/b2/v03/b2_v03.py`
- `vision_pipeline/b2/v03/types.py` (if ActionImpact enum exists)

---

### 2️⃣ Single Intervention Class (Hard-Coded, Non-Extensible)

**Location:** `vision_pipeline/b2/v03/types.py`
- Enum: `ActionImpact`

**Required Structure:**
```python
class ActionImpact(Enum):
    NO_OP = auto()
    NEED_SLOW_DOWN = auto()
    PATH_UNCERTAIN = auto()
    NEED_DETOUR = auto()
    NEED_STOP = auto()  # ← Only intervention case allowed
    # NO MORE VALUES ALLOWED
```

**Forbidden:**
- ❌ Adding `NEED_*_IMMEDIATE`
- ❌ Adding `FORCE_*` categories
- ❌ Adding any new intervention-level actions

**Implementation:**
- Add comment: `# HARD BOUNDARY: Only NEED_STOP is intervention-level`
- Add validation in `_build_message_to_c()` to reject any new intervention actions

**Files to Modify:**
- `vision_pipeline/b2/v03/types.py`
- `vision_pipeline/b2/v03/b2_v03.py` (validation)

---

### 3️⃣ B's NO_OP Must Be Completely Silent

**Location:** `vision_pipeline/b2/v03/b2_v03.py`
- Method: `tick()`

**Required Change:**
```python
def tick(self, frame, frame_ts: float):
    # ... gate evaluation ...
    # ... perception ...
    # ... impact calculation ...
    
    impact = summary.get("impact", ActionImpact.NO_OP)
    
    # ✅ REQUIRED: NO_OP must not write to timeline
    if impact == ActionImpact.NO_OP:
        # Still write trace for audit, but NO timeline
        self._write_trace(trace_data)
        return None  # ← No timeline entry
    
    # Only non-NO_OP impacts write to timeline
    self._write_timeline(summary)
    return summary
```

**Rationale:**
- Prevents B from "showing presence"
- Prevents violating Assumption 5 (Silence Requires No Immediate Explanation)

**Files to Modify:**
- `vision_pipeline/b2/v03/b2_v03.py`

---

### 4️⃣ Time Consistency Validation (Prevent Future Accidents)

**Location:** 
- B side: `vision_pipeline/b2/v03/b2_v03.py` → `_build_message_to_c()`
- C side: `c1_controller/c1_controller.py` (message handler)

**Required Changes:**

**B Side:**
```python
def _build_message_to_c(self, summary):
    message = {
        "header": {
            "msg_id": generate_uuid(),
            "ts": time.time(),  # ← System time
            "frame_id": self.current_frame_id,
            "source": "B2",
            "version": "v0.4.1"
        },
        "action": summary["impact"],
        # ... rest of message ...
    }
    return message
```

**C Side:**
```python
MAX_TIME_DRIFT = 0.1  # 100ms

def handle_message_from_b(self, message):
    system_now = time.time()
    msg_ts = message["header"]["ts"]
    
    # ✅ REQUIRED: Validate time consistency
    drift = abs(msg_ts - system_now)
    if drift > MAX_TIME_DRIFT:
        logger.warning(f"Time drift detected: {drift}s")
        # Still process, but log warning
    
    # Process message...
```

**Files to Modify:**
- `vision_pipeline/b2/v03/b2_v03.py`
- `c1_controller/c1_controller.py`

---

### 5️⃣ B Must Not Decide When to Run

**Location:** `vision_pipeline/b2/v03/b2_v03.py`
- Any method that might control B's execution

**Forbidden:**
```python
# ❌ FORBIDDEN: Auto-wake logic in B
def _should_wake_up(self):
    if self.has_important_evidence():
        return True  # ❌ B cannot decide this

# ❌ FORBIDDEN: Self-trigger based on "nothing to do"
def tick(self, frame, frame_ts):
    if not self.has_work():
        self.stop()  # ❌ B cannot stop itself
```

**Allowed:**
```python
# ✅ ALLOWED: External system scheduling
# ✅ ALLOWED: Gate controls ACTIVE / READ_ONLY / SUSPENDED
def tick(self, frame, frame_ts):
    gate_mode = self.gate_evaluator.evaluate(...)
    if gate_mode == "SUSPENDED":
        return None  # ← Gate controls, not B itself
```

**Files to Check:**
- `vision_pipeline/b2/v03/b2_v03.py`
- `vision_pipeline/b2/v03/runtime_state_machine.py`

---

## 🚫 Explicitly Forbidden Changes

If anyone proposes these, reject immediately:

### 1. ❌ Let B "Confirm Danger"
```python
# ❌ FORBIDDEN
if risk_level == "CONFIRMED":
    send_force_stop()
```

### 2. ❌ Let B Force C on Non-Safety Issues
```python
# ❌ FORBIDDEN
if comfort_issue:
    force_c_to_slow_down()  # Only safety can force
```

### 3. ❌ Let C Request "More Certain Judgment" from B
```python
# ❌ FORBIDDEN
c_message = {
    "request": "please_confirm_risk",
    "need_certainty": True
}
```

### 4. ❌ Let B Output Frequently Because "No Change"
```python
# ❌ FORBIDDEN
if no_change_detected:
    send_heartbeat()  # B should be silent
```

---

## 📋 Implementation Checklist

- [ ] Remove all "confirmed/verified/must" semantics from B output
- [ ] Hard-code ActionImpact enum (no new intervention actions)
- [ ] Ensure NO_OP never writes to timeline
- [ ] Add system time to B→C messages
- [ ] Add time drift validation in C
- [ ] Remove any auto-wake/self-trigger logic from B
- [ ] Add comments referencing `bc_boundary_assumptions_v1.md`
- [ ] Update DCS rules to check these invariants

---

## 🔍 Code Review Checklist

When reviewing PRs, check:
- [ ] No new intervention-level actions added
- [ ] NO_OP does not write to timeline
- [ ] B messages use system time
- [ ] No "confirmed/verified" language in B output
- [ ] No auto-wake logic in B
- [ ] All changes reference `bc_boundary_assumptions_v1.md`

---

## 📝 Testing Requirements

Add tests for:
- [ ] NO_OP does not create timeline entries
- [ ] Time drift validation works
- [ ] B cannot add new intervention actions
- [ ] B messages are always suggestions (not commands)

---

**Version:** v0.4.1  
**Based On:** `bc_boundary_assumptions_v1.md`  
**Last Updated:** 2025-01-12
