# LUNA Voice：新模型接入标准流程（V1）

## 1. 目标与范围

目标：在**不改主链宪法**（不改 prefilter/prompt/schema/validator/builder/fallback 语义，不默认开启灰度，不把实验直接打进默认态）的前提下，让任何新模型都能快速完成：

- 接入准备 → 契约对齐 → 基础测试 → 显式开关灰度 → 结论归档 → 回退机制

适用范围：

- 云端模型 / 本地模型
- 作为：**主选候选 / 备选候选 / 观察池**
- 放置位置（至少覆盖）：
  - 主执行链（长语音模型链）
  - 前置裁剪层/路由层（prefilter 相关能力）
  - 草稿链/对照链（仅用于跑批/对照，不进默认）
  - 中台/大脑候选（若未来存在统一入口，也应复用本 SOP 的契约与闸门）

前置依赖：

- 运行态与开关总表：`docs/architecture/voice/LUNA_VOICE_RUNTIME_MODES_AND_SWITCHES_V1.md`
- 默认运行基线：`docs/architecture/voice/LUNA_VOICE_RUNTIME_DEFAULT_BASELINE_V1.md`
- M3.5 封板：`docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_PHASE_CLOSEOUT.md`

## 2. 接入前分类（必须先回答）

在开始写任何代码/配置之前，先把模型按以下维度归类（写进接入 PR/文档开头）：

### 2.1 模型来源

- [ ] 云端（API 调用） / 本地（推理服务/SDK）
- [ ] 供应商/区域/endpoint（如有）
- [ ] 账号/鉴权是否可用（仅说明是否具备，不在此文档落密钥）

### 2.2 接入角色

- [ ] 主选候选（目标是进入默认主线）
- [ ] 备选候选（目标是作为主备/回退候选）
- [ ] 观察池（仅用于离线/跑批评估，不进入线上默认路径）

### 2.3 放置位置（影响面）

- [ ] 主执行链（长语音模型链）
- [ ] 前置裁剪/路由（prefilter/分档）
- [ ] 对照链（仅 benchmark/smoke/repro）

结论要求：

- [ ] 是否会影响默认主链？（默认必须 **否**；若是，必须走更高等级评审与回退预案）

## 3. 契约对齐清单（先对齐“能吃”，再谈“好不好”）

目标：保证新模型不会污染主链语义，且能稳定走通结构化产物。

### 3.1 结构化输出契约

- [ ] schema：能否按既有结构化 schema 输出（字段齐全/类型一致）
- [ ] validator：能否通过 validator（失败类型需可解释）
- [ ] builder：builder 能否消费（不因新模型输出形态变化导致 builder 行为漂移）
- [ ] fallback 语义：新模型失败时的回退路径与语义是否保持一致（不改变“失败定义”）

### 3.2 parse bridge / unwrap / enrich

- [ ] provider 返回体可稳定解析（unwrap 不依赖偶发文本形态）
- [ ] enrich/adapter 不引入新字段语义（仅补齐系统字段/白名单清洗）
- [ ] notes/metadata 的关键口径可观测（便于后续灰度与审计）

### 3.3 禁止项（契约阶段不得做）

- [ ] 不改 schema/validator/builder/fallback 的定义来“迎合某模型”
- [ ] 不引入新功能字段作为接入前置条件

## 4. 基础测试清单（统一口径）

目标：用统一脚本/口径快速回答“能不能跑、稳不稳、哪里风险”。

### 4.1 必跑测试（最小集合）

- [ ] smoke（最小冒烟）
- [ ] benchmark（固定 case 集，多轮）
- [ ] mixed（C1/C7 等边界）
- [ ] unsupported（R* 等拒答/规则链）
- [ ] 多步骤（itinerary/multi-step）
- [ ] 分时段（day/night）
- [ ] 主备（若作为主备候选/或影响主备）
- [ ] 灰度开关验证（确认不开开关时默认行为不变）

### 4.2 指标口径（建议对齐 M3.5）

- 硬指标：`json_rate_model_routes` / `val_rate_model_routes` / `fallback_rate_model_routes` / `mixed_preserve_rate`
- 运营指标：`avg_e2e_ms` / `p95_e2e_ms` / `rule_or_reject_ratio` / `timeout_hint_count` / `pause_stop_expand_gray`

## 5. 灰度流程（显式开关、非默认）

目标：任何新模型都必须先进入显式开关灰度，而不是直接替换默认主链。

### 5.1 灰度规则（写死）

- [ ] 先显式开关（默认关闭）
- [ ] 不直接替换主链默认态
- [ ] 小范围灰度 → 再逐步扩大（若阶段允许）
- [ ] 必须有停止条件与回退条件

### 5.2 扩灰条件 / 停止条件（闸门）

建议最小闸门（与既有口径对齐）：

- [ ] `json_rate_model_routes == 1.0`
- [ ] `val_rate_model_routes == 1.0`
- [ ] `fallback_rate_model_routes == 0.0`
- [ ] `mixed_preserve_rate` 不得退化（阈值由阶段定义）
- [ ] `timeout_hint_count` 不得异常上升
- [ ] `rule_or_reject_ratio` 不得异常偏高
- [ ] `pause_stop_expand_gray == false`

## 6. 结论分级（必须归档）

