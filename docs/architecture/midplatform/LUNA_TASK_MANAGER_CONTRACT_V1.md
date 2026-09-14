# Luna — Task Manager Contract v1

**Phase**：`Task-Manager-Contract-v1-001`  
**性质**：任务生命周期提交者契约；contract only；非 runtime

## 职责

Task Manager **拥有**任务生命周期提交权；MidPlatform / Voice / Navigation 只能提交 **candidate**。

- 接收 task state / lifecycle candidate（来自 MidPlatform）
- **Task Context Enrichment**：时空锚点、GPS、路线、场景、记忆引用、观察上下文等 **candidate**（非事实写入）
- transition guard、confirmation gate、safety gate、idempotency
- commit decision candidate（`allowed_now=false` 于 contract 阶段）
- rollback / abort、audit / trace
- 输出 guidance / speech **candidate**（不直接 TTS/VOP/导航）

## 边界

- `task_manager_runtime_available=false`
- `task_state_committed_now=false`
- 不创建/取消/暂停/恢复真实任务；不写事实层

## 下一推荐 Phase

**Task-Manager-Runtime-DryRun-v1** — 已完成（见 `LUNA_TASK_MANAGER_RUNTIME_DRYRUN_V1.md`）  
**Vision-OCR-Evidence-Ingest-Integration-Check-v1** — 下一集成检查

## 实现

- `capabilities/midplatform/task_manager_contract_v1.py`
- `tools/evaluation/midplatform/run_task_manager_contract_v1.py`
- `tools/evaluation/midplatform/verify_task_manager_contract_v1.py`
