# Luna — Navigation Guidance to Speech Candidate Adapter v1

**Phase**：`Navigation-Guidance-to-Speech-Candidate-Adapter-v1-001`  
**性质**：adapter only；guidance → speech candidate；非 TTS/VOP runtime

## 链路

```
Action support / Task downstream guidance
  → SpeechRequest candidate
  → Speech Gate admission (dryrun candidate)
  → VOP handoff candidate (later)
```

## 边界

- guidance ≠ speech；speech candidate ≠ TTS；VOP handoff ≠ VOP 调用
- safety 优先；全部须经 Speech Gate；禁止 direct TTS/VOP bypass
- 不写 fact；不 commit task；不触发导航

## 下一推荐 Phase

**Basic-Navigation-Guidance-Loop-DryRun-v1** — 已完成（见 `LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_DRYRUN_V1.md`）  
**Safety-Task-Arbitration-Policy-v1**

## 实现

- `capabilities/midplatform/navigation_guidance_to_speech_candidate_adapter_v1.py`
- `tools/evaluation/midplatform/run_navigation_guidance_to_speech_candidate_adapter_v1.py`
- `tools/evaluation/midplatform/verify_navigation_guidance_to_speech_candidate_adapter_v1.py`
