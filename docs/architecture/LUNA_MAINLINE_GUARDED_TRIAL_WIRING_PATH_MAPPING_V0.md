# LUNA Guarded Trial Wiring Path Mapping v0

**Phase**：Phase-Mainline-RuntimeReadiness-003  
**定位**：将 Phase-002 的三条 trial 闸门 **映射到仓库内候选文件/符号**，并产出 **默认关闭** 的 gate 快照；**不启用真实 trial、不调 provider、不播报、不跑 TTS**。

---

## 产物与工具

| 工具 | 作用 |
|------|------|
| `tools/evaluate_mainline_guarded_trial_wiring_path_v0.py` | 静态生成 wiring matrix、gate decisions、TRW/abort 矩阵 |
| `tools/verify_mainline_guarded_trial_wiring_path_v0.py` | 校验默认全关、global kill、无效模式、矩阵齐全 |

输出目录示例：`logs/mainline_guarded_trial_wiring_path_003_<timestamp>/`。

---

## 三条线的接线候选（摘要）

- **YOLO**：`model_perception/yolo_shadow_adapter_v0.py`（帧/检测）、`core_trw/yolo_request_trace_shadow_adapter_v0.py`（RequestTrace）、`runtime_readiness/guarded_trial_abort_rollback_hooks_v0.py`（abort/rollback 占位）。
- **OCR**：`model_ocr/offline_source_policy_v0.py`、`model_ocr/yolo_ocr_bridge_v0.py`、`core_trw/ocr_request_trace_shadow_adapter_v0.py`、同上 abort/rollback。
- **Qwen Voice**：`voice/output/voice_output_governance_v0.py`、`voice/output/governed_voice_provider_entry_v0.py`、`voice/runtime/tts_unified_entry.py`、`voice/output/voice_output_plane_v1.py`、`voice/output/voice_output_trw_adapter_v0.py`、同上 abort/rollback。

完整表见生成文件：`mainline_guarded_trial_wiring_path_matrix.json`（含 `allowed_in_phase_003`: `mapping_only` | `gate_stub_only`）。

---

## 代码模块（Phase-003 新增）

- `capabilities/runtime_readiness/guarded_trial_gate_v0.py`：global kill、分项 env、mode 解析、gate decision。
- `capabilities/runtime_readiness/guarded_trial_trw_validator_v0.py`：TRW 字段校验骨架。
- `capabilities/runtime_readiness/guarded_trial_abort_rollback_hooks_v0.py`：abort/rollback 占位。

详见：`LUNA_MAINLINE_GUARDED_TRIAL_GATE_AND_GLOBAL_KILL_SWITCH_V0.md`。
