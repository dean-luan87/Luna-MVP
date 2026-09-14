# Real Scenario Pack M0（真实场景包 M0）交付

## 1. 定位（写死）

本轮不是扩平台能力，而是把**已有真实场景载体**接入统一评测支架，形成第一版“真实场景基线包”。

硬要求：

- 结果结构必须沿用 `ScenarioBenchmarkResult`（不另造格式）
- 判定规则沿用 Scenario Benchmark Harness（quality_floor / expected_issue / default pass）
- 真实场景与 synthetic benchmark 产物可对照：结构树 / 质量等级 / issue / 优化建议 / 验证结果

## 2. 交付件

- 真实场景包入口：`tools/real_scenario_pack.py`
- 真实场景载体（M0）：`tests/real_scenarios/snapshots/*.json`（snapshot_json）
- smoke：`tools/smoke_real_scenario_pack.py`（输出 `logs/smoke_real_scenario_pack_*.json`）

## 3. 真实 case 结构说明

复用 `ScenarioBenchmarkCase`，并新增输入引用（input_ref）概念：

- `input_mode`: image / trace / snapshot_json
- `input_ref`: 文件路径
- `ctx_override`: 预留（M0 未强制使用）

M0 重点跑通 `snapshot_json`；对 image/trace 仅做加载占位与 graceful fallback，不扩平台能力。

## 4. 接入的真实 case（M0 最小 6 个）

- R1_container_real
- R2_occlusion_real
- R3_general_search_real
- R4_feedback_effective_real
- R5_feedback_ineffective_real
- R6_blocked_or_fallback_real

## 4.1 M0.1 第二批真实场景扩充
第一批 6 个真实基线已用于完成 `Post-Fix` 重刷；本轮进入第二批扩充（M0.1）新增 4 个 `ctx_json` case（R7~R10），详细结果见：`docs/REAL_SCENARIO_PACK_M0_1_DELIVERY.md`。

每个 case 都提供最小预期字段（focus_text / expected_flow_family / expected_quality_floor 或 expected_issue_type / notes）。

## 5. 运行方式

### 单真实 case

```bash
python3 tools/real_scenario_pack.py --case_id R1_container_real
```

### 整包运行

```bash
python3 tools/real_scenario_pack.py
```

### 输出文件

```bash
python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m0.json
```

输出格式：`{ summary, results }`，其中 results 为 `ScenarioBenchmarkResult[]`。

## 6. summary 输出

在 benchmark summary 基础上，额外补充：

- real_case_ids
- worst_real_case_ids
- real_case_quality_overview

## 7. 强约束（写进 CONTRACT）

后续新增真实场景验证时，应优先接入 Real Scenario Pack / Scenario Benchmark Harness 的统一 case 结构，不得长期以散落脚本或口头说明替代标准化真实场景基线。

## 8. 结论（M0）

真实场景包已接入统一评测支架，形成第一版真实基线载体（snapshot_json）。后续可逐步将载体替换为 image/trace 等更接近真实输入来源的形式，但评测结果与判定规则必须保持统一。

## 9. 分诊板（Benchmark Triage Board）

真实场景评测结果的研发优先级整理见：`docs/BENCHMARK_TRIAGE_BOARD_M0_DELIVERY.md`（case/module/issue 排序 + next focus）。

## 10. Post-Fix 统一基线重刷（M0）

定点 sprint（Recheck / Confirmation / Hypothesis）之后，建议重刷并固定一份「post-fix」产物便于对照：

```bash
python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m0.json
```

结论与 before/after 摘要（含 R1/R5/R6）：`docs/POST_FIX_REBASELINE_M0.md`。

