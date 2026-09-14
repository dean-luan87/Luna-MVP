# LUNA — Scene Delta Task Context Re-evaluation Policy v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose

写死“task_context_changed 即使内容未变也允许重评”的中台规则，避免把旧分类/旧路由错误地复用到新任务。

本阶段只定义，不实现。

## Core rule（冻结）

即使信息本身没有变化，如果 task_context 变化，仍允许重新评估 relevance 与下游路由：

- `change_summary.task_context_changed=true`
- `delta_status=task_context_changed`
- 默认触发 `delta_action=full_reprocess | partial_update`（由输入类型与签名比较结果决定）

## Examples（定义性示例）

### 示例 1：商业信息从 ambient → 体验增强

- 默认看到“星巴克第二杯半价”
  - `commercial_context_text`
  - `ambient_context_candidate`
  - 不进入任务链

- 用户任务变成“帮我找咖啡店”
  - `task_context_changed=true`
  - 触发重评
  - 允许作为 `experience_enrichment_candidate`（仍禁止导航动作，仍 candidate-only）

### 示例 2：用户明确请求读取（user_requested_override）

- 用户说“读一下这个广告牌”
  - `user_requested_override=true`
  - 允许 readout candidate
  - `navigation_action` 仍必须为 `null`

## Relationship to filtering/blocking（约束）

task_context_changed 只能影响“是否重评与是否重新进入处理链”，不改变治理禁止项：

- 不允许执行（allows_execute_now=false）
- 不允许导航动作
- 不允许真实播报
- 不允许真实世界模型写入

