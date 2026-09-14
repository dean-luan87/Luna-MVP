# Luna Evaluation & Test Board — Artifact Standard v0

**Phase**：`Phase-Luna-Evaluation-Test-Board-001`  
**定位**：**Luna 全局** 测评产物命名与最小集合；**非 OCR 专属**。各模块工具可扩展字段，但 **须** 满足本 v0 基线以便 Test Board 聚合与复验。

---

## 1. 每个测试等级运行的最小产物（base）

任意一次纳入 Test Board 的 **可报告运行**，输出根目录下 **至少** 包含：

| 文件 | 说明 |
|------|------|
| `test_summary.json` | 一次运行的总 verdict、范围、版本、输入摘要 |
| `test_matrix.json` | 本运行覆盖的用例行（对应统一矩阵字段子集） |
| `metrics.json` | 数值指标聚合（延迟、吞吐、错误率等） |
| `error_report.json` | 结构化错误与分类 |
| `audit_report.json` | 禁止项、副作用、网络、缓存、routing 等审计位 |
| `notes.md` | 人工可读说明、已知限制、复现命令 |
| `verifier_report.json` | 静态或后置 verifier 结论与 blockers |

**schema 提示**：各模块可沿用既有 `*_summary.json` 等名称，**须在** `test_summary.json` 中以 `artifact_alias` 或 `includes` 字段 **显式映射** 到上述逻辑名，便于 Board 聚合（本 v0 文档层约定；具体字段以模块 schema 为准）。

---

## 2. 长稳运行（Level 6）附加产物

| 文件 | 说明 |
|------|------|
| `resource_timeseries.jsonl` | CPU/内存/GPU/温度等时间序列 |
| `latency_timeseries.jsonl` | P50/P90/P95 或逐请求延迟 |
| `queue_timeseries.jsonl` | 若存在队列/背压 |
| `stability_report.json` | 泄漏、漂移、退化、恢复次数汇总 |

配置键：`required_artifacts.long_run`（见 example JSON）。

---

## 3. 中断与恢复（Level 5 / Level 4 部分）附加产物

| 文件 | 说明 |
|------|------|
| `interrupt_trace.jsonl` | 中断事件时间线 |
| `recovery_state.json` | 暂停/续跑检查点 |
| `cancellation_report.json` | 取消原因、最终一致状态 |

配置键：`required_artifacts.interrupt`。

---

## 4. 跨模态 STCM（Level 8）附加产物

| 文件 | 说明 |
|------|------|
| `stcm_event_trace.jsonl` | STCM 事件轨迹 |
| `deadline_outcome_matrix.json` | deadline 与结果矩阵 |
| `stale_result_report.json` | 过期丢弃与原因 |
| `voice_notice_report.json` | 语音请求/丢弃/播报窗口 |

配置键：`required_artifacts.stcm`。

---

## 5. 复验与留存

- 所有产物 **须** 可随 `output_root` 整体打包归档；  
- **禁止** 将仅含 base 产物的低等级运行 **宣称为** Level 6/8/9 完成。

---

**非 OCR 专属声明**：本标准为 Vision、Voice、TaskChain、Risk、MidPlatform 等模块 **同等适用**。
