# LUNA Voice — Governed Entry RequestTrace Test Matrix v0（Phase-Voice-Qianwen-003）

**输入**：Phase-002 online/offline **dry-run** 根目录。

---

## 1. 矩阵列（`voice_qwen_provider_mode_comparison_matrix.json`）

| 字段 | 期望 |
|------|------|
| selection_consistent_with_policy | 各样本 **online/offline** 与 governance **final_action** 一致 |
| qwen_only_online | **offline** 行永不包含 **qwen** |
| hard_audit_ok | **hard_audit** 不变量成立 |

---

## 2. 样本级期望（与 Phase-002 一致）

- **accepted_dry_run**：online **qwen**，offline **piper**。  
- **fallback_candidate**：online/offline **均为 piper**（健康回退语义）。  
- **blocked**：online/offline **均为 none**。  

---

## 3. Verifier

`tools/verify_voice_qwen_governed_entry_request_trace_v0.py` 对照 **A–Y**（含 trace/replay/whitebox 非空、默认 `voice_tts_config.yaml` 未漂移）。
