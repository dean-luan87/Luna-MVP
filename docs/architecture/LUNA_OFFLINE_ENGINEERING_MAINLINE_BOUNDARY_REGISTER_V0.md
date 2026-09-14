# LUNA Offline Engineering Mainline Boundary Register v0

## Phase

- Phase-EngineeringFlow-Closure（Offline Engineering Mainline Closure v0）

## Purpose

冻结离线工程主链（EF-001~EF-006）禁止项与写死声明，确保后续不会把 offline mainline 误解为真实 runtime 或 controlled live。

## Hard boundary statements (must remain true)

### Runtime & live

- `runtime_allowed=false`
- `controlled_live_allowed=false`
- 不进入 `controlled_live_stream`
- 不进入 full controlled trial
- 不开放真实用户测试
- 不允许直接进入用户侧

### Execution & side effects

- `navigation_execution_allowed=false`
- 不执行导航动作
- 不扩大真实 side effects 面
- 不允许任何“默认路径”隐式打开执行面

### Voice / output

- `real_tts_allowed=false`
- 不真实播报（禁止 real TTS 调用）

### Evidence boundary

- `pending_real_sidewalk_run` **必须保持 true**
- 不关闭 pending（不得把 pending_real_sidewalk_run 改成 false）
- 不改变 `evidence_type`
- 不允许 evidence boundary 被破坏（controlled_live_stream=true / evidence_type mutation / pending closed 等均为 NO_GO）

### Capability expansion prohibited in closure context

- 不扩 Option A
- 不做 tracking/depth/OCR/dynamic 能力增强（这些必须走 future branch）
- 不新增模型能力（本 closure 与 regression 基线语境下）
- 不改变主链 runner 的安全边界（fail-closed 逻辑不可弱化）

## Enforcement

后续任何改动必须：

- 先通过 EF-006 regression acceptance（硬门槛全通过）
- 若 regression fail：必须阻断后续 closure/合并/发布路径（离线工程主链治理）

