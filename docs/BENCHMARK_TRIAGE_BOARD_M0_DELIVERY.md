# Benchmark Triage Board M0（场景问题分诊板 M0）交付

## 1. 定位（写死）

分诊板是**分诊层**，不是评测层：把 benchmark/真实场景评测结果转成研发优先级输出，回答：

- 哪些 case 最值得先打
- 哪些模块最值得先改
- 哪些 issue 最值得先处理

不做：Jira/工单系统、自动派单、历史趋势看板、多版本回归大盘、自动修复/调参。

## 2. 交付件

- 分诊板工具：`tools/benchmark_triage_board.py`
- 单测：`tests/test_benchmark_triage_board.py`
- smoke：`tools/smoke_benchmark_triage_board.py`（读取 `logs/real_scenario_pack_m0.json`，输出 `logs/smoke_benchmark_triage_board_*.json`）

## 3. 输入来源（只读）

只消费统一 benchmark 输出文件（例如 `logs/real_scenario_pack_m0.json`）中的 `ScenarioBenchmarkResult[]`：

- quality_grade / issue_type
- optimization_hint_module / optimization_hint_type
- blocked/resolved 等摘要字段

不重算主线结果。

## 4. 数据结构

- `BenchmarkTriageCaseItem`：case_id / type / quality / issue / hint_module / priority_score+level / triage_reason
- `BenchmarkTriageModuleItem`：module_name / related_case_count / poor_case_count / issue_types / priority_score+level / triage_reason
- `BenchmarkTriageIssueItem`：issue_type / case_count / poor_case_count / related_modules / priority_score+level / triage_reason
- `BenchmarkTriageBoardResult`：ranked_* + next_focus_* + triage_summary

## 5. 最小分诊规则（M0）

### 5.1 case 排序（规则累加）

- poor +50
- acceptable +20
- blocked_without_resolution +40
- feedback_not_effective +30
- high_dead_branch_ratio +20
- 有明确 optimization_hint_module +10（可行动）

### 5.2 module 排序（聚合）

- 每个相关 case +10
- 每个 poor case +20
- blocked_without_resolution case +25
- feedback_not_effective case +20

### 5.3 issue 排序（类型权重优先）

M0 写死：issue 类型权重应强于出现频次（避免“常见但不致命”盖过“少见但致命”）。

## 6. next focus 输出（M0）

- next_focus_case_ids：取 top 2~3
- next_focus_modules：取 top 2~3
- next_focus_issue_types：取 top 2~3

## 7. 运行方式

```bash
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m0.json
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m0.json --out logs/benchmark_triage_board_m0.json
```

## 8. 强约束（写入 CONTRACT）

后续真实场景评测结果应优先通过 Benchmark Triage Board 转为研发优先级输出；不得长期停留在“有评测结果但没有统一分诊与优先级”的状态。

## 9. 结论（M0）

分诊板已建立：可将真实场景评测结果自动整理为 case/module/issue 优先级与 next focus，推动从“看结果”进入“先打什么/先改什么”的研发闭环。

## 10. Post-Fix 分诊重刷（M0）

在更新 `logs/real_scenario_pack_postfix_m0.json`（或任意同结构的 pack 输出）后：

```bash
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m0.json --out logs/benchmark_triage_board_postfix_m0.json
```

统一 before/after 与下一轮 triage 起点见：`docs/POST_FIX_REBASELINE_M0.md`。

## 11. Post-Fix 分诊重刷（M0.1，第二批）

在更新 `logs/real_scenario_pack_postfix_m01.json` 后：

```bash
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m01.json --out logs/benchmark_triage_board_postfix_m01.json
```

before/after 与 triage 清空结论见：`docs/POST_FIX_REBASELINE_M0_1.md`。

## 12. Post-Fix 分诊重刷（M0.2 / M1，第三批）

在更新 `logs/real_scenario_pack_postfix_m02.json` 后：

```bash
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m02.json --out logs/benchmark_triage_board_postfix_m02.json
```

第三批 before/after 与 triage 清空结论见：`docs/POST_FIX_REBASELINE_M0_2_M1.md`。

## 13. Post-Fix 分诊重刷（M0.7 / M6，第八批）

在更新 `logs/real_scenario_pack_postfix_m07.json`（M1.1 后整包）后：

```bash
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m07.json --out logs/benchmark_triage_board_postfix_m07.json
```

第八批扩包 vs M1.1 后 before/after、triage 清空结论见：`docs/POST_FIX_REBASELINE_M0_7_M6.md`。

## 14. Post-Fix 分诊重刷（M0.8 / M7，第九批）

在更新 `logs/real_scenario_pack_postfix_m08.json`（M1.2 后整包）后：

```bash
python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m08.json --out logs/benchmark_triage_board_postfix_m08.json
```

第九批扩包 vs M1.2 后 before/after、triage 清空结论见：`docs/POST_FIX_REBASELINE_M0_8_M7.md`。

