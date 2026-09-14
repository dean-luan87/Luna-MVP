# LUNA — YOLO Default Offline Perception Source Go/No-Go Pack v0 (Phase-ModelPerception-012)

## Decision
### Result
**GO（offline-only）**

允许：后续 Option A / phone_local 的 **offline evaluation** 默认选择 YOLO shadow perception 作为 perception candidate source。  
不允许：任何 runtime / controlled_live_stream / full trial / 动作 / 真实播报 / 真实 TTS。

## Policy set (this phase)
1. `docs/architecture/LUNA_YOLO_DEFAULT_OFFLINE_PERCEPTION_SOURCE_POLICY_V0.md`
2. `docs/architecture/LUNA_YOLO_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md`
3. `docs/architecture/LUNA_YOLO_OFFLINE_SOURCE_POLICY_AUDIT_REQUIREMENTS_V0.md`

## Why GO
- 011 review 已明确：baseline replacement 仅限 offline evaluation，且必须保留 disable/fallback/rollback。
- 本阶段将范围、回退与审计要求写成不可误解的 policy：
  - **default offline source ≠ runtime default source**
  - fallback 条件覆盖 disable/依赖失败/模型失败/schema 失败/越界/泄漏/工件缺失
  - audit 字段要求保证可复现与可追责
  - pending_real_sidewalk_run 明确禁止关闭

## Hard boundaries (must remain)
- 不新增 runtime
- 不扩 Option A
- 不进入 controlled_live_stream / full controlled trial
- 不执行导航动作、不真实播报、不触发真实 TTS
- 不开启默认路径（runtime）
- 不扩大真实 side effects 面
- 不关闭 pending_real_sidewalk_run

## Hard blockers
- `[]`

## Soft follow-ups
- torch.hub 可复现性风险：需要 pinned local weights + pinned deps（建议进入 Phase-ModelPerception-013）。
- SceneContext runtime gates 后置：仍需后续治理接线，但不得被绕过。

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-013：Pinned YOLO Weights & Dependency Reproducibility Definition v0**