每个模型接入必须输出一个明确结论（只选一类）：

- [ ] 可进入主链评审
- [ ] 可作为备选
- [ ] 可进入观察池
- [ ] 不建议接入
- [ ] 需补契约适配（未满足 schema/validator/builder/fallback 基线）

归档要求（最小）：

- [ ] 指标摘要（硬指标 + p95 + rule_or_reject + timeout）
- [ ] 风险点与复现方式（若有）
- [ ] 对应日志/产物文件名（JSON/MD）

## 7. 回退机制（出问题怎么关、回到哪）

### 7.1 什么时候必须回退

- [ ] 出现硬指标非绿（按窗口与阈值定义）
- [ ] 出现系统性超时/异常导致服务不可用
- [ ] 出现不可恢复的结构化解析失败

### 7.2 回退到谁/回到哪个运行态

- [ ] 回退到默认态（不开 prefilter）
- [ ] 回退到上一个已准入模型（主/备）
- [ ] 回退到规则链（rule_only）作为兜底（按当前配置）

### 7.3 需要保留哪些日志

- [ ] 本轮 benchmark/smoke 的 JSON 产物
- [ ] 失败样本明细（rows 级别）
- [ ] 若复发且需要定位：启用审计开关后产生的关键字段（见下）

### 7.4 哪些 debug 开关何时可启用

- [ ] `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1`：仅在复发定位时启用；默认关闭；不作为长期主链字段依赖

## 8. 与“模型评测与准入中心”的关系

本 SOP 是未来“模型评测与准入中心”的上游流程基线：

- 测试结果、失败记录、调试过程应可被中心统一收录
- 准入/回退闸门应以本 SOP 的指标口径为基线统一
- 任何模型替换应在“运行态框架 + 基线默认态”内完成，而非临时改主链

## 9. 主线当前基线声明（V1）

- 当前默认态基线见：`docs/architecture/voice/LUNA_VOICE_RUNTIME_DEFAULT_BASELINE_V1.md`
- 当前在役主线基线模型口径：**qwen-plus 仍为复杂档主选口径（在灰度/分档中）**；新模型（如 qwen3.6-plus / DeepSeek / 豆包）应作为候选按本 SOP 进入系统。

---

## 附录 A：接入 PR 模板（可直接复制）

将以下内容粘到 PR 描述中，按需删减（但不要改变口径顺序）：

### 背景与目标

- 目标模型：`<provider/model/version>`
- 接入角色：主选候选 / 备选候选 / 观察池（单选）
- 放置位置：主执行链 / 路由层 / 对照链（可多选）
- 是否影响默认主链：是 / 否（默认必须否）

### 契约对齐（必填）

- schema：通过/不通过（说明差异点）
- validator：通过/不通过（失败类型与样例）
- builder：通过/不通过（是否出现行为漂移）
- fallback 语义：保持/有变化（必须说明原因）

### 测试与产物（必填）

- 跑了哪些：smoke / benchmark / mixed / unsupported / 多步骤 / 分时段 / 主备 / 灰度开关验证
- 产物路径（贴文件名即可）：
  - `logs/<...>.json`
  - `logs/<...>.md`

### 指标摘要（必填，写结论用）

- json_rate / val_rate / fallback_rate / mixed_preserve_rate：
- avg_ms / p95_ms：
- rule_or_reject_ratio / timeout_hint_count：
- pause_stop_expand_gray：

### 结论分级（单选）

- 可进入主链评审 / 可作为备选 / 可进入观察池 / 不建议接入 / 需补契约适配

### 回退预案（必填）

- 触发条件（硬指标/系统性错误）：
- 回退到谁/回到哪个运行态（默认态/上一个准入模型/规则链兜底）：
- 需要保留的日志与是否需要启用审计开关：

## 附录 B：产物命名规范（V1）

目的：让任何一次接入/评估的产物都可被检索、可对照、可复现。

建议统一格式（JSON 与 MD 同名）：

- `logs/<category>_<model_tag>_<phase_tag>_<UTC>.json`
- `logs/<category>_<model_tag>_<phase_tag>_<UTC>.md`

字段建议：

- `<category>`：`smoke` / `benchmark` / `audit` / `repro` / `observe`
- `<model_tag>`：如 `qwen_plus` / `qwen_3_6_plus` / `deepseek_v3` / `doubao_xxx`
- `<phase_tag>`：如 `onboarding_v1` / `contract` / `gray` / `regression`
- `<UTC>`：如 `20260407T044056Z`

最低要求：

- 同一次跑批必须同时保留 JSON 与 MD（或至少 JSON + 明确的读取方式）
- 每个产物必须能追溯：git_head、开关/env、case 集、轮数、时段

## 附录 C：结论归档模板（V1）

用于把一次接入结果“收成结论”，避免变成实验流水账：

### 结论（单句）

`<模型/版本>`：<结论分级单选>；原因一句话说明。

### 关键证据（最多 5 条）

- 证据 1：
- 证据 2：
- 证据 3：
- 证据 4：
- 证据 5：

### 风险与边界

- 默认是否启用：否（除非明确进入主链评审并通过）
- 必须暂停/回退条件：
- 是否需要保留/启用审计态：

### 产物引用

- `logs/<...>.json`
- `logs/<...>.md`

