# Luna Vision Mainline — Breakpoints & Minimal Wiring Plan v0（视角主线断点与最小接线计划）

**文件**：`docs/architecture/vision/LUNA_VISION_MAINLINE_BREAKPOINTS_AND_MIN_WIRING_PLAN_V0.md`  
**性质**：执行用清单（只回答断点与最小接线；不写大规划、不展开实现细节）  

上位约束（必须服从）：
- `docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`
- `docs/architecture/LUNA_PHASE1_OPEN_GAPS_AND_NEXT_ACTIONS_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`（当前主链只读消费纪律）

---

## A. 文档定位

- 本文只回答四件事：
  - 视角现在哪些链路还没接上（断点）
  - 哪些只是 shadow / stub（现状）
  - 最先该接哪一跳（最小接线优先级）
  - 最小验证怎么做（可回归脚本口径）
- 本文不做：
  - 视角模型接入细节
  - 复杂中台调度器设计
  - 视觉解释/纠偏策略展开
  - 地图/记忆/联网补证具体策略

---

## B. 当前视角相关“已落地接线点”与性质（shadow/stub 盘点）

### B1. 已落地：Voice V3 视角摘要输入承载（stub）

- **代码锚点**：`capabilities/voice/runtime/vision_semantic_bridge_v3.py`
- **现状**：只读从 `runtime_context.metadata` 读取 summary-level keys（`sidewalk_env_summary_v1 / retail_env_summary_v1 / risk_summary_v1`），构建 `luna_voice_vision_semantic_v3_input` pack。
- **性质**：**stub + metadata-only 承载**（明确“present but not interpreted”）。
- **断点含义**：它不是“视角模块主线”，只是“允许视角摘要以安全方式进入语音事件 metadata”。

### B2. 已落地：Voice V2 对 V3 的只读 vision_shadow（shadow）

- **代码锚点**：`capabilities/voice/runtime/semantic_converter_v2.py`（RuleBasedSemanticConverterV2）
- **现状**：只读观察 `event.metadata["luna_voice_vision_semantic_v3_input"]` 是否存在，并写入 `payload["vision_shadow"]`（seen/not_seen，不解释）。
- **性质**：**shadow read**（观测层，不驱动主链裁决）。

### B3. 已冻结：Vision 分层/接口/最小运行链（文档 V1）

- **文档锚点**：
  - `docs/architecture/vision/LUNA_VISION_MAINLINE_LAYER_FLOW_V1.md`
  - `docs/architecture/vision/LUNA_VISION_MAINLINE_INTERFACES_V1.md`
  - `docs/architecture/vision/LUNA_VISION_MAINLINE_MIN_RUNTIME_V1.md`
- **现状**：接口与运行语义已写清，但 **未形成可被中台/主链消费的稳定 schema 与接线点**。

---

## C. 视角主线断点清单（“哪里还没接上”）

> 口径：只描述断点，不写实现细节。

### C1. 缺“可消费切片（Consumable Slice）”的稳定输出协议（schema）

- **现状**：V3 pack 只承载 summary key 的存在性与占位字段；不提供可消费切片的稳定字段面。
- **断点**：缺 schema → 中台无法“正式消费并调度” → 视角链无法进入工程闭环。

### C2. 缺“中台消费接口”的最小接线入口

- **现状**：架构写死“中台唯一消费调度器”，但代码层缺“中台接口层”的最小承载与观测入口。
- **断点**：没有中台入口 → 视角输出无法在系统层被统一消费与转发。

### C3. 缺“解释/纠偏层”的最小候选输出接入点（哪怕只读/空实现）

- **现状**：架构层明确 C3 只产候选；但工程上没有候选承载位/观测位。
- **断点**：后续想补“纠偏/重排/复核触发”时无统一坑位，易散落到各处破坏边界。

### C4. 缺“消费边界落代码”的最小防线

- **现状**：文档写死“视角不直接驱动语音/记忆/导航执行”，但工程上缺一个最小、可回归的“禁止直接消费连续视角流/禁止越权驱动”的接口面约束。
- **断点**：边界仅在文档 → 后续接线容易越权污染主链。

---

## D. 最先该接哪一跳（最小接线优先级）

> 目标：把“文档断点”翻译成“最小接线动作”，并保持可冻结与可回归。

### 第一优先级：Vision 可消费切片输出协议 schema v0（只定义 schema + 最小样例）

- **为什么是第一跳**：
  - 它是后续中台消费与调度的**必要前置**。
  - 不需要接模型、不需要解释策略，也能先把“可消费接口面”钉死。
  - 与 `LUNA_VISION_MODULE_ARCHITECTURE_V0.md` 的原则完全一致：主链只吃切片，不吃连续流。

### 第二优先级：中台消费接口占位（只读接线 + metadata 观测）

- **为什么是第二跳**：
  - schema 有了，才有“中台消费输入”可挂载的最小对象。
  - 本阶段只做“承载与观测”，不做裁决与执行，避免越权。

### 第三优先级：视角主线断点最小接线（只读）

- **目标**：
  - 把“快链/慢链输入面”落到一个可观测入口（哪怕输出为空/unknown）。
  - 明确哪些输出进入快链候选、哪些进入慢链候选（仍不做实际慢链补证执行）。

---

## E. 最小验证怎么做（可回归脚本口径）

> 原则：每一次“接线”都必须有最小验证脚本，且不改变主链裁决边界。

### E1. 验证点 1：schema 结构稳定性

- **验证目标**：给定一份最小输入（例如 summary-level 环境摘要），产出可消费切片结构满足 schema（字段存在/类型正确/为空时的口径一致）。
- **建议脚本形态**：`tools/verify_vision_consumable_slice_schema_v0.py`（仅示例命名；本节不落代码）。

### E2. 验证点 2：中台消费接口“只读承载”不夺权

- **验证目标**：
  - 中台接口层只写 metadata（或独立承载位），不直接驱动语音/记忆/导航执行。
  - 缺输入时 relevant-only（不写或写 not_applicable，保持一致）。

### E3. 验证点 3：语音主链不被视角侧越权污染

- **验证目标**：
  - 现有 V1/V2/V3 baseline 相关回归继续通过（例如 `tools/verify_voice_v1_minimal_flow.py` 等既有入口）。
  - 视角侧新增承载不会改变 `dispatch_type/route/proposal`。

---

## F. 输出结论（本 v0 的一句话）

视角主线要“打通断点”，第一跳不是接模型、不是解释策略，而是先把 **可消费切片 schema** 钉死，再给中台消费接口留最小只读接线入口，并用脚本把“只读、不夺权、不消费连续视角流”的边界回归住。

