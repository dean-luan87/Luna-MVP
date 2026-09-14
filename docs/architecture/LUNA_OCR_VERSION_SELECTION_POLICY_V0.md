## Phase-ModelOCR-002

OCR Version Selection Policy v0

### 0. 目的

定义“第一接入候选 / 复杂候选 / fallback 候选 / 对照候选”的选择规则与优先级，确保进入 ModelOCR-003 前已经完成分层与风险隔离。

### 1. 硬边界（必须持续成立）

- OCR 主线当前只做 **raw text candidates**（读到了什么原文）
- 不做文本语义提炼（后置到中台阶段）
- 不接 YOLO / 不接中台 / 不进 SceneTask/Fusion/Output
- 本阶段（ModelOCR-002）不实现 runtime，不下载模型，不跑 OCR

### 2. 候选分层选择规则（A/B/C）

#### 2.1 A 类：轻量导航 OCR（第一接入候选）

选择门槛（must-have）：

- 本地离线可运行（CPU 优先）
- 输出结构化：bbox + confidence（或可明确获取）
- 中文/英文/数字支持
- 输入支持视频帧（image/frame）
- 依赖复杂度可控（可打包/可复现）

推荐：

- **PaddleOCR pipeline（优先走 PP-OCRv5 路线）**

版本口径：

- 工具链版本以 PaddleOCR GitHub release 为准（例如 `v3.5.0`）
- 具体 det/rec/cls 权重版本在 ModelOCR-003 才落到 manifest（本阶段只冻结“优先选 PP-OCRv5 能力路径”）

#### 2.2 B 类：复杂版面 OCR / OCR-VL（复杂候选）

选择门槛：

- 版面/复杂元素能力优先（表格/公式/屏幕/图文混排）
- 允许 GPU/更高依赖；不得进入实时链
- 输出形态若偏“文档转 markdown”，必须能在后续阶段被严格约束为 raw text candidates（禁止语义总结）

推荐：

- **PaddleOCR-VL（如 VL-1.5）**：复杂文档解析候选
- **DeepSeek-OCR / OCR-2**：复杂文档对照候选（依赖重，默认不作为第一接入）

#### 2.3 C 类：对照模型 / fallback（系统级）

选择门槛：

- 本机可用、低依赖
- 可输出 text + confidence；bbox 若为归一化坐标可转换即可
- 用途限定：对照/ fallback，不作为主线第一接入源

推荐：

- **macOS Vision OCR（VNRecognizeTextRequest）**

### 3. 优先级排序（v0 冻结）

- **Priority 1（第一接入候选）**：PaddleOCR lightweight pipeline（PP-OCRv5 路线）
- **Priority 2（fallback/对照）**：macOS Vision OCR
- **Priority 3（复杂版面）**：PaddleOCR-VL
- **Priority 4（复杂文档对照）**：DeepSeek-OCR / OCR-2

### 4. 输出格式风险（必须在后续阶段约束）

对“生成式/文档解析型 OCR”候选（如 VL/DeepSeek）必须强约束：

- 只允许输出 raw text candidates（text/bbox/conf/frame/model/order/joined）
- 禁止输出 semantic summary / navigation instruction / task decision

### 5. 进入 ModelOCR-003 的准入条件（本阶段给出的口径）

允许进入 ModelOCR-003（下载/manifest 准备）当且仅当：

- 候选池完整 + A/B/C 分层明确
- 第一接入候选明确（Priority 1）
- fallback/对照候选明确（Priority 2/4）
- 风险登记完成（依赖/权重/在线/API/GPU/许可证/复现）

