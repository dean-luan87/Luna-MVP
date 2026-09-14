# LUNA Evaluation — PaddleOCR Manifest v1 Cache Fill Completion v0（Phase-PaddleOCR-ManifestV1-CacheFill-001）

## 作用

**聚合**以下根目录的产物与逻辑一致性：

| 输入 | 含义 |
|------|------|
| `--prepare-root` | CachePrepare-001 输出（含 **candidate**）。 |
| `--fill-root` | CacheFill-001 输出（fill summary / matrix / missing / download report）。 |
| `--snapshot-root` | 重跑 snapshot 后的目录（summary / pinned / …）。 |
| `--snapshot-verifier-report` | 可选；默认 `<snapshot-root>/paddleocr_manifest_v1_snapshot_verifier_report.json`。 |

## 产出

- `paddleocr_manifest_v1_cache_fill_completion_summary.json`：`completion_verdict`、`blockers`、关键计数。  
- `paddleocr_manifest_v1_cache_fill_completion_verifier_report.json`：结构化 checks。

## `completion_verdict` 规则（摘要）

- **GO**：无 blockers，且 **`snapshot_verdict == GO`**（隐含 pinning / missing / sha 已由 snapshot 与 snapshot verifier 保证）。  
- **CONDITIONAL_GO**：存在非欺诈类 blockers（例如 snapshot 仍为 CONDITIONAL_GO、缺 snapshot verifier 报告等）。  
- **NO_GO**：**欺诈矛盾**（例如 `snapshot_verdict == GO` 但 `pinning_complete` 为 false、或 **有 missing_refs** 却宣称 GO、或 sha 为空等）。

## 与单步 verifier 的区别

- **Snapshot verifier**：只验证 **单次 snapshot 目录** 的自洽性。  
- **Completion verifier**：串联 **prepare → fill → snapshot** 的 **端到端** 状态，防止「前面缺文件却后面宣称 GO」。
