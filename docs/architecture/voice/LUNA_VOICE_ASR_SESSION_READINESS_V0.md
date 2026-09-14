# LUNA Voice — ASR & Session Readiness v0

## ASR

- **期望**：`ASRProvider` 接口 + 可替换实现；trace/replay；无 provider 时的降级策略。  
- **当前盘点**（见 `voice_asr_readiness_matrix.json`）：`capabilities/voice/interfaces/asr_provider.py`、`providers/mock_asr_provider.py` 等存在；**主线 ASR runtime 仍登记为未连接**。  
- **遗留**：`core_snapshot` 等路径可能出现 Whisper 引用，**不等于**当前治理下的主链 ASR。

## Wake / Session

- **期望**：`wake_window`、`session_id`、超时、打断/取消、多轮共享会话状态。  
- **当前盘点**（见 `voice_session_readiness_matrix.json`）：`voice_wake_window_manager.py`、`voice_input_session_manager.py`、`voice_v1_session_state_anchor.py`、`voice_segment_timeout_policy.py` 等模块存在；**与主链端到端 GO 仍分离**。
