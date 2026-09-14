# Simulation Lab crash_recovery × PaddleOCR Batch Recovery v0

**Phase**：`Phase-SimulationLab-CrashRecovery-PaddleOCR-BatchRecovery-001`  
**定位**：在 `crash_recovery` profile 下建立 PaddleOCR batch recovery **合同**、子命令建议、可选 child summary **merge** 与崩溃分类。**不默认运行** PaddleOCR heavy；不做 OCR 准确率；不生成 benchmark。

**能力**：`capabilities/evaluation/simulation_lab_crash_recovery_paddleocr_batch_recovery_v0.py`  
**Runner**：`tools/evaluation/simulation/run_simulation_lab_crash_recovery_paddleocr_batch_recovery_v0.py`  
**Verifier**：`tools/evaluation/simulation/verify_simulation_lab_crash_recovery_paddleocr_batch_recovery_v0.py`

**模式**：

- **materialize_only**（默认）：生成 contract + 建议命令；`recovery_status=pending_child_execution`
- **merge_child_summary**：`--child-summary /path/to/paddleocr_labeled_set_batch_recovery_summary.json`

**建议下一 phase**：`Phase-PaddleOCR-BatchRecovery-Manual-Execution-001`（实跑 child 后 re-merge）
