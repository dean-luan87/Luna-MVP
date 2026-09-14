# Luna Voice Mainline Next-Step Execution Plan v0（主线下一阶段执行清单）

**文件**：`docs/architecture/voice/LUNA_VOICE_MAINLINE_NEXT_STEP_EXECUTION_PLAN_V0.md`  
**性质**：短、硬、可执行的主线推进清单（不是总纲、不是治理文档、不是未来蓝图）  
**目标（写死）**：只回答“接下来主线先做什么、后做什么、暂时不做什么”。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  
- `docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`

---

## A. 文档定位

- 这是一份**主线下一阶段执行清单**。  
- 不是总纲。  
- 不是治理文档。  
- 不是未来蓝图。  
- 只回答：**接下来主线先做什么**（并写死暂缓事项）。

---

## B. 当前主线状态（一段即可）

主线骨架已搭出（V1/V2/V3 + admission layer），治理底线已立住（宪法与 Topic 01~04 的边界已冻结）。当前阶段应从“继续拆专题”切回“继续增强主线能力”，优先提高闭环可用性与接口稳定性，并维持“不夺权、不脑补、不越界”的工程纪律。

---

## C. 下一阶段只推进的 3 个点（只列 3 个）

### 1) 增强语音主链闭环的可用性（不加新分支）

只做“稳定输入 → 状态 → 输出”的闭环体验增强，保持主链裁决边界不变：  
- 强化 “被 gate 拦截时的响应型输出” 的可用性与一致性（例如固定澄清/确认模板的最小闭环与回归）  
- 继续用“最小接入 → 验证 → baseline/freeze”的方式加小能力，不把主线改成对话策略器

### 2) 增强语义层与主链之间的**正式消费接口**（仍不接模型、不夺权）

目标是让 `SemanticConverterV2` 的输出“更稳定、可观测、可对照”，但不让语义层接管裁决：  
- 把语义输出的**可消费字段**进一步收敛成稳定面（仍保持 shadow/assist 为辅）  
- 把“语义命中 vs 主链事实”之间的对照与失败模式更可回归（不引入模型版语义）

### 3) 推进 V3 到“可被主线安全消费”的程度（仍不进入视觉解释）

目标是扩大“输入承载稳定性”和“只读消费的一致性”：  
- 继续完善 V3 输入包在主链中的承载与版本约束（仍保持 summary-only、no fabrication、no anchors）  
- 推进 V2 的只读消费从“seen/not seen”向“结构完整性/字段可用性评估（只读）”演进，但仍不解释、不驱动行为

---

## D. 当前明确暂缓的事项（写死）

- 冲突专题继续细化（本阶段不再拆新专题）  
- 白盒 / provenance 实现  
- 视觉语义解释实现  
- 模型版语义接入  
- Risk Gate 实现  
- `resume/repeat` 行为实现  
- 文本 vs 视角冲突实现  

---

## E. 推荐的唯一第一落点（只选 1 个）

**唯一第一落点**：继续推进“主链可说话响应”的最小闭环 —— **把 gate 命中后的响应型输出模板体系，先做成可冻结、可回归、可扩展的最小接口面**（仍不做协商器、不新增 gate）。  

为什么选它：  
- 与现有主链最连续：落点仍在 `dispatch_voice_final_text(...)` 之后、submit 附近（不改 dispatch/route/proposal）。  
- 风险最小：属于“响应型 submit”，不触碰执行准入裁决，易于守住边界。  
- 直接提升可用性：用户在被 gate 拦截时能得到稳定、保守、可解释的反馈。  

---

## F. 与现有基线的关系（写死）

所有推进必须服从：  
- `LUNA_VOICE_MAINLINE_BASELINE.md`  
- `LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`  
- `LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  

并且不得破坏已冻结的：V1/V2/V3 冻结面、Resource/Information gate baseline、以及已落地的“继续请求固定确认响应模板”冻结面与验证入口。

---

## G. 当前执行纪律（短规则）

- 新能力优先走：**最小接入 → 验证 → baseline/freeze → 总览补索引**  
- 不允许先上复杂实现再补约束  
- 不允许辅助层夺权（语义/视觉/shadow/assist 只能辅助）  
- 不允许为了快而跳过冻结面与回归入口  
- 任何会影响 submit/可说话范围的改动，必须有明确“执行型 vs 响应型”的边界说明

