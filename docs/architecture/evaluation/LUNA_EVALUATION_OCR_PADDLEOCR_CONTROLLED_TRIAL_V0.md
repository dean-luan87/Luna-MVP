# LUNA Evaluation — PaddleOCR Controlled Trial v0（Phase-PaddleOCR-Controlled-Trial-001）

## 定位

**独立 phase**：在 **CacheMaterialize-001 = GO** 且 **pinned manifest** 可读的前提下，于 **evaluation 工具** 内：

- **Layer 1**：`PaddleOCR()` **constructor compatibility**（可实例化、参数与路径组合是否被当前 API 接受）。  
- **Layer 2**（仅 Layer 1 成功后）：**≤3 张**本地固定图的最小 **离线 OCR** 调用（`ocr()`），验证可序列化结果与审计字段。

**不是**：主线接入、默认 provider、RapidOCR 替换、OCR routing 变更、白盒 / MidPlatform、性能 benchmark、中台语义解释、可上线结论。

## 前置

- **materialize_root** 下 **`paddleocr_manifest_v1_cache_materialize_summary.json`** 中 **`materialize_verdict == GO`**。  
- **`snapshot/paddleocr_manifest_v1_pinned_manifest_candidate.json`**：`pinning_complete=true`、`missing_ref_count=0`、`sha256_by_file` 非空。

## cls 保守说明

Pinned **cls** 可能来自 **PP-LCNet_x1_0_textline_ori**（与经典 **`ch_ppocr_mobile_v2.0_cls`** 不一定等价）。**CacheMaterialize GO** 只证明 **manifest / cache / hash / completion 工具链**；**Controlled Trial** 负责记录 **constructor / 最小 OCR** 与 **cls 兼容性观察**；若 cls 导致失败，**trial_verdict** 不得强行 **GO**。

## 工具

```text
python3 tools/evaluation/ocr/run_paddleocr_controlled_trial_v0.py \
  --repo-root <ABS_Luna-Core> \
  --materialize-root <ABS_MATERIALIZE_ROOT> \
  --pinned-manifest <ABS_PINNED_JSON> \
  [--output-root <ABS_TRIAL_OUT>] \
  [--constructor-only] \
  [--no-use-angle-cls] \
  [--image <ABS_IMG> ... 最多 3 次]
```

```text
python3 tools/evaluation/ocr/verify_paddleocr_controlled_trial_v0.py \
  --trial-root <ABS_TRIAL_OUT> \
  [--materialize-root <ABS_MATERIALIZE_ROOT>]
```

## 产物

见 `run_paddleocr_controlled_trial_v0.py` 写出的 **`paddleocr_controlled_trial_*.json`**、**`paddleocr_controlled_trial_notes.md`**；verifier 追加 **`paddleocr_controlled_trial_verifier_report.json`**。
