# Luna — Navigation Real Executor Status Object Implementation v0（执行器标准化状态对象：正式实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_IMPLEMENTATION_V0.md`  
**性质**：Step 3：Navigation Real Executor Status Object Implementation v0（把状态对象从 placeholder 推进到 implemented object，不回传真实运行事实）  

关联：
- 状态对象边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 状态对象 placeholder（只读占位）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_PLACEHOLDER_V0.md`
- 执行器接口契约（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 最小接入顺序（冻结）：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`
- 输入对象实现版（implemented）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是执行器标准化状态对象 `navigation_real_executor_status_v0` 的**正式实现版**文档。
- 当前目标：把状态对象从 placeholder 推进到 implemented object（可被执行器骨架合法回传/识别）。
- 当前不做真实执行器动作。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不驱动中台状态迁移。
- 当前不改变现有主线执行行为（不改 route/proposal/输出策略）。

---

## B. 为什么现在要先实现状态对象

- 执行器本体 skeleton 已存在。
- 输入对象实现版已存在（执行器首次具备“唯一合法输入面”的正式对象）。
- 若没有正式状态对象实现版，后续执行器只能回 placeholder 或散字段，监控链与中台无法稳定消费与治理。
- 因此 Step 3 必须先把状态对象正式实现出来，证明“执行器有唯一合法回传面”。
- 但当前仍不能让执行器回传真实运行事实（running/completed/failed 等都不允许伪造）。

---

## C. implemented status object 的最小定义（写死）

- 它不是 placeholder。
- 它不是执行完成事件。
- 它是执行器未来唯一合法回传对象 `navigation_real_executor_status_v0` 的**正式实现版**。
- 作用：把上游合法依据收束为可被执行器骨架合法回传/识别的标准化对象（但不代表真实执行器已运行）。

---

## D. 当前最小输入依据（写死，合法上游链）

至少包含以下输入（relevant-only，缺一不可）：

1) `navigation_executor_takeover_stub_v0`
   - 提供接管前/接管边界依据
   - 当前若无，则不应生成 implemented status object
2) `navigation_real_executor_input_v0`
   - 提供“正式输入对象已成立”的依据（必须是 implemented object）

可选只读（辅助一致性校验，不扩权）：

- `navigation_real_execution_readiness_gate_stub_v0`（若明确 blocked，则不写出 status object）

并写死：

- 不允许脑补（No Fabrication）
- relevant-only 继续成立
- 这些只是对象实现依据，不代表真实执行器已运行

---

## E. 当前最小输出位（写死）

继续写入：

- `result.metadata["navigation_real_executor_status_v0"]`

但写死：

- 本轮写出的是 **implemented object**（非 placeholder）
- 对象内部语义更明确，不以 `placeholder_pre_execution / unknown_placeholder` 作为主体表达

---

## F. 当前最小字段类别（实现最小可用表达）

至少实现三类（最小表达即可）：

1) **接管状态类**（必需）
2) **执行状态类**（必需）
3) **异常/偏航状态类**（必需）

并写死：

- 资源/能力状态类可以仍保持最小占位
- 回传绑定/路由类可以仍保持最小占位
- 但对象整体已从 placeholder 升级为 implementation

---

## G. 当前最小语义（写死）

当 implemented `navigation_real_executor_status_v0` 被产出时，只表示：

- 上游控制链已能把执行器状态所需最小信息整理成正式对象
- 执行器骨架可合法回传/识别该对象
- 不表示执行器已经开始真实运行
- 不表示执行器已经完成接管
- 不表示任务进入真实执行期

---

## H. 当前不允许做什么（必须写死）

- 不允许执行器拿到对象后伪装成 running/completed/failed 真实事实
- 不允许触发真实导航执行
- 不允许驱动中台迁移
- 不允许触发地图规划
- 不允许触发语音播报
- 不允许把 implemented status 当执行完成

---

## I. 落地位置（实现落点）

实现 builder 模块落点：

- `capabilities/mid_platform/runtime/navigation_real_executor_status_object_v0.py`

理由（最小、连续、最不容易失控）：

- 状态对象的输入证据来自 takeover stub 与输入对象（均为中台/门控链路写入的 metadata）。
- `capabilities/mid_platform/runtime/` 已承载 relevant-only 的只读评估与对象产出模式（stub/placeholder/implemented object builder）。
- 将实现落在此处可保持“只读、relevant-only、不改变主线、不驱动迁移”的安全边界，避免把对象拼装塞进 voice runtime 或 executor skeleton。

---

## J. 当前为什么仍不是 executor runtime status（结论）

- implemented status object 是“唯一合法回传面”的正式承载，但本轮不接真实执行器运行态，也不允许伪造运行事实。
- 执行器 skeleton 的接口只能做“识别/占位回传”，必须保持 `not_implemented / inactive / placeholder-safe`。
- 因此本轮只完成状态对象实现与接线证明，不进入任何真实执行状态实现。

