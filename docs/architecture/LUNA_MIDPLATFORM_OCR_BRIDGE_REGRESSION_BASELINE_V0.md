# LUNA — MidPlatform OCR Bridge Regression Baseline v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-003**

## Purpose

冻结 Bridge-003 回归的 baseline：输入 roots、硬门槛、允许波动项、不允许波动项，为后续回归提供一致口径。

## Baseline roots（示例集合）

（此处为 Bridge-003 参考集合；实际运行时由 regression runner 的 `--roots` 指定）

- sample_matrix output root
- yolo_ocr_bridge_root output root（含 expansion）
- ocr_benchmark_root output root

## Hard gates（必须满足）

- 每个 root 可读
- required output files 齐全
- 每个 root 的 `verification_result.json` 为 GO（或等价通过）
- trace/replay/whitebox 非空
- `semantic_summary=null`
- `navigation_action=null`
- `allows_execute_now=false`
- `real_tts_invoked=false`
- `downstream_invocation_count=0`
- blocked evidence retained（`retained_evidence_ref` 不缺失）

## Allowed to fluctuate（允许波动）

- candidate 数量（text/world/ambient）
- raw text 内容
- `visual_text_relevance_class` 分布
- `delta_decision` 分布

## Must not fluctuate（不允许波动）

- 任意 `semantic_summary` 非 null
- 任意 `navigation_action` 非 null
- 任意 TTS invoked / downstream invocation
- 任意真实世界模型写入（本阶段禁止项）
- trace/replay/whitebox 缺失或为空
- blocked evidence 被删除或缺失 `retained_evidence_ref`

