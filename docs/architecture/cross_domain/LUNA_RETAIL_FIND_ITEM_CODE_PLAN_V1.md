# retail_find_item_v1：最小代码实现计划（V1）

## 1. 第一版代码目标

### 第一版要实现什么（写死）

在《`docs/architecture/cross_domain/LUNA_RETAIL_FIND_ITEM_MIN_IMPLEMENTATION_V1.md`》的闭环定义上，第一版代码只落成：

1. 接收最小输入（零售环境候选 + 找货意图 + 风险摘要 + 时间戳）
2. 产出最小 `scene_type=retail_shelf`（或等价）级别判断，并给出 `gating_passed`
3. 在 gating 通过且存在找货意图时，给出 **OCR 触发决策**（仅决策与边界，不做复杂 OCR 主导链）
4. 在“可补证”时接入 OCR 摘要输入（V1 允许占位/模拟），产出一条最小结论候选
5. 任务链小步更新建议（只给结构化字段，不做复杂任务系统）
6. 完整白盒留痕（可回放、可对账）
7. 默认关闭、可 whitebox-only、可完全回退，且 **安全链优先** 可压制零售链外显

### 第一版不实现什么（写死）

- 不做复杂找货规划（跨区、最短路径、货架拓扑）
- 不做比价/支付/促销/会员
- 不做长文本 OCR 常驻扫描（OCR 不得成为默认主导链）
- 不做购物车逻辑、多商品并行优化
- 不做复杂多模融合/多候选投票
- 不改主链默认逻辑、不新增视觉模型

### 为什么这样切

- 先把「零售环境 gating → 条件触发补证 → 语义/任务链小步更新 → 输出裁决可控噪」的工程闭环落地
- 与前两条旁路保持同一方法论：默认关闭、可白盒、可独立验证、可边缘集成验证

---

## 2. 建议代码落点（不绑死主链）

### 2.1 模块目录与入口

- **建议新增**：`capabilities/cross_domain/retail_find_item_v1/`
- **主入口建议**：`evaluate_retail_find_item_v1(...)`
  - 输入：环境候选、找货意图摘要、风险摘要、OCR 摘要（可选）、时间戳、`risk_interrupt_preempt`（可选）
  - 输出：本轮 `scene_type` / `gating_passed` / `ocr_triggered` / `final_spoken_output` 候选 + `metadata["retail_find_item_v1"]`

### 2.2 零售环境初判入口在哪

- **建议**：`retail_find_item_v1` 内部提供 `_classify_retail_scene(...)`（规则占位/轻量判别），输出：
  - `current_scene_type`（至少 `retail_shelf` / `unknown`）
  - `retail_context_confidence`（0~1）
  - `gating_passed`（布尔）

### 2.3 gating 判断落在哪

- **建议**：与环境初判同层输出，作为后续一切 OCR/补证触发的硬门槛：
  - `gating_passed == false` → 本轮只留白盒，不触发补证、不产外显结论

### 2.4 OCR 触发条件如何接入（只保留接口与边界）

V1 的“触发”分两段，避免 OCR 变主导链：

1. **触发决策**（本模块内做）：给出 `ocr_triggered` 与 `ocr_trigger_reason`（结构化枚举/短串）
2. **OCR 执行**（本模块外做）：由上层或独立 OCR 组件根据 `ocr_triggered` 决定是否真正跑 OCR，再把 `ocr_summary` 回填到本模块（或下一轮输入）

最小触发条件（写死口径）：

- `gating_passed == true`
- `active_find_item_intent == true`
- 且满足任一：
  - `user_requested_reading == true`
  - `need_text_to_progress == true`
- 频控：`ocr_budget_ok == true`（V1 可用简单计数/冷却占位）

### 2.5 语义整理与任务链小步更新落在哪

- **建议**：仍放在 `retail_find_item_v1` 内部做最小整形：
  - 语义整理：把 OCR 摘要 + 目标商品词 合成 `item_match_summary` 与一句 `final_spoken_output` 候选
  - 任务链小步更新：只产出 `task_step_updated` 与 `task_evidence`（结构化 dict），由上层任务系统选择是否采纳

### 2.6 白盒记录落在哪

- **建议**：统一写入 `metadata["retail_find_item_v1"]`，与 `risk_interrupt_v1` / `sidewalk_nav_v1` 并列键

---

## 3. 最小状态字段（第一版需要）

至少定义并在结果中体现：

