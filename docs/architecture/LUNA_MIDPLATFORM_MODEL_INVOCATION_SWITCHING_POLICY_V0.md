# LUNA MidPlatform Model Invocation Switching Policy v0

## Phase

- Phase-MidPlatform-ModelSwitch-001：Unified Model Invocation Switching Policy v0

## Purpose

把“模型调用切换治理”上升为**中台统一规则**，不再只服务 TTS。该规则适用于在线/本地/备用/规则基线等所有 provider，并保证：

- 优先使用高质量模型（在可接受实时性前提下）
- 实时性不满足则自动降级（fallback）
- 失败不阻塞主链（fail-closed + 快速回退）
- 在线能力不得污染离线基线（显式启用、默认关闭）
- 所有切换可观测/可回放/可审计

## Scope（适用模块）

声明适用于（示例，不限于）：

- **TTS**：Qwen / Fish / Piper / macOS say
- **ASR**：cloud ASR / Whisper / local fallback
- **OCR**：PaddleOCR-VL / PaddleOCR / system OCR / not_available
- **Vision**：VLM / YOLO / lightweight detector / fallback baseline
- **Semantic**：cloud LLM / local LLM / rule baseline
- **Decision**：model-assisted / rule engine / MONC fallback / safe_freeze
- **Any future model provider**

## Core principles（必须写死）

1. **模型是 provider，不是主权层**：主链不把控制权交给单一模型。
2. **中台负责选择/超时/降级/熔断/审计**：provider 不能自带“切换主权”。
3. **在线不得污染离线基线**：offline baseline 必须可复现/可回归；在线必须显式 enable。
4. **低延迟任务优先实时性**：质量优先不能阻塞安全链。
5. **fallback 是强制能力**：每个 capability 的 provider 链必须有降级链路且不可为空。
6. **超时是标准运行态**：硬超时必须定义并执行，而非异常边缘处理。
7. **切换必须留痕**：选谁、为何选、为何降级、结果如何必须结构化记录。
8. **输出仍须过合同与治理门**：switching 只决定“调用谁”，不替代模块输出契约/禁用/审计/安全门。

## Five-layer governance stack（五层）

### 1) Provider Selection

- 输入：capability_type、invocation_mode、policy_id、provider registry（online/local/rule/fallback）
- 输出：provider_attempt_order（包含 skip reason，例如 circuit_open / offline_only）

### 2) Latency Budget

- 为每个 invocation_mode 绑定 latency_profile（soft/first_response/hard_timeout）
- hard_timeout 必须可执行（超过即终止等待并进入 fallback）

### 3) Fallback Chain

- 每个 capability 必须定义 fallback_chain（不得为空）
- fallback 后能力边界必须收缩（不得提升权限）

### 4) Circuit Breaker

- 连续失败/超时达到阈值 → open
- open 期间跳过该 provider 直接 fallback
- half-open 探测恢复

### 5) Observability

- 输出统一的 ModelInvocationResult（含 attempts、latency、fallback、circuit、contract gates）
- 必须可 replay（request_id、trace_ref、配置快照 hash/路径）

## Invocation modes（调用模式分类）

- `realtime_critical`
- `realtime_normal`
- `interactive_quality`
- `offline_evaluation`
- `batch_analysis`
- `experimental_online`

## Relationship to recent TTS policy

近期 Qwen TTS 的在线优先 + 800/1200/2000ms + fallback + circuit breaker 是该中台规则的一个**实例**，不应成为语音特例。

## Non-goals（本阶段不做）

- 不实现具体 provider runtime
- 不改导航主链 / 视觉链 / OCR 链 / 语音链默认策略
- 不进入 controlled_live_stream
- 不真实播报/不执行导航动作

