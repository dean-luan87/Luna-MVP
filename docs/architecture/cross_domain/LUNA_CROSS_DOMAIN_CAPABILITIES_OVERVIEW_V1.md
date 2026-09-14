# 跨域旁路能力总览（V1）

## 1. 文档目的

把当前**已落地**且完成**主线边缘集成验证**的跨域旁路能力，收成一份主线入口视图，便于后续扩展第三条及更多旁路时不散、可对照。

**原则（本总览）**：不扩功能、不改实现、不新增模型；仅状态收口与指针。

---

## 2. 当前已落地的跨域旁路能力

| 能力 ID | 一句话 |
|---------|--------|
| `risk_interrupt_v1` | 风险事件 → 最小抢占裁决 + `paused_by_risk` + 白盒 |
| `sidewalk_nav_v1` | 环境初判（规则占位）+ 风险压制 + 最小通行建议 + 白盒 |
| `retail_find_item_v1` | 零售环境 gating + 找货意图对齐 + OCR 触发决策占位 + 最小结论 + 白盒 |

详细设计/实现说明见各能力专文（下表「关键文档」列）。

---

## 3. 每条能力的当前状态

### 3.1 `risk_interrupt_v1`

| 维度 | 状态 |
|------|------|
| 设计 | 已有（含最小实现方案、代码计划、运行策略） |
| 代码实现 | 已有：`capabilities/cross_domain/risk_interrupt_v1.py` |
| 模块验证 | 已有：`tools/test_risk_interrupt_v1.py` |
| 主线边缘集成验证 | 已有：`tools/test_risk_interrupt_v1_integration.py` |
| 默认是否关闭 | **是**（`LUNA_ENABLE_RISK_INTERRUPT_V1` 默认等价关闭） |
| whitebox-only / 降级 | **支持**：`LUNA_RISK_INTERRUPT_WHITEBOX_ONLY`（默认建议先只白盒） |
| 长期保留态 | **是**：作为可长期保留的旁路底座；默认 Level 0，观测时可 Level 1 |

**关键文档**：`LUNA_RISK_INTERRUPT_V1_IMPLEMENTED_NOTE.md`、`LUNA_RISK_INTERRUPT_V1_INTEGRATION_NOTE.md`、`LUNA_RISK_INTERRUPT_V1_RUNTIME_POLICY.md`

### 3.2 `sidewalk_nav_v1`

| 维度 | 状态 |
|------|------|
| 设计 | 已有（最小实现方案、代码实现计划） |
| 代码实现 | 已有：`capabilities/cross_domain/sidewalk_nav_v1/` |
| 模块验证 | 已有：`tools/test_sidewalk_nav_v1.py` |
| 主线边缘集成验证 | 已有：`tools/test_sidewalk_nav_v1_integration.py` |
| 默认是否关闭 | **是**（`LUNA_ENABLE_SIDEWALK_NAV_V1` 默认关闭） |
| whitebox-only / 降级 | **支持**：`LUNA_SIDEWALK_NAV_WHITEBOX_ONLY`（默认只白盒、不外显导航句） |
| 长期保留态 | **是**：旁路形态固定；深化能力另开阶段，不替换本 V1 边界 |

**关键文档**：`LUNA_SIDEWALK_NAV_MIN_IMPLEMENTATION_V1.md`、`LUNA_SIDEWALK_NAV_CODE_PLAN_V1.md`、`LUNA_SIDEWALK_NAV_V1_IMPLEMENTED_NOTE.md`、`LUNA_SIDEWALK_NAV_V1_INTEGRATION_NOTE.md`

### 3.3 `retail_find_item_v1`

| 维度 | 状态 |
|------|------|
| 设计 | 已有（最小实现方案、代码实现计划） |
| 代码实现 | 已有：`capabilities/cross_domain/retail_find_item_v1/` |
| 模块验证 | 已有：`tools/test_retail_find_item_v1.py` |
| 主线边缘集成验证 | 已有：`tools/test_retail_find_item_v1_integration.py` |
| 默认是否关闭 | **是**（`LUNA_ENABLE_RETAIL_FIND_ITEM_V1` 默认关闭） |
| whitebox-only / 降级 | **支持**：`LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY`（默认只白盒、不外显结论） |
| 长期保留态 | **是**：作为场景化补充旁路；默认关闭，观测时可只白盒 |

