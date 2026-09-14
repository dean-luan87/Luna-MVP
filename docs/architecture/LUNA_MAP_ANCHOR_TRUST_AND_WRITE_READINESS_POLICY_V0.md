# LUNA — MapAnchor Trust & Write Readiness Policy v0

## Phase

- **Phase-WorldModel-MapAnchor-001**

## Purpose

定义 MapAnchor 的 trust、空间锚点等级（grade）与对 WriteReadiness 的影响方式（只定义，不写世界模型）。

## SpatialAnchorGrade（v0）

- `grade_A_precise_bound`：GPS/地图/视觉一致，高可信
- `grade_B_probable_bound`：基本可信，但缺一个验证源
- `grade_C_weak_bound`：仅 GPS 或仅地图，精度一般
- `grade_D_unresolved`：缺空间锚点或冲突未解
- `grade_E_contradicted`：地图/GPS/视觉/用户反馈冲突

## WriteReadiness impact（v0）

MapAnchor 只影响 `observed_where` 的锚点强度与 `spatiotemporal_binding` 的 spatial confidence：

- A/B：可进入 `scene_local` / `persistent candidate` 的评估路径（仍需 trust/lifecycle/source chain）
- C：只能 `provisional`，且 `requires_revalidation=true`
- D/E：`no_write` 或 `audit_only`

## Cross validation status（v0）

- `visual_confirmed`：视觉地标对齐地图锚点
- `user_confirmed`：用户纠正或确认（必须记录上下文与来源，不直接覆盖事实）
- `contradicted`：冲突未解（进入 hold/weak bind）

## Hard rules

- MapAnchor 不得单独确认“现场存在/营业/促销有效”
- 任何进入世界模型事实层的内容仍需满足 World Model Spatiotemporal Binding Constitution（observed_at + observed_where + scope）

