# LUNA — Physics Consistency Policy v0 (Phase-SceneContext-003)

## Purpose
Define hard rules to prevent unstable/implausible perception outputs from driving downstream decisions.

This layer:
- checks **consistency / plausibility**
- outputs **candidates and downgrade recommendations**
- never outputs executable actions

Definition-only; no runtime.

## Non-negotiable boundaries (repeat as hard constraints)
- Candidate-only; `allows_execute_now=false`.
- Must not trigger `execute/release/retry/reopen`.
- Must not output real navigation actions.
- Must not decide macro_scene; must not override SceneContext-001/002.
- Under low confidence or physics conflict: must degrade (cannot force certainty).

## Core rules (must be written as hard constraints)

### Rule 1 — 连续帧目标位置不得无理由跳变
If the same target (by track id or best-effort association) shows implausible displacement over short time:
- set `conflict_detected=true`
- `conflict_type=object_position_jump`
- `recommended_handling=downgrade_confidence` or `ignore_as_unstable`
- must not generate any forced avoidance / turn / stop as an executable action

### Rule 2 — 距离/深度不得无理由剧烈跳变
If the same obstacle/boundary distance estimate oscillates sharply (e.g., 2m → 10m → 1m) without consistent parallax support:
- `conflict_type=depth_jump`
- `physical_plausibility=uncertain` (or `implausible` if extreme)
- `recommended_handling=mark_uncertain` or `degraded_mode`
- must not use it as definitive “passable” or definitive “blocked”

### Rule 3 — 运动趋势必须物理合理
If dynamic target motion implies impossible speed/acceleration/direction flip within short time:
- `conflict_type=impossible_motion`
- `motion_plausibility_score` must be low
- must not generate strong avoidance as a certainty
- allowed outputs are only **non-executing candidates** (downstream):
  - `slow_down_candidate`
  - `observe_candidate`
  - `ask_for_help_candidate`

### Rule 4 — 通行空间必须满足几何连续性
Passability cannot be concluded from “no obstacle detected” alone; must consider:
- path width
- ground continuity
- step/height discontinuities
- left/right boundaries
- near-field obstacles
- low-confidence regions

If geometry evidence insufficient:
- `conflict_type=passability_geometry_conflict` (or `unknown` with low score)
- `passability_geometry_score` must be reduced
- `recommended_handling=mark_uncertain` (or `narrow` candidate downstream)
- must not force `passable=true` as a certainty

### Rule 5 — 碰撞风险必须结合相对距离与相对运动
Risk cannot be triggered by class-only, and cannot be ignored by class-only.
Must incorporate (as candidates, not claims):
- relative_distance
- relative_velocity
- approach_direction
- time_to_contact candidate
- confidence

If class low-risk but relative motion suggests high collision likelihood:
- `conflict_type=collision_risk_conflict`
- elevate collision-risk candidate level (still non-executing)
- recommended handling must remain candidate-only (slow/observe/ask)

### Rule 6 — 平面媒介与真实空间要用深度/视差校验
If strong corridor-like content exists but depth/parallax indicates flat surface:
- `conflict_type=flat_surface_depth_conflict` and/or `parallax_conflict`
- must route conservatively:
  - `recommended_handling=degraded_mode` or `ignore_as_unstable`
- must not be treated as real path confirmation
- must not override SceneContext-002 (depicted scene filter); instead reinforce it

### Rule 7 — 物理冲突时降级优先
If any key physics conflict is present:
- cannot output a “certain” decision
- must choose one of:
  - `downgrade_confidence`
  - `mark_uncertain`
  - `degraded_mode`
  - `ask_for_help_candidate`
- must include non-empty `reason_codes` for whitebox audit

## Scoring / thresholds (definition-only)
This doc intentionally does NOT freeze numeric thresholds; it freezes:
- what must be checked
- what conflicts mean
- what handling is allowed

Threshold tuning is deferred to implementation planning, but must preserve rules above.

