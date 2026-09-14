# Luna Model Call Deadline & Timeout Policy v0

**关联**：`LUNA_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md`、`configs/midplatform/spatiotemporal_consistency_manager_v0.example.json`。

## ModelCallDeadline（模型调用时限合同）

每次跨 **OCR / Vision / Voice / VLM / Map** 的模型调用 **必须** 携带或可推导 **ModelCallDeadline**（可与 OCR **OCRRequest** 的 `latency_budget_ms` 对齐，但 **语义上 STCM 高于单模态字段**）。

| 字段 | 说明 |
|------|------|
| `call_id` | 全局唯一，用于与 **ModelCallOutcome** 对账。 |
| `provider_name` | 实现标识。 |
| `provider_level` | 可与 OCR Level 等分级体系对齐的抽象级别。 |
| `modality` | `ocr \| vision \| voice \| vlm \| map` 等。 |
| `task_context` | 任务语义锚点。 |
| `urgency` | `realtime \| near_realtime \| async \| background`。 |
| `requested_at` | 请求发起时间。 |
| `deadline_at` | **硬 deadline**（由 `max_latency_ms` 与 urgency 推导）。 |
| `max_latency_ms` | 与 **deadline_classes** 对齐或可覆盖。 |
| `timeout_policy` | 与 **late_result_policy**、fallback 集合绑定。 |
| `fallback_allowed` | 是否允许降级/换模/缓存。 |
| `cancel_allowed` | 是否允许价值驱动取消。 |
| `async_allowed` | 是否允许转异步。 |
| `voice_notice_required` | 是否在影响行动时 **必须** 走语音治理链。 |

## SpatiotemporalAnchor（与输出绑定）

每条可消费信息或模型输出 **必须** 能关联到 **SpatiotemporalAnchor**（可嵌入 evidence pack 或并行索引）：

| 字段 | 说明 |
|------|------|
| `anchor_id` | 唯一 ID。 |
| `observed_at` | 观测/采样时间。 |
| `received_at` | 系统收到时间。 |
| `valid_until` | 对该任务窗的有效截止时间。 |
| `ttl_ms` | 可选冗余，便于缓存层对齐。 |
| `spatial_anchor_type` | `gps \| visual_frame \| roi \| map_node \| task_node \| unknown`。 |
| `spatial_anchor_ref` | 引用句柄。 |
| `frame_id` / `roi_id` | 视觉/OCR 对齐。 |
| `task_id` | 任务锚点。 |
| `source_module` | `ocr \| vision \| voice \| map \| memory`。 |
| `confidence` | 模型置信摘要。 |
| `stale_risk` / `drift_risk` | 陈旧与空间漂移风险枚举或分数。 |

## 超时与反馈（硬规则）

1. **所有模型调用必须带 deadline**（`model_call_policy.all_calls_require_deadline`）。  
2. **不能在 deadline 到期后仍假定结果「自动有效」**；须产出 **ModelCallOutcome**，`status` 可为 `timeout \| cancelled \| stale_result` 等。  
3. **超时必须即时反馈中台**（`timeout_must_notify_midplatform`）：以事件或状态写入形式留下 **可审计记录**，**禁止**仅进程内静默丢弃后继续当作成功路径驱动任务链。  
4. **迟到结果**：`result_validity` 为 `stale \| expired \| spatially_uncertain` 时，**不得直接进入可驱动用户行动的任务链**（须重验或丢弃，见主文档禁止项）。

## deadline_classes（摘要）

| 类 | 典型场景 | v0 建议 `max_latency_ms` | `late_result_policy` |
|----|-----------|--------------------------|----------------------|
| safety_realtime | 人车、台阶、障碍 | 800 | discard |
| navigation_near_realtime | 门牌、路口、电梯 | 3000 | revalidate_spatial_anchor |
| task_context_medium | 标签、公告 | 10000 | async_or_revalidate |
| background_world_context | 海报、促销 | 60000 | async_only |

具体数值以 **example json** 为准；工程实测后可 **CONDITIONAL_GO** 微调。
