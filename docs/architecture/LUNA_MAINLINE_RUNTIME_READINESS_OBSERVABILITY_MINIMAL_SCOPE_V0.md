# LUNA Mainline Runtime Readiness Observability Minimal Scope v0（Phase-006）

**Phase**：Phase-Mainline-RuntimeReadiness-006  
**定位**：白盒侧 **仅承认最小观测纳入**（与 Phase-005 一致），**不**在本线做白盒产品化。

---

## 1. 允许（minimal）

- `request_trace.stage.runtime_readiness.guarded_trial_hook` 在导出中可见。  
- `mainline_runtime_readiness_v0` 命名空间下的 shadow 记录可审计。  
- side-effect audit：`runtime_invoked` / `provider_invoked` / `playback_invoked` / `world_write` / `navigation_action` / `default_behavior_changed` 等 **可查**。  
- Phase-004/005 工具生成的 trace/replay/whitebox **非空 jsonl**（工程占位 + 审计链）。

---

## 2. 明确不做（当前主线）

- 白盒统一后台、权限分级 UI、跨业务域字段字典、交互式复杂查询引擎。  
- 上述归并为后续独立线：**Phase-Whitebox-Observability-001（System Whitebox Consolidation v0）**，**本仓库主线当前不启动**。

---

## 3. 原则

**纳入与可见** 优先于 **美化与扩展**；主线闭包优先于白盒扩张。
