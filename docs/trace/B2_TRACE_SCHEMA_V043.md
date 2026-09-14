# B2 Runtime Trace Schema v0.4.3 (Frozen)

**版本：** v0.4.3  
**状态：** FROZEN  
**用途：** Cursor/评审/后续 Web

---

## 1. Top-level

```json
{
  "schema_version": "b2.trace.v0.4.3",
  "time": {
    "t_video_s": 100.0,
    "t_str": "01:40.000",
    "frame_id": 3000,
    "fps": 30.0
  },
  "runtime": {
    "module": "B2",
    "version": "0.4.3",
    "state": "ACTIVE|READ_ONLY|SUSPENDED",
    "reason": ""
  },
  "gate": {
    "mode": "ACTIVE|READ_ONLY|SUSPENDED",
    "blocked_by": "...",
    "reason": "...",
    "stability_score": 0.85,
    "details": {}
  },
  "factors": {
    "scores": {},
    "reasons": {},
    "evidences_present": [],
    "main_factor": null
  },
  "impact": {
    "impact": "NO_OP|NEED_SLOW_DOWN|PATH_UNCERTAIN|NEED_DETOUR|NEED_STOP",
    "level": "NOTICE|CONDITION_CHANGE|INTERRUPT",
    "confidence": 0.0,
    "intervention_level": "SOFT|HARD",
    "advisory_only": true
  },
  "to_c": {
    "send": false,
    "msg": {},
    "suppressed_reason": ""
  },
  "writeback": {
    "timeline": false,
    "health": false,
    "memory": false,
    "evidence_pack": false,
    "paths": {}
  },
  "dcs": {
    "score": 0,
    "grade": "GREEN|YELLOW|RED",
    "violations": [],
    "notes": {}
  }
}
```

---

## 2. Invariants (hard)

1. **trace is written every frame**
   - 即使 NO_OP / Gate SUSPENDED 也写

2. **advisory_only must always be true for B output**
   - B 的所有输出必须是 advisory

3. **if gate.mode=="SUSPENDED" => to_c.send=false and summary must be None**
   - Gate=SUSPENDED 时，B 必须完全沉默

4. **if gate.mode=="READ_ONLY" => writeback.* must be false**
   - Gate=READ_ONLY 时，不允许任何写回

5. **impact==NO_OP => to_c.send=false and timeline must be false**
   - NO_OP 时，不发送消息，不写 timeline

---

**版本：** v0.4.3  
**最后更新：** 2025-01-12  
**状态：** ✅ FROZEN
