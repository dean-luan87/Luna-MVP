# LUNA OCR Bridge — Shadow Serialization Test Matrix v0

| 用例 | 输入 | 期望 |
|------|------|------|
| T1 正常 OCR-007 root | 含 `ocr_evidence_routing_pack.json` + summary 中 boundary_eval | `validation_passed=true`，无伪造 ref |
| T2 缺 boundary map | 缺 `ocr_capability_boundary_map.json` | 校验可能失败；verifier **NO_GO**（暴露数据缺口） |
| T3 Review/RFC root | 任意存在路径 | summary 标记 summary 是否存在；不强制内容 |
| T4 trace/replay/audit | 任意规模 pack | 三份 jsonl **非空** |
| T5 forwarding 阻断 | 任意 | `forwarding_block_report` 三开关为 false |

## 非目标

- 不调 RapidOCR / PaddleOCR。  
- 不接真实 MidPlatform HTTP/SDK。  
- 不改 OCR 主线 router。
