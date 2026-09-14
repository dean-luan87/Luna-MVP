# Luna — Execution Monitoring Minimal Loop Implementation v0（执行期最小监控闭环：正式实现版）

**文件**：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_IMPLEMENTATION_V0.md`  
**性质**：Step 4：Execution Monitoring Minimal Loop Implementation v0（把监控闭环从 placeholder 推进到 implemented loop，不驱动真实治理）  

关联：
- 执行期最小监控闭环（冻结）：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_V0.md`
- 执行期监控状态 placeholder（只读占位）：`docs/architecture/LUNA_EXECUTION_MONITORING_STATUS_PLACEHOLDER_V0.md`
- 执行器状态对象边界冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 执行器状态对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 最小接入顺序（冻结）：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`

---

## A. 文档定位（写死）

- 这是执行期最小监控闭环的**正式实现版**文档。
- 当前目标：把监控闭环从 placeholder 推进到 implemented loop（可合法消费执行器状态对象并产出监控对象）。
- 当前不做真实执行器动作。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不驱动中台真实治理动作。
- 当前不改变现有主线执行行为（不改 route/proposal/输出策略）。

---

## B. 为什么现在要先实现监控闭环

- 执行器本体 skeleton 已存在。
- 输入对象实现版已存在。
- 状态对象实现版已存在。
- 若没有正式实现版监控闭环，后续执行器即使回传状态对象，也无法形成“可消费的最小闭环观察对象”。
- 因此 Step 4 必须先把监控闭环正式实现出来，证明系统具备“可合法消费状态对象 → 产出监控对象”的最小能力。
- 但当前仍不能驱动真实中台治理与回退动作（只做观测对象产出）。

---

## C. implemented monitoring loop 的最小定义（写死）

- 它不是 placeholder。
- 不是中台治理器。
- 不是正式裁决器。
- 它是“执行期最小监控闭环”的正式实现版。
- 作用：把执行器状态对象收束成可被中台/监控链合法消费的标准化监控对象（但不表示真实监控已全量运行）。

---

## D. 当前最小输入依据（写死，合法上游链）

至少包含以下输入（relevant-only，缺一不可）：

1) `navigation_real_executor_status_v0`
   - 且 `object_kind == "implemented_v0"`（这是主要输入）
2) `navigation_executor_takeover_stub_v0`
   - 提供接管边界的一致性依据

可选只读（辅助一致性校验，不扩权）：

- `navigation_real_executor_input_v0`（若提供，必须是 implemented object；否则不写）

并写死：

- 不允许脑补（No Fabrication）
- relevant-only 继续成立
- 这些只是最小闭环实现依据，不代表真实监控已全量运行

---

## E. 当前最小输出位（写死）

继续写入：

- `result.metadata["navigation_execution_monitoring_status_v0"]`

并写死：

- 本轮写出的是 **implemented monitoring status object**（非 placeholder）
- 不以 `pre_execution_placeholder / unknown_placeholder` 作为主体表达

---

## F. 当前最小字段类别（实现最小可用表达）

至少实现三类（最小表达即可）：

1) **接管监控类**（必需）
2) **执行监控类**（必需）
3) **异常/偏航监控类**（必需）

并写死：

- 退化监控类可以仍保持最小占位
- 回传路由监控类可以仍保持最小占位
- 但对象整体已从 placeholder 升级为 implementation

---

## G. 当前最小语义（写死）

当 implemented `navigation_execution_monitoring_status_v0` 被产出时，只表示：

- 上游控制链已能把执行期监控所需最小信息整理成正式对象
- 中台/监控链未来可合法消费该对象
- 不表示真实执行器已经开始真实动作
- 不表示中台已经开始真实治理
- 不表示回退/中断已被真实触发

---

## H. 当前不允许做什么（必须写死）

- 不允许监控闭环对象触发真实中台治理动作
- 不允许触发真实导航执行
- 不允许驱动地图规划
- 不允许触发语音播报
- 不允许把 implemented monitoring status 当执行完成/治理完成

---

## I. 落地位置（实现落点）

实现 builder 模块落点：

- `capabilities/mid_platform/runtime/navigation_execution_monitoring_status_v0.py`

理由（最小、连续、最不容易失控）：

- 监控对象的输入证据来自 executor status object 与 takeover stub（均为主链 metadata 上的只读产物）。
- `capabilities/mid_platform/runtime/` 已承载 relevant-only 的只读评估与对象产出模式。
- 将实现落在此处可保持“只读、不改变主线、不驱动治理”的安全边界。

---

## J. 当前为什么仍不是 runtime monitoring governance（结论）

- implemented monitoring loop 仅产出“可消费的监控对象”，不包含治理决策与动作接口。
- 任何中断/回退/迁移都仍必须由后续治理层实现并显式接线，当前禁止隐式触发。

