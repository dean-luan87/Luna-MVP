# risk_interrupt_v1 观察窗口执行 SOP（V1）

## 目标

在主线统一回归执行器 **V1.1** 已打通“**测试 → risk analyzer**”链路后，把 risk_interrupt_v1 试点从“能跑”固化为“**固定运转流程**”：

- 什么时候执行
- 怎么执行
- 产物怎么归档
- 谁做三选一结论
- 结论出来后下一步固定动作是什么

本文件只定义流程，不改代码、不扩边界。

---

## 1. 角色与职责（写死）

- **执行者（Runner）**：负责按 SOP 运行回归执行器、收集产物、提交窗口归档草稿（不做结论拍板）。
- **评审者（Reviewer/Owner）**：负责抽检样本、填写窗口结论、做三选一拍板，并决定后续动作（维持/L1/L0）。

> 原则：执行与拍板分离，避免“跑完就顺手扩边界”。

---

## 2. 什么时候跑 `run_mainline_regression_v1.py`

### 2.1 必跑场景（每次改动后）

满足任一即必跑（至少跑一次）：

- 改动任一主线链路：submit/request/playback/cancel
- 改动 orchestrator 或三条旁路的主线接入
- 改动 risk 试点相关（Level2A/2B、telemetry、观测字段）
- 改动 `tools/analyze_risk_interrupt_v1_pilot.py` 或回归脚本集合

### 2.2 推荐频率（观察窗口内）

- **观察窗口期间**：至少每日一次（或每次合并后一次）
- **窗口结束前**：必须跑一次作为窗口封板证据

---

## 3. 什么时候必须连带跑 risk analyzer

> 说明：V1.1 已在执行器中自动追加 analyzer（`risk_analysis` 分组）。

因此“必须连带跑 analyzer”的条件等价为：

- 只要跑了 `tools/run_mainline_regression_v1.py`（且窗口内启用了 risk 相关回归脚本产物），就应保存 analyzer 产物。

特殊情况：

- 若执行器报告 `risk_analysis` 为 **SKIPPED**（找不到 risk trace 输入），则本次不产出窗口结论；需要先修复 trace 产出路径，再重新跑。

---

## 4. 什么时候需要填写窗口结论文档

当满足以下条件时，必须填写并归档窗口结论文档：

- 观察窗口结束（到达预定时长/样本量）
- 或者出现需要紧急决策的情况（例如 suspicious 明显越界、观测链断裂扩大、回退频繁）

填写模板：

- `docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_V1_PILOT_WINDOW_REVIEW_TEMPLATE_V1.md`

归档输出（每个窗口一份）：

- `docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_V1_PILOT_WINDOW_REVIEW_<N>.md`（或按日期/编号命名）

---

## 5. 标准执行步骤（执行 → 分析 → 归档）

### 5.1 执行（Runner）

在仓库根目录运行：

```bash
python3 tools/run_mainline_regression_v1.py
```

产物（必须记录）：

- `logs/run_mainline_regression_v1_<UTC>.md`
- `logs/run_mainline_regression_v1_<UTC>.json`
- `logs/analyze_risk_interrupt_v1_pilot_<UTC>.md`
- `logs/analyze_risk_interrupt_v1_pilot_<UTC>.json`

### 5.2 分析（Runner + Reviewer）

- Runner：从 analyzer 报告中提取核心指标（按 `request_id` 聚合口径），并整理 success/fallback/suspicious 样本列表。
- Reviewer：对 suspicious 做抽检复核（必须），并写“是否越界/是否链断/是否需要回退”的结论依据。

### 5.3 归档（Reviewer）

按模板填写：

- 窗口基本信息（起止时间、样本量口径、trace 来源、开关快照）
- 核心指标填写区
- 样本复核结论（尤其 suspicious）
- **三选一结论区**（必须单选）

并将“本窗口对应的回归报告与 analyzer 产物路径”写入附录，确保可复现。

---

## 6. 三选一结论后的后续动作（写死）

### 6.1 结论：继续维持当前试点

动作：

- 维持当前边界不变（不扩 started playback，不扩输出类型，不扩旁路）
- 继续按窗口节奏跑执行器并归档下一窗口

### 6.2 结论：退回 Level 1

动作（写死）：

- 关闭 Level 2 试点开关（至少）：
  - `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT=0`
  - `LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT=0`
- 保留 `risk_interrupt_v1` Level 1 whitebox-only（按环境配置）
- 记录一次窗口归档，注明回退原因与证据（指标 + 样本）

### 6.3 结论：回到 Level 0

动作（写死）：

- 紧急停止 risk 与/或提交链（按窗口结论选择）：
  - `LUNA_ENABLE_RISK_INTERRUPT_V1=0`
  - `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=0`
- 必须归档：
  - 回退触发原因（guardrail violation / observation chain broken / etc）
  - 关键样本 request_id
  - 回退执行时间点

---

## 7. 禁止项（观察窗口内写死）

观察窗口内禁止：

- 放开 started playback 的取消
- 扩大到更多输出类型
- 扩到其他旁路进入真实输出
- 引入恢复/重播/多 request 编排
- 在未完成窗口结论归档前“顺手扩大边界”

---

## 8. 必须归档的产物清单（每窗口必备）

- 回归报告：
  - `logs/run_mainline_regression_v1_<UTC>.md/.json`
- analyzer 报告：
  - `logs/analyze_risk_interrupt_v1_pilot_<UTC>.md/.json`
- 窗口结论文档：
  - `docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_V1_PILOT_WINDOW_REVIEW_<N>.md`

---

## 一句话收束

执行器先停在 V1.1；risk 试点按“执行 → 分析 → 结论（三选一）→ 固定动作”的 SOP 运转，进入长期可控观察态。

