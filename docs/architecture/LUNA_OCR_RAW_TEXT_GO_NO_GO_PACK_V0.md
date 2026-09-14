## Phase-ModelOCR-001

OCR Raw Text Capability Go/No-Go Pack v0

### 1. 决策对象

本决策包只覆盖“OCR 原文识别能力（raw text capability）”的定义与验收口径，不涉及运行时接入与链路扩展。

### 2. 硬边界复述（必须）

- **OCR 只输出 raw text candidates**
- **不做文本语义提炼**
- **不接 YOLO**
- **不接中台**
- **不接 SceneTask/Fusion/Output**
- **不执行导航动作**
- **不真实播报**

### 3. 本阶段交付物（必须存在且一致）

- **能力定义**：`docs/architecture/LUNA_OCR_RAW_TEXT_CAPABILITY_DEFINITION_V0.md`
- **输出合同**：`docs/architecture/LUNA_OCR_RAW_TEXT_OUTPUT_CONTRACT_V0.md`
- **GT schema**：`docs/architecture/LUNA_OCR_RAW_TEXT_GROUND_TRUTH_SCHEMA_V0.md`
- **评测指标**：`docs/architecture/LUNA_OCR_RAW_TEXT_BENCHMARK_METRICS_V0.md`

### 4. GO 条件（全部满足）

- **OCR 原文职责清楚**：只做 raw text 候选输出，不越权产出语义/指令
- **输出 schema 清楚**：字段集合、bbox 表示、order、joined 规则明确且版本化
- **ground truth schema 清楚**：标注字段、组织方式、对齐建议明确
- **benchmark 指标清楚**：只包含原文识别指标，且说明对齐/归一化规则
- **明确不做语义提炼**：在所有相关文档中显式声明
- **明确后续由中台做文本内容提炼**：作为后置阶段（不在本阶段）

### 5. NO-GO 条件（任一触发）

- OCR 直接输出导航建议 / 指令（或等价字段/语义）
- OCR 直接判断场景结论
- OCR 直接进入任务链（SceneTask/Fusion/Output）
- OCR benchmark 混入语义理解指标（意图识别、任务决策、路线建议等）

### 6. 验收记录（v0）

本阶段为 definition-only，不要求真实模型跑分；但要求：

- 文档之间引用一致（字段命名一致、bbox 格式一致）
- README 索引已更新，能在架构索引中快速定位本阶段产物

