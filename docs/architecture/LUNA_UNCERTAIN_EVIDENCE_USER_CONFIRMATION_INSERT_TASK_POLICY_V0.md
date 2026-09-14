# LUNA — Uncertain Evidence User Confirmation Insert Task Policy v0

##定位

- **类型**：future branch policy（只定义，不接 runtime）
- **用途**：用于 WorldContextEvidence / SceneDelta 的后续策略，处理 `uncertain/expired/low_confidence/contradicted` 等存疑证据的“用户确认插入任务”。

##核心原则（硬约束）

1. **只能在低优先级空档问**
2. **不能打断导航、安全提醒、任务链主流程**
3. **不能强制问；没机会就不问**
4. **必须有时效窗口**
5. **超过窗口后不能突然追问**
6. **超时后只能重新采样、降级、丢入待复核池，或标记 expired/uncertain**

##适用场景（示例）

- 低置信 OCR：牌子疑似写着“东门”，需要确认
- 商业活动：星巴克“第二杯半价”是否还在
- 视觉符号：Logo 是否属于某店铺
- 世界变化：公告栏是否换了新内容
- 风险信息：广告是否疑似诈骗

##任务定义（插入型，不是主任务）

- `confirmation_task_type = inserted_low_priority_confirmation`
- `priority = low`
- `interrupt_allowed = false`
- `expires_in = short_window`

##生成规则（candidate-only）

当 `WorldContextEvidenceCandidate.lifecycle.evidence_status in {uncertain_candidate, expired_candidate, contradicted_candidate, candidate}` 或 `trust.trust_score` 很低时，**允许**生成 `user_confirmation_candidate`：

- 仅作为 **inserted low-priority task**（不进入 primary task decision，不产生导航动作）
- 必须带 `confirmation_window_ms` 与 `expires_at`
- 允许上下文：`idle_chat | post_task | user_initiated_chat`
- 禁止上下文：`navigation | safety_warning | primary_task | emergency`
- 所有问询行为必须记录 `trace/whitebox`（包括 skipped/expired）

##超时与降级（必须）

超过 `expires_at` 后：

- 状态标记为 `confirmation_expired`
- 不得再主动追问
- 只能执行：
  - `requires_revalidation=true`
  - `evidence_status=uncertain_candidate` 或 `expired_candidate`
  - 不写入事实
  - 不进入任务链

##用户反馈效果（只影响 trust，不写事实）

- 用户确认：允许提升 `trust_score`（仍是 candidate-only），必须记录 `confirmation_method=user_confirmed`
- 用户否认：标记 `contradicted`/`rejected`（仍保留引用链与审计）

##Human Interaction Validation Layer（接口约束）

本策略只定义“何时/以何种方式询问”的插入任务编排；问询产出的用户反馈 **不得直接覆盖世界事实**，必须进入：

- `docs/architecture/LUNA_HUMAN_INTERACTION_VALIDATION_LAYER_CONTRACT_V0.md`

进行 truth-type 分类（factual/subjective/emotional/metaphorical/roleplay/falsehood），并分层存储与交叉引用。

##数据结构（新增字段建议）

```json
{
  "user_confirmation_candidate": {
    "confirmation_candidate_id": "...",
    "source_evidence_id": "...",
    "question_text": "...",
    "confirmation_task_type": "inserted_low_priority_confirmation",
    "priority": "low",
    "interrupt_allowed": false,
    "confirmation_window_ms": 300000,
    "expires_at": 0,
    "allowed_context": "idle_chat | post_task | user_initiated_chat",
    "forbidden_context": ["navigation", "safety_warning", "primary_task", "emergency"],
    "status": "pending | asked | confirmed | denied | expired | skipped",
    "on_expired": "mark_uncertain_and_revalidate_later"
  }
}
```

##NO_GO（禁止项）

- 打断安全/导航主任务
- 无时效窗口（缺 `confirmation_window_ms/expires_at`）
- 24 小时后突然追问（超窗追问）
- 用户未确认却提升为事实
- 问询失败后仍写入世界模型/进入任务链

