# 跨域旁路：真实主线深接入状态总复盘（V1）

## 1. 目的

在三条旁路能力都已完成 **Level 1 / whitebox-only** 的真实主线接入后，对当前接入状态做一次收口复盘，明确：

- 三条旁路各自接到了主线哪一层
- 各自当前的 context 输入 key / metadata 留痕 key
- 已收敛的共性规则与仍存在的差异点
- 后续演进顺序建议（但当前不进入 Level 2）

本文件只做收口：**不扩功能、不改现有实现、不新增模型**。

---

## 2. 当前已完成深接入的旁路能力（V1）

- `risk_interrupt_v1`
- `sidewalk_nav_v1`
- `retail_find_item_v1`

---

## 3. 每条能力的真实主线接入状态（事实表）

> 统一口径：三条旁路均在 `capabilities/voice/runtime/voice_final_text_dispatcher.py` 的真实分流路径中，通过单点 hook 读取 `VoiceRuntimeContext.metadata`，并把白盒并入 `VoiceFinalTextDispatchResult.metadata`。

### 3.1 `risk_interrupt_v1`

- **Level 1 / whitebox-only 真实接入**：是  
- **主线接入层**：`voice_final_text_dispatcher`（生成 `VoiceFinalTextDispatchResult` 时）  
- **context 输入 key**：  
  - `VoiceRuntimeContext.metadata["risk_summary_v1"]`（优先）  
  - 回退：`VoiceInputEvent.metadata`（占位兼容）  
- **metadata 留痕 key**：`VoiceFinalTextDispatchResult.metadata["risk_interrupt_v1"]`  
- **是否受风险链压制**：不适用（它本身就是风险链）  
- **是否进入真实输出候选**：否（阶段 1 不抢占、不改输出）  

### 3.2 `sidewalk_nav_v1`

- **Level 1 / whitebox-only 真实接入**：是  
- **主线接入层**：`voice_final_text_dispatcher`  
- **context 输入 key**：  
  - `VoiceRuntimeContext.metadata["sidewalk_env_summary_v1"]`（环境摘要）  
  - `VoiceRuntimeContext.metadata["risk_summary_v1"]`（压制信号复用）  
- **metadata 留痕 key**：`VoiceFinalTextDispatchResult.metadata["sidewalk_nav_v1"]`  
- **是否受风险链压制**：是  
  - `risk_level in {high, critical}` 或 `risk_interrupt_preempt=true` ⇒ `output_suppressed_by_risk=true` 且 `final_spoken_output=""`  
- **是否进入真实输出候选**：否（阶段 1 写死不外显）  

### 3.3 `retail_find_item_v1`

- **Level 1 / whitebox-only 真实接入**：是  
- **主线接入层**：`voice_final_text_dispatcher`  
- **context 输入 key**：  
  - `VoiceRuntimeContext.metadata["retail_env_summary_v1"]`（零售环境摘要）  
  - `VoiceRuntimeContext.metadata["find_item_intent_summary_v1"]`（找货意图摘要）  
  - `VoiceRuntimeContext.metadata["risk_summary_v1"]`（压制信号复用）  
- **metadata 留痕 key**：`VoiceFinalTextDispatchResult.metadata["retail_find_item_v1"]`  
- **是否受风险链压制**：是  
  - `risk_level in {high, critical}` 或 `risk_interrupt_preempt=true` ⇒ `output_suppressed_by_risk=true` 且 `final_spoken_output=""`  
- **是否进入真实输出候选**：否（阶段 1 写死不外显）  

---

## 4. 三条旁路的共性规则（已收敛）

已收敛为“深接入 Level 1 基线”：

- **默认关闭**：不开启时不注入对应 metadata key（零侵入）
- **whitebox-only**：深接入阶段写死只允许白盒留痕
- **context 注入**：通过 `VoiceRuntimeContext.metadata` 注入“输入摘要/事实”
- **dispatch result metadata 留痕**：写入 `VoiceFinalTextDispatchResult.metadata["<capability>_v1"]`
- **不改真实输出内容**：不改 `dispatch_type` / `notes` / 文本候选
- **不改任务链状态**：阶段 1 不挂起、不恢复、不编排
- **不碰 speaking/runtime**：当前 speaking 为“可观测替代”或未接入真实来源
- **风险压制优先**：非安全链（导航/零售）必须被高风险/抢占信号压制

这些共性已被《`LUNA_CROSS_DOMAIN_CONTEXT_METADATA_CONVENTION_V1.md`》约束为统一规范。

---

## 5. 三条旁路的差异点（仍存在且合理）

### 5.1 依赖的 context 摘要不同

- 风险：`risk_summary_v1`
- 人行道：`sidewalk_env_summary_v1` + `risk_summary_v1`
- 零售：`retail_env_summary_v1` + `find_item_intent_summary_v1` + `risk_summary_v1`

### 5.2 gating/scene 条件不同

- `sidewalk_nav_v1`：命中 `outdoor_walkway` 才有导航建议候选；高风险/抢占压制
- `retail_find_item_v1`：零售场景 gating + 找货意图才进入“可补证/可结论”路径；高风险/抢占压制

### 5.3 白盒侧重点不同

- `risk_interrupt_v1`：original_output、interrupt_reason 等裁决白盒为核心
- `sidewalk_nav_v1`：scene_summary + navigation_hint + suppressed 标记为核心
- `retail_find_item_v1`：gating_result + ocr_trigger_reason + item_match_summary/task_evidence 为核心

---

## 6. 后续演进顺序建议（当前不进入 Level 2）

### 6.1 哪条最接近 Level 2 候选

**`risk_interrupt_v1`** 最接近 Level 2 候选（安全优先、价值最高、优先级基准）。  
但进入 Level 2 的前置仍未满足（当前仍缺 submit 实链与 speaking/runtime 真实来源），因此本复盘结论仍为：**先不进 Level 2**。

### 6.2 哪些仍适合继续停留在 whitebox-only

- `sidewalk_nav_v1`：建议继续 whitebox-only，先把环境摘要来源稳定化（上游环境层/vision runtime）与控噪策略准备好
- `retail_find_item_v1`：建议继续 whitebox-only，先验证 intent/gating/OCR 补证接口位的触发边界与控噪

### 6.3 哪些需要等待更稳定的上游 context

- `sidewalk_env_summary_v1` / `retail_env_summary_v1`：未来应尽量来自统一环境层产出（vision/environment runtime），避免由下游各自规则推断导致漂移

---

## 7. 当前阶段不做项（写死）

- 不直接进入 Level 2
- 不做真实输出候选（不提交 `SpeechRequest`）
- 不做 speaking/runtime 接入
- 不做全局裁决器改造

---

## 一句话收束

三条旁路已在真实主线中形成同构的 Level 1 / whitebox-only 深接入基线；先把“接入状态事实 + 共性规则 + 差异点 + 演进顺序”收口清楚，再进入下一阶段的《跨域旁路最小编排规则 V1》设计。

