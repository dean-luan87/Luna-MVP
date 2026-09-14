# Luna — Navigation Real Executor Input Layer v0（真实导航执行器输入层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_LAYER_V0.md`  
**性质**：Phase-Next-15：真实导航执行器输入层最小设计（冻结执行器输入边界，不接执行器）  

关联：
- 主线状态（After Takeover Stub）：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_TAKEOVER_STUB_V0.md`
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`
- readiness gate（类别冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`
- readiness gate 输入面：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_INPUTS_V0.md`
- readiness gate stub（统一只读出口）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`
- takeover plan（接管合法入口冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- takeover stub（接管前统一只读出口）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_STUB_V0.md`
- 执行器标准化输入对象（对象边界冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 输入对象只读占位输出（placeholder v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`

---

## A. 文档定位（写死）

- 这是“真实导航执行器输入层”的最小设计文档。
- 当前目标：**冻结执行器输入边界**（真实执行器未来“吃什么、不吃什么”）。
- 当前不做真实执行器接入。
- 当前不做地图接入。
- 当前不做语音联动。
- 当前不做执行期监控实现。
- 当前不改变现有主线行为。

---

## B. 为什么现在要先定义输入层

- 当前已经有上游控制链：formal decision（极窄放行）、readiness gate（最后门控统一结果）、takeover stub（接管前统一出口）。
- 但真实执行器未来到底该接什么输入，还没有统一边界。
- 若不先定义输入层，后续真实执行器会直接读散乱状态、越层取数、难治理且难回归。
- 因此必须先冻结“执行器输入面”，确保执行器与上游控制链解耦。

---

## C. 执行器输入层在系统中的位置（写死）

执行器输入层应位于：

- formal decision 之后  
- readiness gate 之后  
- takeover 层之后  
- 真实执行器本体之前  

并写死：

- 它不是 formal decision
- 不是 readiness gate
- 不是 takeover 层
- 它是“执行器接入前的最后标准化输入面”

---

## D. 真实执行器未来允许接收的最小合法输入（只定义类别与边界，不做字段表）

只定义最小白名单类别（不发散、不做具体字段表，不设计真实参数结构）：

1) **正式放行结果（已完成窄路径放行）**  
- 执行器输入层只能承认“formal decision 已完成合法放行”的**标准化结果**  
- 不允许用建议层对象替代放行结果

2) **接管层结果（接管后标准化结果）**  
- 执行器未来应只接“接管层输出”及其后续正式接管层结果（当前仅占位说明）  
- 写死原则：执行器不得直接读取多个上游对象拼装“自以为的接管授权”

3) **路径 / 辅助资源输入（标准化执行输入，占位说明）**  
- 地图或非地图辅助资源的标准化执行输入（仅占位类别，不接入）

4) **执行参数输入（占位说明）**  
- 真实执行所需的最小动作参数 / 路径参数 / 控制参数（仅占位类别）

5) **执行约束输入（占位说明）**  
- 启动策略约束  
- 回退/中断约束  
- 安全约束的最终执行态约束（仅占位类别）

---

## E. 明确禁止直接喂给执行器的对象（写死，关键边界）

以下对象**不能直接作为执行器输入**（它们属于候选/建议/占位/门控/接管前状态，仅是前提依据）：

- `vision_consumable_slices_v0`
- `vision_interpretation_candidates_v0`
- `need_navigation_routing_v0`
- `mid_platform_dispatch_consumption_stub_v0`
- `destination_candidate_v0`
- `destination_bound_v0`
- `navigation_handoff_consume_bound_v0`
- `navigation_handoff_post_bound_execution_stub_v0`
- `formal_decision_allow_progress_path_v0`
- `navigation_real_execution_readiness_gate_stub_v0`
- `navigation_executor_takeover_stub_v0`

解释（写死）：

- 这些对象大多属于候选、建议、占位、门控、接管前状态。
- 它们是执行器输入的前提依据（用于上游控制链闭合与可观察治理）。
- 但它们**不是**执行器可直接消费的标准化输入对象；禁止真实执行器越层直读。

---

## F. 执行器输入层的最小职责（写死）

执行器输入层只负责：

- 接收上游“合法接管后”的标准化结果
- 规范化执行器所需输入（标准化输入面）
- 保持执行器与上游控制链解耦

执行器输入层不负责：

- 重新裁决（不替代 formal decision）
- 重新做 readiness 判断
- 重新做 takeover 判断
- 直接产出语音
- 直接改记忆

---

## G. 与现有各层的关系（写死）

### 与 formal decision

- formal decision 决定能否推进
- **不直接构成执行器输入**

### 与 readiness gate

- readiness gate 决定是否具备真实执行前的候选就绪状态
- **不直接构成执行器输入**

### 与 takeover 层

- takeover 层决定未来控制权是否可移交（接管授权）
- 执行器应读取 **takeover 之后的标准化输入层**，而不是直接读 takeover stub

### 与地图 / 非地图资源

- 这些资源未来应在执行器输入层被标准化后再进入执行器
- 当前不接入

### 与语音 / 输出治理

- 执行器输入层不直接决定是否播报
- 启动播报应在执行器输入层之外，由输出治理/语音策略另行消费

---

## H. 当前仍然不能接真实执行器的原因（写死）

- 当前没有真实执行器本体
- 当前没有执行器输入层实现
- 当前没有地图/非地图资源标准化输入
- 当前没有执行期监控真实闭环
- 当前没有启动策略真实接线
- 当前没有回退/中断治理真实接线

---

## I. 当前不做（写死）

- 不做真实执行器接入
- 不做真实地图接入
- 不做执行期监控接入
- 不做语音启动接入
- 不做回退治理接入
- 不做自动切链

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 执行器输入层的输入占位设计
- 再之后才考虑：
  - 真实执行器接入方案
- 当前不跨这两步

---

## K. 未来输入层对象样例（仅说明，不实现、不落代码）

```json
{
  "executor_input_present": true,
  "executor_input_scope": "navigation_real_executor_input_v0",
  "takeover_authorized": true,
  "path_support_mode": "map|non_map|hybrid",
  "execution_constraints_ready": false
}
```

