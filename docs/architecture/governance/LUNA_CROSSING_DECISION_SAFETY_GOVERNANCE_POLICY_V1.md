# Luna — Crossing Decision Safety Governance Policy v1

**Phase**：`Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`  
**性质**：policy / governance / boundary only  
**边界**：不实现 crossing runtime，不判断真实过街安全，不读取真实图像，不打开摄像头，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 GPS runtime，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音

## 目标

本阶段只回答：

1. 为什么 `Crossing Decision` 不能归入普通导航  
2. 什么信息可以作为 crossing evidence candidate  
3. 什么信息不能作为 crossing permission  
4. 红绿灯候选、绿灯候选、倒计时 OCR、人流、地图 hint、路线提示、用户说“走”分别有什么边界  
5. 信息不足、冲突、过期、低置信时如何保守处理  
6. 什么情况下必须输出 `stop / hold / confirm / seek human assistance candidate`  
7. 输出如何保持 `candidate-only`  
8. 如何继承 `Safety Constitution`  
9. 如何为后续 `Crossing Decision DryRun / Controlled Sample / Runtime Guarded Trial` 预留边界

## Policy Position

本阶段必须明确：

- `Crossing Decision` 继承 `Safety Constitution`
- crossing governance 仍然是 policy-only
- `crossing_runtime_allowed=false`
- `crossing_permission_output_allowed=false`
- `crossing_action_instruction_allowed=false`
- 当前 phase 不能决定 `safe-to-cross`

## Crossing Evidence Candidate Schema

允许的 evidence candidate 类型：

- `traffic_light_candidate`
- `traffic_light_state_change_candidate`
- `green_light_candidate`
- `red_light_candidate`
- `countdown_text_candidate`
- `crosswalk_candidate`
- `curb_candidate`
- `vehicle_flow_candidate`
- `vehicle_approach_candidate`
- `pedestrian_flow_candidate`
- `crowd_flow_candidate`
- `map_crossing_hint_candidate`
- `route_crossing_hint_candidate`
- `user_feedback_candidate`
- `audio_environment_candidate`
- `staff_or_human_assistance_candidate`

统一边界：

- `current_action_allowed=false`
- `crossing_permission_allowed=false`
- `fact_status=not_fact`

## Crossing Permission Boundary

本阶段写死以下红线：

- `traffic_light_candidate_not_crossing_permission=true`
- `green_light_candidate_not_crossing_permission=true`
- `countdown_text_candidate_not_crossing_permission=true`
- `crowd_flow_candidate_not_crossing_permission=true`
- `pedestrian_flow_candidate_not_crossing_permission=true`
- `map_crossing_hint_not_crossing_permission=true`
- `route_crossing_hint_not_crossing_permission=true`
- `user_says_go_not_crossing_permission=true`
- `memory_hint_not_crossing_permission=true`
- `single_modality_evidence_not_crossing_permission=true`
- `stale_evidence_not_crossing_permission=true`
- `conflicting_evidence_not_crossing_permission=true`
- `low_confidence_evidence_not_crossing_permission=true`

这表示：

- 红绿灯、倒计时、人流、地图提示、路线提示、用户说“走”，都不能单独变成过街许可
- 单模态、过期、冲突、低置信 evidence 都不能变成过街许可

## Crossing Uncertainty Policy

本阶段冻结如下保守规则：

- `insufficient_evidence -> HOLD_OR_CONFIRM_CANDIDATE`
- `low_confidence -> HOLD_OR_CONFIRM_CANDIDATE`
- `stale_evidence -> REOBSERVE_CANDIDATE`
- `conflicting_evidence -> REOBSERVE_OR_HUMAN_ASSISTANCE_CANDIDATE`
- `occluded_vehicle_flow -> DO_NOT_ADVANCE_CANDIDATE`
- `traffic_light_uncertain -> DO_NOT_ADVANCE_CANDIDATE`
- `no_crosswalk_detected -> DO_NOT_CROSS_CANDIDATE`
- `map_only_crossing_hint -> VISUAL_CONFIRMATION_REQUIRED_CANDIDATE`

## Crossing Conflict Policy

本阶段至少覆盖：

- `green_light_vs_vehicle_flow_conflict`
- `map_crossing_hint_vs_visual_absence`
- `crowd_flow_vs_traffic_uncertain`
- `ocr_countdown_vs_traffic_light_uncertain`
- `route_says_cross_vs_safety_uncertain`
- `user_instruction_vs_safety_boundary`
- `stale_memory_vs_current_observation`
- `audio_cue_vs_visual_uncertain`

冲突原则：

- conflict blocks crossing action
- conflict cannot be resolved by LLM guess
- conflict cannot be resolved by map alone
- conflict cannot be resolved by user command alone
- conflict requires `reobserve / hold / human assistance`

## Crossing Output Policy

允许输出：

- `NO_OUTPUT_SUPPRESSED`
- `SAFETY_HOLD_CANDIDATE`
- `REOBSERVE_CANDIDATE`
- `HUMAN_ASSISTANCE_CANDIDATE`
- `LOW_CONFIDENCE_WARNING_CANDIDATE`
- `VISUAL_CONFIRMATION_REQUIRED_CANDIDATE`
- `TEXT_ONLY_DRY_PREVIEW`

禁止输出：

- `CROSS_NOW`
- `SAFE_TO_CROSS`
- `GO_AHEAD`
- `PROCEED`
- `FOLLOW_THE_CROWD`
- `GREEN_LIGHT_GO`
- `MAP_SAYS_CROSS`
- `COUNTDOWN_SAYS_GO`

并继续保持：

- `speech_allowed=false`
- `user_heard_assumed=false`
- `action_allowed=false`
- `navigation_action_allowed=false`

## Crossing Human Assistance Policy

本阶段只允许 candidate 级的人类协助建议：

- 什么时候建议寻求人类协助
- 什么时候建议寻求工作人员协助
- 什么时候必须停下等待
- 什么时候要求用户自行进行视觉 / 听觉确认
- 什么时候必须声明信息不足

但仍保持：

- no real speech output
- no task state commit
- no navigation action
- no assumption that human assistance was obtained

## Scenario Matrix

本阶段至少覆盖以下 14 个场景：

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

这些场景共同验证：

- `green light` 不等于过街许可
- `countdown OCR` 不等于过街许可
- `crowd flow` 不等于跟着过
- `route says cross` 不等于可执行动作
- 冲突、遮挡、过期、低置信必须保守

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY_READY_FOR_CROSSING_DECISION_DRYRUN`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Crossing-Decision-DryRun-v1-001`

这表示：

- Luna 已完成 `Crossing Decision` 的专项安全治理边界冻结
- 当前仍然不做真实过街判断
- 当前仍然不允许输出“可以过马路”或等价行动指令
- 下一阶段可以进入严格的 `Crossing Decision DryRun`

## 当前状态更新

- `Phase-Crossing-Decision-DryRun-v1-001 = GO`
- `final_decision=CROSSING_DECISION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- dry-run 已用 16 个模拟场景验证保守候选输出与 forbidden register 全部缺席
- `Phase-Crossing-Decision-Post-DryRun-Review-v1-001 = GO`
- `final_decision=CROSSING_DECISION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `Phase-Crossing-Decision-Closure-v1-001 = GO`
- `final_decision=CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE`
