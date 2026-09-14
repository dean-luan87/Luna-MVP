# Luna Voice 最小请求抽链使用说明

## 1. 文档定位

本页说明 **最小可用** 的语音请求抽链：从现有 JSONL/JSON 日志中，按 `request_id` 或 `trace_id` 聚合出一条结构化 **`RequestTraceChain`**。  
**不是**后台、不是存储、不是检索平台。

## 2. 当前能抽什么链

| 链型 `chain_type` | 最小识别条件（实现见 `request_trace_extractor.py`） |
|-------------------|-----------------------------------------------------|
| `success_chain` | `final_execution_mode=provider_chain`，无 fallback/rollback 分叉需求 |
| `provider_fallback_chain` | 存在 `ProviderFallbackObservation` 且终态仍为 `provider_chain` |
| `legacy_rollback_chain` | 存在 `TTSRollbackObservation` 或 `legacy_fallback` 终态 |
| `failed_chain` | `failed_no_output` 或顶层 `ok`/`success` 为 false |
| `suppressed_chain` | **占位**：显式 `suppressed` 或 `OutputDecisionObservation.accepted=false` 且未进 selector（样本少） |

## 3. 数据来源

| 来源 | 说明 |
|------|------|
| `logs/voice_stage22_observations.jsonl` | `validate_local_tts_runtime.py` 写入的信封行：`{"request_id","type","data"}` |
| `logs/voice_stage22_validation_results.json` | 同上脚本汇总 JSON（若存在） |
| `logs/voice_stage22_validation_results.json` | `validate_local_tts_runtime.py` 行数据（若存在） |
| `docs/architecture/voice/fixtures/min_trace_samples.jsonl` | **仓库内固定样例**（3 条：Piper 成功 / Provider fallback / legacy rollback） |

抽链器**按链聚合**：先加载多文件全部行，再按 `request_id`/`trace_id` 过滤合并，**不是**单文件单段语义。

## 4. 阶段覆盖与占位

| 阶段 | 真实覆盖条件 |
|------|----------------|
| `request_ingress` | 有 `TTSCutoverObservation` 时可用 |
| `message_preparation` | 当前多为 **`not_connected`**（`SpeechRequest` 未随日志行落盘） |
| `bridge_or_routing_decision` | `selector_hit` + 可选 `OutputDecisionObservation` |
| `core_or_policy_handling` | **`reserved`**（结构化 policy 未接） |
| `provider_selection` | `ProviderSelectionObservation` |
| `provider_execution` | 由 `cutover_observation.provider_chain_ok` + metadata 推断；非独立 observation 名 |
| `fallback_or_rollback` | `ProviderFallbackObservation` / `TTSRollbackObservation` |
| `playback_result` | `TTSCutoverObservation.final_execution_mode`；细粒度 `PlaybackObservation` 多缺失时为 **missing/partial** |

缺失阶段使用 `status`: `missing` | `not_connected` | `reserved` | `skipped` | `partial`，**不伪造字段**。

## 5. 如何使用脚本

```bash
# 使用仓库默认探测路径（含 fixtures，若 logs 不存在仍有样例）
python3 tools/extract_voice_request_trace.py --request-id fixture_piper_ok_001

# 指定日志文件
python3 tools/extract_voice_request_trace.py --request-id <id> --log logs/voice_stage22_observations.jsonl

# JSON 导出
python3 tools/extract_voice_request_trace.py --request-id fixture_piper_ok_001 --format json

# 按 trace_id（行内需有该字段）
python3 tools/extract_voice_request_trace.py --trace-id trace_fixture_001
```

## 6. 输出结果怎么看

- **`chain_type`**：五类之一（或 `unknown`）。  
- **`final_execution_mode`**：与 `TTSCutoverObservation` 一致（`provider_chain` / `legacy_fallback` / `failed_no_output`）。  
- **`provider_name`**：优先 selection 的 `chosen_provider`，fallback 的 `final_provider_used`，或 cutover metadata。  
- **`stages[]`**：每段 `stage_name`、`status`、`key_fields`、`source_observation_type`。  
- **`errors[]`**：阶段化错误节点（如 execution fail、`failed_no_output`）。  
- **`notes[]`**：如未匹配到日志行、被抑制占位说明等。

## 7. 当前局限

- 无全文检索、无多请求批处理、无时间窗自动修复。  
- `trace_id` 依赖日志行自带；未带则无法按 trace 抽。  
- 被抑制链依赖结构化 `OutputDecisionObservation` 或显式标记，**多数运行路径仍抽不出真实样本**。  
- `PlaybackObservation` 未写入日志时，`playback_result` 仅靠 cutover 粗粒度终态。

## 8. 三条示例（fixtures：真实 request_id / final_execution_mode）

以下与 `docs/architecture/voice/fixtures/min_trace_samples.jsonl` 中三行一一对应，可直接用于 `extract_voice_request_trace.py`。

**说明（验收口径）**：`min_trace_samples.jsonl` 中每条记录为 **与运行时 `validate_local_tts_runtime.py` / 统一入口 `run_tts_unified_entry` 输出同构的 observation 扁平行**（字段与 `__dict__` 序列化一致）。若本机已跑 `validate_local_tts_runtime.py` 并生成 `logs/voice_stage22_observations.jsonl`，对其中 `request_id` 使用同一脚本即可抽链，无需改代码。  
**脚本结构化 JSON 快照**（便于验收归档）：`docs/architecture/voice/fixtures/extracted/` 下 `fixture_*_trace.json` 为对上述三 `request_id` 运行 `--format json` 的导出结果。

### 8.1 Piper 直接成功链

- **request_id**：`fixture_piper_ok_001`  
- **final_execution_mode**：`provider_chain`  
- **observation 片段**：`selection_observation.chosen_provider=piper`，`cutover_observation.provider_chain_ok=true`  

### 8.2 Fish 失败 → Piper fallback 成功链

- **request_id**：`fixture_provider_fallback_002`  
- **final_execution_mode**：`provider_chain`  
- **observation 片段**：`selection_observation.chosen_provider=piper`，存在 `fallback_observation`（`fallback_provider=piper`，`output_valid=true`）  

### 8.3 Provider chain 失败 → legacy rollback 链

- **request_id**：`fixture_legacy_rb_003`  
- **final_execution_mode**：`legacy_fallback`  
- **observation 片段**：`cutover_observation.provider_chain_ok=false`，存在 `rollback_observation`（`rollback_trigger=provider_chain_failure`）  

运行：

```bash
python3 tools/extract_voice_request_trace.py --request-id fixture_piper_ok_001 --format json
python3 tools/extract_voice_request_trace.py --request-id fixture_provider_fallback_002 --format json
python3 tools/extract_voice_request_trace.py --request-id fixture_legacy_rb_003 --format json
```

## 9. 主线—白盒—日志一致性检查

- **A 主线**：抽链数据来自统一入口跑出的 observation 序列（或 fixtures）。  
- **B 白盒**：阶段名与 `WhiteboxPipelineStageV1` / 文档对齐。  
- **C 日志**：`request_id` 为合并主键；缺失阶段显式标注。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**（抑制链/细粒度 playback 为已知缺口）。
