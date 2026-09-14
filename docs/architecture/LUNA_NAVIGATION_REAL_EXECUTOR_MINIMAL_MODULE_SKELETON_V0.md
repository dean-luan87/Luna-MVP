# Luna — Navigation Real Executor Minimal Module Skeleton v0（真实执行器本体最小模块骨架：设计与落地）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`  
**性质**：Step 1：Navigation Real Executor Minimal Module Skeleton v0（把“执行器本体定义”落成可导入/可接线但不可执行的模块骨架）  

关联：
- 执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 执行器接口契约（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器输入对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 执行器状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- takeover → executor skeleton 接线（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_V0.md`
- 最小接入顺序（冻结）：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`

---

## A. 文档定位（写死）

- 这是“**真实执行器本体最小模块骨架**”的设计与落地文档。
- 当前目标：把执行器本体从“定义”推进为“可接入的模块骨架（skeleton）”。
- 当前不做真实执行器接入。
- 当前不做真实动作执行。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 skeleton

- 执行器本体定义已经冻结（边界、最小能力面、禁止越权已写死）。
- 最小接入顺序已明确：**Step 1 就是执行器本体最小模块骨架**。
- 如果没有 skeleton：
  - 输入对象实现版/状态对象实现版/监控闭环实现版将缺少明确“挂载点”与“对端接口”；
  - 后续很容易在接线阶段临时拼字段或越层读取，导致越权与不可回归。
- 因此必须先把执行器本体实体化为“可被未来接线的壳子”，但依然保持**不可执行**。

---

## C. skeleton 的最小定义（写死）

skeleton 是：

- 一个“真实执行器本体”的**可导入模块壳子**，用于承载身份与最小接口位。

skeleton 不是：

- 不是可运行导航器（不执行真实导航动作）。
- 不是接管层（不做 takeover 合法性与控制权移交）。
- 不是 formal decision（不裁决）。
- 不是 readiness gate（不做门控）。

一句话（写死）：

**skeleton 只提供未来可接线的执行器壳子与接口位，默认不执行、不接管、不扩权。**

---

## D. skeleton 最小能力面（写死四项）

### D1. 模块身份（必需）

- 有固定 `identity / scope`
- 示例：`navigation_real_executor_v0`

### D2. 输入接口占位（必需）

- 未来只接受 `navigation_real_executor_input_v0`
- 当前只做接口占位，不做真实消费、不做真实动作

### D3. 状态回传接口占位（必需）

- 未来只回 `navigation_real_executor_status_v0`
- 当前只做接口占位，不产真实运行态，不伪装 running/completed/failed

### D4. 异常上报接口占位（必需）

- 未来异常必须走标准接口（不走临时字段）
- 当前只做占位：返回标准化“placeholder / not_implemented”级别异常对象

---

## E. skeleton 默认行为（写死）

- 默认不执行真实动作
- 默认不接管控制权
- 默认不接地图
- 默认不驱动语音
- 默认不驱动记忆
- 默认只返回 `not_implemented / inactive / placeholder` 级别结果

并写死：

- 不新增时间/空间字段
- 不引入地图与坐标依赖

---

## F. 与现有链路的关系（写清）

### 与输入对象

- skeleton 未来只吃标准化输入对象（`navigation_real_executor_input_v0` 的正式实现版）。
- 当前不直接消费 placeholder（`*_placeholder_v0` 的产物不等同于正式输入对象实现版）。

### 与状态对象

- skeleton 未来只回标准化状态对象（`navigation_real_executor_status_v0` 的正式实现版）。
- 当前不产真实状态，只保留接口位，并返回 placeholder/inactive 级别结果。

### 与 takeover 层

- skeleton 不负责决定是否接管。
- 未来只能在 takeover 完成后被接入（控制权移交不在本轮范围）。

### 与 formal decision / readiness

- skeleton 不参与上游裁决与门控。
- 只在后续阶段作为被接线目标出现。

---

## G. 当前不允许做什么（必须写死）

- 不允许执行真实导航动作
- 不允许直接接主链控制权
- 不允许直接吃散字段
- 不允许直接回临时状态字段
- 不允许绕过 takeover / input object / status object 的边界

---

## H. 本轮落地位置（落点说明）

本轮 skeleton 代码落点建议：

- `capabilities/navigation/runtime/navigation_real_executor_v0.py`

理由（最小、连续、最不容易失控）：

- 放在 `capabilities/` 下与现有能力模块一致（voice/vision 已采用 `capabilities/<domain>/runtime/`）。
- 该位置天然表达“这是能力模块（executor 本体）”，而不是中台门控/stub（`capabilities/mid_platform/runtime/`）或语音链路（`capabilities/voice/runtime/`）。
- `capabilities/mid_platform/runtime/` 当前承载的是 gate/stub/placeholder 的评估函数；把 executor 本体放进去会混淆“治理链/门控链”与“执行器本体”职责边界。
- 把 skeleton 放进 `capabilities/voice/runtime/` 会把执行器错误归属为语音运行时的一部分，造成层级污染（voice 负责输入/输出与会话治理，不应承载导航执行器本体）。

---

## I. 当前为什么只能是 skeleton，不是 runtime executor（结论）

- 当前没有真实接管接线（takeover → executor）与主链控制权移交许可。
- 当前输入对象/状态对象仍处于设计冻结/placeholder 阶段，尚未进入“正式实现版”。
- 当前执行期监控闭环尚未进入“最小可运行实现版”。

因此本轮只能落“可接入但不可执行”的模块骨架，禁止任何真实执行行为。

