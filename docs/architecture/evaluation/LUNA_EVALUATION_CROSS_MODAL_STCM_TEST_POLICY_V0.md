# Luna Evaluation & Test Board — Cross-Modal STCM Test Policy v0

**Phase**：`Phase-Luna-Evaluation-Test-Board-001`  
**Level**：8  
**定位**：OCR / Vision / Voice 与 **STCM** 的 **时空间一致性** 联测策略；**非 OCR 专属**（OCR 为子集）。

**边界**：本 phase 文档 **不** 要求运行模型；运行级用例在 **未来** 由专项 harness 执行，并落盘 Artifact Standard **§4** 所列 STCM 产物。

---

## 1. 必须覆盖的语义（设计级 v0）

- **model_deadline_timeout**：模型调用在 deadline 内未完成时的分支。  
- **stale_result_discarded**：过期结果 **不得** 静默驱动用户行动。  
- **voice_notice_requested** / **expired_voice_notice_dropped**：语音通知请求与过期丢弃。  
- **spatial_anchor_revalidated**：空间锚更新后旧结果的失效策略。  
- **cache_reused**：缓存命中与 TTL 一致性。  
- **fallback_model_selected**：降级模型路径与审计。  
- **async_defer**：异步推迟与可观测性。

---

## 2. 与 Level 9 的边界

Level 8 **只证明** 跨模态时空间策略在 **测评/影子** 环境下的可观测性；**不** 等同于 **Level 9** shadow/release 通过。Level 9 **后置**，须单独满足无副作用与回滚。

---

## 3. GO 条件（摘要）

STCM 事件链 **完整** 可重建；过期结果 **可证明** 未进入下游行动链；语音通知 **可证明** 未在过期后播报。

---

**非 OCR 专属声明**：本策略以 **STCM 为中枢** 约束 OCR/Vision/Voice 并行管线。
