# LUNA TTS Qwen Preferred Fallback Test Matrix v0

## Phase

- Phase-VoiceTTS-RuntimeMode-001

## Verifier

- `tools/verify_tts_runtime_mode_qwen_preferred_v0.py`

## Matrix（A–L）

- **A** offline_only 时 qwen 不会被调用（过滤/不进入 effective）
- **B** online_prefer_qwen 时 qwen 在 effective_order 第一位
- **C** qwen 缺 API key 时 fallback（piper 或 legacy）
- **D** qwen timeout > 2000ms 时 fallback（通过 hard_timeout 配置与 timeouts 生效）
- **E** qwen provider_success 时不 fallback（在线条件下验证；离线 verifier 不强制）
- **F** piper 保留
- **G** macOS say fallback 保留
- **H** main.py 仍走 unified entry
- **I** qwen 不生成播报文本
- **J** qwen 不绕过 Speech Gate / unified entry
- **K** online_prefer_qwen 不删除 offline_only baseline
- **L** runtime metadata 记录 mode/effective_order/filtered_out/latency policy

