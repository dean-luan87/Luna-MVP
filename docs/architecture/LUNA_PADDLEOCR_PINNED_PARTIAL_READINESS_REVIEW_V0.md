# LUNA — PaddleOCR Pinned Partial Readiness Review v0

## Phase

- **Phase-ModelOCR-003-Fix-004**
- **Subject:** HF acquire 之后的 **pinned_partial** 复审与收口（不接 OCR runtime、不跑 benchmark）。

## Hard boundaries（本阶段）

- 不进入 OCR runtime；不执行 OCR 推理或 benchmark。
- 不接 YOLO、中台、SceneTask/Fusion/Output；不做语义提炼；不执行导航；不真实播报。
- 复审仅基于：**权重落盘 + prepare + readiness 工具输出 + manifest**，不将「未安装 paddle」误判为 acquire 失败。

---

## 1. HF acquire 结果摘要

| 项 | 状态 |
|----|------|
| 来源 | Hugging Face：`PaddlePaddle/PP-OCRv5_mobile_det`、`PaddlePaddle/PP-OCRv5_mobile_rec` |
| 格式 | PP-OCRv5 HF 布局：`inference.json` + `inference.pdiparams`（同目录） |
| acquire 工具 | `tools/acquire_paddleocr_weights_v0.py`，`--source-type huggingface`，`--cls-optional` |
| 记录日志（示例） | `logs/paddleocr_alternative_acquire_hf.json` |
| 工具顶层结果 | `ok: true`，`hard_blockers: []` |

---

## 2. det / rec 路径、sha256、source_url（权威摘录）

**Pinned 目标根目录（prepare 输出）：** `models/ocr/paddleocr_ppocrv5/`（det/rec 子目录由 prepare 复制生成；file-level 权威见 `models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json`）。

**Staging 示例路径（某次运行；用于对照 acquire 日志）：**  
`logs/paddleocr_acquire_staging_<timestamp>/hf_det`、`.../hf_rec`。

**核心文件（det — PP-OCRv5_mobile_det）：**

| 文件 | sha256 | source_url |
|------|--------|------------|
| `inference.json` | `05feef1acb00aa4cd7362b15f7f501fc4f99d7b1fa73c1c871e0c7b1504b0f5c` | `https://huggingface.co/PaddlePaddle/PP-OCRv5_mobile_det/resolve/main/inference.json` |
| `inference.pdiparams` | `afa1820cb16c1fd0dad589d0f8b389139061c1ef6d68019685fd07be997dda5b` | `https://huggingface.co/PaddlePaddle/PP-OCRv5_mobile_det/resolve/main/inference.pdiparams` |

**核心文件（rec — PP-OCRv5_mobile_rec）：**

| 文件 | sha256 | source_url |
|------|--------|------------|
| `inference.json` | `24587345250c7332d0fc6f9a44e794d078cdaeb64c302fef906f325619de2569` | `https://huggingface.co/PaddlePaddle/PP-OCRv5_mobile_rec/resolve/main/inference.json` |
| `inference.pdiparams` | `2460da90875937c94db97eba74ae3d9e5d4c4c57c42f1f41531c09a26bcc771a` | `https://huggingface.co/PaddlePaddle/PP-OCRv5_mobile_rec/resolve/main/inference.pdiparams` |

同目录另含 `inference.yml`、`config.json` 等辅助文件，均在 acquire 的 `downloads[]` 中有记录。

---

## 3. cls 当前状态

| 项 | 值 |
|----|-----|
| `cls_dir`（acquire 发现） | `null`（未获取 cls 权重） |
| 本阶段策略 | **cls 对第一阶段 raw text 可选**：与 `--cls-optional` 一致；manifest/readiness 侧表现为 partial |
| 能力声明 | 见 `LUNA_PADDLEOCR_PINNED_PARTIAL_CAPABILITY_BOUNDARY_V0.md`（旋转/方向校正不声明） |

---

## 4. dependency_check 当前状态（不阻断权重线）

