# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation First Minimal Real Write Code v0（第一版真实最小写入代码：实现方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_FIRST_MINIMAL_REAL_WRITE_CODE_V0.md`  
**性质**：Phase-Next-128：在所有冻结边界闭合后，进入“第一版真实但极小的写入代码”之前的实现方案文档（本轮先冻结方案；除非边界足够稳定，否则不落真实写入代码）

基于（已具备）：
- live implementation definition / skeleton / stub（冻结 + 在位）
- live implementation minimal code skeleton（在位）
- live runtime activation stub / live runtime implementation stub（在位）
- live implementation admission & acceptance（冻结）
- live implementation minimal implementation plan（冻结）
- live implementation non-effect wiring（在位）
- live implementation dry-run execution（在位）
- live code path dry-run（在位）
- first real write rollout plan（冻结）
- real-write go/no-go gate（冻结）
- first real code activation definition（冻结）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## 1. 为什么现在可以进入第一版真实最小写入代码（写死理由）

- definition / skeleton / stub / minimal code skeleton / runtime activation stub / runtime implementation stub 已在位。
- non-effect wiring / dry-run execution / code path dry-run 已证明“路径可走通且零副作用演练成立”。
- rollout plan / go-no-go gate / first real code activation definition 已冻结。
- 因此已经具备进入第一版真实最小写入代码的前置条件，但仍必须坚持：
  - 默认不开
  - 显式批准/信号
  - 失败优先收口
  - 只允许三类真实副作用

---

## 2. 最小代码落点判断（写死结论 + 理由）

### 2.1 候选落点（默认）

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0.py`

### 2.2 为什么放这里最小、最连续、最不容易失控（写死）

- 与现有 `governance/runtime` 家族同域，边界最清晰，易审计。
- 物理隔离真实代码体与 placeholder 层（skeleton/stub/code skeleton），避免混层与误接线。
- 不改主线行为：默认不接入 dispatcher；只有显式调用才可能触发（且仍需显式信号与 gate 前提）。

### 2.3 为什么不能直接改现有 skeleton / stub 文件（写死）

- skeleton/stub 必须永远保持“非动作、不可真实写入、不可打开 side_effects_released”的可回归性与可信度。
- 把真实逻辑塞进去会破坏占位层的冻结边界，增加失控风险。

---

## 3. 最小允许真实副作用面（写死）

第一版真实最小写入代码 **只允许** 三类真实副作用：

- `execution_state_real_write`
- `result_object_real_write`
- `exception_or_failure_real_write`

除此以外全部禁止（写死）：

- route
- voice
- memory
- migration
- rollback
- interrupt
- map/path side-effect source
- 越过标准对象吐散字段

---

## 4. 最小真实执行前提（写死）

只有在以下全部满足时，才允许进入第一版真实最小写入代码（写死；少任一项不得进入）：

- real-write go/no-go gate == `first_live_minimal_real_effect_real_write_go`
- live code path dry-run == `first_live_minimal_real_effect_live_code_path_dry_run_executed`
- `side_effects_released == false`
- **显式 real-write approval / signal 在位**
- execution_state / result / exception_or_failure path 在位
- 默认开关仍为 false（默认不开）
- 单环境、单版本、单链路

---

## 5. 最小真实执行顺序（写死）

### 正常路径（固定顺序）

1) 确认 `side_effects_released == false`  
2) 进入受控短时真实激活  
3) 真实写 `execution_state`  
4) 真实写 `result_object`  
5) 恢复或确认 `side_effects_released == false`  
6) 交还治理链  

### 异常路径（固定顺序）

1) 立即恢复 `side_effects_released == false`  
2) 写失败/退出态 `execution_state`  
3) 写失败 `result_object`  
4) 写 `exception_or_failure`  
5) 交还治理链  

---

## 6. 最小测试矩阵（写死最少覆盖）

至少覆盖：

- 正常路径通过
- approval/signal 缺失
- `side_effects_released != false`
- state 写入失败
- result 写入失败
- exception/failure 写入失败
- 任一步骤后是否恢复 false
- V1 最小闭环回归

---

## 7. 最小止损与回退（写死）

任一异常必须按固定优先级收口：

1) 先恢复 `side_effects_released == false`
2) 再写失败 state
3) 再写失败 result
4) 再写 exception/failure
5) 再交还治理链

并写死：

- 禁止扩权补救
- 禁止保留半开启状态

---

## 8. 明确禁止（写死）

- route / voice / memory / migration
- rollback / interrupt
- map/path side-effect source
- 越过标准对象吐散字段
- 默认开启 rollout
- 默认开启 `side_effects_released`

---

## 9. 下一步边界（写死）

- 本轮之后，才考虑是否同轮落第一版真实最小写入代码文件：
  - `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0.py`
- 若落代码：只允许最小实现，不允许扩面；失败路径优先级高于成功路径；且不得接入任何默认路径。

