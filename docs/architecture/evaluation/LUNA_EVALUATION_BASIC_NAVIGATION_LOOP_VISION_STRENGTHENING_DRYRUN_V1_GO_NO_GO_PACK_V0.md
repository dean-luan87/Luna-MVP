# Luna Evaluation — Basic Navigation Loop Vision Strengthening DryRun v1 GO / NO-GO Pack

对应 phase：`Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001`

## GO Conditions

- required input roots 全部成功加载
- `NavigationVisionStrengtheningDryRunCase` / `NavigationFeedbackIntakeCandidate` / `VisionAwareNavigationGuidanceCandidate` / `NavigationSafetyArbitrationBridgeCandidate` / `NavigationOutputCandidateDryRun` / `NavigationVisionStrengtheningBoundaryDecision` 六个 schema 全部定义
- 12 个指定 dry-run 场景全部覆盖
- 每个场景都生成：
  - `NavigationFeedbackIntakeCandidate`
  - `VisionAwareNavigationGuidanceCandidate`
  - `NavigationSafetyArbitrationBridgeCandidate`
  - `NavigationOutputCandidateDryRun`
  - `NavigationVisionStrengtheningBoundaryDecision`
- `guidance_candidate_count>=12`
- `output_candidate_count>=12`
- safety priority / task guidance / active view adjustment / ocr later / tracking later / map conflict / crossing uncertain 全部至少覆盖一例
- `boundary_ok=true`
- `violations=[]`

## NO_GO Conditions

- 任一 required input root 未加载
- 任一 required document 缺失
- 任一 schema 未定义
- `scenario_count<12`
- 任一指定场景缺失
- `dryrun_results_generated!=true`
- `guidance_candidate_count<12`
- `output_candidate_count<12`
- 出现 runtime / write / speech / action 越权
- `ocrrequest_submitted=true`
- `tracking_runtime_invoked=true`
- `safety_task_arbitration_runtime_invoked=true`
- `speech_gate_invoked=true`
- `tts_invoked=true`
- `vop_invoked=true`
- `navigation_action_triggered=true`
- `world_model_written=true`
- `memory_written=true`
- `library_written=true`
- `fact_written=true`
- `entity_resolution_runtime_invoked=true`
- `memory_consolidation_invoked=true`

## GO Meaning

`GO` 的语义仅表示：

- 第一轮“视觉增强导航闭环” dry-run 成立
- `Visual-OCR-Map-Task feedback` 已可回流到 `Basic Navigation Guidance Loop`
- `Safety-Task Arbitration` 已有 dry-run bridge candidate
- `Navigation Guidance Candidate` 与 `Text-only / dry output candidate` 链路成立

`GO` **不表示**：

- live navigation 已启用
- camera / OCR provider / tracking / map API 可调用
- `Speech Gate / VOP / TTS` 已开放
- `WorldModel / Memory / Fact / Library` 可写
- 可以直接触发导航动作

## Next Phase

本阶段通过后，只允许推荐：

- `Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001`

下一阶段仍然：

- 不接真实 `camera / OCR provider / tracking / map API`
- 不导入或调用 `Supervision / ByteTrack / OC-SORT`
- 不写 `WorldModel / Memory / Fact / Library`
