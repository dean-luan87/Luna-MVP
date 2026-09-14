# LUNA Voice Prefilter Routing M3.5.7a C7/night Audit（定点观察 + 最小代码溯源）

## 背景

在 M3.5.7 稳定性观察中，主链硬指标（model routes 的 `json_rate/val_rate/fallback_rate`）保持全绿，但出现了：

- `C7_mixed_sleep_park_nav` 在 **night 段**发生 mixed 关键词保留掉档（`mixed_failure_count > 0`）
- 其他 case 基本稳定

该形态既可能来自 **模型输出随机性/波动**，也可能来自 **代码链路（清洗/提取/匹配/统计口径）对 C7 不够稳**。

本轮目标是在不扩灰、不改骨架、不做修复的前提下，把问题先归到两类之一：模型随机性 vs 代码链路/口径问题。

## 本轮原则（冻结项）

1. 不扩灰
2. 不改 prefilter 规则
3. 不改 prompt
4. 不改 schema / validator / builder / fallback
5. 不切模型
6. 只做观察与溯源，不做修复

## 执行任务 A：C7/night 定点观察

### 脚本

- `tools/observe_c7_mixed_night_m3_5_7a.py`

运行示例：

```bash
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY=...
export LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1
export LUNA_QWEN_MODEL_TIMEOUT_MS=120000

python3 tools/observe_c7_mixed_night_m3_5_7a.py --rounds 25 --time-slot all
```

产物：

- `logs/observe_c7_mixed_night_m3_5_7a_<UTC>.json`
- `logs/observe_c7_mixed_night_m3_5_7a_<UTC>.md`

### 需要关注的输出字段（每条样本）

- `slot` / `round`
- `mixed_preserved` / `missing_keywords`
- `selected_provider_model_id` / `routing_suggestion`
- `cleaned_text`
- `non_task_payload_exists`
- `non_task_payload_summary` / `non_task_segments`
- `e2e_ms`

目标：确认 C7 的 mixed 掉档是否 **night 更容易复发**，以及复发频率大概是多少。

## 执行任务 B：最小代码溯源（不做修复）

只围绕 C7/night 检查以下链路：

### 1) cleaned_text 生成链

- 入口：`capabilities/voice/bridge/voice_long_input_prefilter_v0.py`
  - `prefilter_long_voice_text_v0()` 使用 `_clean_conservative()` 进行 **极保守清洗**（仅剔除口头禅/停顿词）
- C7 原始文本：
  - `最近睡眠不太好，想去公园走走散心，帮我导航到附近适合散步的城市公园。`
- 预期：清洗不应删除 “睡眠” 等 mixed 词。

**需要核对：**原始文本与 `cleaned_text` 是否有差异、是否删掉了 mixed 关键词。

### 2) non_task_payload 生成链

- 模型链收口：`capabilities/voice/bridge/voice_long_input_structured_to_parse_result.py`
  - `structured_to_voice_long_input_parse_result()` 会把 structured 的 `non_task_payload` 映射到 `VoiceLongInputParseResult.non_task_payload`

**需要核对：**失败时是 `non_task_payload` 整体缺失（exists=false/None），还是 segments 存在但内容缺少“睡眠”等表达。

### 3) mixed 关键词匹配链（统计口径）

在 benchmark/观测脚本里，mixed 保留的口径是：

- 从 `VoiceLongInputParseResult.non_task_payload.segments[].content` 拼接成 `blob`
- `mixed_preserved = any(keyword in blob for keyword in mixed_keywords)`（当前 C7 的 `mixed_keywords = ["睡眠"]`）

该口径的脆弱点（潜在“代码口径问题”方向）：

- 仅做 **子串命中**，不覆盖同义改写（如 “没睡好/困/想睡/睡不着”）
- 若模型把睡眠表达写进 task 相关字段而非 non_task_payload，会被统计为失败
- 若 segments 内容包含标点/空格/换写法，可能导致单词形态不一致而未命中

### 4) mixed_preserve_rate 的统计口径

`mixed_preserve_rate` 只对 `mixed_preserved is not None` 的样本统计；C7 为 mixed case，因此每轮都纳入统计。

### 5) day / night 是否存在输入差异

脚本层面 `day/night` 目前仅作为 **标签**（request_id/session_id 的差异），没有额外参数差异。

因此若出现 night 更容易掉档，优先从：

- 模型随机性/输出波动
- 或 night 批次运行环境差异（并发、网络、服务侧）  

两方向解释，而不是脚本直接改写输入。

## 结论填写区（执行后补齐）

请只回答三个问题：

1. **C7/night 的 mixed 波动是否可稳定复现？**
2. **失败时是 non_task_payload 整体缺失，还是仅关键词 “睡眠” 没命中？**
3. **当前更像模型随机性，还是代码链路/统计口径问题？**

结论判别框架：

- **更像代码问题**：non_task_payload 里其实有睡眠相关表达，但 `missing_keywords` 仍显示未命中；或清洗/拼接/口径导致漏判；或 day/night 仅标签不同但统计结果被不同口径算出差异。
- **更像模型随机性**：同样输入/同样 cleaned_text，模型有时在 non_task_payload 写出“睡眠”，有时完全不写或改写成同义词（被子串口径漏判）。

