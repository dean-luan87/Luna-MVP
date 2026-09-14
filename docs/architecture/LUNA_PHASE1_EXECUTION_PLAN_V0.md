# Luna Phase 1 — Execution Plan v0（一期执行工作计划）

**文件**：`docs/architecture/LUNA_PHASE1_EXECUTION_PLAN_V0.md`  
**性质**：一期执行总计划（清晰顺序 + 最小交付物 + 可校验纪律；不是愿景文/roadmap/功能大全）  

---

## A. 文档定位

- 这是 **Luna 一期执行工作计划**。
- 作用：为 Cursor 与后续开发提供**主线执行顺序**与**可校验交付物**，避免碎片化推进。
- 当前目标：打通**最小可运行主线**，不是构建完整世界模型。
- 本计划**基于已冻结的架构与主线文档**，不替代它们；它只是“执行顺序的总导航”。
- 当前阶段状态收束（After P4）：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_P4_V0.md`

---

## B. 一期当前目标（工程语言）

一期目标不是“功能越多越好”，而是打通并冻结一条可生长的工程主线：

- 打通：**视角输入 → 中台消费 → 任务链/导航链承接**
- 形成：**可冻结、可回归、可逐步生长的事实层**

一期工程关注点写死：
- 优先保证：**当下行为是否安全、是否正确**
- 导航是**专项能力**，不是默认主链
- 地图是**辅助骨架**，不是核心事实源

下一阶段首入口（设计冻结）：
- 中台正式裁决层 v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`

---

## C. 一期主线执行顺序（5 个阶段，必须按顺序推进）

### P1 视角主线接口化（第一优先级）

重点：
- Vision Consumable Slice Output Schema
- 中台消费入口占位
- 视角主线只读接线
- 视角消费边界落代码

### P2 轻量解释 / 纠偏层接入准备

重点：
- 解释层输入输出协议
- 纠偏 / 重识别触发逻辑占位
- YOLO / OCR / 轻量模型职责边界（候选，不裁决）

### P3 中台导航 / 非导航分流

重点：
- Need-Navigation Routing
- 导航/非导航任务分流规则
- 中台是否应激活导航链的判断（观测先行，不夺权）

### P4 导航链正式执行前承接

重点：
- 在前置目标绑定链稳定后，规划 handoff 之后如何对接真实执行
- 本阶段仍不深挖完整执行系统

### P5 碎片建模与个体环境沉淀

重点：
- 环境碎片候选协议
- L1/L2/L3 建模更新口径
- 与记忆消费边界对接（不等于直接写记忆事实）

---

## D. 每个阶段的最小交付物（具体、可检查）

### P1 最小交付物

- **Vision Consumable Slice Output Schema v0**（稳定字段面 + 最小样例）
- **Vision Mid-Platform Consume Stub v0**（只读承载 + metadata 观测，不裁决）
- **Vision Mainline Minimal Wiring v0**（只读接线：快链/慢链输入面可观测）
- **验证入口**：schema 稳定性 + 只读不夺权 + 语音主链回归不被污染
- **freeze/baseline**：P1 交付物完成后必须出 baseline 文档或在总基线索引中冻结入口

### P2 最小交付物

- **Visual Interpretation & Correction Output v0**（候选输出承载位/协议；不裁决）
- **轻量解释/纠偏模型接入设计 v0**（不接代码）：`docs/architecture/vision/LUNA_LIGHTWEIGHT_VISUAL_INTERPRETATION_MODEL_INTEGRATION_PLAN_V0.md`
- **轻量解释层输入输出边界说明**（写死“候选，不驱动语音/记忆/导航执行”）
- **重识别触发循环占位**（仅占位：触发条件/回路入口，不实现策略）
- **验证入口**：解释层输出不越权、只写承载位、缺输入 relevant-only
- **freeze/baseline**：P2 交付完成需冻结接口面与禁止项

### P3 最小交付物

