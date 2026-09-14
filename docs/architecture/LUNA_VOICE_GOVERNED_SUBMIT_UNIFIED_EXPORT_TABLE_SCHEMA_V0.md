# Phase-Voice-OutputGovernance-009
# Governed Submit Unified Export Table Schema v0

本文件冻结 Phase-009 导出表 schema（shadow-only）。

---

## 1) gate position table

`voice_governed_submit_gate_position_table.json`

```json
{
  "request_id": "...",
  "submit_gate_position": "_maybe_submit_real_output_v1_pre | VoiceOutputPlane.submit_entry",
  "submit_shadow_result": "...",
  "submit_allowed": false,
  "submit_block_reason": null,
  "source_submit_shadow_decision_id": "...",
  "source_governance_decision_id": "...",
  "hard_audit_ok": true
}
```

---

## 2) result distribution table

`voice_governed_submit_result_table.json`

```json
{
  "submit_shadow_result": "submit_allowed_shadow",
  "count": 0,
  "request_ids": []
}
```

---

## 3) request matrix

`voice_governed_submit_request_matrix.json`

```json
{
  "request_id": "...",
  "maybe_submit_pre_result": "...",
  "output_plane_entry_result": "...",
  "positions_consistent": true,
  "hard_audit_ok": true
}
```

