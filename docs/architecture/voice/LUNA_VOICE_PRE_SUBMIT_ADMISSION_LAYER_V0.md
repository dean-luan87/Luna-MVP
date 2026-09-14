# Luna Voice — Pre-Submit Admission Layer v0（执行准入层总览）

**文件**：`docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`  
**性质**：已冻结 gate 的小总览（唯一挂点）  
**目标**：把当前已冻结的两个 pre-submit admission gate 的职责、顺序、边界与验证入口收束成一张小地图，作为后续新增 gate 的唯一挂载入口。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  

---

## A. 当前层级定位

- 这是 **pre-submit admission layer** 的总览。  
- 层级位置固定在：  
  - `dispatch_voice_final_text(...)` **之后**  
  - `_maybe_submit_real_output_v1(...)` **之前**  
- 当前作用：在**不改主链裁决**（dispatch_type/route/proposal）的前提下，决定“是否允许进入 submit”。  
- 该层不是：主链裁决器、reply 控制层、白盒/溯源系统、中台审核实现。

---

## B. 当前已存在的 gate（仅 2 个）

### 1) Resource Sufficiency Gate v0

- **负责**：执行资源是否足以支撑继续进入 submit  
- **当前只看**（最小集）：  
  - `battery_ok`  
  - `required_modules_ok`  
- **baseline/freeze**：`docs/architecture/voice/LUNA_RESOURCE_SUFFICIENCY_GATE_V0_BASELINE.md`

### 2) Information Confirmation Gate v0

- **负责**：是否已足够明确到可以执行（引用对象缺失/歧义 → 需确认）  
- **当前只看**（最小集）：  
  - 指代词集合：`这个/那个/这里/那里`  
  - 是否存在唯一绑定事实（v0 极保守：仅 proposal 显式 id 才算绑定）  
- **baseline/freeze**：`docs/architecture/voice/LUNA_INFORMATION_CONFIRMATION_GATE_V0_BASELINE.md`

**明确当前不存在**：Risk Gate、通用 Required Fields Gate、用户协商/确认策略器、中台审批 gate。

---

## C. 当前顺序（写死冻结）

当前执行准入顺序固定为：

1. **Resource Sufficiency Gate v0**（先判“能不能执行”）  
2. **Information Confirmation Gate v0**（再判“是否足够明确到可以执行”）  
3. 若两者都放行，才进入 `_maybe_submit_real_output_v1(...)`

规则：  
- 顺序冻结。后续若要调整顺序，必须专项设计与评审。  
- 不允许新增 gate 后随意插队。

---

## D. 各 gate 的职责边界（写死）

### Resource Sufficiency Gate v0

- **负责**：资源是否足够（电量/必要模块可用性）  
- **不负责**：风险判断、信息完整性、用户协商、引用解析

### Information Confirmation Gate v0

- **负责**：显式指代对象缺失/歧义时阻断 submit 并标记需要确认  
- **不负责**：通用参数缺失、历史记忆补绑定、视觉补绑定、复杂引用解析系统

---

## E. 当前统一硬约束

- **主链裁决不变**：gate 只影响 submit 准入，不改 dispatch_type/route/proposal。  
- **主链事实高于辅助信号**：语义/视觉/shadow/assist 不能替代主链事实成为准入裁决。  
- **No Fabrication Rule 继续成立**：不得脑补缺失条件。  
- **统一时空锚点原则**：不得自造系统级时间戳/空间坐标。  
- gate 只能依据已注入/已存在的事实源，不得假装拥有资源/引用绑定事实。

---

## F. 当前验证入口总表（最小回归入口）

- `tools/verify_voice_resource_gate_v0.py`  
- `tools/verify_voice_confirmation_gate_v0.py`  
- `tools/verify_voice_v1_minimal_flow.py`

改到 gate 落点、顺序、读取方式、submit 准入逻辑时，必须重跑对应脚本。

---

## G. 当前明确不做的事

- 不做 Risk Gate  
- 不做通用 Required Fields Gate  
- 不做用户协商策略器  
- 不做文本 vs 视角冲突处理  
- 不做中台审核实现  
- 不做白盒 / provenance 实现  
- 不把 gate 抽象成大而全框架  

---

## H. 后续新增 gate 的接入原则（流程写死）

任何新增 gate 必须遵循顺序：  

**专题文档 → 最小实现 → baseline/freeze → 纳入本总览**  

禁止：  
- 直接把实验性 gate 插入 admission layer  
- 让辅助信号层（shadow/assist/vision shadow）变成 admission 裁决层  

