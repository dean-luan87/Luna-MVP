# Luna Spatiotemporal Consistency Manager v0（Phase-Spatiotemporal-Consistency-Manager-001）

**英文全称**：Time-Space Consistency & Model Call Governance v0  
**中文名**：**时空间一致性管理器**（简称 **STCM**）

## 定位与层级

**STCM 是中台基础设施层**，位于 **OCR Orchestrator**、**Vision Model Scheduler**、**Voice Output Scheduler** 等 **单模态调度器之上**（概念层级；本 phase **不** 实装 MidPlatform、**不** 接主线、**不** 改 routing）。

**STCM 不是 OCR 子模块，也不是「OCR timeout 参数」的别名。** 它统一治理：**信息在当前任务时间窗内是否仍有效**、**空间锚点是否仍成立**、**模型调用是否仍能在 deadline 内返回**、**迟到的结果是否必须视为过期**、以及 **超时后是否允许静默进入任务链**（**不允许**）。

**核心命题**：模型在 **错误的时间**、**错误的空间状态**、**错误的系统负载** 下返回的内容，即使字面正确，也可能对任务产生 **错误影响**。因此 **时间治理、空间治理与模型调用治理必须绑定**，不能只抽象为「算完即真理」。

---

## 职责边界（必须同时满足）

1. **时间有效性**：该信息在 **当前时刻** 对当前任务是否仍有效？`valid_until` / `ttl_ms` 是否已越过？  
2. **空间有效性**：该信息对应的 **空间锚点**（帧、ROI、地图节点、任务节点等）是否仍与用户/设备状态一致？  
3. **调用时限**：该 **ModelCallDeadline** 下，provider 是否仍被允许同步完成？若将迟到，是否必须 **取消 / 降级 / 异步 / 换模**？  
4. **结果处置**：**超出时效窗口的结果不得直接进入任务链**（不得驱动用户 **即时行动**）；必须经过 **再校验、降级证据、或丢弃** 等显式策略。  
5. **超时反馈**：**超时必须即时反馈中台**（不可仅局部吞掉）；由 **InformationValueAssessment** 驱动后续分支。  
6. **语音协同**：若影响用户 **当前行动**，须进入 **Voice Output Governance** 下的短句播报；**语音通知本身也受 deadline 管理**，**过期播报不得继续执行**。

---

## 逻辑结构（概念树）

```text
MidPlatform（概念）
 └── Spatiotemporal Consistency Manager（STCM）
      ├── Time Anchor（observed_at / valid_until / ttl）
      ├── Space Anchor（spatial_anchor_type / ref / frame / roi）
      ├── Model Call Deadline（deadline_at / max_latency_ms / policies）
      ├── Information TTL（与任务窗对齐的 TTL 分层）
      ├── Timeout Feedback（中台可观测事件，禁止静默吞没）
      ├── Value-based Cancellation（按信息价值取消或丢弃）
      ├── Model Switching（在 STCM 与模态调度器协同下允许/禁止）
      ├── Async Downgrade（异步或降级路径）
      └── Voice Notification Policy（行动受影响时的短句与过期清理）
```

---

## 核心对象（合同字段摘要）

完整字段表见各拆分文档；**最小必备对象**：

| 对象 | 作用 |
|------|------|
| **SpatiotemporalAnchor** | 每条模型输出或可消费信息的 **时空绑定** 与 **陈旧风险**。 |
| **ModelCallDeadline** | 每次模型调用的 **时限、取消/降级/异步/语音** 策略入口。 |
| **ModelCallOutcome** | 单次调用的 **完成态、是否过期、是否已通知中台、是否已触发语音**。 |
| **InformationValueAssessment** | 对任务阻塞度、安全相关度、用户行动相关度的 **价值评估**，驱动超时后的动作集合。 |

字段清单见：`LUNA_MODEL_CALL_DEADLINE_AND_TIMEOUT_POLICY_V0.md`、`LUNA_INFORMATION_VALUE_AND_FALLBACK_POLICY_V0.md`。

---

## 时效分层（与任务窗对齐）

必须区分 **safety_realtime**、**navigation_near_realtime**、**task_context_medium**、**background_world_context** 等 **deadline_classes**（数值见 `configs/midplatform/spatiotemporal_consistency_manager_v0.example.json`，v0 为建议区间，工程可 CONDITIONAL 微调）。

原则摘要：

- **安全强实时**：迟到结果 **丢弃**，**不得**用于行动；通常 **必须语音提示**（若影响行动）。  
- **导航近实时**：迟到须 **重验空间锚点**；用户可能已离开目标区域。  
- **中窗任务上下文**：可 **异步或重验**，避免阻塞主链路。  
- **背景世界上下文**：**仅异步**，不打断主任务。

---

## 与 OCR Provider Runtime Governance 的关系（协同，非重复）

- **OCR Provider Runtime Governance**：回答 **「调用哪个 OCR、如何分级、如何走 Bridge」**（**OCRRequest → OCRDispatchDecision / OCRExecutionPlan**）。  
- **STCM**：回答 **「这次调用在任务时间上是否仍被允许、空间是否仍成立、迟到后结果是否仍准入任务链、超时后如何反馈与降级」**。

**OCR Orchestrator 在裁定 OCRExecutionPlan 时，必须查询 STCM**：`ModelCallDeadline`、`SpatiotemporalAnchor` 候选的有效期、以及 **timeout / voice** 策略。**二者共同约束** 最终是否执行 OCR、同步或异步、以及结果是否可进入下游消费（仍须满足 OCR 证据与 Bridge 治理）。

---

## 跨模态适用范围（强制）

STCM 规则 **同等适用于**：

- **OCR**（文字识别 deadline、ROI 超时、cache、Bridge evidence TTL）；详见 `LUNA_CROSS_MODAL_TIME_SPACE_GOVERNANCE_V0.md` **§OCR**。  
- **Vision**（检测/跟踪 deadline、动态风险过期、frame 一致性）；**§Vision**。  
- **Voice**（播报时效、过期播报取消、TTS 队列清理）；**§Voice**。  
- **Map / Memory / Scene Delta / WorldContext evidence**（地图与记忆漂移、候选 TTL）；**§Map / Memory / Scene Delta**。

**Vision** 与 **Voice** 与 **OCR** 并列写入 cross-modal 文档；本能力 **不得** 退化为仅 OCR 文本路径。

---

## 禁止事项（设计层）

1. **过期结果驱动用户行动**：任何已判定 **expired / stale / spatially_uncertain** 的 **ModelCallOutcome** 不得直接进入 **可改变用户即时行为** 的任务链。  
2. **超时后静默进入任务链**：模型 **timeout / cancelled** 后，不得在无 **中台事件、无价值评估、无 STCM 记录** 的情况下将旧结果 **静默** 当作仍有效输入继续下游。  
3. **将 STCM 降级为 OCR timeout 配置项**：禁止在文档或配置语义上把 STCM 描述为 **仅 OCR 子模块**。  
4. **本 phase**：不运行模型、不接主线、不改 routing、不实装 MidPlatform runtime。

---

**一句话**：STCM 回答的是 **「世界是否还在等这个结果」**；不是模型能不能算，而是 **算出来时是否仍允许影响任务与用户行动**。
