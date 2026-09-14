# LUNA — Scene Delta Boundary Register v0

## Phase

- **Phase-MidPlatform-SceneDelta-003**

## Purpose

登记并冻结 Scene Delta 的禁止项与硬边界，用于 `closed_v0` 收口。

## Hard boundaries（冻结）

- 不接真实 runtime
- 不接真实中台
- 不进入 SceneTask/Fusion/Output
- 不写真实世界模型
- 不上传蜂巢
- 不执行导航动作（`navigation_action=null`）
- 不真实播报（`real_tts_invoked=false`）
- 不接推荐系统

## Auditability invariants（冻结）

- trace/replay/whitebox 必须非空且可追责
- 不允许压缩后丢失审计链（必须保留 canonical、first/last、duplicate_count、样本帧策略或 cold storage ref）
- 所有“阻断/暂存/复用/重处理”决策必须可解释（whitebox）

