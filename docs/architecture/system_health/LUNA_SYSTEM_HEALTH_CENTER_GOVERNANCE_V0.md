# System Health Center Governance v0

**Phase**：`Phase-SystemHealthCenter-Governance-001`  
**定位**：统一 OCR / Vision / Voice / STCM / CrossModal / TaskChain 等模块的**健康检测、故障分类、恢复动作、能力遮罩与运行模式**治理契约。**不接 runtime**，不真实恢复，不改 routing。

**角色分工**：

| 组件 | 职责 |
|------|------|
| 模块 | 自检、心跳、错误码、局部建议 |
| System Health Center | 统一判断、分级、隔离、降级、恢复决策、capability mask、operating mode |
| Gate | 能否输出 / 写入 / 行动 |
| TaskChain | 读取 capability_mask 决定任务如何继续 |
| Simulation Lab | 制造压力与故障 |
| Benchmark Collector | 记录结果 |

**能力**：`capabilities/system_health/system_health_center_governance_v0.py`  
**Runner**：`tools/evaluation/system_health/run_system_health_center_governance_v0.py`  
**Verifier**：`tools/evaluation/system_health/verify_system_health_center_governance_v0.py`

**下游引用（contract-only）**：`Phase-Poster-Real-OCR-Gated-Execution-001` 通过 `poster_real_ocr_system_health_link_report.json` 引用本治理契约；**不接 runtime health**（`provider_health_runtime_checked=false`）。

**建议下一 phase**：`SystemHealthCenter-DryRun-001`
