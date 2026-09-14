# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Trial Implementation v0（155→156 映射说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-156：说明 156 short-window trial runtime 如何逐条映射 155 guardrail（不 default-on、不 full trial、不扩面）

---

## 1) 本阶段真正新增的 runtime 行为（写清）

- 新增 short-window trial 显式入口：`run_first_live_controlled_short_window_trial_v0(...)`
- 新增 “pack 必须 go/conditional_go” 的显式 gate（来自 154）
- 新增 “显式 intent + 人工确认/等价批准” gate（entry guardrail）
- 新增 window 上限强制检查（trial_window_max_ms + observed_elapsed_ms），超时直接 abort
- 新增 unauthorized_surface 的 intent-level 检查（requested_surfaces 必须在三类白名单内）
- 新增 audit trace 完整性检查（enablement trace/order 必须存在）
- 复用 152 enablement 作为唯一 start_event 产生者，并以其 closure 作为短窗收口依据

---

## 2) 156 如何映射 155（逐条对齐）

### Entry Guardrails

- 非默认：无显式 intent 或无 approval → 直接 aborted（不进入 started）
- pack 必须 go：154 pack 非 go/conditional_go → aborted

### Window Guardrails

- trial_window_max_ms 必须存在且为正；observed_elapsed_ms 必须可解析且非负
- `observed_elapsed_ms > trial_window_max_ms` → abort_trigger=`trial_window_timeout`

### Runtime Guardrails

- started 判据唯一：156 不自造 started，只通过调用 152 并读取其 `start_event_observed`
- release 仅 started 后发生且最终回落：156 对 “closure 后 se 仍为 true” 直接 abort（se_not_recovered）
- 副作用面不扩：intent requested_surfaces 若包含非白名单 → abort（unauthorized_side_effect_surface）

### Abort / Recovery / Closure Guardrails

- 156 的 abort 统一进入 closed=true 且 se=false 的安全闭合态（v0 最小策略）
- 成功/失败都依赖 152 的 closure；失败路径确保 closed=true 且 se=false

---

## 3) 明确仍未进入（写死）

- 未开启默认路径
- 未进入 full controlled trial
- 未扩大真实 side effects 面（仍仅三类写入）
- 本阶段不等于 full release

