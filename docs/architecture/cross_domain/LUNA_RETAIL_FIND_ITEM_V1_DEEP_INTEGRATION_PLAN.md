# retail_find_item_v1：主线深接入方案（V1）

## 1. 目标

`retail_find_item_v1` 已完成：最小代码落地、模块验证、主线边缘集成验证，且跨域旁路的统一 `context/metadata` 规范已形成（见《`LUNA_CROSS_DOMAIN_CONTEXT_METADATA_CONVENTION_V1.md`》）。  
本方案回答：当要把它推进到“主线深接入准备”时，应当 **怎么挂、挂在哪、第一阶段开什么级别**，并确保：

- 默认关闭零侵入
- 第一阶段优先 whitebox-only
- 不进入真实输出候选
- 安全链优先（高风险/抢占时压制）
- key 命名与版本化遵循统一规范

为什么现在适合进入深联调方案阶段：

- 作为第三条旁路，它是验证统一规范是否够用的最佳样本（环境 gating + OCR 补证接口位 + 非安全型闭环）。
- 前两条旁路（`risk_interrupt_v1`/`sidewalk_nav_v1`）已跑通 whitebox-only 深接入路径；本方案只需要“复用路径 + 固化零售侧的 context 摘要 key”。

---

## 2. 当前状态回顾（简要）

### 2.1 已实现什么

- 旁路模块：`capabilities/cross_domain/retail_find_item_v1/`
  - 主入口：`evaluate_retail_find_item_v1(...)`
  - 输出白盒：`metadata["retail_find_item_v1"]`
  - 安全压制：`risk_level in {high, critical}` 或 `risk_interrupt_preempt=true` 时不外显结论
- 开关：
  - `LUNA_ENABLE_RETAIL_FIND_ITEM_V1`（默认 0）
  - `LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY`（默认 1）

### 2.2 已验证到什么程度

- 模块验证：`tools/test_retail_find_item_v1.py`
- 主线边缘集成验证：`tools/test_retail_find_item_v1_integration.py`（模拟主链式 metadata 合并）

---

## 3. 主线真实接入点候选（必须遵循统一规范）

> 统一规范要点（写死）：context 放“供主线消费的输入摘要”，metadata 放“本轮旁路处理输出/白盒”；全部版本化 `_v1`；metadata 顶层“一能力一 key”。

### 3.1 零售环境摘要最适合挂在哪个 VoiceRuntimeContext.metadata key

推荐新 key（V1）：

- `VoiceRuntimeContext.metadata["retail_env_summary_v1"]`

建议最小结构（摘要/事实，不含大 payload）：

- `scene_type_candidate`：`retail_shelf|retail_aisle|unknown`
- `retail_context_confidence`：0~1
- `shelf_visible`：bool（可选）
- `gating_passed`：bool（若上游已产出；否则可留空由旁路规则推断）
- `timestamp_ms`：时间戳（若可得）
- `source`：来源（如 `vision_environment_v1` / `runtime_rule` / `unknown`）

说明：

- 与 `sidewalk_env_summary_v1` 保持同一命名风格（`<domain>_env_summary_v1`），避免各写各的。
- 不把 OCR 原文/候选列表塞进 context；OCR 仍为补证接口位（V1）。

### 3.2 找货意图摘要是否需要独立 context key

推荐独立 key（V1）：

- `VoiceRuntimeContext.metadata["find_item_intent_summary_v1"]`

理由：

- 意图不是“零售环境的一部分”，而是任务/语义层对齐的输入摘要，单独 key 更利于复用（未来也可用于其他室内找物场景）。
- 避免把 intent 混在 env summary 里导致字段膨胀。

建议最小结构：

- `active`：bool
- `query`：string（目标商品词/类别）
- `user_requested_reading`：bool
- `need_text_to_progress`：bool
- `ocr_budget_ok`：bool（频控占位）
- `timestamp_ms`、`source`（可选）

### 3.3 白盒字段最终应落在哪个 VoiceFinalTextDispatchResult.metadata key

写死使用能力 key（已落地）：  

- `VoiceFinalTextDispatchResult.metadata["retail_find_item_v1"]`

并保持现有白盒结构（参考模块实现中的 `metadata["retail_find_item_v1"]` 字段集合），不另起新 key。

### 3.4 与 `risk_interrupt_v1` / `sidewalk_nav_v1` 的交界点

交界点必须落在“上层编排顺序”而不是模块 import：

1. 上层先汇总风险摘要到 `VoiceRuntimeContext.metadata["risk_summary_v1"]`（或等价注入）
2. 在深接入 hook 处读取：
   - `risk_level`
   - `risk_interrupt_preempt`
