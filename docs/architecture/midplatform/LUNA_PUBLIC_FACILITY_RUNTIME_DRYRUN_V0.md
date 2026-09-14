# Public Facility Runtime DryRun v0

**Phase**：`PublicFacility-Runtime-DryRun-001`  
**定位**：将 PublicFacility Semantic Correction Governance 推进到 **semantic-first runtime dry-run**（6 fixture stubs、语义/纠错候选、证据组合、gate dry-run、cautious speak 候选）。**不运行 OCR/Vision**，不写事实层，不 TTS，不改 routing。

**前置**：Governance GO；v1 Track Closures `closed_for_evaluation`；Benchmark Real Values Planning GO。

**能力**：`capabilities/midplatform/public_facility_runtime_dryrun_v0.py`  
**Runner**：`tools/evaluation/midplatform/run_public_facility_runtime_dryrun_v0.py`  
**Verifier**：`tools/evaluation/midplatform/verify_public_facility_runtime_dryrun_v0.py`

**核心原则**：`semantic_first_required=true`，`default_ocr_mainline_allowed=false`；OCR 仅 auxiliary；`Toliet` 保留 raw；ambiguous → `hold_for_review`。

**Benchmark Real Values Smoke** 已消费本 dry-run 的 T1 功能计数。建议下一 phase：Simulation Lab crash_recovery；或 Poster/RealVideo 门控执行线。
