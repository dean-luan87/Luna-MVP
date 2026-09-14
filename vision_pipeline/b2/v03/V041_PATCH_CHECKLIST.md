# B2 v0.4.1 Patch - Cursor 可执行 Checklist

**目标：** 任何实现只要有一条不满足，就不允许合并

**格式：** 逐条对勾制（⬜ 未检查 / ✅ 通过 / ❌ 失败）

---

## ✅ P0｜语义与边界（必须全部满足）

### ⬜ 1. B2 输出必须显式声明"只提醒"

**检查点：**
- summary 中必须存在字段：`"advisory_only": true`

**拒绝条件：**
- ❌ 缺失该字段
- ❌ 或值不为 `true`

**验证方法：**
```python
assert "advisory_only" in summary
assert summary["advisory_only"] is True
```

**代码位置：**
- `b2_v03.py` → `_summarize_world_change()` 返回值
- `b2_v03.py` → `_build_message_to_c()` payload

---

### ⬜ 2. B2 不允许输出"确认性语义"

**检查点：**
- ActionImpact 中只能存在：
  - NO_OP
  - NEED_SLOW_DOWN
  - PATH_UNCERTAIN
  - NEED_DETOUR
  - NEED_STOP

**拒绝条件：**
- ❌ 出现以下任一语义（即使未使用）：
  - CONFIRMED_*
  - FORCE_*
  - CERTAIN_*
  - WORLD_*

**验证方法：**
```python
allowed_impacts = {"NO_OP", "NEED_SLOW_DOWN", "PATH_UNCERTAIN", "NEED_DETOUR", "NEED_STOP"}
for impact in ActionImpact:
    assert impact.name in allowed_impacts
    assert not impact.name.startswith("CONFIRMED_")
    assert not impact.name.startswith("FORCE_")
    assert not impact.name.startswith("CERTAIN_")
    assert not impact.name.startswith("WORLD_")
```

**代码位置：**
- `b2_v03.py` → `ActionImpact` 枚举定义
- `b2_v03.py` → `_summarize_world_change()` assert 检查

---

### ⬜ 3. B2 唯一允许的"越权干预"= NEED_STOP

**检查点：**
```python
if impact == NEED_STOP:
    intervention_level == "HARD"
else:
    intervention_level == "SOFT"
```

**拒绝条件：**
- ❌ 存在第二种 HARD 干预
- ❌ 或 NEED_STOP 未标记为 HARD

**验证方法：**
```python
impact = summary.get("impact")
intervention_level = summary.get("intervention_level")

if impact == ActionImpact.NEED_STOP:
    assert intervention_level == "HARD"
else:
    assert intervention_level == "SOFT"
```

**代码位置：**
- `b2_v03.py` → `_summarize_world_change()` 中设置 `intervention_level`

---

## ✅ P1｜时间与尺度统一（硬约束）

### ⬜ 4. 系统时间唯一来源

**检查点：**
- 所有 summary / trace 只能包含：`"system_ts": <float>`

**拒绝条件：**
- ❌ 出现以下任一字段：
  - `frame_ts`
  - `perception_ts`
  - `camera_ts`

**验证方法：**
```python
forbidden_time_fields = {"frame_ts", "perception_ts", "camera_ts"}
assert "system_ts" in summary
for field in forbidden_time_fields:
    assert field not in summary
```

**代码位置：**
- `b2_v03.py` → `tick()` 开头
- `b2_v03.py` → `_summarize_world_change()` 返回值
- `b2_v03.py` → `_build_message_to_c()` payload header

---

### ⬜ 5. B / C 通信不携带时间偏移

**检查点：**
- B → C 消息中不得出现：
  - 相对时间
  - "未来 X 秒后一定发生"表述

**允许：**
- 风险窗口（模糊、非承诺）

**验证方法：**
```python
payload = to_c_message.get("payload", {})
payload_str = str(payload).lower()

# 禁止绝对时间承诺
forbidden_phrases = [
    "will happen in",
    "must occur",
    "guaranteed at",
    "certain to happen"
]
for phrase in forbidden_phrases:
    assert phrase not in payload_str
```

**代码位置：**
- `b2_v03.py` → `_build_message_to_c()` payload

---

## ✅ P2｜NO_OP 沉默机制（不可省略）

### ⬜ 6. NO_OP 不写 timeline

**检查点：**
```python
if impact == NO_OP:
    return None  # 或 timeline_written = False
```

**拒绝条件：**
- ❌ timeline 中出现 NO_OP 决策

**验证方法：**
```python
if impact == ActionImpact.NO_OP:
    assert not writeback.get("timeline_written", False)
```

**代码位置：**
- `b2_v03.py` → `tick()` 中 NO_OP 处理
- `b2_v03.py` → `_write_outputs()` 方法

---

### ⬜ 7. NO_OP 必须写 trace（但标明沉默原因）

**检查点：**
```python
"decision_state": "SILENT",
"silence_reason": "no_behavioral_impact"
```

**拒绝条件：**
- ❌ 沉默但无原因
- ❌ 或直接无 trace

