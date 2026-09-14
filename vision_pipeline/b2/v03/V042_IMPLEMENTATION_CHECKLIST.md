# B2 v0.4.2：实现对照清单（逐文件点名）

**版本：** v0.4.2  
**状态：** 实现对照清单  
**用途：** 对照顺序图，逐文件检查 v0.4.2 实现完整性

---

## 📋 对照依据

- **顺序图：** `V042_TICK_SEQUENCE_DIAGRAM.md`
- **Guard 模板：** `V042_TICK_GUARD_TEMPLATE.md`
- **Gate Authority：** `gate/GATE_AUTHORITY_TABLE.md`

---

## 1️⃣ 核心文件：`b2_v03.py`

### 1.1 tick() 方法结构

#### ✅ 必须实现

- [ ] **0. 系统时间锚点**
  - 位置：`tick()` 方法开头
  - 检查点：`system_ts = time.time()`
  - 禁止：使用 `frame_ts` 或其他时间源

- [ ] **1. Gate 评估（最高优先级）**
  - 位置：`tick()` 方法开头，在 perception 之前
  - 检查点：`gate_mode_str, gate_trace = self.gate_evaluator_v05.evaluate(...)`
  - 输入：`view_state`, `range_state`, `evidence_state`
  - 输出：写入 `trace["gate_eval"]`

- [ ] **2. Gate Mode 分流**
  - 位置：Gate 评估后立即执行
  - 检查点：
    - `if gate_mode_str == "SUSPENDED": return None`
    - `is_read_only = (gate_mode_str == "READ_ONLY")`
  - 必须：SUSPENDED 直接返回，但仍写 trace

- [ ] **3. Perception（仅 ACTIVE / READ_ONLY）**
  - 位置：Gate 分流后
  - 检查点：`evidences = build_factor_evidences(future_states)`
  - 规则：只产出 raw evidence，不允许语义判断

- [ ] **4. Evidence Lifecycle**
  - 位置：Perception 后
  - 检查点：`self.evidence_lifecycle.update(...)`
  - 状态机：OBSERVING → CONFIRMED → DEGRADED → DROPPED

- [ ] **5. Impact 评估**
  - 位置：Evidence 更新后
  - 检查点：`summary = self._summarize_world_change(...)`
  - 硬约束：只回答"如果继续前进，可能会发生什么"

- [ ] **6. Intervention 裁决**
  - 位置：Impact 评估后
  - 检查点：`intervention_level`, `advisory_only`
  - 规则：Gate 可降级 HARD → SOFT，不可升级

- [ ] **7. Output 分流**
  - 位置：Intervention 裁决后
  - 检查点：
    - `if impact == ActionImpact.NO_OP: return None`
    - `if is_read_only: 不写 timeline`
    - `if gate_mode_str == "ACTIVE" && impact != NO_OP: 完整输出`

- [ ] **8. Trace（无条件执行）**
  - 位置：每帧最后
  - 检查点：`self.trace_writer.write(trace)`
  - 最低字段：`time`, `gate_mode`, `impact`, `intervention_level`, `advisory_only`

#### ⚠️ 禁止实现

- [ ] ❌ Gate 评估在 perception 之后
- [ ] ❌ Gate=SUSPENDED 仍执行 perception
- [ ] ❌ Gate=READ_ONLY 仍写 timeline
- [ ] ❌ NO_OP 写入 timeline
- [ ] ❌ 使用非系统时间做裁决

---

## 2️⃣ Gate 模块：`gate/gate_evaluator_v05.py`

### 2.1 GateEvaluatorV05 类

#### ✅ 必须实现

- [ ] **evaluate() 方法**
  - 输入：`stability_score`, `range_m`, `visibility_score`, `evidence_state`
  - 输出：`(gate_mode_str, gate_trace)`
  - 返回值：`"ACTIVE" | "READ_ONLY" | "SUSPENDED"`

