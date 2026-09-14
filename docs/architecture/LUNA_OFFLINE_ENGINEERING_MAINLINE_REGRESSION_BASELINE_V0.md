# LUNA Offline Engineering Mainline Regression Baseline v0

## Phase

- Phase-EngineeringFlow-Closure（Offline Engineering Mainline Closure v0）

## Purpose

记录 EF-006 regression acceptance 的基线输入 roots、硬门槛、允许波动项、不允许波动项，作为后续变更的阻断基线。

## Baseline roots (frozen snapshot)

- EF-004 normal_root：`logs/offline_mainline_ef004_20260428_105303`
- EF-004 fallback_root：`logs/offline_mainline_ef004_fallback_20260428_105303`
- EF-005 observability_root：`logs/offline_mainline_observability_ef005_20260428_1100`
- EF-006 regression_output_root：`logs/offline_mainline_regression_ef006_20260428_1112`

## Baseline hard thresholds (must pass)

以 EF-006 `regression_gate_results.json` 为准（硬门槛摘要）：

- Chain complete rates == 1.0（normal + fallback）
- Schema valid rates == 1.0（五阶段）
- Source policy distribution：normal yolo_shadow=3；fallback baseline_mock=3；fallback_count=3
- SceneContext complete_rate == 1.0
- Output：real_tts_invoked_false_rate == 1.0；allows_execute_now_false_rate == 1.0
- Observability：required files exist；EF-005 verifier all_pass；broken_refs == 0
- Safety leakage totals == 0（所有项）
- Evidence boundary rates == 1.0；mutation/closed counts == 0

## Allowed variance (v0)

不作为阻断项（允许变化，但必须记录）：

- detection_count_total 可变化
- detected class distribution 可变化
- message_text_candidate 可模板化
- SceneContext degraded_or_uncertain 可保持 true
- fusion/output policy 维持 v0 minimal rules
- 样本数仍为 3
- report 无 UI/可视化

## Not allowed (any is NO_GO)

- candidate-only 被破坏
- real_tts_invoked=true
- allows_execute_now=true
- pending_real_sidewalk_run=false
- controlled_live_stream=true
- evidence_type 被改写
- fallback path 不可用
- source policy audit 字段缺失（导致无法判断 source 分布）
- trace/replay/whitebox index 缺失
- safety leakage 非 0