**验证方法：**
```python
if impact == ActionImpact.NO_OP:
    assert "decision_state" in trace
    assert trace["decision_state"] == "SILENT"
    assert "silence_reason" in trace
    assert trace["silence_reason"]  # 非空
```

**代码位置：**
- `b2_v03.py` → `tick()` 中 NO_OP 处理

---

## ✅ P3｜Gate 只影响 B，不得触碰 C

### ⬜ 8. Gate 只能产生三态

**检查点：**
- ACTIVE
- READ_ONLY
- SUSPENDED

**拒绝条件：**
- ❌ Gate 直接输出 C 行为
- ❌ Gate 修改 C 参数

**验证方法：**
```python
allowed_gate_states = {"ACTIVE", "READ_ONLY", "SUSPENDED"}
gate_state = get_gate_state_from_mode(gate_mode.value)
assert gate_state.value.upper() in allowed_gate_states

# Gate 不得包含 C 相关字段
gate_output = trace.get("gate_eval", {})
forbidden_c_fields = {"c_action", "c_command", "c_parameter"}
for field in forbidden_c_fields:
    assert field not in str(gate_output)
```

**代码位置：**
- `gate_runtime.py` → `BGateState` 枚举
- `b2_v03.py` → `tick()` 中 Gate 处理

---

### ⬜ 9. READ_ONLY = 不产出新判断

**检查点：**
```python
if gate == READ_ONLY:
    # evidences 可以收集，但不产生新 impact
    # 或 evidences == {}（如果完全不处理）
```

**验证方法：**
```python
if gate_state == BGateState.READ_ONLY:
    # READ_ONLY 时，如果产生 impact，必须是 NO_OP
    if summary:
        assert summary.get("impact") == ActionImpact.NO_OP or summary.get("impact") is None
```

**代码位置：**
- `b2_v03.py` → `tick()` 中 READ_ONLY 处理

---

## ✅ P4｜DCS 守卫（只审判，不学习）

### ⬜ 10. DCS 不得反向影响决策

**检查点：**
- `dcs_guard` 只读 summary
- 输出只进入：`trace.dcs`

**拒绝条件：**
- ❌ DCS 改变 impact / level

**验证方法：**
```python
# DCS 检查前后，summary 不应改变
summary_before = copy.deepcopy(summary)
violations = dcs_check(summary)
summary_after = summary

assert summary_before == summary_after  # DCS 不修改 summary
assert "dcs" in trace  # DCS 结果只写入 trace
assert "impact" not in trace.get("dcs", {})  # DCS 不包含决策字段
```

**代码位置：**
- `dcs_guard.py` → `dcs_check()` 方法
- `b2_v03.py` → `tick()` 中 DCS 调用

---

### ⬜ 11. 违规必须可见

**检查点：**
```python
"dcs": {
  "violations": [...],
  "score_delta": <number>
}
```

**验证方法：**
```python
assert "dcs" in trace
dcs_data = trace["dcs"]
assert "violations" in dcs_data
assert "score_delta" in dcs_data
assert isinstance(dcs_data["violations"], list)
assert isinstance(dcs_data["score_delta"], (int, float))
```

**代码位置：**
- `b2_v03.py` → `tick()` 中 DCS 记录

---

## ✅ P5｜角色与责任声明（给未来用）

### ⬜ 12. B2 必须自报身份

**检查点：**
```python
"role": "B",
"expects_confirmation_from": "C"
```

**拒绝条件：**
- ❌ 角色缺失
- ❌ 或角色不明确

**验证方法：**
```python
assert "role" in summary
assert summary["role"] == "B"
assert "expects_confirmation_from" in summary
assert summary["expects_confirmation_from"] == "C"
```

**代码位置：**
- `b2_v03.py` → `_summarize_world_change()` 返回值

---

## ✅ 最终 Gate（Cursor 必须能回答）

### 6 个核心问题

1. **⬜ B 是否从未确认风险？**
   - 检查：`advisory_only == True` 且无确认性语言

2. **⬜ B 是否只在 NEED_STOP 时越权？**
   - 检查：只有 NEED_STOP 的 `intervention_level == "HARD"`

3. **⬜ 所有不说话是否可追溯？**
   - 检查：NO_OP 时 `decision_state == "SILENT"` 且有 `silence_reason`

4. **⬜ 时间是否唯一且统一？**
   - 检查：只有 `system_ts`，无其他时间字段

5. **⬜ Gate 是否不污染 C？**
   - 检查：Gate 只产生三态，不输出 C 行为

6. **⬜ DCS 是否只观察、不干预？**
   - 检查：DCS 不修改 summary，只写入 trace

**❌ 任一为否 → 不准合并**

---

## 📋 使用方式

### 对于 Cursor

1. 生成/修改 B2 代码后
2. 逐条检查此 checklist
3. 所有 ⬜ 必须变为 ✅
4. 任一 ❌ → 拒绝合并

### 对于 Code Review

1. PR 必须包含此 checklist 的完成状态
2. 所有 P0 项必须 ✅
3. 所有最终 Gate 问题必须回答"是"

---

**Version:** v0.4.1  
**Last Updated:** 2025-01-12
