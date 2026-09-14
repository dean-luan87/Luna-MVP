# Luna — Navigation Real Executor Status Placeholder v0（执行器标准化状态对象：只读占位输出）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_PLACEHOLDER_V0.md`  
**性质**：Phase-Next-20：执行器标准化状态对象占位输出（只读、可观察、不可执行）  

关联：
- 状态对象边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 执行器接口契约（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器输入对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 输入对象只读占位输出：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 执行器接管层方案（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- 执行期监控状态只读占位输出：`docs/architecture/LUNA_EXECUTION_MONITORING_STATUS_PLACEHOLDER_V0.md`

---

## A. 文档定位（写死）

- 这是执行器标准化状态对象的**只读占位设计**。
- 当前目标：让系统真正产出统一的状态对象占位（实体承载），用于观测与回归验证。
- 当前不接真实执行器。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 placeholder

- 状态对象边界已经冻结（Status Object v0）。
- 但当前系统里还没有真正的统一状态对象输出位。
- 若没有 placeholder，后续真实执行器接入时仍会回到临时回传字段，监控链与中台无法稳定消费。
- 因此必须先把状态对象“实体化”为只读占位输出，证明系统可预留统一承载位。

---

## C. placeholder 的最小定义（写死）

- 它不是执行器
- 不是执行完成事件
- 不是 takeover 真状态
- 只是“执行器标准化状态对象”的**只读占位实例**
- 作用：验证系统未来是否能把执行器状态收束成统一对象（可观察、可回归）

---

## D. 当前最小输入（写死只读）

只读以下输入（不允许脑补）：

1) `result.metadata["navigation_executor_takeover_stub_v0"]`  
- 至少提供接管前状态依据

2) `result.metadata["navigation_real_executor_input_v0"]`  
- 至少提供“统一输入对象已形成”的依据

3) 如有必要，可只读：`result.metadata["navigation_real_execution_readiness_gate_stub_v0"]`  
- 仅作为辅助占位依据，不扩权

并写死：
- 缺一不可或按最小 relevant-only 原则处理（本期实现采用 relevant-only：缺任一关键依据则不写）
- 不允许脑补
- 这些只是 placeholder 组装依据，不代表真实执行器已经回传状态

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_real_executor_status_v0"]`

最小结构（固定建议）：

```json
{
  "executor_status_present": true,
  "executor_status_scope": "navigation_real_executor_status_v0",
  "takeover_state": "placeholder_pre_execution",
  "execution_state": "not_started_placeholder",
  "anomaly_state": "unknown_placeholder",
  "executor_capability_state": "unknown_placeholder",
  "status_route_binding_ready": false,
  "consume_mode": "read_only"
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“统一状态对象已形成占位实例”

---

## F. 当前最小字段组织原则（非常克制）

- **接管状态类**：当前只能占位，不得伪装成真实 started/active/released
- **执行状态类**：当前只能占位，不得伪装成 running/completed/failed/interrupted
- **异常/偏航状态类**：当前只能占位，不得伪装成真实异常
- **资源/能力状态类**：当前只能占位
- **回传绑定/路由类**：当前只能 ready/not-ready 占位，不做真实绑定

---

## G. 当前最小结果语义（写死）

当 `navigation_real_executor_status_v0` 被产出时，只表示：

- 系统已能为未来真实执行器预留统一状态对象承载位
- 后续真实执行器可基于该对象设计正式回传
- 不表示真实执行器已经开始运行
- 不表示真实执行器已经接管
- 不表示任务进入执行期

---

## H. 当前不允许做什么（写死）

- 不允许真实执行器消费/回传该对象
- 不允许触发真实导航执行
- 不允许触发地图规划
- 不允许触发语音播报
- 不允许把 `executor_status_present == true` 当执行开始

---

## I. 与现有链路的关系（写死）

### 与 executor input object

- input object 是执行器未来的标准化输入
- status object placeholder 是执行器未来的标准化输出占位
- 两者不能混用

### 与 takeover stub

- takeover stub 提供接管前占位判断
- status placeholder 只把它作为组装依据之一

### 与真实执行器

- 真实执行器未来应只回传该状态对象（或其正式版本）
- 当前不接入执行器本体

