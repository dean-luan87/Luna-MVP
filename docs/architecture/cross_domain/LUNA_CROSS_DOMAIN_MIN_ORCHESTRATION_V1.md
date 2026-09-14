# 跨域旁路：最小编排规则（V1）

## 1. 目标

三条旁路能力已全部完成 **Level 1 / whitebox-only** 的真实主线接入（同构路径：context 注入 + dispatch result metadata 留痕）。  
当旁路从“单点建设”进入“多旁路共存”，若没有编排规则，会立刻出现：

- 谁先跑、谁后跑不清晰（导致压制信号/依赖关系失真）
- 多条旁路同时命中时，metadata 留痕顺序与共存方式不明确
- “哪些只留痕、哪些可进入真实输出候选”的边界被各旁路各自定义，进而发散

本文件给出 **最小编排规则**（写死口径），只做规则收口：**不扩功能、不改现有实现、不新增模型**，并以当前阶段仍为 **whitebox-only** 为前提。

---

## 2. 当前纳入编排的能力（V1）

- `risk_interrupt_v1`（安全优先链）
- `sidewalk_nav_v1`（日常主导航底盘）
- `retail_find_item_v1`（场景化补充：零售找货）

---

## 3. 最小运行顺序（写死）

### 3.1 固定顺序

1. **`risk_interrupt_v1` 优先**
2. **`sidewalk_nav_v1` 第二**
3. **`retail_find_item_v1` 第三**

### 3.2 为什么这样排（写死）

- **安全优先**：风险链是全局优先级基准，必须先于任何非安全链做“压制信号”确定与白盒留痕。
- **主导航优先**：人行道通行属于日常主路底盘（在室外场景命中频繁），应先于零售等场景化补充能力。
- **场景化补充最后**：零售找货属于“进入特定环境后的补充闭环”，且涉及 OCR 补证边界，更应在风险压制已知后运行。

---

## 4. 压制与依赖关系（写死）

### 4.1 `risk_interrupt_v1` 对另外两条的压制关系

当满足任一条件时：

- `risk_level in {high, critical}`
- 或 `risk_interrupt_preempt=true`（上层已判定风险打断需抢占/压制）

则：

- `sidewalk_nav_v1` 与 `retail_find_item_v1` 必须进入“**只留白盒**”路径：
  - `output_suppressed_by_risk=true`
  - `final_spoken_output=""`

说明：当前阶段三条旁路均不进入真实输出候选；此处“压制”主要体现为白盒中的抑制标记与外显为空，避免未来升级时语义混乱。

### 4.2 `sidewalk_nav_v1` 与 `retail_find_item_v1` 的关系

两者 **不互相压制**，但各自依赖场景/gating：

- `sidewalk_nav_v1` 依赖：`sidewalk_env_summary_v1`（室外人行道语境）与风险摘要
- `retail_find_item_v1` 依赖：`retail_env_summary_v1` + `find_item_intent_summary_v1` 与风险摘要

当前阶段建议上层环境判别尽量做到“单一主语境”，避免同一轮同时强命中室外与零售两种语境（见最小冲突规则）。

### 4.3 共享与不共享（写死）

共享（必须）：

- `VoiceRuntimeContext.metadata["risk_summary_v1"]`：三条旁路统一使用该风险摘要口径（风险链可回退 event.metadata 占位，但主线口径以 context 为主）。

不共享（写死）：

- 环境摘要不共享：`sidewalk_env_summary_v1` 与 `retail_env_summary_v1` 分属不同 domain，不得混用。

---

## 5. 白盒留痕顺序与共存方式（写死）

### 5.1 留痕顺序

在同一轮 `VoiceFinalTextDispatchResult` 生成过程中，建议按运行顺序写入：

1. `metadata["risk_interrupt_v1"]`
2. `metadata["sidewalk_nav_v1"]`
3. `metadata["retail_find_item_v1"]`

### 5.2 多条旁路同时命中时如何共存

- 允许三条旁路白盒 **并列共存** 于同一个 `VoiceFinalTextDispatchResult.metadata`（不同顶层 key）。
- 不做跨能力合并裁决，不做“写一份统一 cross_domain 白盒总包”（避免在 V1 过早引入大 schema）。

### 5.3 为什么当前阶段不做跨能力合并裁决

- 当前阶段的主目标是“可观测性与零侵入”，不是“输出融合”。
- submit 实链与 speaking/runtime 真实来源仍未成型，合并裁决会把问题提前推到全局调度与去噪。

---

## 6. 当前阶段进入真实输出候选的边界（写死）

### 6.1 当前三条旁路都不进入真实输出候选

V1 统一写死：

- `risk_interrupt_v1`：仅 Level 1 whitebox-only 深接入，不抢占、不改输出。
- `sidewalk_nav_v1`：深接入阶段强制 `final_spoken_output=""`，不进入候选。
- `retail_find_item_v1`：深接入阶段强制 `final_spoken_output=""`，不进入候选。

### 6.2 后续若允许能力进入 Level 2，应先从哪条开始、为什么

候选顺序建议（仅定义方向，不在本文件实施）：

1. `risk_interrupt_v1`（安全优先、价值最高、优先级基准）

前置条件（不在本文件实现，但作为边界提醒）：

- submit 实链成型（可控地提交/中断候选输出）
- speaking/runtime 真实来源可得（而不是可观测替代）
- 去重/恢复/回退策略能秒级止血（Level 2 必须短窗可回退）

---

## 7. 最小冲突规则（写死）

### 7.1 高风险时的统一规则

高风险/抢占标记存在时：

- 导航链与零售链都只留白盒，不外显任何结论/建议（`final_spoken_output=""`）。

### 7.2 人行道与零售场景的并发冲突

若同一轮 context 同时给出：

- `sidewalk_env_summary_v1` 强命中（室外人行道）
- `retail_env_summary_v1` 强命中（零售货架）

则当前阶段建议：

- 两条旁路都可写白盒（用于对账）
- **不进入强结论态**（当前本就不外显）
- 后续若进入真实输出候选，必须先由“统一环境层/场景判别”解决冲突（不在本文件实现）

### 7.3 环境摘要冲突/不稳

当环境摘要不稳（置信度低/互相矛盾）时：

- 旁路可继续白盒留痕，但不得推动任何外显候选（V1 写死）

---

## 8. 当前阶段不做项（写死）

- 不做全局裁决器重写
- 不做多旁路融合输出
- 不做复杂优先级动态调度
- 不做自动升级到 Level 2

---

## 一句话收束

先把三条旁路在同一轮主线里的最小编排顺序、压制关系与白盒共存方式写死（仍以 whitebox-only 为前提），再讨论是否让 `risk_interrupt_v1` 进入 Level 2 候选评审，或让某条能力进入真实输出候选试点。

