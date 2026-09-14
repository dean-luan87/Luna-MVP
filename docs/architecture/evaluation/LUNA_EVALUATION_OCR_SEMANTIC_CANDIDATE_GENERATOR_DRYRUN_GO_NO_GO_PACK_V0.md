# Luna — OCR Semantic Candidate Generator DryRun GO/NO_GO Pack v0

## GO

- 14 条 OCRTextEvidencePack 均生成 OCRSemanticCandidate dry-run
- Poster 4 条 non-empty 有语义分类；RealVideo 10 条 empty 仅 unknown/unreadable
- raw text preservation 完整；no-write boundary 通过；`verifier=GO`

## CONDITIONAL_GO

- 部分 semantic_type 为 unknown，但 schema/guard/boundary/audit 完整
- 无越界行为

## NO_GO

- 重跑 OCR；运行语义模型/LLM/VLM；覆盖 raw OCR；提交 correction/completion
- empty_text 当 no_text_fact；WM attach 执行；Scene Delta；写事实层；benchmark claim；改 routing