记录在 acquire 日志中的 **import 探针**（示例 `.venv-tx`）：

| module | import_ok |
|--------|-----------|
| paddleocr | false |
| paddle | false |
| PIL | false |
| cv2 | true |
| numpy | true |

**结论：** 缺失推理依赖 **不否定** HF acquire / prepare / file-manifest 成功；它阻断的是「在同一 venv 内实际跑 Paddle 推理」与 **004B 中 adapter 的 dependency readiness**。adapter 设计应采用 **fail-closed**：依赖不齐则声明不可用并拒绝初始化推理，而非伪造 ready。

---

## 5. readiness 为 partial 的主要原因

1. **`weights_source=pinned_partial`**：det+rec 已 pinned，cls 未纳入（与 optional 策略一致）。
2. **readiness 工具**返回 `readiness_status=partial`（与 manifest 的 partial 语义一致）。
3. **推理依赖未安装**可导致「运行时 full ready」在后续阶段才可达成；本阶段不把其算作 acquire **hard_blocker**。

---

## 6. pinned_partial 是否成立

**成立。** 依据：`prepare.returncode=0`，`readiness.ok=true`，`hard_blockers=[]`，det/rec 均有可追溯 hash 与 `source_url`，且符合 `LUNA_PADDLEOCR_PINNED_WEIGHTS_GO_NO_GO_PACK_V0.md` 中 **CONDITIONAL_GO** 条件。

---

## 7. Go / CONDITIONAL_GO / NO_GO 结论

| 维度 | 结论 |
|------|------|
| PaddleOCR **权重获取线**（替代源 HF） | **CONDITIONAL_GO**（相对默认托管路径曾 NO_GO） |
| **pinned_partial**（资产+manifest+readiness） | **成立** |
| 全量 **full ready**（含 cls + 推理依赖 + ready 状态） | **未达成**（预期内） |

---

## 8. hard_blockers / soft follow-ups

- **hard_blockers：** 无（与 acquire 日志一致）。
- **soft follow-ups：**
  - 可选：补充 cls 权重并重新 prepare，或继续在 manifest 中固定 `cls_optional` 与能力边界文档。
  - 004B 前：在专用文档或 checklist 中记录 **dependency readiness**（`paddlepaddle` / `paddleocr` / `Pillow`），与 benchmark（005）隔离。

---

## 9. 推荐下一阶段（执行顺序建议）

1. **ModelOCR-003-Fix-004（本文）**：收口 pinned_partial（已完成文档化目标）。
2. **ModelOCR-004A：** macOS Vision OCR raw text harness（与 Paddle 权重解耦，可并行）。
3. **ModelOCR-004B：** PaddleOCR raw text adapter skeleton；**须** dependency readiness 或 **fail-closed**，不接主 OCR runtime。
4. **ModelOCR-005：** OCR raw text ground truth benchmark（独立门禁）。

---

## 验收输出（索引）

1. **新增/修改文件路径：** 见本节仓库变更清单（以 PR/提交为准）；核心为本文 + `LUNA_PADDLEOCR_PINNED_PARTIAL_CAPABILITY_BOUNDARY_V0.md` + 两份 GO_NO_GO pack 追加节 + `README.md` 索引。
2. **各文件一句话：** 见 `docs/architecture/README.md` 对应条目。
3. **—12.** 正文 §1—§8 与边界文档已覆盖：HF 摘要、路径/hash/url、cls、依赖、partial 原因、边界、Go 结论、blockers、follow-ups、阶段建议。

**Cross-reference:** `LUNA_PADDLEOCR_PINNED_PARTIAL_CAPABILITY_BOUNDARY_V0.md`，`LUNA_PADDLEOCR_ALTERNATIVE_WEIGHT_SOURCE_GO_NO_GO_PACK_V0.md`（Fix-004 记录节），`LUNA_PADDLEOCR_PINNED_WEIGHTS_GO_NO_GO_PACK_V0.md`（记录节）。
