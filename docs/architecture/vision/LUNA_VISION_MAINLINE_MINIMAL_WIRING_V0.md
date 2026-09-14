# Luna Vision — Mainline Minimal Wiring v0（视角主线最小接通）

**文件**：`docs/architecture/vision/LUNA_VISION_MAINLINE_MINIMAL_WIRING_V0.md`  
**性质**：P1-3 最小接线（打一跳：输入摘要 → 1 种 slice → 中台 consume stub 观测）  

基于已完成：
- `docs/architecture/vision/LUNA_VISION_CONSUMABLE_SLICE_OUTPUT_SCHEMA_V0.md`
- `docs/architecture/vision/LUNA_VISION_MID_PLATFORM_CONSUME_STUB_V0.md`
- `capabilities/vision/runtime/vision_mid_platform_consume_stub_v0.py`
- `docs/architecture/vision/LUNA_VISION_MAINLINE_BREAKPOINTS_AND_MIN_WIRING_PLAN_V0.md`
- `docs/architecture/LUNA_PHASE1_EXECUTION_PLAN_V0.md`

---

## A. 文档定位（写死）

- 这是 **P1-3 的最小接线设计**。
- 当前目标是打通一条最小视角主线，使其可运行、可回归、可观察。
- 当前不做：
  - 中台裁决
  - 语音/记忆/导航派发或执行联动
  - 复杂解释层

---

## B. 当前最小主线定义（本轮打通的链路）

本轮打通链路（只打一跳）：

**现有视角摘要输入**（来自 `runtime_context.metadata`）  
→ **最小 slice 生成**（只选 1 种类型）  
→ 写入 `runtime_context.metadata["vision_consumable_slices_v0"]`  
→ **中台 consume stub**（`vision_mid_platform_consume_stub_v0`）观测到并写入 `result.metadata["vision_mid_platform_consume_stub_v0"]`

注意：
- 这不是完整视角链
- 只是一期最小 wiring（可运行、可观察、不可夺权）

---

## C. 本轮选定的 slice 类型（只选 1 种）

**选定**：`risk_slice`

**输入来源**：`runtime_context.metadata["risk_summary_v1"]`

**理由（最小、最连续、最不容易失控）**：
- `risk_summary_v1` 已是现有主链可见的摘要输入之一（V3 pack 也以其为 allowed summary）。
- 字段更容易收敛（相比环境/路况/零售 OCR 片段），更适合作为第一条 wiring。
- 本轮只做“摘要 → slice”的结构化转换，不引入模型、不引入解释层推断。

---

## D. 本轮接线边界（写死）

- 本轮只做 slice 生产与 stub consume 打通
- 不做中台裁决
- 不做语音派发
- 不做记忆写入
- 不做导航激活

---

## E. 当前最小验证口径（写死）

必须满足：
- 至少有一种真实输入（`risk_summary_v1`）能转成合规 `risk_slice`
- slice 能进入 `vision_consumable_slices_v0`
- consume stub 能观测到它并产出 `vision_mid_platform_consume_stub_v0`
- 语音主链不被污染（不改 route/proposal/dispatch_type）
- `tools/verify_voice_v1_minimal_flow.py` 回归仍通过

---

## 本轮硬约束（继续成立）

### No Fabrication Rule
- 不允许主链自己造 slice（无输入就不写）
- 只能把已有视角摘要转换为合规 slice
- 不补全缺失字段，不做推断性填充

### 统一时空锚点原则
- 本轮不新增任何模块自造的时间/空间字段
- 如未来需要，只能引用统一锚点（本轮不展开）

