# Luna STCM Event Skeleton & Trace Contract v0（Phase-STCM-Event-Skeleton-001）

**定位**：在 **STCM 治理 = GO**、**跨合同字段对齐 = GO** 之后，将 STCM 从「可对齐字段」推进为 **可统一记录、回放、审计的事件流** 设计。**本 phase 仅** 定义 **事件 schema 骨架、trace 合同、静态文档与 verifier**。

**边界（硬）**：**不**运行模型；**不**接入 runtime；**不**改 OCR routing；**不**进入 MidPlatform **实装**；**不**写世界模型；**不**执行中台语义解释。事件定义 **不** 等同于已有生产总线已接线。

## Trace 合同（所有 STCM 事件公共信封）

每条 STCM 事件 **必须** 可嵌入统一 trace 上下文（实现 phase 再定序列化载体）：

| 字段 | 说明 |
|------|------|
| `event_id` | 全局唯一事件 id。 |
| `event_type` | 见 `LUNA_STCM_EVENT_TYPE_REGISTRY_V0.md` 与 `stcm_event_type_registry_v0.example.json`。 |
| `trace_id` | 跨调用、跨模态关联；**与** `call_id` **二选一或并存**（见 registry 每类最小字段）。 |
| `emitted_at` | 事件发出时间（建议 ISO-8601）。 |
| `schema_version` | 如 `stcm_event_skeleton_v0`。 |

**与对齐 phase 的关系**：`call_id`、`deadline_at`、`spatial_anchor_ref` 等字段与 **STCM-Contract-Field-Alignment-001** 中的 **ModelCallDeadline / SpatiotemporalAnchor** 映射一致；本 phase **不** 重复重定义业务含义，只固定 **事件形态**。

## 事件流（概念顺序）

```text
stcm_model_call_requested
  → stcm_model_call_started
      → stcm_model_call_completed | stcm_model_call_timeout
  → stcm_fallback_decision（可插入在 completed 前/后，依状态机）
  → stcm_result_discarded（与 completed/timeout 互斥或后继）
  → stcm_voice_notice_requested → stcm_voice_notice_dropped（可选）
  → stcm_anchor_revalidated（可与导航/视觉重定位并行）
```

## 与后续缺口（STCM-GAP-001 / 002）的关系

- **STCM-GAP-001**：`OcrEvidencePack` 顶层缺 `observed_at` / `valid_until` → **`stcm_model_call_completed`** 的 `output_ref` 仍可指向 pack，但 **有效时间** 须在事件或外包 trace 中显式补齐。  
- **STCM-GAP-002**：Voice trace canonical 未定 → **`stcm_voice_notice_*`** 的 `notice_message_template` / `call_id` 绑定须在未来 **Voice governed submit unified export** 冻结后再收窄。

## 审计不变量（设计层）

1. **`stcm_model_call_timeout` 必须** 含 **`notified_midplatform`**（bool 或枚举），**禁止**超时无中台可观测记录。  
2. **语音通知事件** 必须含 **`deadline_at`** 与 **`expires_at`**，与 **Voice Output Governance** 的 expiry 语义对齐。  
3. **`stcm_result_discarded` 必须** 含 **`discard_reason`**。  
4. **`stcm_anchor_revalidated` 必须** 含 **`spatial_anchor_valid`**。  
5. **所有事件** 须带 **`event_id` + `event_type`**，且须带 **`trace_id` 和/或 `call_id`**（registry 逐类最小集）。

---

**一句话**：本阶段把 deadline、timeout、fallback、丢弃、语音与锚点重验 **固化成可审计事件类型**；**不接 runtime、不跑模型、不改 routing**。
