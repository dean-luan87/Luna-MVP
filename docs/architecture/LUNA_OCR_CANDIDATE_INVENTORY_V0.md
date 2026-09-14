## Phase-ModelOCR-002

OCR Candidate Inventory & Version Selection v0

### 0. 本阶段边界（Definition-only）

本阶段只做 OCR 候选模型盘点与版本选择口径，不做任何实现与运行：

- 不实现 runtime
- 不下载模型/权重
- 不跑 OCR
- 不接 YOLO
- 不接中台
- 不进 SceneTask/Fusion/Output
- 不执行导航动作
- 不真实播报
- 不做文本语义提炼（只盘点“能读原文”的能力）

### 1. 本阶段目标

回答并冻结以下事实（用于进入 ModelOCR-003 的“下载/manifest 准备阶段”）：

- 候选 OCR 模型有哪些、各自的最新/可用版本是什么
- 是否可本地离线运行（CPU/GPU）
- 是否需要联网/API Key
- 是否支持中文/英文/数字
- 是否输出 bbox/confidence
- 是否支持方向/旋转文字、复杂版面
- 依赖与权重下载方式（但本阶段不下载）
- 哪些适合第一接入（raw text benchmark 主线）
- 哪些仅作为复杂候选或对照/ fallback

### 2. 候选池（至少）

#### 2.1 PaddleOCR（轻量 pipeline，PP-OCR 系列）

- **candidate_id**: `paddleocr_ppocr_pipeline`
- **model_family**: PaddleOCR / PP-OCR
- **current_version（工具链）**: PaddleOCR `v3.5.0`（2026-04-21 GitHub release）
  - source: `https://github.com/PaddlePaddle/PaddleOCR/releases/tag/v3.5.0`
- **核心方向**: 传统两阶段 pipeline（det + rec），强调轻量、可部署、bbox/confidence 结构化输出友好
- **PP-OCRv5**: 新一代识别/检测方案（mobile/server 等变体）；更适合“轻量导航 OCR（A 类）”作为第一接入优先
  - doc: `https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5.html`

#### 2.2 PaddleOCR-VL（复杂版面 OCR / OCR-VL）

- **candidate_id**: `paddleocr_vl_series`
- **model_family**: PaddleOCR-VL
- **current_version（代表性模型）**: PaddleOCR-VL-1.5（2026）
  - paper: `https://arxiv.org/abs/2601.21957v1`
  - weights/model card: `https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5`
- **核心方向**: 文档解析、复杂元素（表格/公式/图表/版面）与更强的鲁棒性；通常更重、更偏离“实时导航短文本”
- **定位**: B 类（复杂版面/公告/屏幕/图文混排）候选；不作为实时第一源

#### 2.3 DeepSeek-OCR / DeepSeek-OCR-2（复杂文档理解对照候选）

- **candidate_id**: `deepseek_ocr_family`
- **model_family**: DeepSeek-OCR / DeepSeek-OCR-2
- **current_version**:
  - DeepSeek-OCR（repo）：`https://github.com/deepseek-ai/DeepSeek-OCR`
  - DeepSeek-OCR-2（repo）：`https://github.com/deepseek-ai/DeepSeek-OCR-2`（2026-01）
- **核心方向**: 更接近 VLM/压缩式端到端文档转文本（常见 prompt 输出 markdown 等）
- **定位**: B/C 类（复杂文档对照）；通常 GPU/依赖重，不适合作为第一接入源

#### 2.4 系统级 OCR / 本地 fallback（macOS Vision OCR）

- **candidate_id**: `macos_vision_ocr`
- **model_family**: Apple Vision `VNRecognizeTextRequest`
- **current_version**: macOS 系统框架（随 OS/Xcode）
  - doc: `https://developer.apple.com/documentation/vision/recognizing_text_in_images`
- **离线能力**: on-device（设备端执行，强调隐私/性能）
- **输出能力**: 可返回识别文本与置信度；可通过 observation/candidate boundingBox 获取 bbox（归一化坐标，可转像素坐标）
- **定位**: C 类（本机 fallback / 对照候选），便于 Mac 开发环境快速对照与低依赖备选

### 3. 候选分层（A/B/C）

#### A 类：轻量导航 OCR（优先）

用途：门牌号/出口牌/科室牌/楼层牌/地铁方向牌/公交线路号/短警示牌

要求（优先级从高到低）：

- 本地可跑优先（CPU 优先，GPU 可选）
- 中文/英文/数字支持
- bbox + confidence 必须优先
- 低延迟、低依赖

建议候选：

- PaddleOCR（PP-OCRv5 pipeline）

#### B 类：复杂版面 OCR / OCR-VL（非实时/离线候选）

用途：公告牌/医院流程图/屏幕文字/图文混排说明/表格/长文本

要求：

- 准确率、版面能力优先
- 可作为离线/非实时候选，不进入实时链

建议候选：

- PaddleOCR-VL（例如 VL-1.5）
- DeepSeek-OCR / OCR-2（通常更重，更偏“文档→文本”）

#### C 类：对照模型 / fallback

用途：横向比较、系统级 fallback、低依赖备选

建议候选：

- macOS Vision OCR（on-device）

### 4. 推荐结论（v0）

在不做下载/跑分的前提下，基于离线可用性/依赖复杂度/结构化输出能力，推荐排序如下：

- **Priority 1**：PaddleOCR lightweight pipeline（PP-OCR 系列，优先 PP-OCRv5 能力路径）  
  角色：第一接入候选，负责 raw text benchmark 主线。
- **Priority 2**：macOS Vision OCR（系统 OCR fallback / 对照）  
  角色：本机 fallback / 对照候选。
- **Priority 3**：PaddleOCR-VL（复杂版面/公告/屏幕候选）  
  角色：复杂文档分支候选，不作为实时第一源。
- **Priority 4**：DeepSeek-OCR / OCR-2（复杂文档理解对照）  
  角色：对照候选，不作为第一接入源。

### 5. 下一阶段建议（ModelOCR-003）

进入“下载/manifest 准备阶段”之前应满足：

- 已完成候选清单、能力矩阵、版本选择策略、风险登记与 GO/NO-GO pack
- 仍保持“raw text only”的主线口径（语义提炼后置中台）

