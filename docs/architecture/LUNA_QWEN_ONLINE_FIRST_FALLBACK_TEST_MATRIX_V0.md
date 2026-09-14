# LUNA Qwen Online-First Fallback Test Matrix v0

## Phase

- Phase-VoiceTTS-Policy-002

## Verifier

- `tools/verify_qwen_online_first_fallback_policy_v0.py`

## Matrix（A–L）

- **A** offline_only=true 时 qwen 不会被调用
- **B** online_runtime.enabled=false 时 qwen 不会被调用
- **C** online_runtime.enabled=true 时优先尝试 qwen
- **D** qwen 成功且耗时 <800ms 时不 fallback（在线环境验证）
- **E** qwen 超过 2000ms 时 fallback 到 Piper（线程硬超时 + 结构化 timeout）
- **F** qwen 抛异常时 fallback 到 Piper
- **G** qwen 缺 API key 时 fallback 到 Piper/legacy
- **H** 连续 3 次失败后 circuit_open，后续直接 Piper（运行态验证）
- **I** half_open probe 成功后 circuit_closed（运行态验证）
- **J** Qwen 不生成文本，只消费输入文本
- **K** main.py 仍走 unified entry
- **L** Piper/macOS say fallback 保留

