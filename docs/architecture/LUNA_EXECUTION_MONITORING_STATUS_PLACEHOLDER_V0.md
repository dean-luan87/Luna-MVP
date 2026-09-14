# Luna — Execution Monitoring Status Placeholder v0（执行期监控闭环状态：只读占位输出）

**文件**：`docs/architecture/LUNA_EXECUTION_MONITORING_STATUS_PLACEHOLDER_V0.md`  
**性质**：Phase-Next-24：执行期最小监控闭环标准化状态对象占位输出（只读、可观察、不可执行）  

关联：
- 执行期最小监控闭环（冻结）：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_V0.md`
- 执行器状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 执行器状态占位输出：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_PLACEHOLDER_V0.md`
- 执行器接口契约（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`

---

## A. 文档定位（写死）

- 这是执行期监控闭环标准化状态对象的**只读占位设计**。
- 当前目标：让系统真正产出统一的监控状态对象占位（实体承载），用于观测与回归验证。
- 当前不接真实执行器。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 placeholder

- 监控闭环边界已经冻结（Minimal Loop v0）。
- 但当前系统里还没有真正的统一监控状态输出位。
- 若没有 placeholder，后续真实执行器接入时仍会回到“临时监控字段”，难以稳定接线与回归。
- 因此必须先把监控状态对象“实体化”为占位输出，证明承载位可在主链出现。

---

## C. placeholder 的最小定义（写死）

- 它不是监控治理器
- 不是 formal decision
- 不是 readiness gate
- 不是 takeover 授权
- 只是“执行期监控闭环标准化状态对象”的**只读占位实例**
- 作用：验证系统未来能否把执行期状态收束成统一监控回传对象（可观察、可回归）

---

## D. 当前最小输入（写死只读）

只读以下输入（不允许脑补）：

1) `result.metadata["navigation_real_executor_status_v0"]`  
- 提供执行器状态占位依据（作为监控闭环的上游事实来源之一）

2) `result.metadata["navigation_executor_takeover_stub_v0"]`  
- 提供接管前/接管边界依据（仅作占位组装依据之一）

3) 如有必要，可只读：`result.metadata["navigation_real_executor_input_v0"]`  
- 仅作为辅助占位依据，不扩权

并写死：
- 缺一不可或按最小 relevant-only 原则处理（本期实现采用 relevant-only：缺任一关键依据则不写）
- 不允许脑补
- 这些只是 placeholder 组装依据，不代表真实监控链已经运行

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_execution_monitoring_status_v0"]`

最小结构（固定建议）：

```json
{
  "monitoring_status_present": true,
  "monitoring_status_scope": "navigation_execution_monitoring_status_v0",
  "takeover_monitor_state": "pre_execution_placeholder",
  "execution_monitor_state": "not_started_placeholder",
  "anomaly_monitor_state": "unknown_placeholder",
  "degradation_monitor_state": "unknown_placeholder",
  "upstream_report_required": false,
  "consume_mode": "read_only"
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“统一监控状态对象已形成占位实例”

---

## F. 当前最小字段组织原则（非常克制）

- **接管监控类**：当前只能占位，不得伪装成真实 started/active/released 监控事实
- **执行监控类**：当前只能占位，不得伪装成真实 running/completed/failed/interrupted
- **异常监控类**：当前只能占位，不得伪装成真实偏航/不可执行/环境突变
- **退化监控类**：当前只能占位
- **回传要求类**：当前只允许 true/false 占位，不做真实回传路由实现

---

## G. 当前最小结果语义（写死）

当 `navigation_execution_monitoring_status_v0` 被产出时，只表示：

- 系统已能为未来执行期监控闭环预留统一状态对象承载位
- 后续真实执行器与监控链可基于该对象设计正式接入
- 不表示真实执行器已经开始运行
- 不表示真实监控闭环已经启动
- 不表示上游必须立即采取行动

---

## H. 当前不允许做什么（写死）

- 不允许真实执行器回传/消费该对象
- 不允许触发真实导航执行
- 不允许触发地图规划
- 不允许触发语音播报
- 不允许把 `monitoring_status_present == true` 当监控闭环已运行

---

## I. 与现有链路的关系（写死）

### 与 executor status object

- executor status placeholder 是执行器侧标准化状态占位
- monitoring status placeholder 是监控闭环侧统一消费/回传占位
- 两者不能混用

### 与 takeover stub

- takeover stub 提供接管前占位依据
- monitoring placeholder 只把它作为组装依据之一

### 与真实监控闭环

- 真实监控闭环未来应只回传该对象或其正式版本
- 当前不实现监控运行时

