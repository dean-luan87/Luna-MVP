# LUNA Voice — ASR Runtime Flag & Kill Switch Plan v0

## 环境变量（建议名）

| Flag | 默认 | 含义 |
|------|------|------|
| `LUNA_DISABLE_VOICE_ASR_RUNTIME_V1` | **true** | **全局禁用最高优先级**：为 **true** 时不得调用任何 ASR provider、不得派发 final_text |
| `LUNA_ENABLE_VOICE_ASR_SHADOW_V1` | **false** | 仅 shadow/trace 路径，不调用真实 provider |
| `LUNA_ENABLE_VOICE_ASR_PROVIDER_V1` | **false** | 真实 provider 调用（另开授权 phase） |
| `LUNA_ENABLE_VOICE_ASR_FINAL_TEXT_DISPATCH_V1` | **false** | 向主链派发 `final_text`（另开授权 phase） |

**默认全部关闭（保守）**：总开关禁用 + 三项 ENABLE 均为 false；与 Readiness-002「不接真实 ASR」一致。Wiring phase 再冻结 unset 的解析规则（未设置 env 时是否等同默认值）。

##  rollout 顺序（建议）

1. 可开 **shadow**（`LUNA_ENABLE_VOICE_ASR_SHADOW_V1`）。  
2. **final_text dispatch** 独立开关。  
3. **provider 真实调用** 最后打开。  
4. **global disable** 任意时刻可切断。
