# LUNA — Offline Mainline Runner Test Matrix v0 (Phase-EngineeringFlow-004)

## Artifacts
- normal run output_root：`logs/offline_mainline_ef004_20260428_105303`
- fallback run output_root：`logs/offline_mainline_ef004_fallback_20260428_105303`
- verifier report：`logs/offline_mainline_runner_verify_001_20260428_1058.json`

## Verifier A–J（对应需求）
- A 正常 YOLO selected path 全链路跑通：pass（stage_complete_rates 全 1.0；source_selected=yolo_shadow）
- B disable_yolo=true fallback path 全链路跑通：pass（stage_complete_rates 全 1.0；source_selected=baseline_mock）
- C SceneContext gate 缺失时 fail-closed：本版通过“stage_outputs/scene_context 必须存在 + complete_rates”间接覆盖（runner 中 gate 失败会退出）
- D Output real_tts_invoked 不得为 true：pass（real_tts_invoked_false_rate=1.0）
- E allows_execute_now 不得为 true：pass（allows_execute_now_false_all_stages_rate=1.0）
- F pending_real_sidewalk_run 不得关闭：pass（pending_real_sidewalk_run_true_rate=1.0）
- G controlled_live_stream=true 必须拒绝或 fallback：本版通过 evidence_boundary_rates 强约束为 false（若为 true 会在 PerceptionEval/SceneContext 产生 hard blockers）
- H trace/replay/whitebox index 必须存在：pass（3 个 index 文件存在）
- I stage output 缺失必须 NO_GO：pass（verifier 检查 per-sample refs 均存在）
- J evidence boundary 保持：pass（evidence_type/controlled_live/phone_local/pending rates=1.0）

