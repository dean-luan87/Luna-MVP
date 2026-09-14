# Luna — Task Observation Request Contract v1

**Phase**：`Task-Observation-Request-Contract-v1-001`  
**性质**：观察需求标准化层；contract only；**非** camera/OCR/detector 调用

## 定位

Observation Request 回答：为什么观察、观察什么、可能在哪、baseline 还是 task-driven、需要 vision/OCR/用户引导/人工帮助/地图记忆参考、是否允许、须经哪些 gate、结果如何进入 evidence ingest。

## 请求来源

- `baseline_safety_loop`（可无任务）
- `task_manager_action_schedule` / `midplatform_task_state` / `task_context_enrichment`
- `user_guidance_recovery` / `safety_task_arbitration`

## 边界

- `request_allowed_now=false`（contract 阶段）
- OCR 须经 OCR activation + STC joint gate
- Voice 不得直接生成 observation request
- 不写 fact；不 invoke camera/OCR/VOP

## 下一推荐 Phase

**Vision-OCR-Evidence-Ingest-Integration-Check-v1** — 已完成（见 `LUNA_VISION_OCR_EVIDENCE_INGEST_INTEGRATION_CHECK_V1.md`）  
**Navigation-Guidance-to-Speech-Candidate-Adapter-v1**

## 实现

- `capabilities/midplatform/task_observation_request_contract_v1.py`
- `tools/evaluation/midplatform/run_task_observation_request_contract_v1.py`
- `tools/evaluation/midplatform/verify_task_observation_request_contract_v1.py`
