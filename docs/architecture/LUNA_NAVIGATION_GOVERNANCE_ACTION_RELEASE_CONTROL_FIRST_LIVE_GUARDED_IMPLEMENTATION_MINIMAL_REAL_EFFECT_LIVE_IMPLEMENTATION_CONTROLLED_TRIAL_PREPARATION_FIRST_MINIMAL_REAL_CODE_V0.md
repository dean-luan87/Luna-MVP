# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Code v0（准备态第一版最小真实启用代码）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_CODE_V0.md`  
**性质**：Phase-Next-144：在 preparation admission / implementation / dry-run 都闭合后，第一次落“真实但极小”的 preparation 启用代码（显式调用；默认不开；严格三类写入）

---

## 1) 为什么现在可以进入第一版真实 minimal preparation code（写死）

当前已经具备：

- controlled trial preparation admission gate / implementation / dry-run 已在位且可演练
- controlled trial enablement 链已在位（go/no-go、dry-run、real enablement ready）
- 因此具备进入第一版真实最小 preparation 启用代码的前置条件

本轮仍写死：

- 不接入默认路径
- 不扩面到任何额外副作用面

---

## 2) 最小代码落点判断（写死）

真实代码建议落点：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_real_v0.py`

理由（写死）：

- 与 `...controlled_trial_real_enablement_v0.py` 同层级、同“显式调用真实最小写入”风格，最连续、最不易失控
- 不直接改 `...controlled_trial_preparation_v0.py`（它是 placeholder 承接位，必须保持非动作）
- 不直接改 `...controlled_trial_preparation_dry_run_v0.py`（它是零副作用演练层，必须保持非动作）

---

## 3) 最小允许真实副作用面（写死）

只允许三类真实副作用（通过注入 writer 实现）：

- `execution_state_real_write`
- `result_object_real_write`
- `exception_or_failure_real_write`

其余全部禁止（写死）：

- route / voice / memory / migration
- rollback / interrupt
- map/path side-effect source
- 越过标准对象吐散字段
- 默认开启 preparation
- 默认开启 trial
- 默认开启 side_effects_released

---

## 4) 最小真实执行前提（写死）

当且仅当以下条件满足，才允许进入真实最小执行入口（否则 blocked/not_ready）：

- `controlled_trial_preparation_status == first_live_minimal_real_effect_controlled_trial_preparation_admitted`
- `controlled_trial_preparation_dry_run == first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed`
- `controlled_trial_go_no_go == first_live_minimal_real_effect_controlled_trial_go`
- `controlled_trial_first_minimal_real_enablement == first_live_minimal_real_effect_controlled_trial_real_enablement_ready`
- `side_effects_released == false`（进入前必须是 false）
- **显式 preparation real-code approval/signal 在位**
- `execution_state_v0 / result_v0 / exception_or_failure_path_v0` 在位
- 默认开关仍为 false；单环境、单版本、单链路；显式调用入口

---

## 5) 最小真实执行顺序（写死）

### 正常路径（写死）

- 确认 `side_effects_released == false`
- 进入“受控短时 preparation 启用语义”（局部语义，不影响默认路径）
- 写 `execution_state_real_write`
- 写 `result_object_real_write`
- 恢复/确认 `side_effects_released == false`
- 交还治理链

### 异常路径（写死；失败优先）

- 任何异常：**立即恢复/确认 `side_effects_released == false`**
- 写失败 `execution_state_real_write`
- 写失败 `result_object_real_write`
- 写 `exception_or_failure_real_write`
- 交还治理链

---

## 6) 最小测试矩阵（写死）

- 正常路径通过（writer 全成功；顺序正确；最终恢复 false）
- approval/signal 缺失（不得进入真实执行）
- `side_effects_released != false`（blocked）
- state 写入失败（进入异常路径；优先恢复 false；再收口写入）
- result 写入失败（进入异常路径；优先恢复 false；再收口写入）
- exception/failure 写入失败（仍必须保证恢复 false，不扩权补救）
- 任一步骤后是否恢复 false（强制断言）
- v1 最小闭环回归（不污染默认路径）

---

## 7) 最小止损与回退（写死）

- 任一异常先恢复 `side_effects_released == false`
- 再写失败 state
- 再写失败 result
- 再写 exception/failure
- 再交还治理链
- 禁止扩权补救（不引入新增副作用面、不拓展写入种类）

---

## 8) 明确禁止（写死）

- route / voice / memory / migration
- rollback / interrupt
- map/path side-effect source
- 越过标准对象吐散字段
- 默认开启 preparation / trial / side_effects_released

