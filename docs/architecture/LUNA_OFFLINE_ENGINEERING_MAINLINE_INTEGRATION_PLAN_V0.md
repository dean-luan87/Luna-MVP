# LUNA — Offline Engineering Mainline Integration Plan v0 (Phase-EngineeringFlow-001)

## 本阶段定位
本阶段只做 **离线工程主链（offline engineering mainline）集成计划**，目标是把已验证通过的离线沙盒链路按“工程主链”方式串成可执行的后续集成路线与验收顺序。

### 已成立事实（输入前提）
- PhoneLocal FieldBatch / archive：已完成（phone_local offline）
- YOLO offline perception source closure：已完成
- YOLO 正式状态：`default_offline_perception_candidate_source`
- scope：`OptionA_phone_local_offline_evaluation_only`
- pinned_local_ready：true（weights/sha256/manifest/readiness 已成立）
- YOLO shadow E2E offline：GO（candidate-only/no-real-TTS/no-execute/evidence boundary）
- 当前形态：分阶段工具链 + 多份桥接评测产物，不是统一工程主链入口

## 本阶段目标（必须达成）
定义一条“完整 offline 工程主链”的目标拓扑与工程接入点：

phone_local archive  
→ source policy selection（offline-only）  
→ PerceptionEval 默认入口（offline 默认源选择：YOLO pinned_local → fallback baseline/mock）  
→ SceneContext gates（最小 runtime 化的 gate：**仍只用于 offline 运行时约束，不进入真实 runtime**）  
→ SceneTask candidate  
→ Fusion candidate  
→ Output candidate  
→ trace/replay/whitebox artifacts（统一落盘与索引）  
→ end-to-end report（统一总报告入口）

## 本阶段非目标（必须写死）
- 不新增模型能力（不做 tracking/depth/OCR/dynamic 等）
- 不进入 controlled_live_stream
- 不进入真实 runtime
- 不重跑完整下游链路（本阶段只规划；实现/回归在后续 EF-002~006）
- 不扩 Option A
- 不执行导航动作、不真实播报

## 现状盘点：已完成 vs 仅定义 vs 需集成
### 已完成（可复用）
- phone_local archive/FieldBatch（离线输入）
- YOLO shadow adapter + verifier
- YOLO offline default source policy（策略文件/审计要求）
- pinned_local 权重固化（manifest + sha256 + readiness）
- staged 的 Perception/SceneTask/Fusion/Output bridge 评测与 E2E offline 验证（证明链路可闭合）

### definition_only（需 runtime gate 化，但仍 offline-only）
- SceneContext-001/002/003：目前主要是 definition/contract/policy，需要以“最小 gate”形式落到主链 runner 的运行时检查（**不触达真实 runtime**）

### integration_needed（从分阶段工具链 → 统一主链）
- PerceptionEval 默认入口接入（让 source policy 真正成为默认选择点）
- SceneTask/Fusion/Output 从“桥接评测工具”收敛到“统一 runner 可调用的主链模块链”
- trace/replay/whitebox 的统一落盘结构、索引与总报告入口

## 工程闭合前必须继续保持的边界（红线）
- `side_effects_released` 默认 false（不得被主链集成改变）
- candidate-only：所有输出不得进入执行面
- no-real-TTS：语音/TTS 只能候选态，且必须受控（后续 EF-?? 单独定义）
- `pending_real_sidewalk_run` 必须保持 true
- fallback baseline/mock 必须保留（fail-closed）
- disable_yolo 必须保留
- 不改变 evidence boundary / evidence_type 的治理含义

## 需要形成的“统一工程入口”（定义，不实现）
### 统一离线主链 runner（EF-004）
- 输入：phone_local archive（批处理样本集）
- 运行：source policy selection → PerceptionEval 默认入口 → SceneContext gates → SceneTask → Fusion → Output（全部 candidate-only）
- 产物：按统一目录结构落盘 trace/replay/whitebox + per-sample summary + 全局汇总 report
- 约束：任何失败必须 fail-closed（fallback baseline/mock 或标记样本不可用），不得触发执行面

### 统一观测入口（EF-005）
- 目标：把“多工具、多日志、多 artifact”收敛成一次运行的一份总入口报告
- 内容：coverage、fallback 率、candidate-only/no-real-TTS 统计、evidence boundary、pending_real_sidewalk_run 传播、禁止项扫描结果等

## 后续阶段建议排期（冻结为工程顺序，不在本阶段实现）
- **EngineeringFlow-002**：YOLO default offline source 接入 PerceptionEval 默认入口（把 policy 变成默认选择点）
- **EngineeringFlow-003**：SceneContext gates 最小 runtime 化（作为 offline runner 的 gate，不进入真实 runtime）
- **EngineeringFlow-004**：YOLO → SceneContext → SceneTask → Fusion → Output 一键离线主链 runner
- **EngineeringFlow-005**：统一 trace/replay/whitebox 总报告（观测收口）
- **EngineeringFlow-006**：全链路回归测试与验收（从“能跑”到“稳定可回归”）
- **EngineeringFlow-Closure**：Offline Engineering Mainline Closure（工程主链正式封存）

## 本阶段停止条件
- 计划文档完整：主链拓扑、非目标、模块顺序、红线边界、后续阶段顺序与验收标准已冻结
- 模块状态矩阵完成
- 接入顺序与禁止扩展政策完成
- GO/NO-GO pack 完成
