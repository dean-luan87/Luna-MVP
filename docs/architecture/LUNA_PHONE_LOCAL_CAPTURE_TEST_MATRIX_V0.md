---
phase: Phase-DeviceEnv-004
title: Phone Local Capture Test Matrix v0
status: TEST_MATRIX_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
---

## 0. 目标

定义 phone local controlled capture bundle 的后续实现阶段测试矩阵（bundle 生成 + Mac import + archive 生成 + validator）。

本阶段只写矩阵，不实现测试代码，不执行真实采集。

## 1. 测试矩阵（v0）

### A. valid_phone_bundle_case

- setup：bundle 完整（manifest pass；required_files complete；risk none_observed 有记录）
- expect：bundle validation pass

### B. missing_video_case

- setup：缺 `media/video.mp4` 且无 frames
- expect：fail

### C. missing_metadata_case

- setup：缺 `capture_metadata.json`
- expect：fail

### D. missing_risk_events_case

- setup：缺 `risk_events.jsonl` 或为空且无 none_observed
- expect：fail

### E. hash_mismatch_case

- setup：bundle_manifest hash 与文件实际不一致
- expect：fail

### F. evidence_type_mislabel_case

- setup：capture_metadata.evidence_type 标为 controlled_live 或 recorded_video_replay
- expect：hard fail

### G. safety_assertion_false_case

- setup：任一安全断言 false
- expect：hard fail

### H. privacy_area_violation_case

- setup：privacy_area_checked=false 或 notes 标记 privacy_issue_observed=true
- expect：fail 或 hard fail（实现阶段必须定义一致规则）

### I. mac_import_success_case

- setup：bundle_valid=pass；执行导入
- expect：archive_root complete（required_files complete）

### J. mac_import_preserves_source_case

- setup：导入完成
- expect：archive.run_evidence 里 source_bundle_id/source_bundle_manifest_path preserved

### K. mac_import_mislabels_controlled_live_case

- setup：导入后 run_evidence.evidence_type 被误改为 controlled_live
- expect：hard fail

### L. pending_mac_import_case

- setup：bundle_ready=true 但未导入
- expect：bundle_valid pass；archive not ready（不得伪造 archive）