- [ ] **Gate Trace 结构**
  - 必须字段：`mode`, `blocked_by`, `human_readable`
  - 可选字段：`stability_score`, `details`

#### ⚠️ 禁止实现

- [ ] ❌ Gate 判断风险是否真实
- [ ] ❌ Gate 确认"前方一定有坑"
- [ ] ❌ Gate 修改 impact 语义
- [ ] ❌ Gate 替 C 做最终决策

---

## 3️⃣ Gate Runtime：`gate_runtime.py`

### 3.1 BGateState 枚举

#### ✅ 必须实现

- [ ] **BGateState 枚举**
  - 值：`ACTIVE`, `READ_ONLY`, `SUSPENDED`
  - 用途：类型安全的状态转换

- [ ] **get_gate_state_from_mode() 函数**
  - 输入：`mode_str: str`
  - 输出：`BGateState`
  - 默认：`SUSPENDED`（最保守）

---

## 4️⃣ 输出控制：`_write_outputs()` 方法

### 4.1 READ_ONLY 处理

#### ✅ 必须实现

- [ ] **READ_ONLY 标志检查**
  - 位置：`_write_outputs()` 方法
  - 检查点：`if is_read_only:`
  - 行为：
    - `timeline_written = False`
    - `memory_written = False`
    - `trace_written = True`

#### ⚠️ 禁止实现

- [ ] ❌ READ_ONLY 仍写 timeline
- [ ] ❌ READ_ONLY 仍写 memory

---

## 5️⃣ 消息构建：`_build_message_to_c()` 方法

### 5.1 ACTIVE 检查

#### ✅ 必须实现

- [ ] **Gate=ACTIVE 检查**
  - 位置：`_build_message_to_c()` 方法
  - 检查点：`if gate_mode_str == "ACTIVE":`
  - 行为：只有 ACTIVE 才发送消息给 C

#### ⚠️ 禁止实现

- [ ] ❌ READ_ONLY 发送消息给 C
- [ ] ❌ SUSPENDED 发送消息给 C

---

## 6️⃣ Trace Schema：`trace_schema.py`（如存在）

### 6.1 Gate Trace 字段

#### ✅ 必须实现

- [ ] **gate_eval 字段**
  - 位置：trace 根级别
  - 必须字段：
    - `mode`: `"ACTIVE" | "READ_ONLY" | "SUSPENDED"`
    - `blocked_by`: `str | None`
    - `human_readable`: `str`

---

## 7️⃣ 测试文件：`tests/test_b2_v042_gate_integration.py`（建议创建）

### 7.1 Gate 三权测试

#### ✅ 必须实现

- [ ] **生杀权测试（SUSPENDED）**
  - 场景：视角不稳定
  - 预期：`return None`，但仍写 trace

- [ ] **降权权测试（READ_ONLY）**
  - 场景：视角稳定但证据不足
  - 预期：不写 timeline，不发给 C，但写 trace

- [ ] **可视权测试（Trace）**
  - 场景：所有 Gate 状态
  - 预期：每帧都有 `trace["gate_eval"]`

---

## 📊 实现完整性评分

### 核心实现（60分）

- Gate 评估位置正确：20分
- Gate Mode 分流正确：20分
- Output 分流正确：20分

### 边界检查（30分）

- SUSPENDED 处理：10分
- READ_ONLY 处理：10分
- NO_OP 处理：10分

### Trace 完整性（10分）

- 每帧都有 trace：5分
- Trace 包含最低字段：5分

---

## ✅ 验收标准

### 必须全部满足

1. ✅ Gate 评估在 tick() 最前面
2. ✅ Gate=SUSPENDED → return None（但仍写 trace）
3. ✅ Gate=READ_ONLY → 不写 timeline，不发给 C
4. ✅ Gate=ACTIVE → 完整流程
5. ✅ NO_OP → 不写 timeline，不发给 C
6. ✅ 每帧都有 trace
7. ✅ Trace 包含 `gate_eval` 字段

### 任一不满足 → ❌ 实现不完整

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ 实现对照清单
