# Cursor Guard: Gate Authority Table

**用途：** Cursor 只读 Guard 文档  
**状态：** FROZEN（架构护栏）

---

## 🎯 Gate 的唯一职责

> **Gate 决定 B 是否有资格在当前时刻发声，以及只能以什么姿态发声**
> 
> **Gate 不判断世界，不确认风险，不替 C 做决定。**

---

## 一句话架构裁定

```
Gate decides whether B may speak, and how.
B suggests possible risks.
C verifies and decides action.
```

**中文版：**
```
Gate 决定能不能说、怎么说；
B 负责提醒；
C 负责确认与行动。
```

---

## 🔒 Gate 权限总表（快速参考）

### ✅ Gate 可以裁决

1. **运行级裁决**
   - B 是否运行（ACTIVE / READ_ONLY / SUSPENDED）
   - perception 是否执行
   - aggregation 是否执行

2. **输出级裁决**
   - 是否允许向 C 输出
   - 是否允许写 timeline
   - 是否允许写 memory
   - 是否允许生成 decision

3. **行为姿态裁决**
   - intervention_level（HARD / SOFT）
   - 是否允许 HARD 干预
   - 是否强制降级为 SOFT
   - advisory_only（强制为 True）

4. **时间 / 预测裁决**
   - 是否允许未来风险措辞（"可能会发生"）
   - 是否允许跨时间断言（必须加不确定性）

5. **证据生命周期裁决**
   - evidence 是否可进入 CONFIRMED
   - 是否强制停留在 OBSERVING
   - 是否降级为 DEGRADED
   - 是否允许参与决策

6. **Trace & 审计强制裁决**
   - 是否必须写 trace（强制：每一帧）
   - trace 中必须字段（gate_mode / blocked_by / reason）

---

### ❌ Gate 明确禁止裁决

1. ❌ 判断风险是否真实
2. ❌ 确认"前方一定有坑"
3. ❌ 修改 impact 语义
4. ❌ 替 C 做最终决策
5. ❌ 引入学习 / 自适应（v0.5+ 才允许）

---

## 📋 Cursor 检查清单

### 修改 Gate 相关代码时

- [ ] Gate 评估是否在 tick() 最前面？
- [ ] Gate=SUSPENDED 是否直接返回 None？
- [ ] Gate=READ_ONLY 是否不写 timeline？
- [ ] 每帧是否都写 gate trace？
- [ ] Gate 是否不判断风险是否真实？
- [ ] Gate 是否不修改 impact 语义？

### 实现 Gate 功能时

- [ ] 是否遵循 Gate 三权（生杀权、降权权、可视权）？
- [ ] 是否遵循最低 Trace 要求？
- [ ] 是否不越权裁决（不判断世界、不确认风险）？

---

## 🎯 硬规则

1. **Gate 可以降级干预，不能升级干预**
2. **Gate 阻断 ≠ impact = NO_OP**
3. **Gate 阻断 = 禁止表达判断**
4. **Gate 不生成证据，只裁决证据状态**

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ FROZEN（架构护栏）
