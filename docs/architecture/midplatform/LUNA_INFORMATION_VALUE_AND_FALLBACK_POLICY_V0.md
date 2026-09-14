# Luna Information Value & Fallback Policy v0

**关联**：`LUNA_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md`、`LUNA_MODEL_CALL_DEADLINE_AND_TIMEOUT_POLICY_V0.md`。

## InformationValueAssessment（信息价值评估）

在 **ModelCallDeadline** 触发超时或 **SpatiotemporalAnchor** 指示风险时，中台 **必须** 能读取或推导 **InformationValueAssessment**，以决定 **取消 / 缓存 / 换模 / 异步 / 语音** 分支。

| 字段 | 说明 |
|------|------|
| `info_value_level` | `critical \| high \| medium \| low \| ambient`。 |
| `task_dependency` | `blocking \| helpful \| optional \| irrelevant`。 |
| `safety_relevance` | `safety_critical \| safety_related \| normal`。 |
| `user_action_relevance` | `immediate \| near_term \| background`。 |
| `cancellation_allowed` | 是否允许取消本次调用或丢弃迟到结果。 |
| `fallback_required` | 是否 **必须** 走显式 fallback（不得静默当成功）。 |
| `voice_notice_required` | 是否必须触发 **Voice Output Governance** 下的短句。 |

## 超时后的决策集合（与 STCM 协同）

中台在收到 **timeout / late** 事件后，根据价值评估在下列 **互斥或组合策略** 中选择（实现 phase 再定状态机；v0 只冻结 **允许集合**）：

| 决策 | 含义 |
|------|------|
| `cancel_recognition` | 取消识别/调用，不消费未完成结果。 |
| `reuse_cache` | 在 anchor 仍有效前提下复用缓存证据。 |
| `switch_to_light_model` | 换轻量模型（须仍满足 deadline 与隐私）。 |
| `switch_to_heavy_model` | 换重型模型（通常伴随 **async** 或更长窗）。 |
| `switch_to_remote_or_vlm` | 远程/VLM（须授权与 STCM+隐私闸门）。 |
| `async_defer` | 转后台异步，不阻塞当前行动链。 |
| `request_resample` | 要求新一帧/新 ROI/重新采样。 |
| `ask_user_hold` | 语音请求用户稍等（短句）。 |
| `voice_notify_degraded` | 播报能力降级（非推卸责任的长叙述）。 |
| `silent_drop` | **仅**对 `ambient` / `irrelevant` 且不影响安全与行动的信息静默丢弃（仍须 **中台可观测计数**，不得等于「超时后无记录」）。 |

## fallback_policy（配置摘要）

见 `spatiotemporal_consistency_manager_v0.example.json` 中 **`fallback_policy`**：`allow_cache_reuse`、`allow_model_switching`、`allow_async_defer`、`allow_cancel_low_value_info`。

**原则**：**低价值** 可 `silent_drop` 但仍须审计；**高价值 / safety** 禁止在无记录情况下静默进入任务链。

## ModelCallOutcome（与价值评估对账）

| 字段 | 说明 |
|------|------|
| `call_id` | 对应 **ModelCallDeadline**。 |
| `provider_name` | 实际执行者。 |
| `completed_at` | 完成或失败时间点。 |
| `elapsed_ms` | 耗时。 |
| `status` | `completed \| timeout \| cancelled \| fallback_used \| async_deferred \| stale_result`。 |
| `result_validity` | `valid \| stale \| expired \| spatially_uncertain`。 |
| `output_ref` | 证据/特征句柄。 |
| `error` | 错误摘要。 |
| `fallback_decision` | 实际采取的 fallback 枚举。 |
| `notified_midplatform` | 超时/取消等是否已 **显式** 通知中台。 |
| `voice_notice_emitted` | 是否已触发语音管线（可带 notice_id）。 |
