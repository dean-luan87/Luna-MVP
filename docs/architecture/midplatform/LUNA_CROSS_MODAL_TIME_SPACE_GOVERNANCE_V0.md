# Luna Cross-Modal Time-Space Governance v0

**关联**：`LUNA_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md`。

本文档固定 **STCM 跨模态适用范围**：**OCR、Vision、Voice** 必须写明；**Map / Memory / Scene Delta** 必须写明。  
**STCM 不是 OCR 专属能力**；各模态共享 **deadline、SpatiotemporalAnchor、ModelCallOutcome、InformationValueAssessment** 语义。

---

## 1. OCR

- **门牌、药品说明、商品标签、公告、按钮文字** 等均有 **任务相关时间窗**；用户移动后，同一 ROI 的识别结果可能 **空间失效**。  
- **须绑定**：`ModelCallDeadline`、`spatial_anchor_type`（常为 `roi` / `visual_frame`）、`frame_id` / `roi_id`。  
- **超时**：若用户已走过目标，结果 **不得** 直接用于 **即时导航播报**；须 STCM 判定 **expired / revalidate**。  
- **与 OCR 治理协同**：OCR Bridge evidence **TTL**、缓存命中均须接受 STCM **valid_until** 裁剪。

---

## 2. Vision（视觉）

- **前方人/车/台阶、红绿灯、门、电梯口** 等属 **强实时或近实时**；模型延迟会导致 **结果过期**。  
- **须绑定**：`frame_id`、时间戳、跟踪 id；动态风险须 **safety_realtime** 或 **navigation_near_realtime** 类 deadline。  
- **过期**：**不得**再用过期检测驱动 **即时避障或转向**；须 **重采样或丢弃**。  
- **风险播报**：须与 **Voice** 子策略一致，且播报本身受 **max_notice_latency_ms** 约束。

---

## 3. Voice（语音）

- **播报若晚于任务窗**（如「前方有人靠近」晚数秒），可能造成 **误导**。  
- **须**：对每条播报意图生成 **deadline**；**drop_expired_voice_notice** 清理队列中过期项。  
- **TTS / 队列**：provider 切换须遵守 **Voice Output Governance** 与 STCM **双重** deadline。  
- **与行动相关**：`voice_notice_required` 为 true 时，须在 **InformationValueAssessment** 下选择短句模板，**禁止**长叙述阻塞安全窗。

---

## 4. Map / Memory / Scene Delta

- **地图信息**可能因用户移动而 **过期**；**记忆**中的空间标签可能与当前位置 **漂移**。  
- **Scene Delta 候选**、**WorldContext evidence** 须有 **TTL** 与 **spatial_anchor**；进入主任务链前须经 STCM **valid_until** 检查。  
- **不得**将 Scene Delta **直接等同**世界模型写入（与既有 OCR/世界模型治理一致）；STCM 只管 **是否仍允许消费**。

---

## 统一约束（跨模态）

- **所有模型输出必须带** `observed_at` / `valid_until` / **spatial_anchor**（见主规范与 deadline 文档）。  
- **任何超出任务时效窗口的结果不得直接进入任务链**（尤其 **驱动用户行动** 的链）。  
- **超时必须即时反馈中台**；**禁止**超时后无事件、无 outcome、仍把旧结果当有效输入 **静默** 继续任务链。
