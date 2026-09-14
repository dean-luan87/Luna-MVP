# Luna — Navigation Governance Action Release Control First Live Launch Dry-Run v0（第一次真实放权试运行：最终发车演练层冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_V0.md`  
**性质**：Phase-Next-83：冻结 “approved 之后、真实执行之前” 的最终发车演练层（可冻结、可回归；默认不放权）

基于（已具备）：
- approval gate（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`
- enablement plan（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_PLAN_V0.md`
- enablement dry-run stub（演练层；不放权）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_DRY_RUN_STUB_V0.md`
- live release gate（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`
- side-effect release gate（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`
- guarded live stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 第一次真实放权试运行前的**最终发车演练层**设计文档。
- 当前目标：冻结“approval 之后、真实执行之前”的最后发车前检查层。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在必须先定义 first live launch dry-run

- 当前已经有 approval gate minimal implementation。
- 当前已经有 live release gate / side-effect release gate。
- 当前 `side_effects_released` 仍锁死为 `false`。
- 如果没有 launch dry-run，后续会从 `approved` 直接跳到真实执行，缺少“发车前最后一次演练检查”这一层。
- 因此必须先冻结（并尽量实现）dry-run 层，再考虑真实 live implementation。

---

## C. first live launch dry-run 的最小定义（写死）

`release_control first live launch dry-run` 是：

- approval 通过之后、真实第一次放权试运行之前的最终发车演练层
- 只负责检查是否具备最后发车条件，并产出统一结果

它不是：

- approval gate 本身
- live release gate 本身
- side-effect release gate 本身
- 真实执行器
- 真正的 live implementation

核心定义（写死一句）：

> launch dry-run 只决定“批准通过后，是否具备最后发车条件”，不直接执行动作，也不直接打开 `side_effects_released`。

---

## D. 最小合法输入（写死只允许消费）

launch dry-run **只允许消费**以下输入（缺一不可；缺任一则不成立）：

1) `navigation_governance_action_release_control_first_live_enablement_approval_gate_v0`  
- 必须 `approval_status == "first_live_enablement_approved"`

2) `navigation_governance_action_release_control_live_release_gate_v0`  
- 必须 `live_release_status == "live_release_ready"`

3) `navigation_governance_action_release_control_side_effect_release_gate_v0`  
- 必须 `side_effect_release_status == "side_effect_release_ready"`

4) guarded live stub 状态  
- 必须已进入 candidate（`payload.live_stub_entered == true`）  
- 且 `payload.side_effects_released == false`

5) `navigation_governance_action_release_control_execution_state_v0`（回传面在位）  
6) `navigation_governance_action_release_control_result_v0`（回传面在位）  
7) minimal executor / guarded live stub identity & capability（本体在位与能力边界依据）  
8) failure / rollback path 演练能力（至少语义上已在位，可用于 dry-run 检查）

并写死：

- 缺任一主前提，launch dry-run 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## E. 最小结果集合（写死收敛）

- `first_live_launch_dry_run_ready`
- `first_live_launch_dry_run_not_ready`
- `first_live_launch_dry_run_blocked`

语义（写死）：

1) `first_live_launch_dry_run_ready`
- 仅表示：approval 通过后，系统具备最后发车前条件
- 不表示动作已执行
- 不表示副作用已发生
- 不表示 `side_effects_released == true`

2) `first_live_launch_dry_run_not_ready`
- 当前发车前条件不足
- 不允许进入真实试运行

3) `first_live_launch_dry_run_blocked`
- 当前存在硬阻断 / 身份问题 / 一致性问题
- 明确不允许进入真实试运行

---

## F. 明确禁止（必须写死）

launch dry-run 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## G. 与现有链路的关系（写清）

与 approval gate：
- approval gate 决定“是否批准进入第一次真实放权试运行线”
- launch dry-run 决定“批准后，是否具备最后发车条件”
- `approved != launch_ready`

与 live release gate / side-effect release gate：
- 它们负责资格与放权资格
- launch dry-run 负责发车前最后一次总检查
- 不能混用

与 runtime contract / live execution definition：
- runtime contract 约束进入真实执行后的顺序与禁止面
- live execution definition 约束第一版真实执行边界
- launch dry-run 只负责进入真实执行前的最后检查

---

## H. 当前仍然不能做什么（必须写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许语音/记忆/中台迁移
- 不允许把 `first_live_launch_dry_run_ready` 当动作已开始

---

## I. 当前不做（必须写死）

- 不做真实 live implementation
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - first live launch dry-run 的 minimal implementation（如果本轮未落）
  - 或进入 first live guarded implementation 设计
- 当前不直接跳到真实 live implementation

补充链接：
- Phase-Next-84：first live guarded implementation definition v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`

