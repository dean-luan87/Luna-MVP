# Luna — Basic Functional Loop Stabilization Plan v1

**Phase**：`Luna-Basic-Functional-Loop-Stabilization-Plan-v1-001`  
**性质**：主线功能稳定规划；plan only；非 runtime

## 策略

- **暂缓**：WorldModel runtime、Fragment Weaving runtime、Emotional Context runtime
- **优先稳定**：视觉、OCR（任务型）、语音、中台任务链、基础导航提示
- **受控后续接入**：画面切割、物体追踪、导航地图（future entry only）

## 最小闭环

User Voice → MidPlatform Task Context → Vision/OCR Candidate → Evidence Governance → Task State → Guidance → Speech Gate/VOP → Navigation Prompt

## 下一推荐 Phase（P0）

**Voice-Dialogue-Task-Control-Contract-v1** — 已完成（见 `LUNA_VOICE_DIALOGUE_TASK_CONTROL_CONTRACT_V1.md`）  
**Voice-Dialogue-Task-Control-Runtime-DryRun-v1** — 下一 runtime dry-run

## 实现

- `capabilities/midplatform/luna_basic_functional_loop_stabilization_plan_v1.py`
- `tools/evaluation/midplatform/run_luna_basic_functional_loop_stabilization_plan_v1.py`
- `tools/evaluation/midplatform/verify_luna_basic_functional_loop_stabilization_plan_v1.py`
