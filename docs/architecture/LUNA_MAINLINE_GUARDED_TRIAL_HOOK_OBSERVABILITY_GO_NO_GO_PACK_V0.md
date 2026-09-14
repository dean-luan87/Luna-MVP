# LUNA Mainline Guarded Trial Hook Observability Go/No-Go Pack v0

**Phase**：Phase-Mainline-RuntimeReadiness-005

---

## GO

- Phase-004 hook root 可读且结果被加载。  
- 三条 hook（YOLO / OCR / Qwen Voice）shadow stage 均已生成。  
- `stage_namespace == mainline_runtime_readiness_v0`。  
- observability matrix、side-effect audit export、query table 已生成。  
- `enabled=false`、`no_op=true` 保留；hard_audit 全为预期「无副作用」值。  
- trace / replay / whitebox jsonl 非空。  
- `verify_mainline_guarded_trial_hook_observability_v0.py` 退出码 0。  
- 未修改 guarded trial hook 源码逻辑（本阶段仅新增 evaluate/verify 与文档）。

---

## CONDITIONAL_GO

- 尚未实现交互式 / CLI `query` 子命令，但 **静态 `mainline_guarded_trial_hook_query_table.json`** 已就绪。

---

## NO_GO

- 任一 capability stage 缺失。  
- `enabled=true` 或 `no_op=false`。  
- `provider_invoked`、`playback_invoked`、`world_write_invoked` 任一为 true，或 `downstream_invocation_count > 0`，或 `navigation_action` 非空，或 `default_behavior_changed=true`。  
- 本阶段修改了 Phase-004 hook 行为或启用了真实 trial / provider / TTS / 播报。  
- verifier 失败或 trace/replay/whitebox 为空。

---

## 建议下一阶段

- **Phase-Mainline-RuntimeReadiness-006**（示例）：将 shadow stage **接入** 统一 RequestTrace 抽取器（仍默认 shadow，不激活 runtime）；或实现 query CLI 过滤 `query_table` 字段。