- **Need-Navigation Routing v0**（只读观测层：给出分流建议，不改主链裁决）
- **Navigation / Non-Navigation Dispatch Consumption Plan v0**（消费契约设计：定义未来如何消费建议结果；不裁决、不切换）：`docs/architecture/LUNA_NAVIGATION_NON_NAVIGATION_DISPATCH_CONSUMPTION_PLAN_V0.md`
- **导航 / 非导航测试分组**（最小用例集 + 预期输出字段）
- **中台分流验证入口**（脚本化回归：建议一致性、无越权）
- **freeze/baseline**：P3 交付需冻结“建议层”边界（不夺权）

### P4 最小交付物

- **Navigation Handoff Post-Bound Execution Plan v0**（设计文档）：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`
- **最小真实执行承接设计**（只设计：consume bound 后如何对接执行入口；不等于完整执行系统）
- **验证入口**：只做设计冻结，不落执行代码（除非另行明确）
- **freeze/baseline**：P4 以设计冻结为交付

### P5 最小交付物

- **Environment Fragment Candidate Schema v0**（沉淀候选承载位/协议；可回滚）
- **L1/L2/L3 环境建模更新口径**（保守、慢更新、可撤销）
- **记忆消费边界说明**（写死：不等于直接写记忆事实）
- **验证入口**：候选承载位稳定性 + 不直接写记忆 + relevant-only
- **freeze/baseline**：P5 交付需冻结候选协议与消费边界

---

## E. 当前明确不做（写死）

- 不做完整世界模型
- 不做完整真实导航执行
- 不做地图主导架构
- 不做解释层直接写记忆
- 不做解释层直接驱动语音/导航执行
- 不做白盒全实现
- 不做复杂多轮对话系统
- 不做完整 3D 重建主路线
- 不把连续视角全量喂主链

---

## F. 执行纪律（必须写死）

1. **不允许跳过 schema 直接接模型**（先接口化，再补模型点位）。  
2. **不允许解释层直接驱动语音/记忆/导航**（解释层只产候选）。  
3. **不允许未冻结就推进到下一层执行**（每阶段必须 baseline/freeze）。  
4. **不允许把地图当核心事实源**（地图只能辅助骨架）。  
5. **不允许把连续视角直接全量喂主链**（主链只消费切片）。  
6. **协议治理将逐步统一纳入**：`docs/architecture/LUNA_PROTOCOL_GOVERNANCE_V0.md`（当前阶段先按现有冻结文档执行，后续逐步收束）。  
7. 每完成一段必须补齐：
   - **验证入口**（最小脚本/回归）
   - **freeze / baseline**（文档冻结 + 索引入口）
   - **缺口更新**（更新 `LUNA_PHASE1_OPEN_GAPS_AND_NEXT_ACTIONS_V0.md` 或新增条目）

---

## G. 当前阶段完成判据（简短明确）

- **P1 完成**：视角输出已有统一可消费 schema，且可只读接入中台（不夺权）。
- **P2 完成**：轻量解释层具备清晰输入输出边界与重识别触发占位（仍只产候选）。
- **P3 完成**：中台能给出导航/非导航分流建议的稳定观测面（不改主链裁决）。
- **P4 完成**：导航链具备真实执行前的稳定承接设计（冻结，不落执行）。
- **P5 完成**：环境碎片候选协议可进入长期沉淀链（候选承载位稳定，不直接写记忆事实）。

---

## H. 与已有冻结文档的关系（执行依赖）

本执行计划依赖并服从（非穷举，列最关键入口）：
- 视角架构冻结：`docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`
- Phase 1 缺口清单：`docs/architecture/LUNA_PHASE1_OPEN_GAPS_AND_NEXT_ACTIONS_V0.md`
- 视角断点与最小接线计划：`docs/architecture/vision/LUNA_VISION_MAINLINE_BREAKPOINTS_AND_MIN_WIRING_PLAN_V0.md`
- 语音主线基线：`docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`

写死：
- 本计划不替代任何 baseline/architecture 文档；它只提供**一期执行顺序**与**交付检查口径**。

