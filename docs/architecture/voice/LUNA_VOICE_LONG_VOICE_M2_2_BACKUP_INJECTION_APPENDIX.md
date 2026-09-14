# M2.2 备路注入式验证附录

## 目的

在 **不依赖** 真实网络偶发故障的前提下，验证接入层 **qwen-plus → qwen-turbo** 主备切换语义：主路三种失败注入后，备路接管且结构化链路健康，且 **不与规则链 fallback 混为一谈**。

---

## 注入方式

- **位置**：仅替换「主」`VoiceLongInputModelProvider` 的 `parse_long_input` 行为；**备**为 `MagicMock`，固定返回可通过 `validate_model_structured_output` 的最小合法 `VoiceLongInputStructuredParseResult`。
- **全链路**：`run_long_input_task_planning_v1(..., parse_config=model_preferred_with_rule_fallback, model_provider=主备 bundle)`，与 M1/M2 smoke 一致地对 `validate_model_structured_output` 做挂钩以读取 validator 结果。
- **json / fallback 口径**：与 benchmark 一致 — `json_ok` = bundle 层 `parse_long_input` 返回非 `None`；`fallback` = `not (json_ok and validator_ok)`。

**代码**：`tests/test_qwen_long_voice_backup_injection_m2_2.py`

---

## 三种注入 case

| Case | 主路行为 | 预期 `provider_switch_reason` 子串 |
|------|----------|-------------------------------------|
| 1. timeout | `parse_long_input` 抛出 `TimeoutError` | `primary_exception:TimeoutError` |
| 2. exception | `parse_long_input` 抛出 `RuntimeError`（parametrize）/ `ValueError`（聚合用例） | `primary_exception:RuntimeError` / `ValueError` |
| 3. returns None | `parse_long_input` 返回 `None` | `primary_returned_none` |

---

## 接管结果（断言摘要）

每次注入后均满足：

- **turbo 接管**：`backup.parse_long_input` 被调用一次；`backup_provider_used is True`；`selected_provider_model_id == qwen-turbo`。
- **结构化健康**：`json_ok == True`，`validator_ok == True`，`fallback == False`（单 case 与三 case聚合均为 `json_rate=1.0`、`val_rate=1.0`、`fallback_rate=0.0`）。
- **非规则链误报**：最终 `VoiceLongInputParseResult.notes` 含 `model_chain`，表明走模型链成功路径，而非将「接入层切备」记成纯规则链兜底。

**validator 失败后不得再调备路**：仍由 `tests/test_qwen_long_voice_primary_backup_provider_m1.py::test_validator_failure_does_not_invoke_backup` 保证，本附录不重复展开。

---

## 是否通过

| 项 | 结果 |
|----|------|
| pytest `tests/test_qwen_long_voice_backup_injection_m2_2.py` | **通过**（含 parametrize 三注入 + 聚合验收用例） |
| 注入后必须 plus → turbo | **满足** |
| 接管后 json / val / fallback | **1.0 / 1.0 / 0.0**（本附录定义之口径） |
| 与规则链 fallback 语义隔离 | **满足**（`model_chain` + M1 validator 边界用例） |

---

## 最终结论

**M2.2 备路注入式验证通过。** 在受控注入下，接入层主备切换行为与 orchestrator/validator 边界符合 M1 设计；与 M2.1 真实压测（主路未触发切换）互补后，**长语音任务拆解主备链在工程上闭环**。

---

## 相关文档

- 主链路线图：`LUNA_VOICE_LONG_VOICE_TASK_PARSE_MAINLINE_ROADMAP_M1.md`
- M2.1 分时段 benchmark：`LUNA_VOICE_LONG_VOICE_M2_1_BENCHMARK_APPENDIX.md`
