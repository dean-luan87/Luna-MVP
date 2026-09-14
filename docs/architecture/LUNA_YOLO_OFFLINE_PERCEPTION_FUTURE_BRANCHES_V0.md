# LUNA — YOLO Offline Perception Future Branches v0 (Phase-ModelPerception-Closure-001)

## 目的
列出 YOLO offline 默认感知源闭合后的**后续分支路线**。本文件只定义路线与注意事项，不授权执行、不改变当前禁止项。

## Branch A — Dependency isolation / AutoUpdate hardening
### 动机
即使 pinned_local 权重已成立，YOLOv5 代码路径仍可能出现依赖自检/AutoUpdate 尝试日志，带来不可控变更风险。
### 目标
- 明确并隔离任何“自动安装/自动更新依赖”的行为
- 让所有依赖变更只能通过明确的依赖清单与审批流程发生

## Branch B — SceneContext runtime gate implementation
### 动机
SceneContext-001/002/003 定义已完成，但 runtime enforce 仍需独立实现与验证。
### 目标
- 将 SceneContext gates 作为 runtime 进入执行面的强约束（但这必须另开阶段，不得由 offline closure 直接推导）

## Branch C — Sample expansion（phone_local）
### 动机
当前 phone_local 样本规模有限，仍需要更广覆盖的离线样本来增强证据强度。
### 目标
- 扩充多场景、多光照、多遮挡、多路况样本
- 保持 candidate-only + evidence boundary + pending_real_sidewalk_run=true

## Branch D — Controlled live preparation
### 动机
phone_local 离线回放 ≠ controlled_live_stream。受控实时流需要独立治理与安全门控。
### 目标
- 明确 controlled_live 的数据获取、审计、回退、禁用、观察窗口与退出策略

## Branch E — Model version upgrade admission policy
### 动机
模型升级必须可审计、可回滚、可并行对比，避免“原地覆盖导致证据失效”。
### 规则（冻结建议）
- 每次升级必须新建 `model_config_id`
- 必须提供新权重 sha256 / size / provenance
- 必须与上一版本并行 shadow 对比与离线验收
- 禁止直接替换旧版本权重并声称“同一模型”

## Branch F — Runtime integration readiness（未来可能）
### 动机
若未来考虑 runtime，必须有完整治理入口与执行面隔离，不能由 offline default 直接继承。
### 规则（冻结建议）
- 必须另开阶段、另写 contract、另做红线审计
- 必须证明不会扩大 side effects 面，且默认 `side_effects_released=false`