**关键文档**：`LUNA_RETAIL_FIND_ITEM_MIN_IMPLEMENTATION_V1.md`、`LUNA_RETAIL_FIND_ITEM_CODE_PLAN_V1.md`、`LUNA_RETAIL_FIND_ITEM_V1_IMPLEMENTED_NOTE.md`、`LUNA_RETAIL_FIND_ITEM_V1_INTEGRATION_NOTE.md`

---

## 4. 每条能力的定位

### 4.1 `risk_interrupt_v1`

- **解决什么**：在「普通任务提示正在播报」等状态下，对 **high/critical** 风险做最小抢占，避免安全信息被任务提示淹没；并留全链路白盒。
- **主线优先级**：跨域安全类 **第一优先**（与场景优先级文档一致时，安全链先于普通导航提示）。
- **与语义 / 任务链 / 输出裁决**：不替代语义生成；通过 `task_paused` / `paused_by_risk` 与任务链状态对齐；**最终播什么**仍由统一输出裁决口汇总（本模块给出抢占时的 `final_spoken_output` 候选与白盒）。

### 4.2 `sidewalk_nav_v1`

- **解决什么**：在室外/人行道语境下给出 **一条最小通行建议**，并在高风险或风险链抢占时 **压下** 普通导航提示；完整白盒可对账。
- **主线优先级**：日常主路类 **第二优先**（在风险链之后；被 `risk_interrupt_v1` 或高风险摘要压制）。
- **与语义 / 任务链 / 输出裁决**：不内置复杂 NLG；输出 `navigation_hint` / `final_spoken_output` 候选与 `metadata["sidewalk_nav_v1"]`；**未默认接入主链**，需上层显式调用与合并。

### 4.3 两条能力的关系（固定）

- **风险链优先于普通导航提示**：`sidewalk_nav_v1` 通过高风险摘要或 `risk_interrupt_preempt` 与 `risk_interrupt_v1` 对齐，不 import 对方模块，由上层编排。

---

## 5. 开关与运行策略摘要

### 5.1 `risk_interrupt_v1`

| 项 | 说明 |
|----|------|
| 总开关 | `LUNA_ENABLE_RISK_INTERRUPT_V1`（**默认 0**） |
| whitebox-only | `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY`（**默认 1**：只记录，不抢占） |
| 真实生效（抢占）条件 | 总开关开 + whitebox-only 关 + `high/critical` + 当前输出状态可抢占（见实现与运行策略） |
| 回退 | 关总开关 → 零侵入；仅 whitebox → 不抢占；详见《`LUNA_RISK_INTERRUPT_V1_RUNTIME_POLICY.md`》Level 0/1/2 |

### 5.2 `sidewalk_nav_v1`

| 项 | 说明 |
|----|------|
| 总开关 | `LUNA_ENABLE_SIDEWALK_NAV_V1`（**默认 0**） |
| whitebox-only | `LUNA_SIDEWALK_NAV_WHITEBOX_ONLY`（**默认 1**：白盒含 `navigation_hint`，`final_spoken_output` 为空） |
| 真实生效（外显导航句）条件 | 总开关开 + whitebox-only 关 + 人行道命中 + 未被风险压制 |
| 回退 | 关总开关 → 不写 `metadata["sidewalk_nav_v1"]`；whitebox-only → 不外显播报候选 |

---

## 6. 当前不做项（跨能力共性）

- **未做自动恢复逻辑**（如风险解除后的任务自动续播策略，以专文/后续版本为准）。
- **未做复杂多模型 / 多风险事件融合**（V1 均为单事件或单摘要接入）。
- **未接入默认主链**：两条能力均为**旁路**，需上层在输出裁决处显式调用与合并 `metadata`。
- **仍停留在旁路验证阶段的部分**：主线边缘集成验证使用**模拟 metadata**，非全链路 dispatcher/TTS 联调。

---

## 7. 下一步候选能力（仅清单，不展开实现）

- 人行道导航 **第二阶段**（更深环境输入、仍不默认污染主链）
- `retail_find_item_v1`：**已完成最小实现方案设计，尚未进入代码实现**（见《`docs/architecture/cross_domain/LUNA_RETAIL_FIND_ITEM_MIN_IMPLEMENTATION_V1.md`》）
- 其他跨链能力（地铁站/医院/商场等），按场景优先级文档迭代

---

## 8. 一句话收束

已落地的 **`risk_interrupt_v1`** 与 **`sidewalk_nav_v1`** 具备同一套工程闭环（设计 → 实现 → 模块验证 → 边缘集成验证 → 默认关闭 → 可白盒降级）；本总览作为跨域旁路 **V1 总入口**，后续新增旁路前先对照本表再开主线。
