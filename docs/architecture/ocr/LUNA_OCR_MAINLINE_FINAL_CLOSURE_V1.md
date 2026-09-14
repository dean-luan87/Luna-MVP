# Luna — OCR Mainline Final Closure v1

**Phase**：`Phase-OCR-Mainline-Final-Closure-v1-001`  
**性质**：closure / consolidation / handoff only；**不**新增 OCR runtime 能力

## 目标

对当前 OCR 主线做最终收口，明确：

- OCR 主线已经完成到什么程度
- 哪些能力已经过 governance / dry-run / reference / gated / readonly / regression 验证
- 哪些能力仍然只是 candidate / reference-only / no-fact
- OCR 与 `Static Reading` / `Poster` / `RealVideo` / `Memory` / `WorldModel` / `Minimal Runtime Integration` 的关系
- OCR 主线是否还能继续扩展
- 主线应否正式交还给 **视角强化**

## 当前收口结论

OCR 主线当前只收口到：

- governance baseline
- gated path baseline
- reference-only baseline
- candidate / readonly baseline
- no-runtime / no-write baseline

它**不等于**：

- 生产 OCR runtime
- 已启用 OCR provider
- 已提交 `OCRRequest`
- 已写入 `WorldModel` / `Memory` / `Fact`
- 已生成 `Scene Delta`
- 已进入真实 benchmark

## 已完成阶段矩阵（收口视角）

本次收口至少覆盖并归档以下阶段：

- `RealVideo OCR Text-Bearing Sample Planning`
- `Mixed Video Poster Batch Smoke v2 Gated Path Only`
- `OCR Evidence Pack Adapter v1`
- `ROI Crop Execution DryRun`
- `ROI-to-OCRRequest Reference`
- `ROI BBox Expansion Proposal`
- `Better Frame Extraction DryRun`
- `BBox Adjustment Proposal v2 Multiframe`
- `Static Readable Region Discovery Guidance Policy`
- `Hardware Camera Control Contract`
- `WorldModel Lookup for Reading Framework`
- `OCR StaticReading Poster RealVideo Regression Route Compliance`
- `Minimal Runtime Integration Closure`

## 已验证内容

- OCR activation governance 已存在并冻结在 policy 层
- OCRRequest reference 路径已存在，但仍是 reference-only
- ROI crop / better-frame / bbox proposal 路径已形成 dry-run 或 proposal 链
- gated path 已替代 direct provider bypass
- Evidence Pack adapter 已支持 scan observation alignment
- `scan_observation` 不是 OCR text primary evidence
- `SQ_E` / 低质量输入不会默认进入 OCR
- full-frame OCR 默认禁止
- `Static Reading` 必须先经过 readable region discovery
- Poster OCR 保持 segment-first / governance-first 逻辑
- `RealVideo` 侧仅收口到 planning / readonly / reference，不进入 benchmark execution
- empty OCR text 不自动等于失败，也不自动等于 fact
- `Memory` / `WorldModel` 写入仍保持关闭
- OCR 后续只能作为视觉主线的 candidate / reference / verification 辅助层

## 仍然关闭的能力

以下能力在本阶段后仍明确保持关闭：

- real OCR provider runtime
- `OCRRequest` actual submission
- PaddleOCR runtime
- RapidOCR runtime
- DeepSeek OCR runtime
- camera runtime
- frame sampling runtime
- detector runtime
- segmentation runtime
- tracking runtime
- provider comparison benchmark
- benchmark accuracy update
- `Memory` write
- `WorldModel` write
- `Fact` write
- `Scene Delta` commit
- navigation action
- task commit
- map API

## 非声明项

本收口必须明确：

- OCR closure **不等于** 生产 OCR runtime
- OCRRequest reference **不等于** OCRRequest submitted
- crop/reference artifact **不等于** provider executed
- Evidence Pack candidate **不等于** fact
- scan observation **不等于** OCR text evidence
- semantic candidate **不等于** `WorldModel` write
- readable region candidate **不等于** detected text fact
- static reading handoff **不等于** camera capture
- RealVideo planning **不等于** 真实视频 OCR benchmark
- Minimal Runtime Integration text-only output **不等于** 真实语音输出
- OCR 主线不得绕过 `STC` / `SourceQuality` / `Readability` / `OCRRequest gate`

## 与其他主线的关系

### Static Reading

OCR 只作为 `readable region -> static capture/OCR gate` 之后的未来候选链，不能跳过 readable region discovery。

### Poster

Poster OCR 继续保持 `segment-first / governance-first / gated-path-first`，本收口不把 Poster 路径升级为生产 OCR。

### RealVideo

RealVideo 侧只保留 text-bearing sample planning、readonly consumer、reference closure 等规划/归档价值；不在本阶段进入真实采帧、真实 OCR 或 benchmark。

### Memory / WorldModel

OCR 当前只能提供 lookup/reference/candidate 价值；不能写 `Memory`、不能写 `WorldModel`、不能升格为 fact。

### Minimal Runtime Integration

OCR 收口必须与 `Minimal Runtime Integration Closure v1` 对齐，即当前系统只收口到 `text-only controlled output baseline`，并继续保持 no-runtime / no-write 边界。

## 延后能力池

以下能力明确延后，且**不进入下一阶段主线**：

- real OCR provider integration
- PaddleOCR heavy runtime
- RapidOCR runtime execution
- DeepSeek OCR / remote heavy OCR
- OCRRequest actual submission
- provider comparison benchmark
- real camera capture
- real frame sampling
- real crop generation from live stream
- text detector runtime
- segmentation / tracking assisted OCR
- WorldModel OCR fact write
- Memory OCR write
- Scene Delta generation
- public facility semantic correction runtime
- Poster OCR production route
- RealVideo OCR benchmark execution

## 主线交接

OCR 在后续视觉主线中的角色：

- candidate/reference evidence provider
- text-region hint provider
- readable-region support
- posterior verification tool
- worldmodel verification candidate，**不是** fact writer
- map/route scene label auxiliary source，**不是** route authority

下一主线优先级：

- `Phase-Return-To-Vision-Mainline-Planning-v1-001 = GO`
- `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`
- viewpoint segmentation / view slicing
- object tracking
- visual candidate stabilization
- map / route / location context integration
- basic navigation loop strengthening

## 最终结论

`OCR Mainline` 到此完成最终收口。  
它正式停留在 **governance / gated / reference / candidate / readonly / no-write baseline**，不再继续扩展 OCR 主线，不启用真实 provider runtime，不写 `WorldModel` / `Memory` / `Fact`，主线正式交还给 **视角强化规划**。  
该规划阶段现已由 `Return-To-Vision-Mainline-Planning-v1-001` 正式冻结完成，下一阶段固定为 `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`。

## 实现

- `capabilities/midplatform/ocr_mainline_final_closure_v1.py`
- `tools/evaluation/ocr/run_ocr_mainline_final_closure_v1.py`
- `tools/evaluation/ocr/verify_ocr_mainline_final_closure_v1.py`

说明：`capabilities/ocr` 当前尚未设立，本阶段 capability 暂放 `midplatform`；后续如 OCR capability layer 独立，可迁移。
