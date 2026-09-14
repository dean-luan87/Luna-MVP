# LUNA — Offline Mainline Integration Sequence v0 (Phase-EngineeringFlow-001)

## 目的
冻结 offline engineering mainline 的后续接入顺序，避免在工程闭合前陷入模块局部优化或能力增强。

## 冻结顺序（必须按序推进）

### EngineeringFlow-001（本阶段）
- 输出：主链集成计划 + 模块状态矩阵 + 接入顺序 + 无扩展边界政策 + GO/NO-GO

### EngineeringFlow-002（下一阶段）
- **YOLO default offline source 接入 PerceptionEval 默认入口**
- 要点：
  - 把 source policy 变成统一默认选择点（pinned_local → fallback baseline/mock）
  - 保持 disable_yolo 与 fail-closed
  - 不进入 runtime

### EngineeringFlow-003
- **SceneContext gates 最小 runtime 化**
- 要点：
  - 将 SceneContext-001/002/003 的核心 gates 变成 offline runner 的运行时检查
  - 只在 offline mainline 生效，不触达真实 runtime

### EngineeringFlow-004
- **统一离线主链 runner**
- 要点：
  - phone_local archive → source selection → PerceptionEval → SceneContext gates → SceneTask → Fusion → Output（candidate）
  - 统一生成 trace/replay/whitebox
  - 失败必须 fallback/标记，不得触发执行面

### EngineeringFlow-005
- **统一 trace/replay/whitebox 总报告（观测收口）**
- 要点：
  - 单入口总报告：coverage、fallback、candidate-only/no-real-TTS、evidence boundary、pending 传播、禁止项扫描

### EngineeringFlow-006
- **全链路回归测试与验收**
- 要点：
  - 把“能跑”推进到“可回归、可验收、可审计”
  - 先全链路回归，再进入模块专项测试

### EngineeringFlow-Closure
- **Offline Engineering Mainline Closure**
- 要点：
  - 冻结工程主链入口、版本策略、审计口径、禁止项

## 明确不允许的跳跃
- 不允许从 EF-001 直接跳到“模块增强/能力增强”
- 不允许在 EF-004 之前做模块专项测试优先化
- 不允许在 EF-Closure 前进入 controlled_live/runtime/full trial