3. 调用 `evaluate_retail_find_item_v1(...)` 时把压制信号映射为 `RiskSummaryInput(risk_level, risk_interrupt_preempt=...)`
4. 若压制成立：仍写白盒，但 `final_spoken_output` 必为空（不进入真实输出候选）

与人行道环境分流一致性：

- `sidewalk_env_summary_v1` 与 `retail_env_summary_v1` 应来自同一“环境层/场景判别”口径（未来 vision 主链落地后由统一环境层产出）。
- 深接入阶段不强制互斥裁决，但建议上层环境判别优先产出明确 `scene_type_candidate`，避免同一轮同时命中室外与零售两套旁路。

---

## 4. 第一阶段建议接法（推荐：whitebox-only 深接入）

### 4.1 第一阶段级别建议

**建议第一阶段只接 whitebox-only**，并写死“不进入真实输出候选”。  
理由：

- 目前 submit 实链与 speaking/runtime 真实来源仍未成型；外显会把问题提前推到裁决/去噪/排队。
- `retail_find_item_v1` 涉及 OCR 补证与控噪，更适合先做可观测性与触发边界验证。

### 4.2 第一阶段最小改造范围（写死）

仅允许 1 个最小 hook（与前两条一致思路）：

- 在 `voice_final_text_dispatcher` 的真实主线路径上：
  - 从 `VoiceRuntimeContext.metadata` 读取 `retail_env_summary_v1` / `find_item_intent_summary_v1` / `risk_summary_v1`
  - 调用 `evaluate_retail_find_item_v1(...)` 生成白盒
  - 并入 `VoiceFinalTextDispatchResult.metadata["retail_find_item_v1"]`
  - 强制 `final_spoken_output=""`（不外显）

---

## 5. 与风险链的关系（写死）

压制条件（任一满足即压制）：

- `risk_level in {high, critical}`
- 或 `risk_interrupt_preempt=true`

压制结果（写死）：

- `output_suppressed_by_risk=true`
- `final_spoken_output=""`（深接入阶段本就不外显，但此处必须在白盒中明确标记）

当前阶段不做更复杂联动的原因：

- 不做“抢占/恢复/排队/合并”编排；只验证压制信号可被正确透传与留痕。

---

## 6. 与环境链的关系（与 sidewalk_nav_v1 的一致性）

### 6.1 零售环境摘要是否来自统一 scene/context

建议是（方向写死）：未来由统一环境层产出，分别注入：

- `sidewalk_env_summary_v1`（室外通行类）
- `retail_env_summary_v1`（零售货架类）

### 6.2 哪些字段应该共享，哪些不共享

共享（推荐）：

- `timestamp_ms`、`source`、以及 `scene_type_candidate/confidence` 的命名风格

不共享（写死）：

- 零售侧的 intent/OCR 触发预算等任务特定字段，不应进入 `sidewalk_env_summary_v1`

---

## 7. 主线对象最小改造清单

### 7.1 需要加的最小 context key（新增）

- `retail_env_summary_v1`（见上）
- `find_item_intent_summary_v1`（见上）

### 7.2 需要接最小 hook 的层

- `voice_final_text_dispatcher.dispatch_voice_final_text(..., runtime_context=...)`（与前两条一致）

### 7.3 绝对不要动（写死）

- 不改全局裁决器
- 不引入真实输出候选（不提交 SpeechRequest）
- 不在默认关闭时注入任何字段或触发任何计算

---

## 8. 验证与回退

### 8.1 深联调后如何验证（第一阶段）

必须覆盖：

- 默认关闭（`LUNA_ENABLE_RETAIL_FIND_ITEM_V1=0`）→ 主线零侵入（metadata 不含 `retail_find_item_v1`）
- 开启 + whitebox-only → 主线 metadata 出现 `retail_find_item_v1` 白盒
- context 环境为非零售 → gating 不通过，白盒仍可留痕但不误触发主流程外显
- 风险压制存在 → `output_suppressed_by_risk=true` 且 `final_spoken_output=""`
- `dispatch_type/notes` 不被改写

### 8.2 回退方式（写死）

- 先保持 whitebox-only（默认已是）
- 出现主链污染/异常 → 直接关闭：`LUNA_ENABLE_RETAIL_FIND_ITEM_V1=0`

---

## 9. 当前阶段不做项（写死）

- 不做真实输出候选
- 不做复杂 OCR 调度/常驻扫描
- 不做购物车/支付/比价
- 不做多来源融合
- 不做全局裁决器改造

---

## 一句话收束

先把 `retail_find_item_v1` 按统一规范（context 摘要 + metadata 白盒）写清楚深接入方案，并写死“第一阶段 whitebox-only + 风险压制优先 + 不进真实输出候选”，再进入后续第一阶段主线接入实现。

