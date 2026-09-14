# Luna — Navigation Real Execution Readiness Gate Inputs v0（最后门控输入面：设计/占位）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_INPUTS_V0.md`  
**性质**：Phase-Next-11：真实执行前最后门控层的输入面定义（只定义输入与承接位，不做门控判定/不接执行器）  

关联：
- 真实执行前最后门控（类别冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`
- 下游占位消费契约：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`

---

## A. 文档定位（写死）

- 这是“真实执行前最后门控层”的**输入面**设计文档。
- 当前目标：定义最后门控输入如何进入系统（最小结构 + 只读承接位）。
- 当前不做真实门控实现。
- 当前不做真实执行器接入。
- 当前不做地图接入。
- 当前不改变现有主线行为。

---

## B. 为什么现在必须补“最后门控输入层”

- 当前最后门控类别已经冻结（见 `READINESS_GATE_V0`）。
- 但仍没有正式输入位。
- 若没有输入位，后续接真实执行器时会被迫读散乱状态、越层取数、不可回归。
- 因此必须先把最后门控输入层钉住：**从哪里来、以什么最小结构进入主链**。

---

## C. 最小输入集合（5 类，只定义最小集合）

> 口径：只定义最小字段与枚举语义；不做真实参数设计、不做数值策略。

### C1. 执行器存在性输入（Executor Existence）

最小字段：
- `executor_gate_present`: bool
- `executor_available`: bool
- `executor_status`: `available | unavailable | blocked`
- `executor_takeover_allowed`: bool

### C2. 路径/辅助资源可用性输入（Path / Support Resources）

最小字段：
- `path_support_gate_present`: bool
- `map_support_available`: bool
- `non_map_support_available`: bool
- `path_support_status`: `available | partial | unavailable`

### C3. 执行期监控闭环输入（Execution Monitor Loop）

最小字段：
- `execution_monitor_gate_present`: bool
- `monitor_feedback_available`: bool
- `drift_detection_available`: bool
- `execution_monitor_status`: `ready_candidate | partial | unavailable`

### C4. 启动策略输入（Start Policy）

最小字段：
- `start_policy_gate_present`: bool
- `start_output_policy_available`: bool
- `start_policy_status`: `ready_candidate | restricted | unavailable`

### C5. 回退/中断输入（Fallback / Interrupt Recovery）

最小字段：
- `fallback_gate_present`: bool
- `fallback_path_available`: bool
- `interrupt_recovery_available`: bool
- `fallback_status`: `ready_candidate | partial | unavailable`

---

## D. 这些输入未来来自哪里（来源说明，不做实现）

- **执行器存在性输入**：未来来自真实导航执行器注册/状态层
- **路径/辅助资源输入**：未来来自地图能力或非地图辅助能力状态层
- **执行期监控输入**：未来来自执行监控闭环 / 偏航检测 / 成功失败反馈层
- **启动策略输入**：未来来自输出治理 / 语音启动策略层
- **回退/中断输入**：未来来自回退治理 / 中断恢复策略层

---

## E. 当前最小输入原则（写死）

1. 没有输入位 ≠ 默认可用  
2. 输入缺失时不得脑补  
3. 任一门控输入即使存在，也不代表真实可执行  
4. 只有后续门控层统一消费这些输入，才能形成“真实执行前 readiness”判断  
5. 当前这些输入只是未来 readiness gate 的上游原料，不是执行信号  

---

## F. 与现有链路的关系（写死）

### 与 formal decision

- formal decision 当前最多只把结果推进到下游占位层
- 不直接消费这些真实执行前最后门控输入

### 与 post-bound execution stub

- 当前 stub 消费 allow-progress
- 后续若要继续推进到真实执行器前状态，应由 readiness gate 消费这些输入

### 与真实执行器

- 真实执行器未来应位于 readiness gate 之后
- 当前不接入执行器本体

---

## G. 当前不做（写死）

- 不做真实执行器注册/接入
- 不做地图接入
- 不做执行监控实现
- 不做启动语音策略实现
- 不做回退/中断治理实现
- 不做 readiness gate 真实判定
- 不做真实导航执行

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 把这些 gate inputs 接成一个统一的 readiness gate input 对象（只读）
- 再之后才考虑：
  - 真实 execution readiness gate stub
- 当前不跨这两步

---

## I. 推荐的只读承载位（仅建议，非强制）

建议未来上游将 5 类输入占位写入 `runtime_context.metadata` 的独立键（示例）：
- `navigation_executor_gate_v0`
- `navigation_path_support_gate_v0`
- `navigation_execution_monitor_gate_v0`
- `navigation_start_policy_gate_v0`
- `navigation_fallback_gate_v0`

当前它们只是“输入占位键”，不代表已实现能力。

