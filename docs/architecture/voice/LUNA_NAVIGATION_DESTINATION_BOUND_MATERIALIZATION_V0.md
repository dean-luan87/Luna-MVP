# Navigation Destination Bound Materialization v0（导航目的地 bound 材料化专题）

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_V0.md`  
**性质**：导航主流程下的“destination_bound materialization”专题（只做设计与口径冻结，不做实现）  

上位约束（必须服从）：
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_SUFFICIENCY_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BINDING_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_FACT_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_CONFIRMATION_FACT_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_UPGRADE_V0.md`

并写死（继续成立）：
- **No Fabrication Rule**：不得把“candidate/confirm/语义高置信”当作可复核绑定 id；不得自动构造 `place_id/destination_id/...`；不得在材料化中偷偷做地点解析/检索。
- **主链事实高于辅助信号**：语义/记忆/视觉只能提供观察性线索，不能替代材料化所需的硬证据。
- **统一时空锚点原则**：材料化结构中不引入任何模块自造的时间/空间字段（timestamp/坐标/定位）。

---

## A. 专题定位

- 这是导航主流程下的 **destination_bound 材料化** 专题。
- 当前只讨论：在什么条件下，允许把现有只读前置链的硬材料——
  - `destination_candidate_v0`
  - `destination_confirmation_fact_v0`
  - `destination_bound_check_v0`
  - `destination_bound_upgrade_eval_v0`
  - 以及 `proposal` 内显式绑定字段
  ——真正写成一个稳定、可被 future handoff 消费的 `destination_bound` 事实位。
- 当前不实现：
  - 地图解析 / 地点检索 / POI 搜索
  - 历史记忆补地点
  - 视觉补地点
  - 真实导航启动
  - destination_bound 的写入实现（本轮只做规则设计冻结）

---

## B. 当前问题定义（写死）

当前导航启动前主线已经形成完整只读前置链（工程事实）：

`start_navigation`
→ `destination_sufficiency_eval_v0`
→ `destination_candidate_v0`
→ `destination_confirmation_fact_v0`
→ `destination_bound_check_v0`
→ `destination_bound_upgrade_eval_v0`

当前断点（写死）：
- 现在缺的不是线程/接线，也不是候选/确认/绑定依据评估，而是：**什么时候可以把“评估层”推进到“主链正式事实层”**，写出 `destination_bound`。

为什么要单独专题（写死理由）：
- 一旦 materialize，就第一次把“观察层”推进到“可被后续执行入口消费的事实层”，风险与越权点显著上升，必须先冻结规则。

---

## C. materialization 的最小定义（极保守）

`destination_bound_materialization_v0` 指：在严格 start_navigation 语境下，把既有硬材料组合为一个 **可复核、可消费** 的结构化 bound fact：
- `destination_bound == true`
- 携带可复核的 `binding_key/binding_value`
- 明确 `binding_reason/bound_scope`

材料化 **不等于**：
- 把 candidate_text 直接写成 bound（文本不是唯一绑定）
- 用户说“对”就写 bound（缺绑定 id）
- `eligible=true` 就写 bound（eligible 只代表“前提候选”，不是“允许写事实”）

材料化必须满足（写死）：
1) **candidate 存在**：`destination_candidate_v0.candidate_present == true`
2) **confirmation 成立**：`destination_confirmation_fact_v0.confirmation_ready == true` 且目标指向当前 candidate
3) **绑定依据存在且可复核**：来自 `proposal.place_id/destination_id/target_id/reference_id` 之一（或未来冻结的等价字段），且非空
4) **upgrade_eval 通过**：`destination_bound_upgrade_eval_v0.eligible == true`
5) **无明显歧义/冲突未解除**：任一“仍需确认/仍需追问”的观察信号存在时，必须禁止材料化（宁可不写）

---

## D. 材料化条件分层（至少三类）

### D1. 明确不能材料化（写死）

任一成立即禁止写出 `destination_bound`：
- 缺 `destination_candidate_v0`
- 缺 `destination_confirmation_fact_v0` 或 `confirmation_ready != true`
- 缺 `destination_bound_check_v0.bound_ready == true`（即缺绑定依据）
- 缺 `destination_bound_upgrade_eval_v0.eligible == true`
- 任一层观察到“仍需确认/仍需追问/明显歧义”（例如 `needs_confirmation==true`、或语义辅助 `ambiguities/requires_followup` 触发）：**禁止材料化**
- 仅有辅助信号（语义/记忆/视觉）“看起来很像”：禁止材料化

### D2. “前提接近但仍不材料化”（写死）

满足：
- candidate + confirmation 都存在
- 但绑定依据缺失或 upgrade_eval 未通过

