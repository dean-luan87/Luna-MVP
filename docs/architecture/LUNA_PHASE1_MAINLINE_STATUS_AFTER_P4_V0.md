# Luna Phase 1 — Mainline Status After P4 v0（P1–P4 主线阶段性收束）

**文件**：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_P4_V0.md`  
**性质**：阶段性主线状态收束（不是 roadmap / 愿景文 / 缺口大全）  

后续状态更新：
- After Executor Takeover Stub v0：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_TAKEOVER_STUB_V0.md`

---

## A. 文档定位（写死）

- 这是 **P1–P4 完成后的主线状态收束文档**。
- 目标：统一梳理当前主线完成度，用于后续阶段入口决策。
- 当前不展开新实现，不替代既有 execution plan / gaps 文档。

---

## B. 当前主线总状态摘要（短）

- 已完成：视角主线接口化骨架、解释/纠偏层候选协议与闭环占位、中台导航/非导航建议与消费占位、导航执行前承接层的设计冻结与只读 stub。
- 未进入：中台正式裁决、真实导航执行、地图接入、真实轻量模型上线、记忆真实消费与沉淀、任务缓存/恢复治理等。
- 总体状态：**已打通骨架与观测位，未进入实战执行**。

---

## C. 已落地链路（按阶段归类）

> 口径：清楚区分“代码已接入 / 只读 stub / 文档冻结”。

### C1. P1 已落地（视角主线接口化）

- **Vision Consumable Slice Output Schema v0（文档冻结）**  
  - `docs/architecture/vision/LUNA_VISION_CONSUMABLE_SLICE_OUTPUT_SCHEMA_V0.md`
- **Vision Mid-Platform Consume Stub v0（代码已接入，只读观测）**  
  - `capabilities/vision/runtime/vision_mid_platform_consume_stub_v0.py`  
  - 在主链写入观测：`result.metadata["vision_mid_platform_consume_stub_v0"]`
- **Vision Mainline Minimal Wiring v0（代码已接入，最小可运行接线）**  
  - `capabilities/vision/runtime/vision_mainline_minimal_wiring_v0.py`（risk_summary_v1 → risk_slice）  
  - 写入：`runtime_context.metadata["vision_consumable_slices_v0"]`

### C2. P2 已落地（解释/纠偏层准备）

- **Visual Interpretation & Correction Output v0（文档冻结：候选协议）**  
  - `docs/architecture/vision/LUNA_VISUAL_INTERPRETATION_AND_CORRECTION_OUTPUT_V0.md`
- **Lightweight Visual Interpretation Model Integration Plan v0（文档冻结：接入设计）**  
  - `docs/architecture/vision/LUNA_LIGHTWEIGHT_VISUAL_INTERPRETATION_MODEL_INTEGRATION_PLAN_V0.md`
- **Recognition → Correction → Re-recognition Loop v0（代码已接入：最小占位链 + 观测）**  
  - `capabilities/vision/runtime/vision_rerecognition_loop_v0.py`（risk_slice → needs_rerecognition_candidate，占位规则）  
  - 写入：`runtime_context.metadata["vision_interpretation_candidates_v0"]`

### C3. P3 已落地（中台导航/非导航分流：建议 + 消费占位）

- **Need-Navigation Routing v0（代码已接入：只读建议层 + metadata 观测）**  
  - `capabilities/mid_platform/runtime/need_navigation_routing_v0.py`  
  - 写入：`result.metadata["need_navigation_routing_v0"]`
- **Navigation / Non-Navigation Dispatch Consumption Plan v0（文档冻结：消费契约）**  
  - `docs/architecture/LUNA_NAVIGATION_NON_NAVIGATION_DISPATCH_CONSUMPTION_PLAN_V0.md`
- **Mid-Platform Dispatch Consumption Stub v0（代码已接入：只读消费占位 + metadata 观测）**  
  - `capabilities/mid_platform/runtime/mid_platform_dispatch_consumption_stub_v0.py`  
  - 写入：`result.metadata["mid_platform_dispatch_consumption_stub_v0"]`

### C4. P4 已落地（导航真实执行前承接：设计 + stub）

- **Navigation Handoff Post-Bound Execution Plan v0（文档冻结：执行前承接层规则）**  
  - `docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`
- **Navigation Handoff Post-Bound Execution Stub v0（代码已接入：只读承接占位 + metadata 观测）**  
  - `capabilities/voice/runtime/navigation_handoff_post_bound_execution_stub_v0.py`  
  - 写入：`result.metadata["navigation_handoff_post_bound_execution_stub_v0"]`

并且（导航目标事实层前置链已存在，属于“导航专项主线骨架”）：
- **destination_bound_v0（已材料化写入）**：`result.metadata["destination_bound_v0"]`（见 `LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_IMPL_V0.md`）  
- **navigation_handoff_consume_bound_v0（handoff 已只读消费 bound）**：`result.metadata["navigation_handoff_consume_bound_v0"]`

---

## D. 已冻结但未进入真实执行的链路（不要混淆“存在”与“执行”）

当前仍处于 **设计冻结 / 只读 stub / 观测层 / 占位层** 的典型能力包括：
- **中台正式裁决层**（尚未实现；目前只有建议层与消费占位 stub）
- **真实导航执行入口**（尚未实现；P4 只有执行前承接设计与 stub）
- **地图接入**（未进入）
- **真实轻量解释模型接入**（未进入；目前只有协议与接入设计 + 占位闭环）
- **记忆真实消费/沉淀链**（未进入；目前强调边界纪律与占位）
- **任务缓存/恢复治理**（未进入；占位方向存在但未实现）
- **视角目标生命周期管理分支**（占位文档存在，未实现运行时治理）

---

## E. 当前仍未进入的真实能力边界（明确写死）

- 真实导航执行（turn-by-turn / 实时引导 / 执行链）
- 地图辅助执行（地图骨架/路径规划/位置坐标依赖）
- 中台正式任务分流裁决与跨链执行切换
- 真实轻量模型上线（推理、性能、稳定性、降级）
- 记忆真实沉淀链（写入、升级、回滚、治理）
- 生命周期治理真实运行时实现（TTL/Recovery/挂起监控的真实逻辑）

---

## F. 当前阶段最关键的收束结论（读一眼就知道到哪了）

- 视角主线接口化已完成（schema + 最小接线 + 中台只读接住）
- 解释/纠偏层候选协议与闭环占位已完成（但未接真实轻量模型）
- 中台导航/非导航建议与消费占位已完成（但未进入正式裁决与切换）
- 导航执行前承接层已完成设计冻结与只读 stub（但未进入真实执行）
- **真实执行能力尚未开始**

---

## G. 下一阶段候选入口（只列入口，不做详细规划，不拍板优先级）

建议候选入口（3~5 个）：
- **中台正式裁决层（设计冻结入口）**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
- **正式裁决层门控输入（安全/任务有效性）**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_GATE_INPUTS_V0.md`
- **中台正式裁决层（Task Branch Decision Layer）**
- **真实导航执行链（Post-PreExecution → Real Executor）**
- **轻量解释模型真实接入（按 P2-2 设计接入到候选协议）**
- **视角运行时生命周期治理分支（Target Lifecycle Runtime Governance）**
- **任务缓存/恢复治理（跨会话任务承接）** 或 **记忆真实消费链**（二选一进入下一阶段讨论）

---

## H. 当前不做（写死）

- 不在本文件中新增实现计划
- 不在本文件中展开下一阶段详细路线
- 不在本文件中修改现有主线顺序
- 不在本文件中替代既有 execution plan / gaps 文档

