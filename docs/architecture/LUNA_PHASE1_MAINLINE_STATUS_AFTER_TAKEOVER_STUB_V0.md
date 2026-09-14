# Luna Phase 1 — Mainline Status After Executor Takeover Stub v0（主线阶段状态收束）

**文件**：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_TAKEOVER_STUB_V0.md`  
**性质**：阶段状态收束（不是 roadmap / 不是新规划 / 不是缺口大全）  

关联（上游既有状态收束）：
- After P4：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_P4_V0.md`
后续接入评审：
- Real Executor 接入就绪评审 v0：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTEGRATION_READINESS_REVIEW_V0.md`

---

## A. 文档定位（写死）

- 这是 **P1 主线推进到 Navigation Executor Takeover Stub v0 之后**的阶段状态收束文档。
- 目标：统一更新当前主线完成度，用于后续决定是否进入“真实执行器接入阶段”。
- 当前不展开新实现，不替代既有 execution plan / gaps / previous status 文档。

---

## B. 当前主线总状态摘要（一句话能读懂）

系统已从视角输入主线推进到 formal decision、readiness gate、takeover stub，**已具备“真实执行器接管前”的完整只读占位控制链**，但**仍未进入真实导航执行阶段**。

---

## C. 当前主线已落地链路（按“真实链路层级”归类）

> 口径：每层明确区分 **已有代码占位** / **仅设计冻结** / **仅只读观测**（含只读接线）。

### C1. 感知 / 视角输入层

- **仅设计冻结**
  - Vision Consumable Slice Output Schema v0：`docs/architecture/vision/LUNA_VISION_CONSUMABLE_SLICE_OUTPUT_SCHEMA_V0.md`
- **已有代码占位（最小接线）**
  - Vision Mainline Minimal Wiring v0（`risk_summary_v1` → `risk_slice`）：`capabilities/vision/runtime/vision_mainline_minimal_wiring_v0.py`
  - 产出落点：`runtime_context.metadata["vision_consumable_slices_v0"]`
- **已有代码占位（只读观测/消费）**
  - Vision Mid-Platform Consume Stub v0：`capabilities/vision/runtime/vision_mid_platform_consume_stub_v0.py`
  - 观测落点：`result.metadata["vision_mid_platform_consume_stub_v0"]`

### C2. 解释 / 纠偏层

- **仅设计冻结**
  - Visual Interpretation & Correction Output v0（候选协议）：`docs/architecture/vision/LUNA_VISUAL_INTERPRETATION_AND_CORRECTION_OUTPUT_V0.md`
  - Lightweight Visual Interpretation Model Integration Plan v0（接入设计）：`docs/architecture/vision/LUNA_LIGHTWEIGHT_VISUAL_INTERPRETATION_MODEL_INTEGRATION_PLAN_V0.md`
- **已有代码占位（只读接线 + 观测）**
  - Recognition → Correction → Re-recognition Loop v0（占位闭环链）：`capabilities/vision/runtime/vision_rerecognition_loop_v0.py`
  - 产出落点：`runtime_context.metadata["vision_interpretation_candidates_v0"]`

### C3. 中台建议与消费层（Routing / Consumption）

- **已有代码占位（只读建议）**
  - Need-Navigation Routing v0：`capabilities/mid_platform/runtime/need_navigation_routing_v0.py`
  - 观测落点：`result.metadata["need_navigation_routing_v0"]`
- **仅设计冻结**
  - Navigation / Non-Navigation Dispatch Consumption Plan v0：`docs/architecture/LUNA_NAVIGATION_NON_NAVIGATION_DISPATCH_CONSUMPTION_PLAN_V0.md`
- **已有代码占位（只读消费观测）**
  - Mid-Platform Dispatch Consumption Stub v0：`capabilities/mid_platform/runtime/mid_platform_dispatch_consumption_stub_v0.py`
  - 观测落点：`result.metadata["mid_platform_dispatch_consumption_stub_v0"]`

### C4. 执行前承接层（Pre-Execution Handoff）

- **已有代码占位（事实材料化 / 只读承接）**
  - `destination_bound_v0`（目的地绑定事实写入）：`result.metadata["destination_bound_v0"]`
  - `navigation_handoff_consume_bound_v0`（handoff 只读消费 bound）：`result.metadata["navigation_handoff_consume_bound_v0"]`
- **仅设计冻结**
  - Navigation Handoff Post-Bound Execution Plan v0：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`
  - Navigation Handoff Post-Bound Execution Stub Consumption Plan v0：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`
- **已有代码占位（只读 stub）**
  - Navigation Handoff Post-Bound Execution Stub v0：`capabilities/voice/runtime/navigation_handoff_post_bound_execution_stub_v0.py`
  - 观测落点：`result.metadata["navigation_handoff_post_bound_execution_stub_v0"]`

### C5. 正式裁决层（Formal Decision）

- **仅设计冻结**
  - Formal Decision Layer v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
  - Formal Decision Allow-Progress Preconditions v0（设计冻结）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_ALLOW_PROGRESS_PRECONDITIONS_V0.md`
