# LUNA — Offline Mainline Boundary & No-Expansion Policy v0 (Phase-EngineeringFlow-001)

## 目的
在 offline engineering mainline 闭合之前，冻结边界与“禁止扩展”政策，避免工程主线偏航到模块增强与能力扩展。

## 适用范围（本政策覆盖）
- 仅覆盖：Option A / phone_local / offline evaluation 的工程主链集成（EngineeringFlow-001~Closure）
- 不覆盖：controlled_live_stream、真实 runtime、full trial、用户测试

## 红线边界（必须持续成立）
- `side_effects_released` 默认 **false**
- candidate-only：全链路输出仅候选态，不进入执行面
- no-real-TTS：不得触发真实播报
- `pending_real_sidewalk_run` 必须保持 **true**（不得关闭/不得绕过）
- fail-closed fallback baseline/mock 必须保留
- disable_yolo 必须保留
- 不改变 evidence boundary / evidence_type 的治理含义

## 闭合前禁止做的事（No-Expansion）
在 EngineeringFlow-Closure 完成前，明确禁止：
- 新增/宣称新的模型能力（tracking / depth / OCR / dynamic / collision 等）
- 进入 controlled_live_stream
- 进入真实 runtime
- 进入 full controlled trial 或开放真实用户测试
- 开启任何 default-on 路径或扩大 side effects 面
- 执行导航动作（execute）
- 真实播报（real TTS emit）
- 移除/弱化 fallback、disable_yolo、pending 约束、candidate-only 约束

## 允许的工程变更类型（只为闭合服务）
允许且推荐（在后续 EF-002~006 中落实）：
- 把“策略/定义”接入为“统一默认入口”（source policy → PerceptionEval）
- 把“definition-only”落成“最小 gate”（SceneContext runtime gates，但仅 offline runner）
- 把“分阶段工具链”收敛到“统一 runner”
- 把“多日志/多 artifact”收敛到“统一观测入口与总报告”
- 把链路纳入“全链路回归测试与验收”

