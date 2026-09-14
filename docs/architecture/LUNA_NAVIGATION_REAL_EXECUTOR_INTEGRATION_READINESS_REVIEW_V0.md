# Luna — Navigation Real Executor Integration Readiness Review v0（真实执行器接入就绪评审：阶段收束）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTEGRATION_READINESS_REVIEW_V0.md`  
**性质**：Phase-Next-21：真实执行器接入前系统级就绪评审（不是 roadmap / 不是技术方案 / 不是缺口大全）  

关联（评审依据）：
- 主线状态（After Takeover Stub）：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_TAKEOVER_STUB_V0.md`
- 执行器输入层边界：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_LAYER_V0.md`
- 执行器输入对象边界：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 输入对象占位输出：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 执行器接口契约：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器状态对象边界：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 状态对象占位输出：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_PLACEHOLDER_V0.md`
- 接管层合法入口冻结：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- readiness gate（类别冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`
- 最小接入顺序（设计冻结）：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`
- 回退/中断治理入口（冻结）：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`
- 回退/中断治理决策层（冻结）：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_V0.md`
- 治理动作边界层（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理动作执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`

---

## A. 文档定位（写死）

- 这是“真实执行器接入前”的阶段评审文档。
- 目标：评估当前是否具备进入接入阶段的最低条件，并收束硬阻断项与可后补项。
- 当前不展开真实接入实现，不给接入技术方案。
- 当前不改变现有主线顺序。

---

## B. 当前已具备的接入前骨架（按能力块归类）

> 口径：每块只列关键项，并标明 **设计冻结 / 只读占位 / 代码已落地**。

### B1. 控制链骨架

- **Formal Decision（代码已落地：只读裁决骨架）**
  - `mid_platform_formal_decision_stub_v0` 已支持结构化 pending/block 原因，且存在极窄 allow-progress 路径（vNext）。
- **Allow-progress Preconditions（设计冻结）**
  - 放行前提已被明确定义为设计冻结约束（不在本轮评审中展开）。
- **Handoff / Readiness / Takeover 控制链（代码已落地 + 设计冻结混合）**
  - `readiness gate inputs/stub`：输入面设计冻结 + stub 统一出口已落地（只读）。
  - `takeover plan`：合法入口语义设计冻结。
  - `takeover stub`：统一只读出口已落地（只读）。

### B2. 输入侧骨架

- **Executor Input Layer（设计冻结）**
  - 执行器输入层边界已冻结：位于 formal decision/readiness/takeover 之后、执行器之前。
- **Executor Input Object（设计冻结）**
  - 标准化输入对象类别/必需类别已冻结（不允许执行器越层直读上游对象）。
- **Executor Input Placeholder（代码已落地：只读占位输出）**
  - `navigation_real_executor_input_v0` 已能在极窄条件下只读产出（relevant-only）。

### B3. 输出侧骨架

- **Executor Interface Contract（设计冻结）**
  - 执行器唯一合法输入与最小输出类别/回传状态集合已冻结。
- **Executor Status Object（设计冻结）**
  - 标准化状态对象类别/必需类别已冻结（用于监控/中台消费）。
- **Executor Status Placeholder（代码已落地：只读占位输出）**
  - `navigation_real_executor_status_v0` 已能只读产出（relevant-only，明确为 placeholder，不伪装真实运行态）。

### B4. 接管前骨架

- **Takeover Plan（设计冻结）**
  - 接管合法入口与接管语义已冻结（强调接管不等于完成）。
- **Takeover Stub（代码已落地：只读统一出口）**
  - `navigation_executor_takeover_stub_v0` 已存在统一只读占位结果。
- **Downstream Stub Consumption（设计冻结）**
  - post-bound execution stub 的消费契约已冻结（当前仍为占位链，不进入真实执行）。
- **Readiness Gate / Inputs / Stub（设计冻结 + 代码已落地）**
  - 最后门控类别/输入面冻结；stub 统一出口已落地（只读）。

