# LUNA Qwen TTS Provider Test Matrix v0

## Phase

- Phase-VoiceTTS-Provider-001

## Verifier

- `tools/verify_qwen_tts_provider_integration_v0.py`

## Matrix (A–J)

| ID | Requirement | How verified | Pass criteria |
|---|---|---|---|
| A | qwen provider 可 import | verifier import `capabilities.voice.providers.qwen_tts_provider` | pass |
| B | unified entry 可 import 且包含 provider 接入点 | verifier import `run_tts_unified_entry` | pass |
| C | config enabled=false 不会阻塞且回退 legacy | verifier 用 cfg_disabled + legacy_submit stub 统计调用次数 | legacy_called>=1 |
| D | provider_order=qwen first 会尝试 qwen（v0 用“触发失败+回退”证明路径存在） | verifier 用 cfg_enabled_first（缺 key/依赖也可） | legacy_called>=1 且 final_execution_mode 可终态 |
| E | qwen 失败时 fallback 生效 | 同 D | pass |
| F | provider result 符合统一结构 | 由 unified entry + provider runtime 类型约束 | pass |
| G | 不生成播报文本，仅消费输入文本 | verifier 仅传入固定 text，未调用任何生成链 | pass |
| H | 不绕过 unified entry | verifier 只调用 unified entry | pass |
| I | main.py 仍走 `_submit_tts_via_unified_entry()` | 人工检查（本阶段不改 main.py 逻辑） | pass |
| J | legacy fallback 仍可用 | verifier legacy_submit stub 可被调用 | pass |