- **已有代码占位（只读门控输入承接）**
  - Formal Decision Gate Inputs v0：`capabilities/mid_platform/runtime/formal_decision_gate_inputs_v0.py`
  - 观测落点：`result.metadata["formal_decision_gate_inputs_v0"]`
  - Formal Decision Handoff Gates v0：`capabilities/mid_platform/runtime/formal_decision_handoff_gates_v0.py`
  - 观测落点：`result.metadata["formal_decision_handoff_gates_v0"]`
  - Formal Decision Information Gates v0：`capabilities/mid_platform/runtime/formal_decision_information_gates_v0.py`
  - 观测落点：`result.metadata["formal_decision_information_gates_v0"]`
- **已有代码占位（只读裁决骨架）**
  - Formal Decision Stub v0/v1/v2（结构化 pending/block 原因）与 vNext（极窄 allow-progress）：
    - 代码：`capabilities/mid_platform/runtime/mid_platform_formal_decision_stub_v0.py`
    - 文档：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V0.md`、`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V2.md`、`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`
  - 观测落点：`result.metadata["mid_platform_formal_decision_stub_v0"]`
  - allow-progress 窄路径观测：`result.metadata["formal_decision_allow_progress_path_v0"]`

### C6. 真实执行前最后门控层（Readiness Gate）

- **仅设计冻结**
  - Navigation Real Execution Readiness Gate v0：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`
  - Navigation Real Execution Readiness Gate Inputs v0（输入面冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_INPUTS_V0.md`
- **已有代码占位（只读输入承接 + 只读 stub 统一出口）**
  - Gate Inputs 承接：`capabilities/mid_platform/runtime/navigation_real_execution_readiness_gate_inputs_v0.py`
  - 观测落点：`result.metadata["navigation_real_execution_readiness_gate_inputs_v0"]`
  - Gate Stub v0（统一出口）：`capabilities/mid_platform/runtime/navigation_real_execution_readiness_gate_stub_v0.py`
  - 观测落点：`result.metadata["navigation_real_execution_readiness_gate_stub_v0"]`

### C7. 接管层（Executor Takeover）

- **仅设计冻结**
  - Navigation Executor Takeover Plan v0：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- **已有代码占位（只读 stub 统一出口）**
  - Navigation Executor Takeover Stub v0：`capabilities/mid_platform/runtime/navigation_executor_takeover_stub_v0.py`
  - 观测落点：`result.metadata["navigation_executor_takeover_stub_v0"]`
  - 文档：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_STUB_V0.md`

---

## D. 当前已经具备的控制骨架（强调“控制能力”，不等于真实执行）

- 已能用结构化字段解释 **为什么 block**（formal decision v2/vNext 的结构化原因；readiness gate 的 blocked 原因）。
- 已能用结构化字段解释 **为什么 pending / not_ready**（formal decision 的 hold_pending；readiness gate 的 not_ready）。
- 已能在**极窄条件**下输出 `allow_progress`（formal decision vNext），且只产生只读“下游接口目标”观测（`formal_decision_allow_progress_path_v0`）。
- 已能把 readiness 收束为统一出口（`navigation_real_execution_readiness_gate_stub_v0`）。
- 已能把 executor takeover 收束为统一只读出口（`navigation_executor_takeover_stub_v0`），形成“接管前占位链”的最后统一结果位。

---

## E. 当前仍未进入的真实执行能力（必须明确：占位不等于真实能力）

- 真实导航执行器接入（真实控制权移交与执行驱动）
- 地图 / 非地图执行资源真实接入（路径、定位、辅助资源）
- 执行期监控闭环真实实现（运行态、异常、超时、撤销、回报）
- 语音启动策略真实实现（“开始导航”播报与输出治理）
- 回退 / 中断治理真实实现（失败回收、抢占、恢复、降级）
- 真实接管层实现（takeover executor / 控制权移交器本体）
- 接管后状态回传真实接线（takeover_started/active/failed/...）

---

## F. 进入真实执行器前还差什么（按“必须先有”列）

1) **真实执行器输入层**（执行器可读的最小输入面与验证/对齐规则）  
2) **真实执行器接管层实现**（从 `ready_to_takeover` 到真实控制权移交的正式实现与边界）  
3) **执行期监控闭环**（运行态观测、异常/超时、中断/取消、状态回传）  
4) **启动策略与输出治理接入**（何时播报/如何播报/如何与执行态同步）  
5) **回退 / 中断治理接入**（接管失败/中断后的控制权回收与路径治理）  
6) **地图 / 非地图执行资源真实接入**（资源存在性、可用性、降级与安全边界）

---

## G. 当前阶段最关键的收束结论（短条目）

- 主线已完成从“建议”到“接管前占位链”的闭合（formal decision → readiness → takeover stub）。
- formal decision 已从纯 stub 升级为带结构化原因、并支持极窄 allow-progress 的裁决骨架。
- readiness / takeover 均已有统一出口（统一结果位已存在且可观察）。
- 系统仍然**没有真实执行器**，也**没有真实接管**与执行期闭环。
- 下一阶段是否进入真实执行器接入，必须谨慎决策，且必须先补齐“必须先有”的输入/接管/监控/治理能力。

---

## H. 下一阶段候选入口（只列入口，不规划）

- 真实执行器输入层
- 真实执行器接管层实现
- 执行期监控闭环实现
- 输出治理 / 启动策略接入
- 回退 / 中断治理实现
- 地图 / 非地图资源接入

---

## I. 当前不做（写死）

- 不在本文件中新增实现计划
- 不在本文件中展开真实执行器接入路线
- 不在本文件中改现有主线顺序
- 不在本文件中替代 execution plan / gaps / previous status 文档

