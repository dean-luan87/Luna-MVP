# Public Facility Runtime DryRun — GO / NO_GO Pack v0

## GO

- `runtime_scope=dry_run_only`，`semantic_first_required=true`，`default_ocr_mainline_allowed=false`
- 6 fixtures（含 Toliet typo、ambiguous hold）
- semantic/correction/evidence/gate/speak/risk/metrics/benchmark-link 完整
- Toliet `raw_ocr_text_preserved`；`correction_committed=false`；ambiguous `hold_for_review`
- cautious speak 仅候选文案；`tts_invoked=false`；无强断言措辞
- audit 全 no-OCR/no-write/no-TTS；verifier **GO**

## CONDITIONAL_GO

- 部分 fixture 细节待补，但 Toliet/ambiguous/gate/audit 完整且无越界

## NO_GO

- 运行 OCR/Vision；覆盖 raw_ocr_text；纠错提交为事实；强断言播报；写事实层；TTS；改 routing

## 下一 phase

Benchmark Collector Real Values Smoke（显式 phase）；或 RealVideo OCRRequest gated submission。
