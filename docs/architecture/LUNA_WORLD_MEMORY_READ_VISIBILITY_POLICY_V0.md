# LUNA — World Memory Read Visibility Policy v0

## Phase

- **Phase-WorldModel-WriteReadiness-002**

## Purpose

定义不同状态/等级的世界记忆对象的读取可见性：哪些可被任务读取、哪些只能审计读取、哪些隔离态不可用于任务。

本阶段只定义，不实现 runtime。

## Visibility classes

- `task_readable`：可被任务链读取（但不得直接触发动作，需遵循更上层门控）
- `weak_readable`：弱读取（仅用于补充上下文，不得主导决策）
- `audit_only`：仅审计/回放可读
- `hidden`：默认不可读（仅隔离/人工复核）

## Policy（v0）

- `committed_scene_local`：默认 `weak_readable`
- `committed_persistent`：默认 `task_readable`（仍需 domain policy + revalidation 门控）
- `persistent_candidate_requires_revalidation`：默认 `audit_only` 或 `weak_readable`（不得强决策）
- `quarantined`：`hidden`（不可任务读取/推荐/播报）
- `expired/superseded`：`audit_only`（历史/审计）
- `contradicted`：`audit_only`（冲突分析）

## Hard rules（强制）

- `quarantined` 不得被任务直接读取
- `commercial_activity` 不得作为 `task_readable` 的长期事实
- 所有可见性变更必须通过 revision + audit envelope 记录

## Spatiotemporal binding constraints（硬约束）

读取可见性必须受 `spatiotemporal_binding` 的时间/空间范围限制：

- **temporal scope**：过期（`valid_until` 之外）或弱时间置信的记忆不得作为强信号消费
- **spatial scope**：不允许跨 `spatiotemporal_anchor_ref` 误用；`scope_type/anchor_ref` 不匹配时必须降级到 `audit_only` 或拒绝
- **weakly_bound/unresolved**：只能 `weak_readable` 或 `audit_only`，不得 `task_readable`

