# LUNA OCR Bridge — Shadow Source Ref Policy v0

## 前缀分类

| 前缀 | 用途 |
|------|------|
| `eval:` | Evaluation / OCR-006/007 等离线测评产物 |
| `shadow:` | Bridge Implementation-001 绑定、trace/replay/audit 束 |
| `offline_trial:` | 离线 trial 输出（显式标记） |

## 禁止伪造

以下前缀 **不得** 出现在本 phase 生成的 shadow 包字符串字段中（除非未来授权 runtime wiring phase 显式引入）：  
`runtime:`、`production:`、`midplatform:`、`scene_delta:`、`world_context:`。

## 顶层绑定字段

- `source_image_ref` / `source_provider_ref` / `source_quality_gate_ref` / `source_layout_ref` / `source_eligibility_gate_ref`：来自既有 builder 的 `eval:*` 或显式 `offline_trial:*`。  
- `trace_ref` / `replay_ref` / `audit_ref`：由 serializer 写入 **shadow_envelope.binding**（见 `ocr_evidence_pack_shadow_source_ref_report.json` 的 `binding_refs`）。

## `missing_source_refs`

任一顶层 ref 缺失时：`midplatform_contract.forwarding_mode` **不得**为 `eligible_text_only`；本 Implementation-001 **强制** `allowed_to_forward_to_midplatform=false`。
