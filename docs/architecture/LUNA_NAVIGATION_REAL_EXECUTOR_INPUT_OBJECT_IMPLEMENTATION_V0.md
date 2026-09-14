# Luna — Navigation Real Executor Input Object Implementation v0（执行器标准化输入对象：正式实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`  
**性质**：Step 2：Navigation Real Executor Input Object Implementation v0（把输入对象从 placeholder 推进到 implemented object，不接真实执行动作）  

关联：
- 输入对象边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 输入对象 placeholder（只读占位）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 执行器本体模块骨架（不可执行）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 最小接入顺序（冻结）：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`

---

## A. 文档定位（写死）

- 这是执行器标准化输入对象 `navigation_real_executor_input_v0` 的**正式实现版**文档。
- 当前目标：把输入对象从 placeholder 推进到 implemented object（可被执行器骨架合法接收）。
- 当前不做真实执行器动作。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线执行行为（不改 route/proposal/输出策略）。

---

## B. 为什么现在要先实现输入对象

- 执行器本体 skeleton 已存在，但仍是“不可执行壳子”。
- 如果没有正式输入对象实现版：
  - 执行器骨架只能面对 placeholder 或散字段，必然导致越层取数与不可回归；
  - 后续状态对象与监控闭环也缺少稳定的对端输入面。
- 因此 Step 2 必须先把输入对象正式实现出来，证明“执行器有唯一合法输入面”。
- 但当前仍然禁止：执行器消费后产生真实动作（仍保持 not_implemented/no-op）。

---

## C. implemented object 的最小定义（写死）

- 它不是 placeholder。
- 它不是执行命令。
- 它是执行器未来唯一合法输入对象 `navigation_real_executor_input_v0` 的**正式实现版**。
- 作用：把上游合法依据收束为可被执行器骨架接收的标准化对象（不代表执行已开始）。

---

## D. 当前最小输入依据（写死，仅允许合法上游链）

仍只允许来源于以下四个合法上游依据（缺一不可；relevant-only）：

1) `mid_platform_formal_decision_stub_v0`
   - 且 `decision_result == "allow_progress"`
2) `formal_decision_allow_progress_path_v0`
   - 且 `downstream_placeholder_interface == "navigation_handoff_post_bound_execution_stub_v0"`
3) `navigation_real_execution_readiness_gate_stub_v0`
   - 且 `readiness_status == "ready_candidate"`
4) `navigation_executor_takeover_stub_v0`
   - 且 `takeover_status == "ready_to_takeover"`

并写死：

- 不允许倒退为散字段拼接
- 不允许补全缺失依据（No Fabrication）

---

## E. 当前最小输出位（写死）

继续写入：

- `result.metadata["navigation_real_executor_input_v0"]`

但写死：

- 本轮写出的是 **implemented object**（非 placeholder）
- 对象语义更明确，不再以 `executor_input_present + unknown_placeholder` 作为主体表达

---

## F. 当前最小字段类别（实现最小可用表达）

至少实现三类（最小表达即可）：

1) **接管授权类**（必需）
2) **目标/任务上下文类**（必需）
3) **执行约束类**（必需，允许以“未实现”形式表达但必须有承载位）

并写死：

- 路径/辅助资源类可以仍保持最小占位（当前不接地图）
- 监控回传绑定类可以仍保持最小占位（当前不接监控真实闭环）
- 但对象整体已从 placeholder 升级为 implementation

---

## G. 当前最小语义（写死）

当 implemented `navigation_real_executor_input_v0` 被产出时，只表示：

- 上游控制链已把执行器所需最小信息整理成正式对象
- 执行器骨架可合法接收该对象
- 不表示执行器已经开始动作
- 不表示控制权已真实交给执行器
- 不表示真实导航已开始

---

## H. 当前不允许做什么（必须写死）

- 不允许执行器拿到对象后直接执行动作
- 不允许接地图
- 不允许驱动语音/记忆
- 不允许绕过 takeover/readiness/formal decision
- 不允许把 implemented object 当执行完成或执行开始

---

## I. 落地位置（实现落点）

实现 builder 模块落点：

- `capabilities/mid_platform/runtime/navigation_real_executor_input_object_v0.py`

理由（最小、连续、最不容易失控）：

- 当前输入对象的来源完全来自“中台/门控/接管”的上游证据（metadata 上的 stub/gate 输出）。
- `capabilities/mid_platform/runtime/` 现有模式已承载这些 relevant-only 的只读评估与对象产出（stub/placeholder）。
- 将 implemented object 先落在此处可以：
  - 继续保持“只读、relevant-only、不改变主线”的安全边界；
  - 避免把对象拼装逻辑塞进 voice runtime 或 executor skeleton，造成层级污染与越权风险。

---

## J. 当前为什么仍不是 executor runtime action（结论）

- implemented object 只是“唯一合法输入面”的正式承载，不包含动作、地图或控制权移交。
- 执行器 skeleton 的 `accept_executor_input` 仍必须保持 `not_implemented/no-op` 默认行为。
- 因此本轮只完成对象实现与最小接线证明，不进入任何真实执行能力。

