# LUNA Voice Prefilter Routing M3.5 Phase Closeout（灰度维持态封板）

## 阶段范围

M3.5.1 ～ M3.5.7a-2（含主线扩灰、mixed 边界专项、model_chain 归因补证、稳定性观察与 C7/night 定点观察）。

覆盖的主要文档/附录：

- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_1_GRAY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_2_GRAY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_3_GRAY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_4_GRAY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_4a_GRAY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_4b_GRAY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_5_GRAY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_6_GRAY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_6A_MODEL_CHAIN_AUDIT.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_6B_MODEL_CHAIN_PROOF.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_7_STABILITY_APPENDIX.md`
- `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_7A_C7_NIGHT_AUDIT.md`

## 核心结论（封板）

**M3.5 阶段已完成封板：当前显式开关灰度能力可维持，但默认不启用；当前不建议继续扩大灰度范围；后续推进应进入“准入切换准备”阶段，而非继续实验扩灰。**

## 当前稳定结论（对外口径）

- **分档骨架成立**：在不改变默认主链的前提下，已形成可回退的 prefilter 分档路由骨架（simple→turbo / complex→plus / rule_or_reject→规则链）。
- **显式开关灰度成立**：通过 `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1` 在进程/灰度口径内开启，不开时默认主链行为不变。
- **多轮扩灰整体稳定**：主线在较大样本量下保持硬指标可观测、可控（以各轮附录/跑批产物为准）。
- **mixed 单点问题已处理**：M3.5.4a/4b → M3.5.5 主线恢复后，mixed 边界未出现稳定复发（以 5.5 附录为准）。
- **M3.5.6 非绿未坐实为系统性问题**：
  - 扩灰后出现过少量 model routes 非绿（集中 day），但后续补证与 repro 未稳定复现；
  - 因此不在当前阶段推进“修 detection / 修 provider”。
- **C7/night 波动不构成稳定缺陷**：在 M3.5.7 与后续 5.7a 定点观察中，C7/night 未表现为必现 bug；更符合低频偶发 + 统计口径脆弱的组合风险（需在复发时再定点归因）。

### 最新观测窗口摘要（M3.5.7）

- **本轮结论**：当前灰度范围可维持，但需继续观察。
- **关键事实**：
  - M3.5.6 型 model_chain 非绿未复发（model routes 上 `used_model_chain=false` / day 段非绿未再现）。
  - aggregate 硬指标继续健康（model routes：`json_rate=1.0`、`val_rate=1.0`、`fallback_rate=0.0`）。
  - `C7_mixed_sleep_park_nav` 在 night 段出现低频 mixed 波动（本轮结论维持“可维持，不扩灰”）。
- **引用产物**：
  - `logs/benchmark_prefilter_routing_m3_5_7_20260407T044056Z.json`
  - （可选观察）`logs/observe_c7_mixed_night_m3_5_7a_20260407T064445Z.json`（C7/night 30 轮未再捕获 mixed 掉档）
- **边界说明**：该摘要仅用于说明封板时的最近观测状态，不改变本文件“默认不开启、当前不建议继续扩大、骨架冻结”的阶段结论。

## 当前边界（写死）

### 1) 默认不开启

- **默认主链不变**：不开 `LUNA_VOICE_ENABLE_PREFILTER_ROUTING` 时行为与历史一致。
- **显式开关**：仅允许在灰度/跑批/专项进程中显式开启。

### 2) 当前不建议继续扩大

当前阶段定位为“灰度维持态”，不再推动更大规模扩灰；若后续要推进，必须走准入/切换准备（见下文）。

### 3) 骨架冻结（本阶段不再改）

冻结项（不再继续改动/对齐）：

- `prefilter_v0` 规则（`capabilities/voice/bridge/voice_long_input_prefilter_v0.py`）
- prompt
- schema / validator / builder / fallback 语义
- 不切 `qwen3.6-plus`、不接 DeepSeek / 豆包（进入准入阶段后再统一接入）

## 不再继续做的事项（本阶段明确停止）

- 不继续扩大显式开关灰度范围（不再以“更大规模 benchmark”作为主线目标）
- 不在缺乏稳定复现的前提下推进 detection/provider 逻辑修复
- 不引入新模型、新 prompt、新规则变量来“掩盖”现象

## 保留能力清单（工程能力化）

### A. 正式保留（长期能力）

- **显式开关**：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`
- **超时配置**：`LUNA_QWEN_MODEL_TIMEOUT_MS=120000`（灰度口径）
- **路由骨架**：prefilter 路由建议 + dispatcher 选择单模型 provider / rule_only
- **provider 能力**：qwen 单模型 provider；主备 bundle（保留诊断字段）
- **基准脚本**（主线）：`tools/benchmark_prefilter_routing_m3_5_*.py`（用于回归/对照/稳定性观察）

### B. 仅作为应急审计工具保留（默认关闭）

- **专项开关**：`LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1`（默认关闭；仅复发时启用）
- **专项脚本**：
  - `tools/audit_model_chain_failures_m3_5_6a.py`
  - `tools/repro_model_chain_failures_m3_5_6b.py`
  - `tools/observe_c7_mixed_night_m3_5_7a.py`
- **专项文档**：
  - `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_6A_MODEL_CHAIN_AUDIT.md`
  - `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_6B_MODEL_CHAIN_PROOF.md`
  - `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_7A_C7_NIGHT_AUDIT.md`

## 准入/切换准备（最小清单）

本阶段只做“准备说明”，不做产品化/后台实现。

后续若要把显式开关灰度能力长期留在产品后台，至少需要：

### 1) 开关配置入口

- 开关语义：**非默认开启**，仅人工/灰度开启
- 开关范围：按环境/租户/用户分群（待准入系统定义）
- 默认值：关闭

### 2) 指标看板字段（运行态可观测）

建议最小字段集合（与 M3.5 产物对齐）：

- `json_rate_model_routes` / `val_rate_model_routes` / `fallback_rate_model_routes`
- `mixed_preserve_rate`
- `avg_e2e_ms` / `p95_e2e_ms`
- `route_counts` / `rule_or_reject_ratio`
- `timeout_hint_count`
- `pause_stop_expand_gray`
- `selected_provider_model_id_counts`

### 3) 暂停条件（闸门）

建议保留现有 pause_check 口径作为准入闸门基线：

- `val_rate < 1.0` 或 `fallback_rate > 0.0` → 暂停推进
- `mixed_preserve_rate < 阈值`（例如 0.95）→ 暂停推进
- `rule_or_reject_ratio` 异常抬升 → 暂停推进
- `timeout_hint_count` 异常上升 → 暂停推进

### 4) 回退条件（必须自动回退的触发）

- 连续窗口内出现硬指标非绿（按准入系统定义窗口）
- 明确出现系统性错误/超时/不可恢复失败

### 5) 运行态说明（SOP）

- 什么时候允许人工开启（准入通过后）
- 触发 pause/回退后如何处置（收集产物 → 启用应急审计 → 定点归因）
- 如何复现（复用 M3.5 工具链，而非临时脚本）

### 6) 与“模型评测与准入中心”的衔接

建议以“准入中心”作为唯一入口来做：

- 模型/版本准入（替代当前 ad-hoc 扩灰）
- 指标口径统一（复用 M3.5 指标字段）
- 开关审批/权限/审计
- 回退策略自动化（与 pause/回退条件对齐）

## 最终结论（对外一句话）

**M3.5 阶段已完成封板，当前显式开关灰度能力可维持但默认不启用；后续若需推进，进入“准入切换准备”阶段，而非继续实验扩灰。**

