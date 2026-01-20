# B2 v0.4.2：tick() Guard 注释模板

**版本：** v0.4.2  
**状态：** FROZEN（代码内可直接贴用）  
**用途：** 作为 `tick()` 方法的架构护栏注释

---

## 📋 使用说明

将此模板直接粘贴到 `tick()` 方法中，作为实现对照和架构护栏。

---

## 🎯 tick() 方法 Guard 注释模板

```python
def tick(
    self,
    frame_ts: float,
    perception: Dict[str, Any],
    frame_id: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """
    B2 v0.4.2 Tick 主循环（Gate-first Runtime Pipeline）
    
    核心原则：
    先裁决"有没有资格看世界"，再谈"看到了什么"
    
    一句话架构裁定：
    Gate decides whether B may speak.
    B suggests possible future risks.
    C verifies reality and decides action.
    
    执行顺序（不可改变）：
    0. 系统时间锚点（ts_now）
    1. Gate 评估（最高优先级）
    2. Gate Mode 分流（SUSPENDED / READ_ONLY / ACTIVE）
    3. Perception（仅 ACTIVE / READ_ONLY）
    4. Evidence Lifecycle（抗视角污染）
    5. Impact 评估
    6. Intervention 裁决（Gate 参与）
    7. Output 分流
    8. Trace（无条件执行）
    
    详细顺序图：见 V042_TICK_SEQUENCE_DIAGRAM.md
    """
    
    # =========================
    # 0. 系统时间锚点（BC 唯一时间标尺）
    # =========================
    # 强约束：
    # - ts_now = 系统当前时间
    # - 禁止使用缓存时间 / 帧时间做裁决
    system_ts = time.time()
    trace = {}
    
    # =========================
    # 1. Gate 评估（最高优先级，必须先执行）
    # =========================
    # Gate 输入：
    # - view_state (stability_score, camera_motion, camera_pose, fov_state)
    # - range_state (min_distance, effective_range)
    # - evidence_state (连续性 / 冷却 / 稳定度)
    # 
    # Gate 输出（必须写 trace）：
    # {
    #   "gate_mode": "ACTIVE | READ_ONLY | SUSPENDED",
    #   "blocked_by": "...",
    #   "human_readable": "..."
    # }
    gate_mode_str, gate_trace = self.gate_evaluator_v05.evaluate(...)
    trace["gate_eval"] = {
        "mode": gate_mode_str,
        "blocked_by": gate_trace.get("blocked_by"),
        "human_readable": gate_trace.get("human_readable", "")
    }
    
    # =========================
    # 2. Gate Mode 分流（硬分支，不可合并）
    # =========================
    
    # ⛔ SUSPENDED: 当前视角不配看世界
    # - perception: ❌ 不执行
    # - aggregation: ❌ 不执行
    # - decision: ❌ 不生成
    # - output to C: ❌
    # - timeline: ❌
    # - trace: ✅（必须）
    # → return None
    if gate_mode_str == "SUSPENDED":
        trace["decision_state"] = "SUSPENDED"
        trace["to_c_message"] = {"sent": False, "reason": "gate_suspended"}
        trace["writeback"] = {
            "timeline_written": False,
            "health_log_written": False,
            "memory_written": False
        }
        if self.trace_writer:
            self.trace_writer.write(trace)
        return None
    
    # 👁 READ_ONLY: 可以看，但不许说
    # - perception: ✅（可执行）
    # - aggregation: ✅（仅内部）
    # - decision: ⚠️ 可生成
    # - output to C: ❌
    # - timeline: ❌
    # - memory: ⚠️（只读复用）
    # - trace: ✅
    is_read_only = (gate_mode_str == "READ_ONLY")
    
    # ▶️ ACTIVE: 进入完整 B2 流程
    # （继续执行）
    
    # =========================
    # 3. Perception（仅 ACTIVE / READ_ONLY）
    # =========================
    # 规则：
    # - 只产出 raw evidence
    # - 不允许语义判断
    # - 不允许 risk 结论
    evidences = build_factor_evidences(future_states)
    trace["perception"] = {"factors": factors_dict}
    
    # =========================
    # 4. Evidence Lifecycle（抗视角污染）
    # =========================
    # 状态机：OBSERVING → CONFIRMED → DEGRADED → DROPPED
    # Gate 可强制：
    # - 卡在 OBSERVING
    # - 从 CONFIRMED 降级
    evidence_states = {}
    for factor_key, evidence in evidences.items():
        evidence_state = self.evidence_lifecycle.update(...)
        evidence_states[factor_key.value] = evidence_state_dict
    trace["evidence_state"] = evidence_states
    
    # =========================
    # 5. Impact 评估（仅 ACTIVE / READ_ONLY）
    # =========================
    # 硬约束：
    # - 只回答一句话：「如果继续前进，可能会发生什么」
    # - 禁止确认性语义
    # 
    # 允许的 impact：
    # - NEED_SLOW_DOWN
    # - PATH_UNCERTAIN
    # - NEED_STOP
    # - NO_OP
    summary = self._summarize_world_change(evidences, ts=frame_ts)
    impact = summary.get("impact")
    trace["impact_evaluation"] = {"impact": impact.name if hasattr(impact, 'name') else impact}
    
    # =========================
    # 6. Intervention 裁决（Gate 参与）
    # =========================
    # 规则：
    # - Gate 可降级 HARD → SOFT
    # - Gate 不可升级
    # - advisory_only = True 永久为真
    intervention_level = summary.get("intervention_level", "SOFT")
    advisory_only = summary.get("advisory_only", True)
    trace["decision"] = {
        "intervention_level": intervention_level,
        "advisory_only": advisory_only
    }
    
    # =========================
    # 7. Output 分流（关键）
    # =========================
    
    # impact == NO_OP
    # - 不写 timeline
    # - 不发给 C
    # - 只写 trace
    if impact == ActionImpact.NO_OP:
        trace["decision_state"] = "SILENT"
        trace["silence_reason"] = summary.get("reason") or "no_behavioral_impact"
        trace["to_c_message"] = {"sent": False, "reason": "no_impact"}
        trace["writeback"] = {
            "timeline_written": False,
            "health_log_written": False,
            "memory_written": False
        }
        if self.trace_writer:
            self.trace_writer.write(trace)
        return None
    
    # Gate == READ_ONLY
    # - 不发给 C
    # - 不写 timeline
    # - trace + 内部日志
    if is_read_only:
        trace["to_c_message"] = {"sent": False, "reason": "gate_read_only"}
        trace["writeback"] = {
            "timeline_written": False,
            "health_log_written": False,
            "memory_written": False
        }
        if self.trace_writer:
            self.trace_writer.write(trace)
        return None
    
    # Gate == ACTIVE && impact ≠ NO_OP
    # - 发给 C（advisory）
    # - 写 timeline
    # - 写 health log
    # - 写 trace
    message_to_c = self._build_message_to_c(summary)
    trace["to_c_message"] = {
        "sent": True,
        "payload": message_to_c
    }
    
    # =========================
    # 8. Trace（无条件执行）
    # =========================
    # 每一帧必须有 trace
    # 最低字段：
    # {
    #   "time": ts_now,
    #   "gate_mode": "...",
    #   "impact": "...",
    #   "intervention_level": "...",
    #   "advisory_only": true,
    #   "human_interpretation": "..."
    # }
    trace["writeback"] = {
        "timeline_written": True,
        "health_log_written": True,
        "memory_written": True
    }
    if self.trace_writer:
        self.trace_writer.write(trace)
    
    return message_to_c
```

---

## ✅ 实现检查清单

### Gate 评估位置

- [ ] Gate 评估是否在 tick() 最前面？
- [ ] Gate 输入是否包含 view_state / range_state / evidence_state？
- [ ] Gate 输出是否写入 trace？

### Gate Mode 分流

- [ ] SUSPENDED 是否直接 return None？
- [ ] SUSPENDED 是否仍写 trace？
- [ ] READ_ONLY 是否不写 timeline？
- [ ] READ_ONLY 是否不发给 C？
- [ ] ACTIVE 是否进入完整流程？

### Perception & Evidence

- [ ] Perception 是否只产出 raw evidence？
- [ ] Evidence 状态机是否正确实现？
- [ ] Gate 是否可强制证据状态？

### Impact & Intervention

- [ ] Impact 是否只回答"如果继续前进，可能会发生什么"？
- [ ] 是否禁止确认性语义？
- [ ] Gate 是否可降级 HARD → SOFT？
- [ ] advisory_only 是否永久为 True？

### Output & Trace

- [ ] NO_OP 是否不写 timeline？
- [ ] READ_ONLY 是否不发给 C？
- [ ] 每帧是否都有 trace？
- [ ] Trace 是否包含最低字段？

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ FROZEN（代码内可直接贴用）
