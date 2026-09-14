# LUNA — World Model Write Level & State Policy v0

## Phase

- **Phase-WorldModel-WriteReadiness-001**

## Purpose

定义候选证据进入写入评估与写入后的 **状态机** 与 **写入等级**，用于：

- 防污染
- 防误写
- 可回滚
- 可审计

本阶段只定义，不实现 runtime。

## WorldEvidenceWriteState（状态机）

- `candidate_only`
- `write_evaluation_pending`
- `provisional_world_memory`
- `verified_scene_local_memory`
- `persistent_world_memory`
- `writable_low_priority`
- `writable_scene_local`
- `writable_persistent_requires_revalidation`
- `committed_scene_local`
- `committed_persistent`
- `rejected`
- `expired`
- `superseded`
- `contradicted`
- `rollback_required`
- `quarantined`

### State notes（语义）

- `candidate_only`：默认状态（ContextEvidence-004 产物从这里开始）
- `write_evaluation_pending`：进入写入评估，但尚未通过
- `provisional_world_memory`：占位优先的存疑写入（有保存价值但不足以作为事实；弱读取；必须可复核/可回滚）
- `verified_scene_local_memory`：通过复核后的局部验证记忆（仍有范围与时效约束）
- `persistent_world_memory`：通过更高门槛后的长期稳定记忆（仍需 revision/audit）
- `writable_*`：只表示“具备写入资格”，不代表已经写入
- `committed_*`：表示已写入（本阶段不实现写入，仅定义状态语义）
- `rollback_required`：不允许“冲突证据直接覆盖”，只能触发回滚/降级/复核
- `quarantined`：疑似污染、欺诈、冲突或异常证据隔离区

## WorldModelWriteLevel（写入等级）

1. `no_write`：不写入，只保留 trace/audit
2. `audit_only`：只保留审计证据，不进入世界模型
3. `ephemeral_scene_cache`：临时场景缓存，短 TTL，用于当前/短期上下文
4. `scene_local_memory`：局部场景记忆（可复核）
5. `provisional_placeholder`：占位写入（存疑优先；弱读取；不可强驱动；不可当作稳定事实传播）
6. `verified_scene_memory`：已验证的场景记忆（局部范围）
5. `persistent_world_candidate`：长期候选（仍需周期复核）
6. `committed_world_memory`：长期事实/记忆（高门槛）
7. `quarantine_store`：隔离区（风险/冲突/污染）

## Default mapping（概念性）

Write Readiness 评估产出：

- `allowed_write_level`（本次允许的最高写入等级）
- `write_readiness_status`（ready_* / rejected / quarantine）

并将其投影到 `WorldEvidenceWriteState`：

- `ready_low_priority` → `writable_low_priority`
- `ready_scene_local` → `writable_scene_local`
- `ready_persistent_candidate` → `writable_persistent_requires_revalidation`
- `rejected` → `rejected`
- `quarantine` → `quarantined`

补充（Commit Layer 默认原则：占位优先、事实提交滞后）：

- 通过 WriteReadinessCheck ≠ 直接写成稳定事实
- 默认先进入 `provisional_world_memory`（`provisional_placeholder`），再复核升级到 verified/persistent

## Constitution link（宪法级约束）

写入等级与状态机受“世界模型时空绑定宪法”约束：

- `docs/architecture/LUNA_WORLD_MODEL_SPATIOTEMPORAL_BINDING_CONSTITUTION_V0.md`

补充规则（v0）：

- `unresolved` binding → `no_write` / `audit_only`
- `weakly_bound` → 只能 `provisional_world_memory`（占位存疑）
- `bound` + lifecycle valid + trust pass → 才允许进入 `verified_scene_local_memory` / `persistent_world_memory`
- `expired/contradicted` binding → `rollback_required` / `requires_revalidation` / `quarantined`

