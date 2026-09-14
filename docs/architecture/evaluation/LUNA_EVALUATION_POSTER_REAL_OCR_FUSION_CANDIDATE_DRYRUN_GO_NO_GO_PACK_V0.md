# Luna — Poster Real OCR Fusion Candidate DryRun GO/NO_GO Pack v0

## GO

- fusion candidate dry-run 生成；`fusion_candidate_count=1`
- visual context / text input / hypothesis / review requirement 完整
- `fusion_committed=false`；`semantic_join_committed=false`
- no-write boundary 通过；`verifier=GO`

## CONDITIONAL_GO

- 部分 text evidence 为空，但 candidate / guard / audit 完整
- 无越界行为

## NO_GO

- 重新运行 OCR；committed semantic join
- visual symbol 当普通文本；Scene Delta candidate；写事实层
- benchmark / provider 比较宣称；改 routing；audit 缺失
