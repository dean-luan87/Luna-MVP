# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial First Minimal Real Enablement Code v0（第一版真实最小试运行启用代码：实现方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_FIRST_MINIMAL_REAL_ENABLEMENT_CODE_V0.md`  
**性质**：Phase-Next-138（step1）：冻结第一版“真实但极小”的 controlled trial 启用代码实现方案（先冻结方案，再落最小代码）

---

## 1) 为什么现在可以进入第一版真实 minimal trial enablement code（写死）

前置已齐备：

- controlled trial admission/go-no-go gates 在位
- controlled trial minimal enablement plan 已冻结
- controlled trial minimal enablement implementation 已在位（承接位）
- controlled trial enablement dry-run 已跑通（runtime 顺序可零副作用演练）
- controlled trial first minimal real enablement definition 已冻结（“trial 真正开始”的边界明确）
- 真实最小写入代码已存在（仅三类写入；显式入口；不接默认路径）

因此具备进入第一版真实最小 trial 启用代码的前置条件。

---

## 2) 最小代码落点判断（写死）

### 2.1 真实代码文件路径（写死）

**新增**：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_real_enablement_v0.py`

### 2.2 为什么放这里最小、最连续、最不容易失控（写死）

- 与 `controlled_trial_enablement_v0.py`、`enablement_dry_run_v0.py` 同域（`governance/runtime`），便于保持“trial 启用承接链”在同一边界内闭合。
- 不修改既有 enablement placeholder 与 dry-run：保持“占位层/演练层”不被真实副作用污染。
- 物理隔离：真实启用代码单独文件、显式调用入口，避免意外进入默认路径。

---

## 3) 最小允许真实副作用面（写死）

只允许三类真实副作用（通过注入 writer 实现）：

- `execution_state_real_write`
- `result_object_real_write`
- `exception_or_failure_real_write`

除此以外全部禁止：

- route / voice / memory / migration
- rollback / interrupt
- map/path side-effect source
- 越过标准对象吐散字段
- 默认开启 trial
- 默认开启 `side_effects_released`

---

## 4) 最小真实执行前提（写死）

真实 trial 启用代码必须同时满足：

- `controlled_trial_go_no_go == first_live_minimal_real_effect_controlled_trial_go`
- `controlled_trial_enablement_dry_run == first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed`
- `controlled_trial_first_minimal_real_enablement == ..._ready`（来自 Phase-Next-137 definition 的 ready 边界）
- `side_effects_released == false`
- 显式 `real-enable approval/signal` 在位
- `execution_state_v0` / `result_v0` / `exception_or_failure_path_v0` 在位
- 默认开关仍为 false；单环境、单版本、单链路

并写死：

- 无显式 signal 不得进入真实启用
- `side_effects_released != false` 直接 blocked

---

## 5) 最小真实执行顺序（写死）

### 正常路径（写死）

1) 确认 `side_effects_released == false`（预检）
2) 进入“受控短时真实启用”语义（局部语义，不得泄漏成默认路径）
3) 写 `execution_state`
4) 写 `result_object`
5) 恢复/确认 `side_effects_released == false`
6) 交还治理链

### 异常路径（写死）

1) 立即恢复/确认 `side_effects_released == false`（优先级最高）
2) 写失败 `execution_state`
3) 写失败 `result_object`
4) 写 `exception_or_failure`
5) 交还治理链

---

## 6) 最小测试矩阵（写死）

至少覆盖：

- 正常路径通过（仅三类 writer 被调用）
- approval/signal 缺失 → not_ready
- `side_effects_released != false` → blocked
- state 写入失败 → 走失败收口顺序
- result 写入失败 → 走失败收口顺序
- exception/failure 写入失败 → 仍优先保证恢复 false
- 任一步骤后是否恢复 false（成功/失败都必须）
- V1 最小闭环回归（主链输出不受影响）

---

## 7) 最小止损与回退（写死）

任一异常的固定止损/回退顺序（写死）：

1) 先恢复 `side_effects_released == false`
2) 再写失败 state
3) 再写失败 result
4) 再写 exception/failure
5) 再交还治理链

禁止：

- 失败后扩权补救
- 保留半开启状态

---

## 8) 明确禁止（写死）

- route / voice / memory / migration
- rollback / interrupt
- map/path side-effect source
- 越过标准对象吐散字段
- 默认开启 trial
- 默认开启 `side_effects_released`

---

## 9) 下一步边界（写死）

- step2：只有当上述边界足够稳，才允许同轮落最小真实代码文件与 verify。
- 当前不接入任何默认路径。

