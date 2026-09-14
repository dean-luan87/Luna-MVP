## Phase-ModelOCR-002

OCR Candidate Inventory & Version Selection Go/No-Go Pack v0

### 1. 本阶段边界（必须）

- 只做 OCR 候选模型盘点与版本选择
- 不实现 runtime
- 不下载模型/权重
- 不跑 OCR
- 不接 YOLO
- 不接中台
- 不进 SceneTask/Fusion/Output
- 不执行导航动作
- 不真实播报
- 不做文本语义提炼（raw text only）

### 2. 产物清单（本阶段必须新增/更新）

新增：

- `docs/architecture/LUNA_OCR_CANDIDATE_INVENTORY_V0.md`（候选清单与优先级结论）
- `docs/architecture/LUNA_OCR_CANDIDATE_CAPABILITY_MATRIX_V0.md`（能力矩阵）
- `docs/architecture/LUNA_OCR_VERSION_SELECTION_POLICY_V0.md`（版本/分层选择策略）
- `docs/architecture/LUNA_OCR_CANDIDATE_RISK_REGISTER_V0.md`（风险登记）
- `docs/architecture/LUNA_OCR_CANDIDATE_INVENTORY_GO_NO_GO_PACK_V0.md`（本决策包）

修改：

- `docs/architecture/README.md`（索引挂载）

### 3. 候选池完整性（v0）

本阶段至少覆盖并分层：

- PaddleOCR / PP-OCR pipeline（A 类）
- macOS Vision OCR（C 类 fallback/对照）
- PaddleOCR-VL（B 类复杂版面）
- DeepSeek-OCR / OCR-2（B/C 类对照）

### 4. 推荐结论（v0）

排序与角色（冻结为 v0 口径）：

- **Priority 1**：PaddleOCR lightweight pipeline（PP-OCRv5 路线）→ 第一接入候选（raw text benchmark 主线）
- **Priority 2**：macOS Vision OCR → fallback / 对照候选
- **Priority 3**：PaddleOCR-VL → 复杂版面候选（非实时）
- **Priority 4**：DeepSeek-OCR / OCR-2 → 复杂文档对照候选（非第一接入源）

### 5. GO / CONDITIONAL_GO / NO_GO

#### GO 条件（全部满足）

- 候选池完整（至少覆盖上述四类）
- 每个候选能力矩阵完成（关键字段不缺）
- 第一接入候选明确（Priority 1）
- fallback/对照候选明确（Priority 2/4）
- 风险登记完成
- 本阶段未实现 runtime、未下载模型、未跑 OCR

#### CONDITIONAL_GO 条件（允许进入 ModelOCR-003，但需标注软跟进）

- 部分模型的版本/能力字段仍为 `unknown`，需要 ModelOCR-003 实装验证收敛
- 复杂模型（VL/DeepSeek）的输出形态需要后续基准验证与强约束
- 但第一接入候选足够明确且风险隔离清楚

#### NO_GO 条件（任一触发）

- 没有明确第一接入候选
- 把在线/API OCR 误设为默认主线或 Priority 1
- 未区分短文本 OCR 与复杂版面 OCR（A/B 分层缺失）
- 本阶段直接下载/接入 runtime/跑 OCR
- 盘点混入语义提炼或导航判断

### 6. 推荐下一阶段

- **Phase-ModelOCR-003**：Download/Manifest Readiness（仅做依赖与权重准备、manifest 固化、可复现性约束；仍不进入下游链路）