---

## C. 当前仍未具备的真实能力（明确：占位不等于真实能力）

以下仍未进入（当前不存在或未真实接线）：

- 真实执行器本体
- 真实执行器接管实现（控制权真实移交器）
- 真实执行器输入对象实现版（当前只有只读 placeholder）
- 真实执行器状态对象实现版（当前只有只读 placeholder）
- 地图 / 非地图执行资源真实接入
- 执行期监控闭环真实实现（运行态、异常/超时、取消/中断、状态回传）
- 启动策略与输出治理真实接入（例如“开始导航”播报与执行态同步）
- 回退 / 中断治理真实实现（失败回收、抢占、恢复、降级治理）

---

## D. 硬阻断项 vs 可后补项（关键）

### D1. 硬阻断项（不满足就不应进入真实执行器接入阶段）

> 判定口径：缺少这些会导致“接入即不可控 / 不可观测 / 不可回收”，违反当前安全与治理边界。

- **没有真实执行器本体**  
  - 没有可接入目标，无法验证接口契约与执行行为。
- **没有执行器接管实现（真实控制权移交器）**  
  - 无法把“占位链”与“真实执行”隔离；容易越层直连导致失控。
- **没有真实执行输入对象实现版**  
  - 执行器即使存在也会被迫读取散乱字段，违背“唯一合法输入面”契约。
- **没有执行期监控闭环**  
  - 接入后无法知道执行是否在跑/是否失败/是否中断；无法治理与回收。
- **没有最小回退/中断治理**  
  - 接入后若失败/偏航/中断，没有系统级回收路径与治理口径，风险不可接受。
- **没有启动策略/输出治理的最低接线**  
  - 接入后输出（如播报/提示）可能与执行态不一致，且缺少最小治理边界。

### D2. 可后补项（可在接入后分阶段补强，但当前不是绝对阻断）

> 判定口径：不会决定“能不能接入”，但会影响体验、覆盖面与鲁棒性；可在保证硬阻断项闭合后逐步增强。

- 地图模式增强（更丰富路径能力、更高精度定位/规划能力）
- 非地图辅助增强（视觉/传感辅助的更强策略与资源）
- 更丰富的执行状态枚举（更细粒度状态、原因树、阶段化回报）
- 更完整的资源退化策略（更细的 degraded/partial 能力管理）
- 更丰富的监控回传路由（多链路、多租户、分级告警等）

---

## E. 当前是否适合进入真实执行器接入阶段（明确结论）

**结论：当前不建议进入真实执行器接入阶段。**  

**原因**：硬阻断项仍未满足（至少包括：真实执行器本体、真实接管实现、执行期监控闭环、最小回退/中断治理、启动策略/输出治理最低接线、输入对象实现版）。  

**进入前至少需先补齐**（最小集合，写死口径）：
- 真实执行器本体最小定义（可被接口契约验证）
- 真实接管实现（控制权移交器）
- 执行期监控最小闭环（能观测运行/失败/中断）
- 最小回退/中断治理（能回收与治理）
- 启动策略/输出治理最低接线（防止输出与执行态脱钩）
- 输入对象实现版（保证“唯一合法输入面”不被破坏）

---

## F. 若未来进入接入阶段，最小进入顺序建议（只列顺序，不展开方案）

> 具体“最小接入顺序”的冻结版本见：`docs/architecture/LUNA_REAL_EXECUTOR_MINIMAL_INTEGRATION_SEQUENCE_V0.md`  

1) 真实执行器本体最小模块骨架  
2) 执行器输入对象实现版  
3) 执行器状态对象实现版  
4) 执行期监控最小闭环实现版  
5) takeover → executor 的真实接管接线  

---

## G. 当前不做（写死）

- 不在本文档中实现任何真实执行器接线
- 不在本文档中修改既有主线
- 不在本文档中把评审结论直接变成接入动作
- 不在本文档中替代 execution plan / mainline status 文档

