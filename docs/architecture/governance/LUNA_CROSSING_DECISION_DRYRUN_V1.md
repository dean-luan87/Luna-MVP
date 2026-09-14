# Luna — Crossing Decision DryRun v1

**Phase**：`Phase-Crossing-Decision-DryRun-v1-001`  
**性质**：dry-run / candidate simulation / governance validation / boundary verification only  
**边界**：不实现 crossing runtime，不判断真实过街安全，不读取真实图像，不打开摄像头，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 GPS runtime，不调用 tracking runtime，不调用 optical flow runtime，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音

## 目标

本阶段只回答：

1. `Crossing Safety Governance` 是否能在 dry-run 中生效  
2. 单一绿灯候选是否会被阻止成为过街许可  
3. 倒计时 OCR 候选是否会被阻止成为过街许可  
4. 人流前进是否会被阻止成为“跟随人流”指令  
5. 地图 crossing hint 是否会被阻止成为过街许可  
6. 路线提示“需要过街”是否会被阻止成为过街许可  
7. 用户说“走”是否仍会被安全宪法阻断  
8. 冲突、遮挡、低置信、过期证据是否触发 hold / reobserve / human assistance  
9. forbidden crossing outputs 是否完全不会出现  
10. dry-run 是否保持 no-runtime / no-write / no-action / no-speech

## DryRun Position

- `dryrun_scope=crossing_decision_dryrun_only`
- `inherits_safety_constitution=true`
- `crossing_runtime_allowed=false`
- `crossing_permission_output_allowed=false`
- `crossing_action_instruction_allowed=false`
- `safe_to_cross_claim_allowed=false`
- 所有 evidence 都是 **candidate**，不是 fact

## 核心对象

| 对象 | 说明 |
|------|------|
| `CrossingDecisionDryRunCase` | 单个 dry-run 场景定义 |
| `SimulatedCrossingEvidenceSet` | 模拟 crossing evidence candidates |
| `CrossingGovernanceDecisionCandidate` | 保守决策候选输出 |
| `ForbiddenCrossingOutputCheck` | 逐 case 检查 forbidden register |
| `CrossingConflictEvaluationCandidate` | 冲突评估候选 |
| `CrossingUncertaintyEvaluationCandidate` | 不确定性评估候选 |
| `CrossingDryRunBoundaryDecision` | 单 case 边界决策 |

## 允许的 decision_type

- `SAFETY_HOLD_CANDIDATE`
- `REOBSERVE_CANDIDATE`
- `HUMAN_ASSISTANCE_CANDIDATE`
- `LOW_CONFIDENCE_WARNING_CANDIDATE`
- `VISUAL_CONFIRMATION_REQUIRED_CANDIDATE`
- `NO_OUTPUT_SUPPRESSED`

## 禁止的输出

- `SAFE_TO_CROSS`
- `CROSS_NOW`
- `GO_AHEAD`
- `PROCEED`
- `FOLLOW_THE_CROWD`
- `GREEN_LIGHT_GO`
- `MAP_SAYS_CROSS`
- `COUNTDOWN_SAYS_GO`

## 必须覆盖的 16 个场景

1. `green_light_candidate_only`
2. `green_light_with_vehicle_flow_uncertain`
3. `red_light_candidate`
4. `countdown_text_candidate_only`
5. `crowd_flow_forward`
6. `map_crossing_hint_only`
7. `route_says_cross`
8. `user_says_go`
9. `crosswalk_candidate_but_vehicle_occluded`
10. `traffic_light_uncertain`
11. `no_crosswalk_detected`
12. `stale_traffic_light_evidence`
13. `conflicting_audio_visual_cues`
14. `unknown_speaker_says_safe`
15. `green_light_plus_crowd_flow_plus_map_hint`
16. `all_evidence_low_confidence`

## 实现位置

- Capability：`capabilities/governance/crossing_decision_dryrun_v1.py`
- Runner：`tools/evaluation/governance/run_crossing_decision_dryrun_v1.py`
- Verifier：`tools/evaluation/governance/verify_crossing_decision_dryrun_v1.py`

## Final Verdict

当 runner / verifier 全部通过时：

- `final_decision=CROSSING_DECISION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Crossing-Decision-Post-DryRun-Review-v1-001`

这表示：

- dry-run 已验证保守候选输出稳定
- forbidden crossing outputs 全部缺席
- 当前仍然不做真实过街判断
- 下一阶段进入 Post-DryRun Review，再考虑 closure

## 当前状态更新

- `Phase-Crossing-Decision-Post-DryRun-Review-v1-001 = GO`
- `final_decision=CROSSING_DECISION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `Phase-Crossing-Decision-Closure-v1-001 = GO`
- `final_decision=CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE`
