# B2 v0.4.1 行为回归测试说明

## 📋 测试目标

这个脚本只验证 5 件事：

1. **Gate 是否生效**
   - 稳定 → ACTIVE
   - 不稳定 → READ_ONLY / SUSPENDED

2. **NO_OP 是否真正沉默**
   - NO_OP 不写 timeline
   - NO_OP 但写 trace（标明沉默原因）

3. **impact 是否正确产出**
   - 正确的 impact 枚举值
   - 正确的 intervention_level

4. **B 是否只"提醒"，不"确认风险"**
   - `advisory_only = True`
   - 无确认性语义

5. **trace 是否完整、可读、可追溯**
   - 所有必要字段存在
   - 时间、角色、规则路径清晰

---

## ⚠️ 不涉及

- ❌ OCR / 多镜头 / 学习 / Web
- ❌ C 的真实执行，只看 B → C 的 message

---

## 🚀 运行方式

```bash
cd /Users/luanlei/Desktop/Luna-2
python tests/test_b2_v041_gate_behavior.py
```

---

## 📊 测试场景

### Case A: 稳定 + 路况变化
- **输入：** PATH factor (0.7), 稳定 (0.8), 距离 5m
- **预期：** NEED_SLOW_DOWN, Gate ACTIVE

### Case B: 镜头晃动 → Gate 阻止
- **输入：** PATH factor (0.8), 不稳定 (0.3), 距离 5m
- **预期：** Gate SUSPENDED, B 沉默

### Case C: 远距离高风险事件
- **输入：** EVENT factor (0.9), 稳定 (0.8), 距离 6m
- **预期：** NEED_STOP, Gate ACTIVE

### Case D: 近距离事件 → B 不应发声
- **输入：** EVENT factor (0.9), 稳定 (0.8), 距离 2m
- **预期：** B 沉默（距离边界）

### Case E: 环境变化（ENV）→ 不应该输出
- **输入：** ENV factor (0.9), 稳定 (0.8), 距离 5m
- **预期：** B 沉默（ENV 不触发决策）

### Case F: 人流变化
- **输入：** PEOPLE factor (0.8), 稳定 (0.8), 距离 5m
- **预期：** NEED_SLOW_DOWN, Gate ACTIVE

### Case G: Gate READ_ONLY → 应该只读
- **输入：** PATH factor (0.7), 稳定 (0.8), 证据帧数不足
- **预期：** Gate READ_ONLY

---

## ✅ 验收标准

### 正确行为示例

**CASE A**
```
Gate: ACTIVE
Impact: NEED_SLOW_DOWN
Decision: CONDITION_CHANGE
Advisory Only: True ✅
```

**CASE B**
```
Gate: SUSPENDED | 镜头晃动过大
B Output: SILENT (Gate SUSPENDED) ✅
```

**CASE D**
```
Gate: ACTIVE
B Output: SILENT (NO_OP) ✅
```

---

## ❌ 架构错误判定

如果出现以下任一情况 → ❌ 架构错误：

- B 在 2m 内输出 NEED_STOP
- ENV 触发 CONDITION_CHANGE
- Gate=SUSPENDED 但仍输出 decision
- impact=NO_OP 但写 timeline
- 缺少 `advisory_only = True`
- impact 包含确认性语义（CONFIRMED_*, FORCE_*, CERTAIN_*）
- NEED_STOP 但 intervention_level != HARD
- 非 NEED_STOP 但 intervention_level = HARD

---

## 🎯 这个脚本的意义

**它不是 demo，它是架构断言。**

以后每次改 B / Gate / Impact，都必须先跑它。

---

## 📝 输出解读

### 重点看这几行输出：

1. **Gate Mode** - 是否正确（ACTIVE / READ_ONLY / SUSPENDED）
2. **Impact** - 是否正确（NEED_STOP / NEED_SLOW_DOWN / NO_OP 等）
3. **Advisory Only** - 是否 = True
4. **Intervention Level** - 是否正确（NEED_STOP = HARD，其他 = SOFT）
5. **违规提示** - 是否有 ❌ 违规标记

---

## 🔧 调试建议

如果测试失败：

1. **检查 Gate 配置**
   - 查看 `vision_pipeline/b2/v03/gate/gate_config.yaml`
   - 确认阈值设置

2. **检查 B2 逻辑**
   - 查看 `_summarize_world_change` 方法
   - 确认 impact 计算逻辑

3. **检查 v0.4.1 补丁**
   - 确认 `advisory_only = True`
   - 确认 `intervention_level` 逻辑
   - 确认 assert 检查

---

**版本：** v0.4.1  
**最后更新：** 2025-01-12
