# Luna — OCR Semantic Candidate Generator v1 GO/NO_GO Pack v0

## GO

- 按 `evidence_tier` 正确分流；gated 生成主 OCRSemanticCandidate
- scan / visual / SQ_E 不升级为主语义、不生成强语义
- `raw_text_preservation_rate=1.0`；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- gated primary 数量少但 tier 分流与边界完整

## NO_GO

- scan 提升为主 OCRSemanticCandidate
- visual symbol 解释为普通文字事实
- SQ_E 生成强语义；覆盖 raw OCR；运行 LLM/VLM/语义模型
- WorldModel attach / Scene Delta / 写 fact / benchmark claim / 改 routing
