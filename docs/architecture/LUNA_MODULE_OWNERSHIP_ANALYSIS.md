# Luna 架构整顿 Stage-0：模块归属分析（防污染硬版）

> 目标：**不改主链行为**的前提下，先把“逻辑归属”固化，明确后续只能通过 `interface / schema / registry / adapter / facade / bridge` 演进，避免能力板块反向绑架核心骨架。

## 0. 分层枚举（硬约束）

### 建议归属层（枚举）
- `core_framework`
- `capability_voice`
- `capability_vision`
- `capability_emotion_reserved`
- `individual_backend_capability`
- `mixed_coupling_pending_split`

### 建议处理方式（枚举）
- `keep`
- `wrap_with_facade`
- `add_adapter`
- `add_registry`
- `mark_future_migration`
- `split_later`

### 风险等级（枚举）
- `low`
- `medium`
- `high`

## 1. 扫描结论摘要（只谈结构，不做功能）

- **最高风险污染点**：`main.py`（单文件汇聚 runtime / scheduler / risk / voice / vision / intervention / logging 等多板块，已明显超出“Core Framework”边界）。
- **语音链当前形态**：
  - 播放链（TTS）在 `core/speech_gate.py` + `core/audio_worker.py` + `modules/voice.py` + `main.py` 形成闭环，但**逻辑归属混合**（Core 控制 + capability 实现 + 应用层编排混在一起）。
  - ASR 原型存在于 `modules/voice_to_text.py`（Vosk CLI），但**不在主链闭环**。
- **个体后端能力层**（individual backend capability）已经在 `decision_monitor/` 形成相对独立的白盒/审计/日志链，但在应用层（`main.py` 等）存在“直接拼装/直接引用”的倾向，需要通过 bridge/facade **声明边界**，而不是迁移或重写。
- **Backend（`luna_backend/`）**自成一套服务化结构（routes/services/core），与当前 `main.py` 运行主链属于**并存体系**，应在 ownership 上明确为“能力/后端服务侧”，避免 Core 直接耦合其实现细节。

## 2. 模块归属表（重点条目 + 代表性目录）

> 表格字段：文件路径｜当前职责｜当前耦合对象｜建议归属层｜建议处理方式｜风险等级｜备注

