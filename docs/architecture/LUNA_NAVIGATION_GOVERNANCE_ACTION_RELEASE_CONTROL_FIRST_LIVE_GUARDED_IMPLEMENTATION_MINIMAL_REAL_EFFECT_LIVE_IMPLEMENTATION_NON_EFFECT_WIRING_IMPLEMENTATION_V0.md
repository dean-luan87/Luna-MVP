# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Non-Effect Wiring Implementation v0（最小非动作实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_NON_EFFECT_WIRING_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-119：`live implementation non-effect wiring v0` 的最小非动作实现说明（只接线、不执行；`side_effects_released=false`）

代码落点（最小实现）：
- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0.py`

自测：
- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0.py`

（如需在主线 metadata 中可见）relevant-only 接线：
- `capabilities/voice/runtime/voice_final_text_dispatcher.py`

---

## 1. 输出对象（写死）

写入到 `result.metadata` 的 key：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0`

对象最小形态（示例字段；实现以字典为准）：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0",
  "wiring_status": "first_live_minimal_real_effect_live_wired_ready|first_live_minimal_real_effect_live_wired_not_ready|first_live_minimal_real_effect_live_wired_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## 2. relevant-only 策略（写死）

- 如果上游核心对象均不存在（均非 dict），则返回 `(applicable=False, payload=None)`，不写 metadata。
- 否则必须返回 `(True, payload)`，payload 必须是 attempted 的三态 wiring 对象。

---

## 3. 判定规则（写死；与冻结文档一致）

### 3.1 hard block（blocked）

任一成立则 `wiring_status=first_live_minimal_real_effect_live_wired_blocked`：

- `side_effects_released is True` 或者为不安全值（非 `None|False`）
- live implementation skeleton identity 缺失或不保守
- live implementation stub identity 缺失或不保守

### 3.2 not_ready

缺任一 required upstream object 或任一状态不满足，输出 `wired_not_ready`。

### 3.3 wired_ready

当且仅当全部 required upstream object 在位，且状态满足：

- admission gate == admitted
- guarded launch gate == admitted
- pre-commit dry-run == ready
- commit gate == admitted
- commit dry-run == ready
- activation gate == admitted
- activation dry-run == ready
- execution_state_v0 / result_v0 在位
- `side_effects_released==false`

并且 skeleton/stub identity 均保守且 scope 匹配。

---

## 4. 禁止项（写死）

实现中写死：

- 不打开 `side_effects_released`
- 不执行任何真实写入
- 不执行真实 release_control / rollback / interrupt
- 不做 route / voice / memory / migration

