# LUNA Evaluation — PaddleOCR Labeled Set Quality Evaluation v0（Phase-PaddleOCR-Labeled-Set-Evaluation-001）

## 定位

在 **Materialize = GO** 与 **pinned manifest** 下，使用 **受控标注清单**（**20–50** 张，`ground_truth_text` 建议 **≥80%** 覆盖）对 PaddleOCR current API 做 **分层质量评估**（exact / CER、类别汇总、误识别与阅读顺序/多区域怀疑字段、复核队列），并输出运行时分位数与审计。

**只做**：evaluation-only 跑图、指标、报告、verifier。

**不做**：替换 RapidOCR、改 routing、runtime / 白盒 / MidPlatform、写世界模型、中台语义、provider 切换、下载模型、修改 pinned cache、无边界大规模评测；**不把本阶段 GO 解释为上线许可或质量达标**。

## 前置

- **Benchmark-001 = GO**（工程上表示评测链路已成立；本阶段可独立复跑）。  
- **`materialize_verdict == GO`**；**pinned manifest** 可读。  
- **清单**：`schema_version: paddleocr_labeled_set_manifest_v0`，每条含 **id、绝对路径 image_path、category、ground_truth_text（建议）**；可选 **ground_truth_items**（多行时用于简单阅读顺序一致性启发式）。

## 类别与覆盖

规范类别见 runner 内 **`CANONICAL_CATEGORIES`**。若某出现类别 **<3 张**，写入 **`category_undercovered`**；**严格 GO**（runner 与 verifier 对齐）要求 **无 undercovered** 且 **20≤n≤50**、**GT 覆盖≥0.8**、**全样本 predict 成功**、**审计无越界**。

## 工具

```text
python3 tools/evaluation/ocr/run_paddleocr_labeled_set_evaluation_v0.py \
  --repo-root <ABS_Luna-Core> \
  --materialize-root <ABS_MATERIALIZE_ROOT> \
  --pinned-manifest <ABS_PINNED_JSON> \
  --labeled-set-manifest <ABS_LABELED_SET_MANIFEST_JSON> \
  [--output-root <ABS_OUT>] \
  [--no-use-angle-cls]
```

```text
python3 tools/evaluation/ocr/verify_paddleocr_labeled_set_evaluation_v0.py \
  --labeled-set-root <ABS_OUT>
```

## 清单示例

`configs/evaluation/ocr/paddleocr_labeled_set_manifest_v0.example.json`（**20 张**，用于严格闸门联验；大批量连续推理内存占用高，若遇进程崩溃可拆批或换机重试）。

`configs/evaluation/ocr/paddleocr_labeled_set_manifest_v0.smoke.json`（**3 张**，仅 CI/烟测；**必然 CONDITIONAL_GO**，因 `n<20` 且类别覆盖不足）。

## 产物

`paddleocr_labeled_set_*.json`、`paddleocr_labeled_set_notes.md`、`paddleocr_labeled_set_verifier_report.json`。

**冻结 verdict 与治理 phase 分离归档**：`LUNA_EVALUATION_PHASE_ARCHIVE_PADDLEOCR_LABELED_SET_EVALUATION_001_V0.md`。全量稳定性拆批见：**Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001**（`LUNA_EVALUATION_OCR_PADDLEOCR_LABELED_SET_BATCH_RECOVERY_V0.md`）。
