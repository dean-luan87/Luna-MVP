---
phase: Phase-RealSceneReview-003
title: Mac Camera Live Archive Evidence Quality Matrix v0
status: REVIEW_ARTIFACT
version: v0
last_updated: 2026-04-24
scope: matrix_only
---

## 0. 复审对象

- archive_root: `logs/device_env_003_archive_20260424_135440`
- run_id: `live_beb8d78211`

## 1. Evidence Quality Matrix（v0）

说明：

- status ∈ {pass, partial, fail, not_applicable}
- blocker_level ∈ {hard_blocker, soft_followup, informational}

| item | status | evidence_source | blocker_level | next_action |
|---|---|---|---|---|
| archive_root_exists | pass | archive path exists | informational | none |
| evidence_type_controlled_live | pass | `run_evidence.json.evidence_type=controlled_live` | informational | none |
| input_source_mac_camera | pass | `run_evidence.json.input_source=mac_camera` + `trace.jsonl.camera_opened` | informational | none |
| camera_opened | pass | `trace.jsonl` event `camera_opened=true` | informational | none |
| frame_count_gt_zero | pass | `run_evidence.json.frame_count=30` | informational | none |
| run_evidence_present | pass | `run_evidence.json` exists + parseable | informational | none |
| trace_present | pass | `trace.jsonl` exists + has run_started/mode_entry/frame_captured/run_completed | informational | none |
| replay_present | pass | `replay.jsonl` exists + frame_index 递增记录 | informational | none |
| whitebox_present | pass | `whitebox.jsonl` exists | informational | none |
| model_candidate_trace_present | pass | `model_candidate_trace.jsonl` exists | informational | none |
| output_candidate_trace_present | pass | `output_candidate_trace.jsonl` exists | informational | none |
| operator_notes_present | pass | `operator_notes.md` exists | informational | none |
| risk_events_present_or_none_observed | pass | `risk_events.jsonl` exists + `risk_events_status=none_observed` | informational | none |
| post_run_summary_present | pass | `post_run_summary.md` exists | informational | none |
| archive_manifest_present | pass | `archive_manifest.json` exists | informational | none |
| manifest_missing_files_zero | pass | `archive_manifest.json.missing_files=[]` | informational | none |
| manifest_hash_mismatch_zero | pass | `archive_manifest.json.hash_mismatches=[]` | informational | none |
| validator_recommendation_go | pass | `validate_controlled_live_evidence_collection_execution_v0.py` summary=go | informational | none |
| no_execute_leakage_assertion | pass | `run_evidence.json.no_execute_leakage_assertion=true` | informational | none |
| no_default_on_assertion | pass | `run_evidence.json.no_default_on_assertion=true` | informational | none |
| no_side_effect_expansion_assertion | pass | `run_evidence.json.no_side_effect_expansion_assertion=true` | informational | none |
| failed_camera_path_does_not_fake_archive | pass | DeviceEnv-003 verifier：camera-index=9999 不生成 required_files，仅 `failed_run_report.json` | informational | keep verifier in pre-run checklist |
| frame_ref_traceability | partial | `replay.jsonl.frame_ref=controlled_live://frame/N`（无真实帧字节引用） | soft_followup | 建议增加 media 落盘或 video+mapping（不阻塞） |
| whitebox_per_tick_auditability | partial | `whitebox.jsonl` 仅 1 行 gate 声明 | soft_followup | 建议按 tick 写最小白盒（不阻塞） |

## 2. 汇总

- hard_blockers: none
- soft_followups:
  - frame_ref_traceability
  - whitebox_per_tick_auditability

