# Gate Authority Table (B2 v0.4.2)

**Purpose:** Gate is the ONLY authority that can stop / downgrade B2 runtime.  
**It does NOT change factor logic; it only decides whether B2 is allowed to speak / write / message C.**

---

## Authority Matrix

| Gate Mode   | B2 Perception Ingest | Evidence Update | World/Memory Write | Timeline Write | B→C Message | Notes |
|------------|-----------------------|-----------------|--------------------|----------------|------------|------|
| SUSPENDED  | Optional (cheap only) | NO              | NO                 | NO             | NO         | Hard stop. Return None. Must record gate_eval trace if trace enabled. |
| READ_ONLY  | YES                   | YES (local)     | YES (optional, low-cost) | NO        | NO         | "Only read / accumulate." No outward behavior influence. |
| ACTIVE     | YES                   | YES             | YES                | YES (only non-NO_OP already enforced) | YES | Full pipeline. Must include gate_eval in trace. |

---

## Block Reasons (examples)

- `camera_shake` / `unstable_pose` / `bad_fov` / `too_close` / `too_far` / `insufficient_evidence` / `cooldown`

---

## Non-negotiables

1. **Gate=SUSPENDED => tick() MUST return None (SILENT).**
2. **Gate=READ_ONLY => tick() MUST NOT send message to C, MUST NOT write timeline.**
3. **Gate decision must be written into runtime trace (gate_eval) for every tick.**

---

**版本：** v0.4.2  
**状态：** ✅ FROZEN  
**最后更新：** 2025-01-12
