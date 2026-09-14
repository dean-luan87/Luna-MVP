## Phase-VoiceTTS-SpeedControl-Closure-001

Runtime TTS Speed Control Policy & Provider Mapping v0

### 目标

把“语速控制”收口为 **Voice runtime control** 的一部分（TTS runtime 参数），而不是导航语义、任务链、模型决策的一部分；并为后续白盒排查提供可审计的 metadata。

### 硬边界（必须成立）

- **语速控制 = 白名单短指令**（如“语速慢一点/快一点/语速0.25/0.5/0.75/1.0”）
- **作用范围 = TTS runtime 参数**（运行态内存；不落盘）
- **不改变 message text**（语速控制不改既有播报文本内容）
- **不改变导航决策**
- **不改变 Output candidate**（不引入新的导航/任务/输出候选）
- **不写入长期记忆**
- **不扩大 side effects**

### 运行态规格（v0 冻结）

- **默认档位**：0.75
- **范围**：0.25–1.0
- **步进**：0.25（档位化/离散化）
- **保存方式**：进程内内存（runtime-only）
- **触发方式**：仅白名单短指令

### Provider-specific mapping（必须）

将统一档位 `tts_runtime_speed` 映射到各 provider 参数（尽量继承）：

- **Qwen**：`qwen.speed = tts_runtime_speed`
- **Piper**：`piper.length_scale = f(tts_runtime_speed)`（length_scale 越大越慢；映射需保守，避免极端失真）
- **macOS say fallback**：`say -r rate = g(tts_runtime_speed)`（以当前 Voice 默认 rate=180 为基线映射）

### fallback 继承（必须）

- 当 Qwen 失败 fallback 到 Piper / macOS say 时，**语速档位仍应继承**并通过对应 mapping 生效。

### 白盒 / metadata（必须记录）

每次 TTS 输出至少记录（在 cutover/rollback observation metadata 中）：

- `tts_runtime_speed`
- `speed_control_source`
- `speed_control_applied`
- `provider_selected`
- `provider_speed_param`
- `fallback_used`

### 验证（smoke）

短指令 smoke（只验证白名单 + runtime 控制）：

```bash
cd "/Users/luanlei/Desktop/Luna-Core"
python3 tools/smoke_voice_tts_speed_control_command_v0.py --text "语速慢一点"
python3 tools/smoke_voice_tts_speed_control_command_v0.py --text "语速0.25"
python3 tools/smoke_voice_tts_speed_control_command_v0.py --text "语速快一点"
```

provider mapping dry-run smoke（只验证映射与继承预期，不做在线合成）：

```bash
cd "/Users/luanlei/Desktop/Luna-Core"
python3 tools/smoke_tts_speed_provider_mapping_v0.py --speed 0.25
python3 tools/smoke_tts_speed_provider_mapping_v0.py --speed 0.75
python3 tools/smoke_tts_speed_provider_mapping_v0.py --speed 1.0
```