- `current_scene_type`
- `gating_passed`
- `active_find_item_intent`
- `ocr_triggered`
- `item_match_status`
- `task_step_updated`

说明（V1 最小口径建议）：

- `item_match_status`：`unknown | no_match | weak_match | maybe_found`（V1 不追求 SKU 精确）
- `task_step_updated`：布尔；V1 仅表示“是否生成了可供上层采纳的小步更新建议”

---

## 4. 最小白盒字段（第一版必须）

`metadata["retail_find_item_v1"]` 至少包含：

- `scene_summary`
- `gating_result`
- `ocr_trigger_reason`
- `ocr_summary`
- `item_match_summary`
- `task_evidence`
- `final_spoken_output`
- `event_timestamp`

字段口径建议：

- `scene_summary`：输入候选 + 归一化后的 `scene_type`、置信度
- `gating_result`：`passed`、`confidence`、`reasons[]`（可空）
- `ocr_summary`：V1 允许为空 dict；一旦存在至少含 `text_digest`、`confidence`、`roi_hint`
- `task_evidence`：V1 最小含 `intent_query`、`ocr_text_digest`、`timestamp`

---

## 5. 最小执行顺序（文字版）

1. 环境初判
2. gating 判断
3. 若未通过 → 只留白盒（记录 scene/gating），`final_spoken_output` 为空
4. 若通过且存在找货意图 → 计算 OCR 触发决策（仅决策）
5. 若 OCR 摘要可用（本轮或回填）→ 语义整理短句结果，计算 `item_match_status`
6. 生成任务链小步更新建议（结构化 `task_evidence`）
7. 输出裁决决定是否播报一句结论（受 whitebox-only 与风险压制约束）
8. 写白盒

---

## 6. 触发边界（写死）

### 6.1 OCR 不得主导

- 未通过 `gating_passed`：不得触发 OCR
- 无找货意图：不得触发 OCR
- 未满足触发条件：不得触发 OCR（即使在零售场景）

### 6.2 安全链优先

本旁路的外显输出应被以下任一条件压制：

- 风险摘要 `risk_level in {high, critical}`
- 或上层已判定 `risk_interrupt_v1` 抢占：传入 `risk_interrupt_preempt=True`

压制时：

- `final_spoken_output` 必须为空或被标记 suppressed
- 仍可写白盒（便于对账）

---

## 7. 开关与回退方式（V1 先定义语义）

建议最小开关（与前两条旁路一致风格）：

- `LUNA_ENABLE_RETAIL_FIND_ITEM_V1=0`（默认关闭）
- `LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY=1`（默认只白盒）

行为要求：

- 默认关闭：不执行或不挂载 `metadata["retail_find_item_v1"]`，零侵入
- 开启 + whitebox-only：写白盒、可产 `ocr_triggered` 决策，但 `final_spoken_output` 为空
- 开启 + 非白盒：允许在未被风险压制时播报一句最小结论

回退边界：

1. 异常/噪声：先切回 `WHITEBOX_ONLY=1`
2. 仍有问题：`ENABLE=0` 完全关闭，不影响主链

---

## 8. 验证入口（实现后怎么测）

建议新增脚本（实现阶段落地）：`tools/test_retail_find_item_v1.py`

最小用例矩阵：

- 非零售环境 → `gating_passed=false`，不触发 OCR，只留白盒（开启时）
- 零售环境但无找货意图 → 不触发 OCR，只留上下文/白盒
- 零售环境 + 找货意图 + 触发条件成立 → `ocr_triggered=true`；若有 OCR 摘要则产最小结论
- 风险存在或 `risk_interrupt_preempt=true` → 外显被压制，白盒仍完整
- 默认关闭 → 不挂载 `metadata["retail_find_item_v1"]`

建议边缘集成验证脚本（实现阶段落地）：`tools/test_retail_find_item_v1_integration.py`，口径与 `risk_interrupt_v1`、`sidewalk_nav_v1` 一致：用主链式 metadata dict 合并白盒并断言零侵入。

---

## 9. 当前阶段不做项（再次写死）

- 不做复杂找货规划
- 不做比价/支付/促销
- 不做长文本 OCR
- 不做购物车逻辑
- 不做复杂多模融合

---

## 一句话收束

先把 `retail_find_item_v1` 的**代码落点、最小状态、白盒字段、OCR 触发边界、验证入口与回退方式**写清楚，再进入后续最小代码实现阶段；并保持“默认关闭、可白盒、可被安全链压制”的旁路工程基线。

