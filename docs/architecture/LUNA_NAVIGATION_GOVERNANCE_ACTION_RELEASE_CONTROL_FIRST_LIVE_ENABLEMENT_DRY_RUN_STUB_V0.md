# Luna — Navigation Governance Action Release Control First Live Enablement Dry-Run Stub v0（第一次放权试运行：干跑 stub）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_DRY_RUN_STUB_V0.md`  
**性质**：Phase-Next-80：把 `first live enablement plan` 推进为“可演练、可观测、不可放权”的 dry-run stub（落代码；不触发真实动作）

关联：
- enablement plan（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_PLAN_V0.md`
- side-effect release contract / gate（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`
- live release gate（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`
- guarded live stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- minimal runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control first live enablement` 的 dry-run stub 设计与落地文档。
- 当前目标：把 enablement plan 推进到 dry-run stub（只演练，不放权）。
- 当前不把 `side_effects_released` 从 `false` 改成 `true`。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 dry-run stub

- enablement plan 已冻结，但还缺少代码里的“试运行演练层”。
- 若直接从 plan 跳到真实 live implementation，会缺少对以下关键点的可回归验证：
  - 显式批准信号如何进入系统
  - enablement 前提如何被代码识别
  - 回退顺序能否在不放权情况下先演练一遍
  - `side_effects_released=false` 能否在全流程保持锁死
- 因此必须先有一个“可演练但不放权”的代码承载位。

---

## C. dry-run stub 的最小定义（写死）

- 它不是 first live enablement 真正启用器。
- 它不是 side-effect release gate。
- 它只是“试运行启用流程”的代码演练层。
- 只负责演练条件检查、灰度检查、回退顺序，不负责真实放权。

---

## D. dry-run stub 最小能力面（写死 5 个）

1) **stub 身份**  
- 固定 identity / scope

2) **enablement 输入接口占位**  
- 未来只接受 enablement plan 所需前提  
- 当前不真实消费

3) **启用前提检查接口占位**  
- 未来检查 live gate / side-effect gate / candidate / state/result / approval  
- 当前只返回 dry-run 结果对象

4) **回退路径演练接口占位**  
- 未来演练 restore `side_effects_released=false` 等顺序  
- 当前不真的修改状态

5) **异常/阻断接口占位**  
- 未来在前提不满足时收口  
- 当前只返回 placeholder-safe / blocked-safe

---

## E. 默认行为（写死）

- 默认可进入 dry-run 候选
- 默认不打开 `side_effects_released`
- 默认不触发真实 `release_control`
- 默认不触发 route / voice / memory / migration
- 默认只返回 `dry_run_ready|dry_run_not_ready|dry_run_blocked|not_implemented`

---

## F. 与现有链路的关系（写清）

与 enablement plan：
- plan 是规则文档  
- dry-run stub 是代码承载位  
- 两者不能混用

与 side-effect release gate：
- side-effect release gate 判断未来是否具备副作用放权资格  
- dry-run stub 演练第一次启用流程  
- 当前不真正放权

与 guarded live stub：
- guarded live stub 负责 live candidate  
- dry-run stub 负责试运行启用流程演练  
- 两者职责不同

---

## G. 当前不允许做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许触发语音播报
- 不允许写记忆
- 不允许触发中台真实迁移
- 不允许绕过 enablement plan / release contract

---

## H. 代码落点（本轮落地）

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_enablement_dry_run_stub_v0.py`

