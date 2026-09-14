# LUNA — Visual Medium Scene Grounding Policy v0 (Phase-SceneContext-002)

## Purpose
Define hard rules that prevent:
- depicted scene (inside photo/screen/poster/ad/book cover/reflection)
from being mistaken as:
- real world scene (macro_scene / zone reasoning / task/risk triggers)

Definition-only; no runtime.

## Core principles (write as hard constraints)
- **Real-world scene updates must be grounded** in spatial/temporal evidence.
- **Depicted scene is content**: recordable for audit, not actionable.
- **When in doubt, degrade**: keep `previous_macro_scene` or mark `uncertain_degraded`.

## Rule 1 — scene inside object不得成为real_world_scene
If medium detected (poster/photo/screen/book cover/ad board):
- content may only be tagged as `depicted_scene`
- must not directly modify `macro_scene`
- default:
  - `macro_scene_transition_allowed=false`
  - `task_trigger_allowed=false`
  - `risk_trigger_allowed=false`

## Rule 2 — 单帧强语义不得触发macro_scene跳变
Examples:
- coworking_space + beach poster
- metro_station + hospital ad

Expected action:
- `visual_medium_detected=true`
- `depicted_scene=<content>`
- `macro_scene_transition_allowed=false`
- `action=keep_previous_macro_scene` (or `mark_as_depicted_scene_only`)

## Rule 3 — 媒介内容不得触发任务/风险/导航动作
If `depicted_scene != none` under detected medium:
- must not create/upgrade any navigation task candidate
- must not create/upgrade any risk candidate
- must not be used as basis for “go to hospital/avoid water edge” etc.

Hard forbidden semantics:
- any downstream candidate that implies execute/release/retry/reopen based on depicted scene content.

## Rule 4 — 真实场景切换必须依赖空间证据 + SceneContext-001
Macro scene switching must rely on:
- large field-of-view scene consistency
- depth/parallax/spatial layout support
- sustained multi-frame evidence
- transition evidence
AND must be evaluated by **SceneContext-001 transition policy**.

This layer may only set:
- `scene_context_001_policy_required=true`
and provide grounding evidence scores/flags.

## Rule 5 — 平面媒介/屏幕/反射优先降级
If any of the following cues are present with medium likelihood high:
- frame boundary / bezel
- poster edge / wall-mounted plane
- screen UI/refresh patterns
- mirror/glass reflection cues
then:
- prefer `action=mark_as_depicted_scene_only` OR `uncertain_degraded`
- block macro scene transition unless strong grounding evidence exists.

## Rule 6 — 冲突时保持previous_macro_scene
If `previous_macro_scene` is stable (SceneContext-001 inertia) and current frame introduces a conflicting depicted scene:
- keep `previous_macro_scene`
- `conflict_detected=true`
- `conflict_type` set appropriately
- `action=keep_previous_macro_scene` or `uncertain_degraded`

## Reflection handling (v0)
### mirror_reflection
Default behavior:
- treat reflected space as **reflection_candidate**, not real transition evidence.
- do not allow macro_scene switch based on reflection alone.

### glass_reflection
Default behavior:
- treat outdoor street appearing in glass as `reflection_candidate`.
- block macro_scene switch to street unless spatial evidence supports a real doorway/exit transition.

## Degraded / uncertain policy (v0)
Trigger degraded if:
- medium likelihood high but type unknown, OR
- conflict between depicted content and spatial grounding, OR
- reflection likelihood high, OR
- sustained evidence insufficient.

Degraded output must include:
- `action=uncertain_degraded`
- `macro_scene_transition_allowed=false`
- `task_trigger_allowed=false`
- `risk_trigger_allowed=false`

## Claims boundary
This policy does NOT claim actual medium detection accuracy.
It only defines the **safety gating and interpretation constraints**.

