# LUNA OCR Bridge — Implementation RFC Go/No-Go Pack v0 (Phase-OCRBridge-Implementation-RFC-001)

## GO（本 RFC phase）

- `LUNA_OCR_BRIDGE_RUNTIME_BINDING_RFC_V0.md`：绑定点盘点完成。  
- `LUNA_OCR_BRIDGE_RUNTIME_SOURCE_REF_PLAN_V0.md`：runtime ref 规则与来源规划完成。  
- Flag / kill switch、shadow-only、abort/rollback 文档完成。  
- `review_ocr_bridge_runtime_binding_rfc_v0.py` 与 `verify_ocr_bridge_runtime_binding_rfc_v0.py` **通过**。  
- **无** runtime 代码行为变更、**无**真实 MidPlatform / 白盒接线。

## CONDITIONAL_GO

- 部分绑定点仍为 **候选路径**（如未来 PaddleOCR executor 未落地）。  
- `source_ref` 具体序列化格式在 **Implementation phase** 再定；**语义**以本 RFC 为准。  
- Flag **名称**可经 ADR 微调，**语义与默认安全姿态不可变**。

## NO_GO

- 在本 phase **提交**真实 MidPlatform / SceneDelta / WorldContext 接线。  
- **`raw_text_joined`** 再次成为中台唯一输入路径。  
- **`LUNA_ENABLE_OCR_EVIDENCE_PACK_FORWARD_MIDPLATFORM_V1` 默认 true** 或 **fact_text 默认 true**。  
- **无全局 kill** 或 **伪造 runtime source_ref / trace_id**。  
- **改动 OCR provider routing** 且无单独授权 phase。

---

## 推荐下一阶段

**Phase-OCRBridge-Implementation-Authorize-001**（或等价命名）：书面授权 shadow 开闸范围、日志保留策略、与 MidPlatform 接口 dry-run **mock** 范围（仍不调生产）。