结论：
- 必须停留在只读观测链，继续要求用户或上游系统提供**显式绑定依据**（不在本专题实现）。

### D3. 可材料化（future 条件，仍需写死纪律）

当且仅当同时满足：
- candidate_present == true
- confirmation_ready == true
- bound_check.bound_ready == true（并能指出 `binding_key_seen`）
- bound_upgrade_eval.eligible == true
- 且不存在任何 “needs_confirmation/ambiguities/requires_followup” 类歧义未解除信号

才允许 materialize（future 实现）：
- 写出 `destination_bound` 结构（见 §F）
- 但仍不代表“立即启动真实导航”（启动需要后续 handoff 消费与执行入口治理）

---

## E. 主链事实 vs 辅助信号（材料化消费纪律）

### E1. 材料化允许消费的硬材料（写死）

- `proposal.task_action == "start_navigation"`
- `destination_candidate_v0`
- `destination_confirmation_fact_v0`
- `destination_bound_check_v0`（尤其 `binding_key_seen`）
- `destination_bound_upgrade_eval_v0`
- `proposal.place_id/destination_id/target_id/reference_id`（绑定 id 本体）

### E2. 只能用于“禁止材料化”的辅助观察（写死）

- `semantic_v2.ambiguities` / `semantic_v2.requires_followup`
- 各层 `needs_confirmation == true`（来自 confirmation_fact / bound_check / bound_upgrade_eval）

写死结论：
- 辅助观察可以“拉闸禁止材料化”，但不能“放行材料化”，更不能补 id。

---

## F. 最小 destination_bound 结构建议（future；只设计不实现）

建议极小结构（克制，不做大 schema）：

```json
{
  "destination_bound": true,
  "binding_key": "destination_id",
  "binding_value": "dest_123",
  "binding_reason": "materialized_from_explicit_binding_field_after_user_confirmation",
  "bound_scope": "navigation_destination_bound_materialization_v0"
}
```

约束（写死）：
- `binding_key/binding_value` 必须来自显式绑定字段（id 型），不得来自文本猜测或语义推断。
- 不引入任何时空字段。
- 不把 candidate_text 写成 binding_value（除非未来冻结“文本可作为唯一绑定”的规则；v0 明确不允许）。

---

## G. handoff 消费边界（继续写死）

- future `navigation_handoff_v0` **只能消费 `destination_bound`**。
- handoff **不得**消费 `destination_candidate_v0`、`destination_confirmation_fact_v0`、`destination_bound_upgrade_eval_v0` 或任何语义高置信/视觉/记忆线索。

---

## H. 当前明确禁止项（写死）

- 不允许把本专题变成地点解析/地点检索系统
- 不允许在材料化中引入地图/历史记忆/视觉作为绑定依据
- 不允许因为 eligible=true 就写 bound
- 不允许自动构造任何 `place_id/destination_id/...`
- 不允许在本专题里顺手实现真实导航启动

---

## I. 推荐的最小未来落点（只选一个；本轮只设计不实现）

**唯一推荐落点**：在 `destination_bound_upgrade_eval_v0` 之后，新增一个独立的 **`destination_bound_materialization_v0`**（materializer）。

输入（只读）：
- `destination_candidate_v0`
- `destination_confirmation_fact_v0`
- `destination_bound_check_v0`
- `destination_bound_upgrade_eval_v0`
- `proposal` 内显式绑定字段

输出（写入事实位）：
- `metadata["destination_bound_v0"] = { ... }`（或同等固定 key；最终命名需与后续 handoff 消费契约一致）

为什么选这里：
- 最连续：upgrade_eval 已把三层硬材料组合成 eligible；materializer 只负责“是否允许写事实位”的最后一道闸门（仍需更保守条件，如 needs_confirmation 必须为 false）。
- 最不易失控：把“评估”和“写事实”隔离成两个模块/阶段，便于冻结与回滚。

---

## J. 为什么现在还不能真实启动导航（写死）

- 当前仍未 materialize 出 `destination_bound`（只有评估层）。
- `navigation_handoff_v0` 尚未实现“只消费 bound 的真实执行入口”，且现状仍有 `proposal.metadata` 文本松散检查（不应视为 bound）。
- 因此不能进入真实导航启动。

---

## K. 下一步最小实现建议（只给 1 个方向）

只建议一个方向（仍先实现只读，不 materialize）：
- 先实现一个 `destination_bound_materialization_eval_v0`（只读）：
  - 明确给出 “能否 materialize / 为什么不能”
  - 把 `needs_confirmation` 作为硬阻断条件
  - 不写 bound，不启动导航

