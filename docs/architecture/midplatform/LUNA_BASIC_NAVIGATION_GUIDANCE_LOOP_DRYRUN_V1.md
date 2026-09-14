# Luna — Basic Navigation Guidance Loop DryRun v1

**Phase**：`Basic-Navigation-Guidance-Loop-DryRun-v1-001`  
**性质**：端到端候选链 dry-run；非真实导航

## 双链

**Baseline Safety**（可无任务）：observation → vision evidence → action support → speech candidate → Speech Gate/VOP candidate

**Task-Driven**（须 task context）：task schedule → observation → vision/OCR evidence → action/verification support → guidance → speech candidate

## 边界

- dry-run only；不触发 TTS/VOP/导航/相机/OCR；不写 fact

## 下一推荐 Phase

**Safety-Task-Arbitration-Policy-v1** — 已完成（见 `LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md`）  
**Voice-Command-Ownership-Gate-Policy-v1** — 已完成（见 `../voice/LUNA_VOICE_COMMAND_OWNERSHIP_GATE_POLICY_V1.md`）  
**Voice-Interruption-Governance-DryRun-v1** — 已完成  
**Basic-Navigation-Guidance-Loop-Stabilization-Test-v1** — 已完成（见 `LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_TEST_V1.md`）  
**Minimal-Runtime-Integration-Trial-Definition-v1** — 已完成  
**Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1**

## 实现

- `capabilities/midplatform/basic_navigation_guidance_loop_dryrun_v1.py`
- `tools/evaluation/midplatform/run_basic_navigation_guidance_loop_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_basic_navigation_guidance_loop_dryrun_v1.py`
