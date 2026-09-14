# Luna — Voice Dialogue Task Control Contract v1

**Phase**：`Voice-Dialogue-Task-Control-Contract-v1-001`  
**性质**：语音对话任务控制契约；contract / schema / policy only；非 runtime

## 目标

定义用户通过语音/对话控制任务的最小契约（发起、澄清、查询、重复、暂停、恢复、取消、确认目标/场景/继续），并与中台任务状态机挂钩；本阶段 **不执行** runtime。

## 核心原则

1. Voice Input 只生成 **intent candidate** / **command candidate**
2. Voice **不能**直接修改任务状态
3. 任务状态变更由 **MidPlatform / Task Manager** 决定
4. 所有对话输出必须经 **Speech Gate / VOP**
5. 用户确认与对话表达默认 **not_fact**；`write_allowed=false`

## 覆盖能力

- 13 类 intent（含 `START_TASK`、`CANCEL_TASK`、`REPEAT_LAST_GUIDANCE` 等）
- 10 类 command candidate（`CREATE_TASK_CANDIDATE`、`CANCEL_TASK_CANDIDATE` 等）
- dialogue-to-task handoff、短期对话上下文、repeat/pause/resume/cancel、query/clarification/safety、Speech Gate/VOP 输出策略
- 11 态对话 FSM contract、10 条最小中文模板矩阵
- MidPlatform / Task Manager 边界、导航引导链接策略

## 禁止（本 phase）

- ASR / LLM / TTS / VOP runtime
- 真实任务创建/取消/暂停/恢复
- Memory / WorldModel / SceneDelta 写入
- OCR / camera / runtime routing 变更

## 下一推荐 Phase

**Voice-Dialogue-Task-Control-Runtime-DryRun-v1** — 已完成（见 `LUNA_VOICE_DIALOGUE_TASK_CONTROL_RUNTIME_DRYRUN_V1.md`）  
**MidPlatform-Task-State-Runtime-DryRun-v1** — 下一集成 dry-run

## 实现

- `capabilities/midplatform/voice_dialogue_task_control_contract_v1.py`
- `tools/evaluation/midplatform/run_voice_dialogue_task_control_contract_v1.py`
- `tools/evaluation/midplatform/verify_voice_dialogue_task_control_contract_v1.py`
