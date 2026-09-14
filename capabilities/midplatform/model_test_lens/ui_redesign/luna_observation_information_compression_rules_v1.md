# Luna Observation — Information Compression Rules V1

将当前纵向长页面内容重新收纳到单屏仪表盘。

## 收纳映射表

| 当前内容 | 新位置 | 默认可见 |
|----------|--------|----------|
| 综合分 100% | 顶部状态条 / 底部指标摘要一行 | 是（摘要） |
| 一句话结论 | 右侧解释面板顶部 | 是 |
| 关键洞察 | 右侧「我看到了什么」 | 是（1–3 条） |
| 主要问题 | 右侧「我不确定什么」 | 是（1–3 条） |
| 分割得分条形图 | 底部「指标详情」drawer | 否 |
| 详细指标（ATE/漂移等） | 底部「指标详情」drawer | 否 |
| 普通对比图 | 中央画面 Tab「普通对比」 | 切换时 |
| 机器人视角 HUD | 中央画面默认 | 是 |
| Manifest / Job / Runner Bridge | 底部「高级流程」drawer | 否 |
| Raw JSON / artifact_ref / phase_ref | 底部「开发者 JSON」drawer | 否 |
| TestBoard refs | 底部 TestBoard drawer 或开发者区 | 否 |
| Debug zone 全量字段 | 开发者 drawer | 否 |

## 默认首屏只保留

1. **结论摘要**（一行，底部或右侧顶）  
2. **主观察画面**（HUD 默认）  
3. **Luna 解释**（五块压缩）  
4. **核心指标摘要**（底部一行）  

## 不得默认占据主屏

- 分割得分条形图整屏  
- 详细指标表格/列表  
- 关键洞察 + 主要问题独立大段  
- Visual Compare 与 HUD 上下各一整屏  

## 右侧五块压缩规则

每块默认 **1–3 条** bullet；超出部分面板内滚动，不撑高页面。

| 块 | 来源字段 |
|----|----------|
| 当前任务 | task_name + task_goal |
| 我看到了什么 | system_observations + insight bullets |
| 我不确定什么 | uncertainty_summary + top_failures |
| 可能漏掉什么 | missing_information + risks_and_gaps |
| 建议下一步 | recommended_next_steps |

## 底部摘要行示例

```
综合分 100% · Prompt 成功 20/20 · 主要风险：未发现显著失败 · 结果仅供模型评估
```
