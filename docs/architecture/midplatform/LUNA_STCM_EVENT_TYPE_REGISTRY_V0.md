# Luna STCM Event Type Registry v0

**关联**：`LUNA_STCM_EVENT_SKELETON_AND_TRACE_CONTRACT_V0.md`、`configs/midplatform/stcm_event_type_registry_v0.example.json`。

## 1. `stcm_model_call_requested`

模型调用 **被提出**（尚未执行）。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓（可与 `call_id` 并存） |
| `call_id` | ✓ |
| `source_module` | ✓ |
| `modality` | ✓ |
| `provider_name` | ✓ |
| `provider_level` | ✓ |
| `task_context` | ✓ |
| `urgency` | ✓ |
| `requested_at` | ✓ |
| `deadline_at` | ✓ |
| `max_latency_ms` | ✓ |
| `spatial_anchor_ref` | ✓ |
| `info_value_level` | ✓ |
| `voice_notice_required` | ✓ |

## 2. `stcm_model_call_started`

模型 **实际开始** 执行。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓ |
| `call_id` | ✓ |
| `started_at` | ✓ |
| `provider_name` | ✓ |
| `input_ref` | ✓ |
| `input_type` | ✓ |
| `roi_refs` | ✓（可空数组） |
| `cache_checked` | ✓ |
| `cache_hit` | ✓ |

## 3. `stcm_model_call_completed`

模型 **正常完成**。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓ |
| `call_id` | ✓ |
| `completed_at` | ✓ |
| `elapsed_ms` | ✓ |
| `output_ref` | ✓ |
| `result_validity` | ✓ |
| `spatial_anchor_valid` | ✓ |
| `stale_risk` | ✓ |
| `drift_risk` | ✓ |

## 4. `stcm_model_call_timeout`

模型 **超时**。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓ |
| `call_id` | ✓ |
| `timeout_at` | ✓ |
| `elapsed_ms` | ✓ |
| `deadline_at` | ✓ |
| `timeout_policy` | ✓ |
| `notified_midplatform` | ✓（**审计硬字段**） |
| `voice_notice_required` | ✓ |

## 5. `stcm_fallback_decision`

中台 **fallback** 决策。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓ |
| `call_id` | ✓ |
| `fallback_decision` | ✓ |
| `fallback_provider` | ✓（可 null） |
| `fallback_reason_codes` | ✓ |
| `cancel_allowed` | ✓ |
| `async_allowed` | ✓ |
| `cache_reuse_allowed` | ✓ |

## 6. `stcm_result_discarded`

结果 **丢弃**（过期/漂移/低价值等）。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓ |
| `call_id` | ✓ |
| `output_ref` | ✓ |
| `discard_reason` | ✓（**审计硬字段**） |
| `result_validity` | ✓ |
| `expired_at` | ✓（可 null 若策略为空间无效） |
| `user_action_affected` | ✓ |

## 7. `stcm_voice_notice_requested`

**需要** 语音告知用户。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓ |
| `notice_id` | ✓ |
| `call_id` | ✓ |
| `notice_reason` | ✓ |
| `notice_message_template` | ✓ |
| `requested_at` | ✓ |
| `deadline_at` | ✓ |
| `expires_at` | ✓ |
| `user_action_affected` | ✓ |

## 8. `stcm_voice_notice_dropped`

语音通知 **过期或不再播报**。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓ |
| `notice_id` | ✓ |
| `dropped_at` | ✓ |
| `drop_reason` | ✓ |
| `stale_notice` | ✓ |
| `replaced_by` | ✓（可 null） |

## 9. `stcm_anchor_revalidated`

**空间锚点** 被重新校验。

| 字段 | 必填 |
|------|------|
| `event_id` | ✓ |
| `event_type` | ✓ |
| `trace_id` | ✓ |
| `anchor_id` | ✓ |
| `previous_anchor_ref` | ✓ |
| `new_anchor_ref` | ✓ |
| `revalidated_at` | ✓ |
| `spatial_anchor_valid` | ✓（**审计硬字段**） |
| `drift_risk` | ✓ |