| 文件路径 | 当前职责 | 当前耦合对象 | 建议归属层 | 建议处理方式 | 风险等级 | 备注 |
|---|---|---|---|---|---|---|
| `main.py` | 应用主入口/编排：vision pipeline、decision、risk、speech、runtime、日志 | `core/*`, `runtime/*`, `modules/*`, `intervention/*`, `advice/*`, `c3/*`, `a3/*` 等大量直连 | `mixed_coupling_pending_split` | `wrap_with_facade` | `high` | Stage-0 **不动行为**；后续应将“编排”沉到 controller/facade，把 capability 通过 registry 接入 |
| `core/decision_controller.py` | 决策：SPEAK/WAIT/YIELD/RISK_LV1（不直接做 TTS） | `core/speech_gate.py`, `core/risk_assessor.py` | `core_framework` | `keep` | `low` | 明确是 Core 决策层，不应依赖具体 TTS/ASR 实现 |
| `core/speech_gate.py` | 发言权仲裁（去重/冷却/占用） | `main.py` 调用 | `core_framework` | `keep` | `low` | **Core 的治理能力**，不是 voice capability 的附属 |
| `core/audio_worker.py` | 异步音频播放 worker（不阻塞主循环） | `modules/voice.py` 的 `speak()` | `core_framework` | `keep` | `medium` | worker 属于 Core；但当前直接依赖“tts_engine.speak”约定，后续需通过 `TTSProvider` 适配 |
| `modules/voice.py` | macOS `say` TTS 播放实现 | `core/audio_worker.py`（作为 tts_engine） | `capability_voice` | `add_adapter` | `medium` | 应被视为某个 `TTSProvider` 的具体实现（后续迁到 capability/provider 层，Stage-0 不迁移） |
| `modules/voice_to_text.py` | Vosk ASR CLI 工具（文件转文字） | 本地 vosk 模型 | `capability_voice` | `mark_future_migration` | `medium` | 不在主链；应演进为 `ASRProvider` 的一个 provider/adapter |
| `modules/voice_input.py` | 音频输入设备监测脚本（sounddevice） | `sounddevice` | `capability_voice` | `mark_future_migration` | `low` | 工具性质；Stage-0 仅归属声明 |
| `runtime/context.py` | 运行时上下文对象 | `runtime/*` | `core_framework` | `keep` | `low` | Core runtime/state 组成部分 |
| `runtime/observation_loop.py` | 观测循环（read-only） | `runtime/*` | `core_framework` | `keep` | `low` | Core runtime/loop |
| `decision_monitor/` | 白盒/审计/主线/张力/严重度/后处理边界等 | `runtime/context.py`，测试/工具链 | `individual_backend_capability` | `keep` | `medium` | 逻辑上属于个体后端能力层；Stage-0 只做 bridge 占位，不拆服务 |
| `decision_monitor/logger.py` | 白盒日志/JSONL 落地 | `decision_monitor/schema.py` | `individual_backend_capability` | `keep` | `low` | 与 capability 无关，属于后端能力 |
| `tools/real_scenario_pack.py` | 基准/场景压测工具 | `decision_monitor/*` | `individual_backend_capability` | `keep` | `low` | 属于后端能力工具链 |
| `logs/*` | 运行与评测落地数据 | 全局 | `individual_backend_capability` | `keep` | `low` | 逻辑归属：后端能力层（logs/traces/audit） |
| `luna_backend/routes/tts_routes.py` | 后端服务：TTS HTTP API | `luna_backend/services/tts/*` | `capability_voice` | `split_later` | `medium` | 与 `main.py` 主链并存；后续可作为 voice capability 的 provider 实现来源 |
| `luna_backend/services/speech/speech_router.py` | 服务侧语音路由（TTS/真人语音） | `luna_backend/services/tts/*` | `capability_voice` | `split_later` | `medium` | 服务侧能力，不应被 Core 直接 import 绑定 |
| `luna_backend/services/vision/*` | 视觉服务/输出序列化 | `luna_backend/*` | `capability_vision` | `split_later` | `medium` | 服务侧 capability 体系 |
| `core/world_model/*` | world model / map / memory / emotion port 等 | `core/*` | `core_framework` | `split_later` | `medium` | 部分子树（如 emotion）逻辑归属需在后续阶段再细分；Stage-0 仅记录 |
| `core/world_model/emotion/*` | 情感相关占位/port | `core/world_model/*` | `mixed_coupling_pending_split` | `mark_future_migration` | `medium` | 逻辑应归 `capability_emotion_reserved`，但当前位于 core/world_model 下，Stage-0 **不迁移** |
| `core/vision_output_controller.py` | 视觉输出控制（应用侧/输出侧） | `core/*` + vision pipeline | `mixed_coupling_pending_split` | `wrap_with_facade` | `medium` | 可能应拆出到 vision capability bridge；Stage-0 不改 |
| `vision_pipeline/` | 视觉 pipeline（识别/执行器/控制器） | `modules/*`, `core/*` | `capability_vision` | `split_later` | `high` | 目录存在但与 `main.py` 绑定紧；Stage-0 只做归属声明与 future split 标记 |
| `advice/` `intervention/` `c3/` `a3/` | 策略/干预/学习/运行态 | `main.py`, `runtime/*` | `core_framework` | `split_later` | `medium` | 这些更偏 Core policy/controller，但目前与应用编排混合，后续需要治理 |

## 3. 混合耦合与高风险污染点（必须记录）

### 3.1 `main.py`（最高风险）
- **问题**：应用编排层直接 import 了 Core、runtime、capabilities（voice/vision 原型）、policy/intervention、learning、logging 等多个板块。
- **建议**：后续以“controller/facade”为分界，把：
  - Core runtime/taskchain/scheduler/policy/state/session 固化为 Core Framework
  - Voice/Vision 通过 capability registry/provider/adapter 进入
  - whitebox/logs/traces/memory 通过 backend bridge/facade 暴露给 Core

### 3.2 语音链（TTS）
- **问题**：`core/audio_worker.py` 目前依赖传入对象具备 `.speak(text)` 约定；这相当于隐式接口，容易被未来各种实现污染。
- **建议**：Stage-0 建立 `TTSProvider` + `VoiceCapabilityRegistry`（本轮已占位），后续让 legacy `modules/voice.py` 通过 adapter 实现 `TTSProvider`。

### 3.3 个体后端能力层（whitebox/logs/traces/memory）
- **问题**：白盒与审计逻辑已相对独立（`decision_monitor/`），但在应用层可能被“直接拼装”使用，边界不显式。
- **建议**：Stage-0 先建立 `backend_bridge/` README 与 bridge 占位（本轮完成），后续再做物理拆分或服务化。

## 4. 后续迁移优先级建议（只记录，不执行）

1. **先治理 `main.py` 的边界**（不迁移，先 facade/controller 化）：把“编排”收敛到 `core/controller/*` 或 `app/controller/*`（待定），并通过 capability registries 接入。
2. **语音 capability provider/adapter 落地**：将 `modules/voice.py` 封装为 `TTSProvider` adapter；将 `modules/voice_to_text.py` 演进为 `ASRProvider`（保持 CLI 工具存在）。
3. **vision_pipeline 边界治理**：明确输入/输出 schema，减少 Core 直接依赖视觉执行器细节。
4. **individual backend capability 的 bridge 化**：将 decision_monitor 的产物通过稳定 API 暴露给 Core（而不是 Core 直接拿内部结构）。

