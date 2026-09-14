# LUNA — YOLO Offline Perception Source Closure Review v0 (Phase-ModelPerception-Closure-001)

## 本阶段范围（只做收口）
本阶段仅做 **ModelPerception-001 到 015** 的统一收口 review，把 YOLO 在 Luna 体系中的“正式状态/边界/禁止项/后续路线”冻结成文档与索引。

**硬边界：**
- 不新增 runtime，不开启任何默认路径
- 不修改 YOLO adapter（含 shadow adapter）安全边界
- 不重跑完整下游链路（SceneTask/Fusion/Output），不进入 controlled_live_stream / full trial / 用户测试
- 不执行导航动作，不真实播报

## 已成立事实（阶段结论快照）
已完成阶段与结论（以本 repo 文档与工具为准）：
- ModelPerception-001：GO
- 002A：GO
- 002B：历史 CONDITIONAL_GO（后续通过修复与下游证据闭环）
- 003：历史 CONDITIONAL_GO（后续通过 baseline restore 证据闭环）
- Fix-001：GO
- 004：历史 CONDITIONAL_GO（后续通过依赖修复闭环）
- Fix-002：GO
- 005：GO
- 006：GO
- 007：GO
- 008：GO
- 009：GO
- 010：GO
- 011：GO
- 012：GO
- 013：GO
- 014：CONDITIONAL_GO
- 015：GO

## YOLO 当前“正式状态”（冻结口径）
**yolo_status（正式）**：`default_offline_perception_candidate_source`

**scope（严格）**：`OptionA_phone_local_offline_evaluation_only`

**含义：**
- YOLO 可以作为 **Option A / phone_local / offline evaluation** 的默认 perception **candidate source**
- YOLO 已完成 pinned_local 权重固化（manifest+sha256+size+readiness）
- YOLO 已通过 shadow E2E offline 验证（候选链路完整、无 TTS、无执行、无安全泄漏、证据边界成立）

**明确不含义：**
- 不代表 YOLO 已接入真实 runtime
- 不代表 YOLO 已进入 controlled_live_stream 或 full trial
- 不代表具备真实导航执行正确性或用户可靠性证明

## baseline/mock 替代结论（冻结）
- **可以替代的范围**：仅限 **offline evaluation** 的 perception candidate 输入源（并保留 fail-closed fallback）
- **不得替代的范围**：真实 runtime / controlled_live_stream / full trial / 用户测试等
- **fallback 必须保留**：baseline/mock 作为最终回退路径，不得移除

## pinned_local 权重与可复现性状态（冻结）
当前 pinned_local（来自 manifest）：
- weights_source: pinned_local
- weights_path: `models/yolo/yolov5n.pt`
- weights_sha256: `4f180cf23ba0717ada0badd6c685026d73d48f184d00fc159c2641284b2ac0a3`
- verification_status: pass

说明：
- 权重文件不入 git（`.gitignore` 已忽略 `*.pt`），只记录 metadata（path/hash/size）
- torch.hub 仍存在 AutoUpdate 不确定性证据，因此 torch_hub_dev 只能 dev/smoke 口径，不得作为长期默认

## 关键禁止项（收口必须写死）
YOLO 当前 **不得**：
- 成为真实 runtime 默认感知源
- 进入 controlled_live_stream
- 进入 full controlled trial
- 执行导航动作（execute）
- 触发真实 TTS
- 开启任何 default-on 路径
- 扩大真实 side effects 面
- 关闭 `pending_real_sidewalk_run`（必须保持 true）
- 绕过 SceneContext gates / governance
- 声称 OCR / depth / dynamic event / collision risk / stable tracking 等能力已经成立
- 声称真实导航能力已验证

## 风险与后续分支（只列路线，不授权执行）
必须持续保留并在后续独立阶段处理：
- dependency isolation / AutoUpdate hardening
- SceneContext runtime gate implementation（定义已完成，但 runtime enforce 仍需独立阶段）
- sample expansion（当前 phone_local 样本规模有限）
- controlled_live preparation（phone_local ≠ controlled_live）
- model version upgrade admission policy（新 model_config_id + 新 sha256 + 并行 shadow 对比，禁止原地覆盖）
- runtime integration readiness（若考虑 runtime，必须另开阶段；不得由 offline default 直接继承）

## Closure 结论（本阶段）
**closure_recommendation：GO（仅限 offline evaluation source closure）**

原因：
- 001–015 证据链完整
- pinned_local_ready 已达成
- offline E2E shadow 验证为 GO
- 禁止项可冻结、后续分支可明确

