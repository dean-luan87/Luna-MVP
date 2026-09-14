# LUNA — OCR Offline Source Policy Audit Requirements v0

## Phase

- **Phase-ModelOCR-008** — mandatory fields for runs claiming conformance to **`ocr_default_offline_raw_text_source_policy_v0`**

## Policy identity

- **source_policy_id:** `ocr_default_offline_raw_text_source_policy_v0`

## Requirement

Every OCR **source selection** event under this policy (including fallbacks and `not_available`) **must** persist the following fields (or explicit `null` / `n/a` with reason where allowed by harness schema).

## Mandatory fields

| Field | Description |
|-------|-------------|
| `source_policy_id` | Must be `ocr_default_offline_raw_text_source_policy_v0` when policy applies |
| `offline_evaluation` | Boolean |
| `raw_text_only` | Boolean |
| `provider_attempt_order` | Ordered list of provider ids attempted |
| `provider_selected` | Final provider id or `not_available` |
| `fallback_used` | Boolean |
| `fallback_reason` | Structured reason if fallback occurred |
| `provider_status` | success / failed / skipped / disabled |
| `dependency_ready` | Boolean |
| `model_assets_status` | e.g. `pinned_local`, `cache_detected`, `missing`, … |
| `model_config_id` | Config or manifest id when applicable |
| `provider_id` | Selected provider id |
| `provider_kind` | e.g. rapidocr_variant / vision / … |
| `reproducibility_risk` | Recorded risk notes (may reference asset report) |
| `runtime_network_required` | Boolean |
| `avg_latency_ms_per_frame` | Number or n/a |
| `p95_latency_ms_per_frame` | Number or n/a |
| `raw_text_candidate_schema_valid` | Boolean |
| `semantic_interpretation_enabled` | Must be **false** for policy scope |
| `allows_execute_now` | Must be **false** for policy scope |
| `real_tts_invoked` | Must be **false** for policy scope |
| `downstream_invocation_count` | Integer; must be **0** for policy scope |
| `forbidden_semantic_output_count` | Integer |
| `trace_ref` | Reference to trace artifact when required |
| `replay_ref` | Reference to replay bundle when required |
| `whitebox_ref` | Reference to whitebox log when required |

## Mid-platform (future)

These fields are **designed** to align with **Phase-MidPlatform-Monitoring-001** (*Unified Capability Runtime Monitoring*) for **provider selection** and **fallback** statistics. **No** integration is required in Phase-008.

## Non-goals

- This document **does not** require implementing storage — only **what** must be recorded when a run claims policy conformance.
