# Phase-Voice-OutputGovernance-003
# Voice Output Runtime Mode Policy v0（运行模式政策）

**目标**：定义 voice output governance 在不同运行模式下的行为边界，避免默认进入 real_playback。  
**边界**：本阶段只定义 policy，不做 runtime 接线。

---

## 1. 模式枚举（必须支持）

### 1.1 `dry_run`

- **行为**：只生成 governance decision / audit envelope / TRW 对齐字段，不调用 provider，不调用 playback，不 submit。
- **审计**：`real_tts_invoked=false`，`provider_invoked=false`，`playback_invoked=false`。
- **用途**：离线回归、合同验证、字段对齐。

### 1.2 `shadow`

- **行为**：主链照旧（保持现状），并行生成 governance decision（不影响输出）。
- **用途**：真实链旁路观测；用于发现未来接线风险。
- **审计**：shadow 侧仍必须输出 `real_tts_invoked=false`（shadow 本身不执行）。

### 1.3 `governed_submit`

- **行为**：governance 决定是否允许 submit（可仍保持 dry-run 或 submit 但不执行真实 TTS）。
- **用途**：将治理层真正纳入主链“提交前裁决”，但仍不进入真实播放。

### 1.4 `real_playback`

- **行为**：只有在所有 gate 通过且 env 明确允许时，才允许真实 TTS + playback。
- **默认**：禁止作为默认模式。

---

## 2. 默认模式（硬规则）

- 默认模式必须是 `dry_run` 或 `shadow`，不得默认进入 `real_playback`。

---

## 3. env 与模式关系（仅定义，不改语义）

现有开关（如 `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1`、`LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS`、`LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1`）不在本阶段改语义。  
后续 Phase-004/真实接线时，需定义“mode 与开关”的优先级关系，但必须满足：

- 没有显式 allow 的情况下，`real_playback` 不可生效。

