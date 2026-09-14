# LUNA — MidPlatform OCR Bridge Boundary Register v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-003**

## Purpose

登记并冻结 OCR Raw Text → MidPlatform bridge 的禁止项与硬边界，作为 `closed_v0` 的“边界清单”。

## Hard boundaries（冻结）

### 禁止接入与调用

- 不接真实 runtime
- 不接真实中台（real MidPlatform）
- 不接 SceneTask / Fusion / Output
- 不接推荐系统

### 禁止输出与动作

- 不做最终语义提炼：`semantic_summary` 必须为 `null`
- 不生成/不执行导航动作：`navigation_action` 必须为 `null`
- `allows_execute_now=false`（禁止执行）
- `real_tts_invoked=false`（禁止真实播报）
- `downstream_invocation_count=0`（禁止下游调用）

### 禁止写入

- 不写入真实世界模型持久层（world model write not allowed）
- world/ambient/world-context 仅允许 candidate-only 形态

## Auditability invariants（冻结）

- 所有 evidence 必须保留 trace/replay/whitebox 引用
- blocked evidence 不得物理删除，必须保留 `retained_evidence_ref`
- 所有分流/阻断必须记录 `block_level` / `block_reason`

