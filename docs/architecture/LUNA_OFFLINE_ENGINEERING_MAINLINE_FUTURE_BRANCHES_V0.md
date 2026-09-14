# LUNA Offline Engineering Mainline Future Branches v0

## Phase

- Phase-EngineeringFlow-Closure（Offline Engineering Mainline Closure v0）

## Purpose

列出后续“可走但未授权为主线”的分支方向。注意：本文件不是授权令牌，任何分支都必须走明确入口与验收，不得直接污染 offline engineering mainline 闭环。

## Future branches (not authorized by closure)

### 1) OCR 主线

- 目标：补齐文本/标识等视觉信息的离线候选信号
- 前置：输出合同 + 禁止项 + offline-only 评测工具 + 回归门槛

### 2) Scene Belief / Evidence Arbitration

- 目标：在多证据/多帧/多源冲突下形成可审计的 scene belief
- 前置：证据仲裁合同、冲突策略、回放与白盒要求

### 3) SceneContext runtime gate 强化（仍先离线）

- 目标：把 v0 minimal gate 扩展为更强一致性/连续性判定（但仍 candidate-only）
- 前置：保持禁止项不变；必须通过 EF-006 回归基线；不得引入 runtime

### 4) sample expansion（样本扩容）

- 目标：从 3 条 phone_local 扩展到更大样本矩阵
- 前置：样本分层策略、质量门槛、失败分析与性能预算

### 5) controlled_live preparation（受控 live 准备）

- 目标：在严格治理入口下准备 controlled live 的证据链与运行流程
- 前置：必须独立阶段与治理文件；closure 不授权；不得跳过证据契约

### 6) dependency isolation / AutoUpdate hardening

- 目标：进一步提升可复现性与依赖隔离，降低环境漂移
- 前置：manifest/lock 策略、离线安装策略、fail-closed 政策

### 7) model upgrade admission policy

- 目标：模型升级（YOLO 或其他）准入流程、对比矩阵与决策包
- 前置：准入门槛、回滚策略、回归基线更新规则

### 8) runtime integration readiness

- 目标：为未来 runtime 接入做“就绪评审”，但不实际开启 default path
- 前置：独立的 runtime contract、side effects 治理入口、operator runbook、退出机制

## Global constraints for all branches

- 不得改变 offline engineering mainline 的 closed_v0 正式状态
- 不得绕过 EF-006 regression acceptance
- 不得引入真实 runtime / controlled_live_stream / 导航执行 / 真实播报

