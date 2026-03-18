# 主线验证 / 接入观察 M0.5

对当前主线接入做**统计与观察**，不新增大模块；重点看模块消费率、软动作命中率、阻断来源、价值排序。

## 1. 模块消费率

哪些模块在 `integration_consumed_modules` 里**高频**出现、哪些**低频**。

- 运行分析工具后看「1. 模块消费率」：各模块出现次数与占比。
- 高频：几乎每帧都进 consumed → 主流程稳定消费。
- 低频：仅少数帧出现 → 可能依赖特定场景（如 object_search 需有寻物目标）。

## 2. 软动作命中率

哪些 `integration_soft_actions` **常出现**、哪些**几乎没意义**。

- 看「2. 软动作命中率」：各软动作出现次数与占比。
- 常见：如 `arbitration_summary_ready` 在多数帧出现。
- 罕见：如 `bundle_summary_ready`、`look_forward` 可能只在特定条件下出现 → 可评估是否值得保留或加强触发条件。

## 3. 阻断来源

`integration_blocked_actions` 主要**卡在哪些地方**。

- 看「3. 阻断来源」：各阻断类型次数与占比。
- 若 `blocked_recheck_*` 很多 → 守底/人工确认等经常拦住补证，可考虑是否放宽或分层。
- 若 `blocked_bundle_activation` 多 → bundle 常被守底拦住。
- 若 `blocked_task_resume` 多 → 任务链常处于不可恢复。

## 4. 价值排序

当前主线**最有实际价值**的是：search？recheck？arbitration？bundle？experience 观察？还是别的？

- 看「4. 价值排序」：摘要中 search/recheck/arbitration/bundle/experience **有内容**的帧数（非 none）。
- 排序按活跃帧数从高到低，可据此决定下一步优先加强哪一块。

## 使用方式

### 分析已有 JSONL（推荐）

跑完一段带 Decision Monitor 的主流程后，对产出的 JSONL 做统计：

```bash
python3 tools/analyze_mainline_integration.py logs/decision_monitor.jsonl
```

可选：

- `--max-frames 5000`：只分析前 5000 帧。
- `--json-out report.json`：将报告写入 JSON，便于脚本或后续分析。

### 控制台一行观察（每 N 帧）

`DECISION_MONITOR_ENABLED=1` 且 `DECISION_MONITOR_CONSOLE=1` 时，终端摘要中会多一行：

- `[MainlineM0.5] consumed=N soft=K blocked=L | <integration_summary 前 72 字>`

便于实时观察每帧的 consumed/soft/blocked 数量与摘要预览。

### 单帧观察字段（JSONL / Viewer）

每帧 `mainline_integration` 现含：

- `integration_observation_frame_note`：字符串，形如 `consumed=6 soft=1 blocked=0`，便于 grep 或简单统计。

Viewer 主线接入卡片中会展示「M0.5 观察」该行。

## 修改与新增

| 项 | 说明 |
|----|------|
| `tools/analyze_mainline_integration.py` | 新增：读 JSONL 聚合模块消费率、软动作、阻断、价值支柱活跃度并打印报告 |
| `MainlineIntegrationResult.integration_observation_frame_note` | 新增：单帧一行观察（consumed=N soft=K blocked=L） |
| `DecisionMonitorLogger._print_summary` | 每 N 帧打印时增加一行 [MainlineM0.5] |
| Viewer 主线接入卡片 | 展示 integration_observation_frame_note |

## 注意

- 分析工具依赖 JSONL 中每行含 `mainline_integration`（即 M0 接入后产出的帧）。旧 JSONL 无该字段时，报告会显示「含 mainline_integration: 0」。
- 价值排序的「有内容」由 `integration_summary` 的 fg/tc_state/arb/bundle/search/recheck/exp 段是否非 none 判定，用于相对比较，非绝对业务含义。
