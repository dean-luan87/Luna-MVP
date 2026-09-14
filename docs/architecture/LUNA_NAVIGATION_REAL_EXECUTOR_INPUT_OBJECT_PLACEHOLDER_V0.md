# Luna — Navigation Real Executor Input Object Placeholder v0（执行器标准化输入对象：只读占位输出）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`  
**性质**：Phase-Next-17：执行器标准化输入对象占位输出（只读、可观察、不可执行）  

关联：
- 输入对象边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 执行器输入层边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_LAYER_V0.md`
- readiness gate stub（统一只读出口）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`
- takeover stub（接管前统一只读出口）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_STUB_V0.md`
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`

---

## A. 文档定位（写死）

- 这是执行器标准化输入对象的**只读占位设计**。
- 当前目标：让系统真正产出统一的输入对象占位（实体承载），用于观测与回归验证。
- 当前不接真实执行器。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有执行行为。

---

## B. 为什么现在要做 placeholder

- 输入对象边界已经冻结（Input Object v0）。
- 但当前系统里还没有真正的统一对象输出位。
- 若没有 placeholder，后续真实执行器接入时仍会回到“临时拼字段 / 越层取数”。
- 因此必须先把输入对象“实体化”为一个只读占位输出，证明上游控制链能收束出统一对象。

---

## C. placeholder 的最小定义（写死）

- 它不是执行器
- 不是执行命令
- 不是执行完成结果
- 只是“真实执行器标准化输入对象”的**只读占位实例**
- 作用：验证上游控制链是否能把所需最小信息收束成统一对象（可观察、可回归）

---

## D. 当前最小输入（写死只读，缺一不可）

只读以下输入（不允许脑补）：

1) `result.metadata["mid_platform_formal_decision_stub_v0"]`
- 且 `decision_result == "allow_progress"`

2) `result.metadata["formal_decision_allow_progress_path_v0"]`
- 且下游目标链与执行器输入层一致（本期最小约束：`downstream_placeholder_interface == "navigation_handoff_post_bound_execution_stub_v0"`）

3) `result.metadata["navigation_real_execution_readiness_gate_stub_v0"]`
- 且 `readiness_status == "ready_candidate"`

4) `result.metadata["navigation_executor_takeover_stub_v0"]`
- 且 `takeover_status == "ready_to_takeover"`

并写死：
- 缺一不可
- 不允许脑补
- 这些只是 placeholder 组装依据，不代表执行许可已经落地

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_real_executor_input_v0"]`

最小结构（固定建议）：

```json
{
  "executor_input_present": true,
  "executor_input_scope": "navigation_real_executor_input_v0",
  "takeover_authorized": true,
  "task_context_ready": true,
  "path_support_mode": "unknown_placeholder",
  "execution_constraints_ready": false,
  "monitor_binding_ready": false,
  "consume_mode": "read_only"
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“统一输入对象已形成占位实例”

---

## F. 当前最小字段组织原则（非常克制）

- **接管授权类**：必须能映射出 `takeover_authorized`
- **目标/任务上下文类**：当前只允许最小 `ready/not-ready` 语义，不展开复杂上下文
- **路径/辅助资源类**：当前只允许占位态（`unknown_placeholder`）
- **执行约束类**：当前只允许 `ready/not-ready` 占位，不注入真实约束
- **监控回传绑定类**：当前只允许 `ready/not-ready` 占位，不做真实绑定实现

---

## G. 当前最小结果语义（写死）

当 `navigation_real_executor_input_v0` 被产出时，只表示：

- 上游控制链已能把“执行器输入对象”组装成统一占位实例
- 后续真实执行器可基于该对象设计正式接入
- 不表示真实执行器已经消费它
- 不表示真实执行已经开始

---

## H. 当前不允许做什么（写死）

- 不允许真实执行器消费该对象
- 不允许触发真实导航执行
- 不允许触发地图规划
- 不允许触发语音播报
- 不允许把 `executor_input_present == true` 当执行开始

---

## I. 与现有链路的关系（写死）

### 与 formal decision

- formal decision 提供窄路径放行依据
- 不直接等于输入对象本体

### 与 readiness gate

- readiness gate 提供最后门控候选就绪状态
- 不直接等于输入对象本体

### 与 takeover stub

- takeover stub 提供接管前占位判断
- placeholder 以其为关键上游依据之一

### 与真实执行器

- 真实执行器未来应只读取该标准化输入对象（或其正式版本）
- 当前不接入执行器本体

