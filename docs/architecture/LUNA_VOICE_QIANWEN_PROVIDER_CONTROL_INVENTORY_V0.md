# LUNA Voice — Qianwen Voice Provider Control Inventory v0（Phase-Voice-Qianwen-000）

**范围**：只做静态盘点。**不改 runtime**、**不真实调用 Qwen/DashScope**、**不真实 TTS 播报**，不接新 provider，不删除 legacy voice/TTS，不改动现有 env 开关语义与默认策略。

**数据来源**：[`tools/run_voice_qianwen_provider_control_inventory_v0.py`](../../tools/run_voice_qianwen_provider_control_inventory_v0.py) 最近一次运行产物（路径见文末 **inventory output_root**）。  
语义说明：必须把 **(a) 代码资产存在**、**(b) 文档/配置文件声明** 与 **(c) 默认基线或可证明已激活的运行态口径** 分开，不得把文档一句「首选」直接等同主链闭环。

---

## 1. 结论摘要（验收项对应）

### 1.1 Qwen / Qianwen / DashScope / 语音相关代码

- **适配器**：`capabilities/voice/providers/qwen_tts_provider.py`（`QwenTTSProvider.name == "qwen"`；模块边界声明：**仅 text→audio**）。
- **统一入口链路**：`capabilities/voice/runtime/tts_unified_entry.py` → `tts_provider_selector` / `tts_fallback_manager`。
- **长输入侧的 Qwen 模型 provider**（与「播报合成」不同链路）：  
  `qwen_long_input_model_provider.py`、`qwen_external_long_input_model_provider.py`。
- **输出平面**：`capabilities/voice/output/voice_output_plane_v1.py`（可选用 `execute_tts` 调用 unified entry）。
- **输出治理骨架（独立模块）**：`capabilities/voice/output/voice_output_governance_v0.py`。
- **详细分桶**：见当次输出的 `voice_qianwen_code_asset_matrix.json`。

### 1.2 Qwen 是否「voice primary」

| 层级 | 判定 | 证据要点 |
| --- | --- | --- |
| 配置模板 / 声明口径 | **支持**「Qwen 在链首」 | `voice_tts_config.yaml` 下 `runtime_modes.online_prefer_qwen`：`provider_order: [qwen, piper]`，`active_provider: qwen`。 |
| 默认 YAML 顶层基线（仓库签入） | **否**——当前仍为 **offline-only / piper 首链** | 顶层：`tts_runtime_mode: offline_only`，`provider_order: [piper]`，`local_runtime.qwen.enabled: false`。 |
| 主链「已激活且可审计」的首选 | **本阶段未定稿为 GO**——需运行态与接线证明 | 静态证据见下文 guard/SpeechGate/governance **缺口**（H-001）。 |

### 1.3 TTS 是否 fallback（含 Piper）

- **是（在 online_prefer_qwen 模板下）**：`provider_order` 中 `piper` 位于 `qwen` 之后；`tts_fallback_manager`/`fallback` YAML 语义支持超时/无效音频后的链式退路。
- **说明**：fallback 的目标是 **离线/本地 Piper（及 legacy）** 等链路，不等于「删掉 TTS」。

### 1.4 provider selection 是否支持「Qwen first, TTS fallback」

- **配置与选择器链路支持**：存在 `online_prefer_qwen` runtime mode 模板 + unified entry 中对 `execute_provider_chain` 的接线。
- **与默认基线的关系**：默认仓库基线仍为 `offline_only` → **不包含**在线 `qwen`；是否启用取决于运行态与环境（网络、密钥、runtime mode 切换），与本 inventory 的运行时无关。

### 1.5 Qwen 输出是否必经 guard / SpeechGate / output governance

- **模块能力**：`voice_output_governance_v0` **存在**并实现 `guard_v1_speakable_text`、SpeechGate 合同（dry-run）、expiry/interrupt/provider_health 等与 Phase-008/009 shadow 工具的字段相容设计。
- **与 `VoiceOutputPlaneV1.execute_tts` / `run_tts_unified_entry` 的证明性串联**：  
  **`unknown`（无法在静态上证明已通过）**。  
  明确代码注释：`voice_output_plane_v1` 中 **execute_tts 路径仍不接 SpeechGate / audio_worker**（见源码注释）。`_maybe_submit_real_output_v1` 亦未见对 `build_voice_output_governance_decision_v0` 的调用。

### 1.6 source_text / spoken_text / model_generated / diff audit

- 仓库中存在散落的 `spoken_text`、少量 `model_generated_text`/`source_text`/审计相关 token 命中，但 **未发现**可被本 inventory 认定的 **成对结构与 diff_audit 流水线**。
- **`source_text_spoken_text_diff_defined`：false**，登记硬缺口 **QWVoice-INV0-H-002**。

### 1.7 rewrite_allowed / expression_only / no_fabrication（voice 树下）

- 在 **`capabilities/voice/`** 范围内：**未发现** `rewrite_allowed` / `expression_only` 命中 → **rewrite_control_defined: false**，软缺口 **QWVoice-INV0-S-001**。  
（其他顶层能力树可能存在同名 token，但与「播报控制面」不构成已接线事实。）
- **`no_fabrication_control_defined`：false**（voice 树下无结构化字段）；`voice_final_text_dispatcher._maybe_submit_real_output_v1` 仅有占位词启发式替换，不等于 policy，见 **S-002**。

### 1.8 Qwen provider health / fallback 观测

- **存在**：`tts_provider_health_v0.py`、`voice_output_governance_v0` 内 `evaluate_tts_provider_health_v0`；YAML 中层与 online_runtime 模板含 circuit breaker 字段；fallback manager 内含 **qwen 专用超时**等记录。
- **与「已通过 governance 的统一观测」**：受 H-001 影响，端到端证明仍为 **不完整**。

### 1.9 Qwen 是否为「普通 TTS」？

- **`QwenTTSProvider`** 的工程边界：**是「在线 TTS 合成」（text→bytes）**，且代码声明 **不从模型侧生成可读文本**。  
若未来引入「会改写语义」的表达模型，则需按 **expression provider** 另立控制（与本轮 `qwen-tts` 适配器区分开）。

---

## 2. 缺口登记表（节选）

详见当次：`voice_qianwen_control_gap_register.json`。

| gap_id | 级别 |
| --- | --- |
| QWVoice-INV0-H-001 | hard — governance 未证明在 unified TTS 前串联 |
| QWVoice-INV0-H-002 | hard — 缺少 source/spoken/generation diff 审计 schema |
| QWVoice-INV0-S-001 | soft — voice 树无 rewrite/expression_only 字段 |
| QWVoice-INV0-S-002 | soft — no_fabrication 未结构化 |
| QWVoice-INV0-S-003 | soft — 默认仍为 offline_only/piper，易与口述策略混淆 |
| QWVoice-INV0-FUT-001 | future — 密钥/合规运行时 |

决策包：**[`LUNA_VOICE_QIANWEN_PROVIDER_CONTROL_INVENTORY_GO_NO_GO_PACK_V0.md`](./LUNA_VOICE_QIANWEN_PROVIDER_CONTROL_INVENTORY_GO_NO_GO_PACK_V0.md)**。

---

## 3. inventory output_root（最近一次运行）

`/Users/luanlei/Desktop/Luna-Core/logs/voice_qianwen_provider_control_inventory_000_20260506_034227Z/`

此后重跑时请使用 CLI 输出的新目录：`python3 tools/run_voice_qianwen_provider_control_inventory_v0.py --output-root logs/voice_qianwen_provider_control_inventory_000_<timestamp>`。
