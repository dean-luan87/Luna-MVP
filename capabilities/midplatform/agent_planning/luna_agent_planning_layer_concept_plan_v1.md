# Luna Agent Planning Layer — Concept Planning v1

**Phase:** Phase-P1-Midplatform-Luna-Agent-Planning-Layer-Concept-Planning-v1-001  
**Layer:** L2 Agent Planning  
**Status:** Concept planning only — no tool execution, no runner, no fact write

## 1. 为什么需要 L2

L1 Situation Understanding 回答「我处在什么状态、缺什么信息、可能需要什么能力」。  
L2 Agent Planning 回答「接下来怎么做」：目标、步骤、工具计划、失败降级、问用户时机、停止条件，以及如何交给 Tool OS。

## 2. Luna 分层

```
L0 Survival Constitution
L1 Situation Understanding   — scene / task clues / missing info / model need hints
L2 Agent Planning            — 本阶段：plan / tool plan / fallback / handoff
L3 Tool Operating System     — admission / sandbox / envelope / fact admission
L4 Perception / Action Tools — OCR / SAM / Detection / SLAM / …
```

## 3. 边界

### 与 L1 Situation Understanding

| L1 | L2 |
|----|----|
| 输出 situation_understanding_candidate | 消费 L1 输出，生成 agent_plan_candidate |
| 拥有 scene | 不改写 scene |
| model_need_hints | 转为 tool_plan / noop_tool_plan |

### 与 L3 Tool OS

| L2 | L3 |
|----|----|
| handoff_to_tool_os_candidate | 执行 admission / runner / sandbox |
| 不触发 runner | 管理执行与错误 |
| 不写 fact | Fact Admission 在结果之后 |

### 与 Model Activation / Followup Runner Route

Agent Planning 可参考既有 activation / followup 语义，但本阶段独立输出 plan candidate，不直接生成 runner task 或修改既有队列。

## 4. 规划驱动

plan steps 由以下输入驱动：

- `user_goal_candidate`（可覆盖 task_clue 优先级，须留 trace）
- `task_clue_candidates`
- `missing_information_candidates`
- `model_need_hints`（likely / optional / not_needed → tool_plan / noop）

## 5. 输出原则

- 只输出 `agent_plan_candidate`
- `candidate_only=true`，`not_fact=true`
- 不直接执行工具，不安装工具，不调用 runner
- 工具执行必须经 `handoff_to_tool_os_candidate`（含 runner_admission / fact_admission 标记）

## 6. 场景策略摘要

| 场景 / 目标 | 计划重点 | noop |
|-------------|----------|------|
| shopfront + read/identify | OCR tool plan | SLAM / Tracking / Depth |
| subway + find_direction | OCR (± Detection optional) | SLAM unless navigate |
| street_crossing + walkable | Detection / Depth / Tracking | full-image OCR |
| corridor + navigate | Depth / SLAM | OCR unless text |
| unknown_scene | ask_user / VLM / manual_review | blanket tools |

## 7. 本阶段禁止

- 真实联网、真实 teacher、训练模型
- 执行 OCR/SAM/SLAM/Detection/VLM
- 修改 runner、写 fact、触发 Tool OS execution

## 8. 下一阶段建议

**优先：** Phase-P1-Midplatform-Luna-Agent-Planning-Layer-DryRun-v1-001  
将 Agent Planning 接入 L1 dry-run，验证 job_564f1aa93983 → OCR tool plan + SLAM/Tracking/Depth noop + Tool OS handoff。
