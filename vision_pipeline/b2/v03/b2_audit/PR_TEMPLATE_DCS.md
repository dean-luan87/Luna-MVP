# B2 v0.5 PR 设计一致性检查清单

## 📋 必填项

### 1. Gate 合规性（25 分）

- [ ] **Gate 在本次改动中的角色**
  - 是否影响 `stability_score` 计算？
  - 是否修改 Gate 阈值？
  - 是否新增 Gate 条件？

- [ ] **Gate 状态写入 trace**
  - 确认所有 trace 都包含 `gate_eval` 字段
  - 确认 `gate_eval.mode` 合法（SUSPENDED / READ_ONLY / ACTIVE）

**人工评分**: ___ / 25

---

### 2. Evidence 生命周期（15 分）

- [ ] **Evidence 生命周期完整性**
  - 能否回答："这条 evidence 什么时候会消失？"
  - 是否实现了 DEGRADED / DROPPED 逻辑？

**人工评分**: ___ / 15

---

### 3. Trigger 正当性（15 分）

- [ ] **Trigger 正当性说明**
  - 能否用一句话说明："如果 C 什么都不做，会发生什么？"
  - 是否实现了 Trigger 冷却机制？

**人工评分**: ___ / 15

---

### 4. Impact & 干预边界（20 分）

- [ ] **Impact 类型明确性**
  - 这是**建议**还是**唯一允许的安全干预**？
  - 是否使用了标准 Impact 枚举？
  - ENV 因子是否直接产生 impact？（禁止）

- [ ] **FORCE_ALERT 使用**
  - 是否满足置信度阈值（≥ 0.75）？
  - 是否明确说明为什么不能等 C 自己确认？

**人工评分**: ___ / 20

---

### 5. Trace & 可追溯性（15 分）

- [ ] **Trace 完整性**
  - 能否通过 trace 回答："为什么这一秒 B 没说话？"
  - NO_OP 是否包含 `reason` 字段？

**人工评分**: ___ / 15

---

### 6. Timeline 克制性（10 分）

- [ ] **Timeline 克制性**
  - Timeline 上的每一条，是否都会改变人的行为判断？
  - 是否避免了 NO_OP 写入 timeline？
  - 是否避免了高频重复同类事件？

**人工评分**: ___ / 10

---

## 🎯 DCS 评分

### 自动化评分结果
```bash
# 运行 DCS 评分
python vision_pipeline/b2/v03/b2_audit/dcs_runner.py \
    traces/b2_runtime_trace_v05.jsonl \
    timeline.jsonl
```

### 人工评分汇总
- Gate: ___ / 25
- Evidence: ___ / 15
- Trigger: ___ / 15
- Impact: ___ / 20
- Trace: ___ / 15
- Timeline: ___ / 10

**总分**: ___ / 100

### 评分等级
- ✅ **PASS** (≥ 85 分): 可以合并
- ⚠️  **FAIL** (70-84 分): 需要修复
- ❌ **ROLLBACK** (< 70 分): 强制回滚

---

## 📝 改动说明

### 本次改动内容
（简要说明本次 PR 的主要改动）

### 设计哲学对齐
（说明本次改动如何符合 B2 v0.5 的设计哲学）

### 潜在风险
（说明本次改动可能带来的风险）

---

## ✅ 检查清单

- [ ] 自动化验收通过（`audit_runner.py`）
- [ ] DCS 评分 ≥ 85 分
- [ ] 无致命违规（G.FAIL.001）
- [ ] Trace 文件已更新
- [ ] 文档已更新（如有必要）

---

## 💡 重要提示

> **B2 的任何改动，如果不能通过 Audit 和 DCS，一律视为"引入了不可控行为"。**
