# Luna 长语音模型接入变更清单 v1（轨道铺设）

> 本轮目标：**模型可插拔轨道 + 双通道 + 校验 + 降级**，**不**接入真实 Qwen 权重、**不**替换 builder、**不**接执行层。

## 一、新增或强化的对象/脚本

| 路径 | 作用 |
|------|------|
| `capabilities/voice/interfaces/voice_long_input_model_provider.py` | `VoiceLongInputModelProvider` 协议；`MockVoiceLongInputModelProvider`、`PlaceholderVoiceLongInputModelProvider` |
| `capabilities/voice/bridge/voice_long_input_model_adapter.py` | 双通道适配、B 组 enrich、历史 `LongVoiceModelAdapter` 协议（与 orchestrator 的 Provider 并存） |
| `capabilities/voice/bridge/voice_long_input_parse_orchestrator.py` | `orchestrate_long_input_task_planning`：路由 → 模型 → 校验 → enrich → 可选 sanitize → 规则 feedback 合并 → `structured_to_voice_long_input_parse_result` |
| `capabilities/voice/bridge/voice_long_input_parse_route_selector.py` | `parse_mode` / `enable_model_adapter` 判断 |
| `capabilities/voice/bridge/voice_long_input_model_output_validator.py` | `validate_model_structured_output`：域、任务数、mapping 前缀等 |
| `capabilities/voice/bridge/voice_long_input_model_validation.py` | mapping 白名单、sanitize（校验通过后防御性清洗） |
| `capabilities/voice/bridge/voice_long_input_structured_to_parse_result.py` | 结构化结果 → `DomainClassificationResult` + 候选 → **builder** |
| `capabilities/voice/config/voice_long_input_parse_config.yaml` | `parse_mode`、`enable_model_adapter`、`model_timeout_ms`、fallback 等 |
| `capabilities/voice/config/voice_long_input_parse_config.py` | 配置加载与默认 |
| `capabilities/voice/bridge/voice_long_input_task_planner.py` | `run_long_input_task_planning_v1` → orchestrator；`run_long_input_task_planning_v1_rule_chain` → 纯规则链 |
| `tests/test_voice_long_input_model_orchestrator_v1.py` | 双通道与降级场景验收 |

## 二、规则链 / 模型链如何切换

- 配置：`voice_long_input_parse_config.yaml`（或代码 `VoiceLongInputParseConfig`）。
- `parse_mode: rule_only`（默认）或 `enable_model_adapter: false`：**仅** `run_long_input_task_planning_v1_rule_chain`。
- `parse_mode: model_preferred_with_rule_fallback` 且 `enable_model_adapter: true` 且调用方传入 `model_provider`：尝试 `parse_long_input`；失败/超时/校验失败则回规则链。

## 三、validator 做什么

- 校验 `VoiceLongInputStructuredParseResult`：`schema_version`、输入模式与全局判断存在性、`primary_domain` / `secondary_domains` 合法、任务候选数量与 mapping 前缀白名单、`allow_non_task_payload` 约束。
- **失败**：不穿透模型链；orchestrator **回退** `run_long_input_task_planning_v1_rule_chain`。

## 四、fallback 怎么做

| 情况 | 行为 |
|------|------|
| Provider 返回 `None` | 规则链 |
| 超时（`ThreadPoolExecutor` + `model_timeout_ms`） | 若 `fallback_to_rule_on_timeout` → 规则链 |
| Provider 异常 | 若 `fallback_to_rule_on_validation_error` → 规则链（见 orchestrator） |
| 校验失败 | 规则链（当前实现不因校验失败而阻塞主入口） |

## 五、为什么这一轮仍然不是真实模型上线

- 仅定义 **协议**（`VoiceLongInputModelProvider`）、**适配与校验**、**路由**；**无**权重加载、**无**推理引擎绑定。
- 后续接入本地 Qwen 4B 时，只需实现 `VoiceLongInputModelProvider.parse_long_input`，返回符合 `voice_task_parse_v1_1` 的结构化结果，无需改 builder 或执行层。
