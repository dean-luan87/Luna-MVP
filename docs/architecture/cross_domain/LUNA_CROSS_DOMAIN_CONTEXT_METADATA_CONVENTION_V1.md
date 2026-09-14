# 跨域旁路：统一 context 注入 / metadata 留痕规范（V1）

## 1. 目标

在 `risk_interrupt_v1` 与 `sidewalk_nav_v1` 均已完成主线深接入（whitebox-only）的前提下，统一两类“主线承接面”：

- **context 注入面**：`VoiceRuntimeContext.metadata`（主线可消费的输入摘要 / 运行态事实）
- **metadata 留痕面**：`VoiceFinalTextDispatchResult.metadata`（本轮旁路处理结果 / 白盒）

这份规范解决的问题：

- 防止 context key / metadata key 继续增长后 **命名散、层次混、字段混用**
- 明确“哪些字段属于上游注入、哪些字段属于旁路自产”
- 为后续 `retail_find_item_v1` 及更多旁路进入深接入（whitebox-only）提供统一约束

本文件只做约定收口：**不扩功能、不改现有实现逻辑、不新增模型**。

---

## 2. 当前已存在的接入样式（作为基线）

### 2.1 context 侧（VoiceRuntimeContext.metadata）

已存在/已采用的 key（V1）：

- `VoiceRuntimeContext.metadata["risk_summary_v1"]`
- `VoiceRuntimeContext.metadata["sidewalk_env_summary_v1"]`

### 2.2 metadata 侧（VoiceFinalTextDispatchResult.metadata）

已存在/已采用的 key（V1）：

- `VoiceFinalTextDispatchResult.metadata["risk_interrupt_v1"]`
- `VoiceFinalTextDispatchResult.metadata["sidewalk_nav_v1"]`

说明：以上 4 个 key 是当前规范的“事实基线”，后续旁路深接入不得绕开本约定另起炉灶。

---

## 3. context 层规范（VoiceRuntimeContext.metadata）

### 3.1 什么应该进 context

context 只承载 **供主线/其他模块消费的“输入摘要/事实”**，典型包括：

- **环境类摘要**：例如“当前像室外人行道”“置信度多少”
- **风险类摘要**：例如“当前风险等级/类型/方向/距离带/可信度”
- **运行态事实**：例如“当前输出忙闲状态”（后续可扩 speaking/runtime 的真实来源）

### 3.2 命名规范（建议）

- 必须带版本：`*_v1`
- 建议形式：`<domain>_<summary>_v1`
  - 示例：`risk_summary_v1`、`sidewalk_env_summary_v1`
- 禁止无版本裸 key（例如 `risk_summary`）在 context 中扩散。

### 3.3 context 中应存什么，不应存什么

应存（写死）：

- **摘要/事实**：短字段、可解释、可追溯来源（可含 `source`/`timestamp_ms`）

不应存（写死）：

- 大块原始 payload（例如 OCR 全文、长列表候选、模型 raw 输出）
- 本轮旁路“决策结果白盒”（那应进入 metadata 留痕层）
- 与“主线可复用”无关的 debug 中间量（除非明确为 runtime 观测需求）

### 3.4 最小结构约束（推荐）

context 内的 dict 建议满足：

- 必须包含：`timestamp_ms`（若可得）
- 建议包含：`source`（产出链路标识，如 `vision_risk_scan_v1` / `runtime_rule`）
- 字段尽量扁平、稳定；新增字段必须向后兼容（读取端允许缺失）

---

## 4. metadata 层规范（VoiceFinalTextDispatchResult.metadata）

### 4.1 什么应该进 metadata

metadata 承载 **“本轮旁路处理结果/白盒留痕”**，用于回放、审计、排障、对账：

- 旁路是否生效（enabled/whitebox-only）
- 输入摘要（可引用 context 的关键字段，但不整块复制）
- 输出候选/是否压制/最终外显候选（深接入阶段通常为空）
- 原因码与关键决策点

### 4.2 命名规范（建议）

- 必须带版本：`*_v1`
- 建议形式：`<capability_name>_v1`
  - 示例：`risk_interrupt_v1`、`sidewalk_nav_v1`
- 一个旁路能力只允许一个顶层 metadata key（避免同能力多 key 散落）。

### 4.3 metadata 中应存什么，不应存什么

应存（写死）：

- 本轮旁路白盒：`scene_summary`/`risk_summary`/`output_suppressed_by_risk`/`final_spoken_output`/`event_timestamp` 等（以各能力实现说明为准）

不应存（写死）：

- 把 context 整块原样复制进 metadata（会造成重复与漂移）
- 长文本/大对象/大数组（除非有明确审计需求且被采样/截断）

---

## 5. 字段分层原则（写死）

### 5.1 一句话原则

- **context 放“供主线消费的输入摘要”**
- **metadata 放“本次旁路处理输出与留痕（白盒）”**

### 5.2 上游注入 vs 旁路自产

- 上游注入（写入 context）：
  - 风险摘要：`risk_summary_v1`
  - 环境摘要：`sidewalk_env_summary_v1`
  - 运行态事实（未来）：例如 speaking/output_busy_state

- 旁路自产（写入 metadata）：
  - `risk_interrupt_v1` 的裁决白盒（interrupt_reason/original_output/...）
  - `sidewalk_nav_v1` 的环境判定/导航建议/压制白盒

### 5.3 深接入阶段（whitebox-only）的默认口径

在“深接入 whitebox-only”阶段，旁路的 `final_spoken_output` 应默认为空或不进入真实输出候选；所有外显策略应由后续阶段在“submit 实链 + speaking/runtime 可得 + 裁决口可控噪”条件满足后再推进。

---

## 6. 版本化原则（写死）

### 6.1 为什么必须带 `_v1`

- 避免 key 漂移导致读取端不兼容
- 允许并行灰度：`*_v1` 与 `*_v2` 可短期并存

### 6.2 升级时如何并存/替换

- 新版本必须使用新 key（例如 `risk_summary_v2`）
- 旧 key 保留一段时间以兼容读取端；读取优先级可在接入方案中明确
- 禁止“在同一个 key 下做破坏性字段改名/语义翻转”

---

## 7. 对后续能力的约束（写死）

### 7.1 `retail_find_item_v1` 深接入约束

当 `retail_find_item_v1` 进入 whitebox-only 深接入时：

- context 侧应使用版本化摘要 key（建议：`retail_env_summary_v1`、`find_item_intent_summary_v1` 等；以其深联调方案写死为准）
- metadata 侧必须使用能力 key：`retail_find_item_v1`
- 严禁自创不带版本的裸 key，或把 intent/ocr 原始块直接塞进 metadata

### 7.2 未来其他跨域旁路的统一约束

- 必须遵循“context 摘要 / metadata 白盒”的分层
- 必须版本化（`*_v1`）
- 必须单能力单 key（metadata 顶层）

---

## 8. 当前阶段不做项（写死）

- 不做统一大 schema（只做约定）
- 不做代码强校验（不引入强制 validator）
- 不做多来源融合框架
- 不做既有 key 的强制重构（先以约定形式收口，后续渐进整理）

---

## 一句话收束

先把跨域旁路在主线中的 **context 注入** 与 **metadata 留痕** 的分层、命名与版本化规则统一下来（优先服务 whitebox-only 深接入阶段），再继续推进第三条旁路及更多能力的深接入，避免 key 与字段体系发散。

