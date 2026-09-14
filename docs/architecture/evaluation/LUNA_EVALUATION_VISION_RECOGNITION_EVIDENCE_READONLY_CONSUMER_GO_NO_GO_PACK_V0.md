# Luna 评测 — Vision Recognition Evidence ReadOnly Consumer GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/vision/verify_vision_recognition_evidence_readonly_consumer_v0.py`  
**Phase**：`Phase-Vision-Recognition-Evidence-ReadOnly-Consumer-001`

## GO

- 输入根下 **evidence pack** 存在；输出根下 **consumer_view** 与 **audit** 齐全。  
- `consumer_view.schema_version=vision_recognition_evidence_readonly_consumer_view_v0`。  
- `evidence_count_observed > 0`；`provider=vision_stub`。  
- `fact_status_summary.not_fact == evidence_count_observed`；`synthetic_count` 与 `stub_provider_count` 均等于 `evidence_count_observed`。  
- `evidence_by_frame`、`evidence_by_roi_type` 非空；`geometry_summary.bbox_in_frame_count > 0`。  
- audit：`vision_evidence_readonly_consumer_executed=true`；禁止写入 / 禁止模型 / 禁止解释与导航类字段均为 **false**。

## CONDITIONAL_GO

- 无 **NO_GO** blockers，但存在 **soft_notes**（例如 `source_chain_summary` 形态告警等）。

## NO_GO

- 将 stub 当作 **confirmed fact** 或 consumer 输出含 **禁止键名**（实现自检失败）。  
- 生成 **导航动作**、**Scene Delta / WorldModel / MidPlatform** 写入语义（audit 非 false）。  
- 调用 **真实模型** 或 **AI interpretation**。  
- **audit** 或关键产物缺失。

## 一句话

本 smoke **只**验证 evidence pack 的 **只读消费与聚合**；**不**进入事实层、**不**写 Scene Delta / WorldModel。
