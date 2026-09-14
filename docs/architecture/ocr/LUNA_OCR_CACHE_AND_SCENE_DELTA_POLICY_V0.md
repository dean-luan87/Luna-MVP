# Luna OCR Cache & Scene Delta Policy v0

**关联**：`LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md`。

## 缓存与指纹

- **enable_cache**：true；**requires_roi_fingerprint** / **requires_ttl**：true。  
- **概念字段**：`roi_fingerprint`、`image_fingerprint`、`location_anchor`、`observed_at`、`ttl`、`stale_risk`、`cache_hit`/`cache_miss`、`source_provider`、`evidence_id`。  
- **cache_hit_skips_model**：true；命中则 **不得** 重复跑模型。  
- **stale_evidence_requires_revalidation**：TTL 过期或场景显著变化时须重新校验或降级为「不确定」。

## Scene Delta 联动

- OCR 结果须能支撑 **「相对上一观测是否变化」** 的判定，以进入 **Scene Delta / WorldContext 候选**。  
- **禁止**：仅凭 OCR 文本 **直接写世界模型** 或 **中台事实解释**；候选须带 **证据引用与不确定性**。
