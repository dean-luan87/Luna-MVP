## Phase-ModelOCR-001

OCR Independent Raw Text Capability Definition v0

### 1. 本阶段范围（Definition-only）

本阶段**只定义**“OCR 原文（raw text）识别能力”，用于离线工程评测与对比。

- **只输出 raw text candidates**（见输出合同）
- **不做语义提炼**（不总结、不解释、不归因、不指令化）
- **不接 YOLO**
- **不接中台**
- **不接 SceneTask / Fusion / Output**
- **不执行导航动作**
- **不触发真实播报**

### 2. 能力定位（职责）

OCR 在本阶段的职责仅为：

- 把一帧图像中的文字区域识别为**可追溯的原文候选**（raw text candidates）
- 为“多模型原文对比”提供统一输出口径
- 为“人工标注 ground truth”与“原文级评测指标”提供稳定的合同与 schema

### 3. 明确禁止（能力非目标）

OCR **不输出**以下任何内容（即使模型内部可能具备相关能力，本阶段也不允许产出）：

- navigation instruction（导航指令/建议）
- scene conclusion（场景结论）
- task decision（任务决策）
- semantic summary（语义摘要/总结/提炼）
- route advice（路线建议）
- final output text（最终播报文本）

### 4. 输出形态（Raw Text Candidates）

OCR 当前只输出 raw text candidates，每个候选至少包含：

- `text`
- `bbox`
- `confidence`
- `frame_id`
- `model_config_id`
- `line_order`
- `raw_text_joined`

详见：`docs/architecture/LUNA_OCR_RAW_TEXT_OUTPUT_CONTRACT_V0.md`

### 5. 多模型原文对比（定义）

多模型对比的单位是 **frame-level** 的 raw text candidates 集合，对比包括：

- **逐行对比**：按 `line_order`（或 bbox 的阅读顺序规则）对齐后比较 `text`
- **区域对比**：按 `bbox` 进行 IoU/匹配阈值对齐（允许不同模型行切分差异）
- **聚合对比**：使用 `raw_text_joined` 做整帧原文对比（便于快速回归）

对比产物属于评测侧（离线）；OCR 能力本身只需保证输出合同稳定、可追溯。

### 6. Ground Truth（人工标注）定义

本阶段定义 ground truth 的最小 schema（面向原文），用于原文级评测，不包含语义标签。

详见：`docs/architecture/LUNA_OCR_RAW_TEXT_GROUND_TRUTH_SCHEMA_V0.md`

### 7. 原文级评测指标（定义）

本阶段只允许进入验收的指标是**原文识别**指标（字符/词/行/区域级），不允许混入语义理解指标。

详见：`docs/architecture/LUNA_OCR_RAW_TEXT_BENCHMARK_METRICS_V0.md`

### 8. 独立验收（GO/NO-GO）

本阶段的 GO/NO-GO 决策仅基于：

- 职责边界清晰
- 输出 schema 清晰
- ground truth schema 清晰
- benchmark 指标清晰
- 明确“语义提炼后置到中台阶段”

详见：`docs/architecture/LUNA_OCR_RAW_TEXT_GO_NO_GO_PACK_V0.md`

