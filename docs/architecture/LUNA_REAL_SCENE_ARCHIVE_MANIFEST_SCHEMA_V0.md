# Phase-RealSceneFix-001 — Real Scene Archive Manifest Schema v0（归档清单 schema 冻结）

**目的**：定义一次 controlled live run 的 archive manifest 必须包含的文件清单、hash、完整性检查与归档就绪判定。  

---

## 1) archive_manifest.json 顶层字段（必须全部存在）

- `manifest_id`
- `run_id`
- `generated_at_ms`
- `archive_root_path`
- `required_files`（数组：相对路径）
- `file_hashes`（dict：relative_path -> sha256）
- `missing_files`（数组）
- `hash_mismatches`（数组：relative_path）
- `integrity_status`（枚举：`pass` / `partial` / `fail`）
- `archive_ready`（bool）

---

## 2) required_files（写死最小集合）

必须包含（相对 archive_root_path）：
- `run_evidence.json`
- `trace.jsonl`
- `replay.jsonl`
- `whitebox.jsonl`
- `model_candidate_trace.jsonl`
- `output_candidate_trace.jsonl`
- `operator_notes.md`（或 `operator_notes.json`，但必须在 required_files 中明确其一）
- `risk_events.jsonl`
- `post_run_summary.md`（或 `post_run_summary.json`，同上）
- `archive_manifest.json`（自包含）

---

## 3) hash 规则（写死）

- `file_hashes` 必须覆盖所有 required_files
- hash 算法：SHA-256（hex）
- 若文件缺失：加入 `missing_files`
- 若 hash 不一致：加入 `hash_mismatches`

---

## 4) integrity_status 判定（写死）

- `pass`：missing_files 为空 且 hash_mismatches 为空
- `partial`：missing_files 非空 且（关键文件未缺失）且 hash_mismatches 为空
- `fail`：任一关键文件缺失 或 任一 hash_mismatches 非空

关键文件（缺失即 fail）：
- `run_evidence.json`
- `trace.jsonl`
- `replay.jsonl`
- `whitebox.jsonl`
- `archive_manifest.json`
- `post_run_summary.(md|json)`

---

## 5) archive_ready 判定（写死）

- `archive_ready=true` 仅当 `integrity_status=pass`
- `archive_ready=false` 否则

