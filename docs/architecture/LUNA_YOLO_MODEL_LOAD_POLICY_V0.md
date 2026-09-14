# LUNA — YOLO Model Load Policy v0 (Phase-ModelPerception-013)

## 目标
把 YOLO 的“加载路径”从 torch.hub 的可变行为，升级为可审计、可校验、可回退的策略：
- **Preferred**：pinned local weights（长期默认）
- **Dev fallback**：torch.hub dev/smoke（短期临时；明确标风险）
- **Final fallback**：baseline/mock（任何失败/不匹配/越界 => 必须回退）

## Hard boundaries
- torch.hub **不得**作为长期默认生产式加载路径（offline default source 的目标必须是 pinned_local）。
- 任何加载失败/校验失败/依赖失败 => 必须 fallback baseline/mock（保留 disable/fallback/rollback）。
- 不新增 runtime，不改变执行权限，不改变 candidate-only。

## Load priority
### 1) Preferred path — pinned local weights (长期默认)
条件（必须全部满足）：
- manifest exists 且 `weights_source == "pinned_local"`
- `weights_path` 文件存在
- `weights_sha256` 匹配
- 依赖 importable 且版本已记录
- model load dry-run 成功
- one-frame inference smoke 成功
- output schema sanity pass
- forbidden output scan pass

记录要求（审计）：
- model_config_id（稳定）
- weights_source=pinned_local
- weights_path / sha256 / size
- dependency_profile_id + 关键依赖版本
- verification_status=pass/fail/partial

### 2) Dev fallback path — torch.hub dev (仅开发/临时 smoke)
允许条件（必须全部满足）：
- manifest exists 且 `weights_source == "torch_hub_dev"`
- 明确标记 `reproducibility_risk=true`
- 仅用于开发/临时 smoke（不得作为长期默认）

必须记录（审计）：
- hub repo/ref（若可获得）
- hub cache 行为（best-effort）
- dependency_status
- reproducibility_risk=true

### 3) Final fallback — baseline/mock
触发条件（任一满足即触发）：
- pinned weights 不存在 / sha256 不匹配 / 文件损坏
- dependency readiness fail（缺模块/版本不符/不可 import）
- model load fail / inference fail
- schema validation fail / forbidden scan fail
- replay/whitebox/trace 不可写或缺失
- evidence boundary violation
- safety leakage detected
- disable_yolo=true

回退后必须记录：
- source_selected=baseline_mock
- fallback_used=true
- fallback_reason（枚举/字符串原因）

## 禁止项（明确）
- 不允许把 torch.hub dev 作为长期默认路径
- 不允许在 pinning 策略下移除 baseline/mock rollback
- 不允许用 pinning “绕过” candidate-only 或其它治理边界

