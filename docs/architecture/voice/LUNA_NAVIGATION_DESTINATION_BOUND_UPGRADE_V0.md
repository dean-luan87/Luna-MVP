# Navigation Destination Bound Upgrade v0（导航目的地 bound 升级专题）

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_UPGRADE_V0.md`  
**性质**：导航主流程下的“destination bound upgrade”专题（只做设计与口径冻结，不做实现）  

上位约束（必须服从）：
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_SUFFICIENCY_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BINDING_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_FACT_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_CONFIRMATION_FACT_V0.md`

并写死（继续成立）：
- **No Fabrication Rule**：不得因为“文本像地点 / 用户说对 / 语义命中 confirm.yes”就构造 `place_id/destination_id/...` 或写出 `destination_bound`。
- **主链事实高于辅助信号**：语义/记忆/视觉只能辅助观察歧义与追问需要，不能替代 bound 升级依据。
- **统一时空锚点原则**：本专题不引入任何模块自造的时间/空间字段（timestamp/坐标/定位）。

---

## A. 专题定位

- 这是导航主流程下的 **destination bound 升级** 专题。
- 当前只讨论：`destination_candidate_v0` + `destination_confirmation_fact_v0` + **绑定依据** 在什么条件下才允许升级为真正的 `destination_bound`。
- 当前不实现：
  - 地图解析 / 地点检索 / POI 搜索
  - 历史记忆补地点
  - 视觉补地点
  - 真实导航启动
  - destination bound 升级代码逻辑（本轮只做设计冻结）

---

## B. 当前问题定义

当前主链已能（工程事实）：
- 在 `proposal.task_action == "start_navigation"` 的语境下：
  - 形成 `destination_candidate_v0`（严格语境：missing_destination 的 start_navigation 追问后，承载用户补充的一句文本）
  - 形成 `destination_confirmation_fact_v0`（严格语境：candidate 已存在后，对“对/是/没错”等最小确认表达做只读评估）
  - 形成 `destination_bound_check_v0`（只读评估：proposal 是否出现显式绑定字段 `place_id/destination_id/target_id/reference_id` + 语义歧义观察）
  - 形成 `destination_sufficiency_eval_v0`（只读评估：proposal 是否已具备显式绑定字段 → 是否“参数充足”）
  - 形成 `navigation_handoff_v0`（只读可观察：当前仍多为 `not_ready: missing_destination`）

但当前缺口（写死）：
- 缺少一套被冻结的“**什么时候允许把 candidate/confirmation/绑定依据 共同材料化为真正的 `destination_bound`**”的规则。
- 断点已从“能否确认”推进到“**能否升级为 handoff 可消费的稳定事实**”。

---

## C. destination_bound_upgrade 的最小定义（极保守）

`destination_bound_upgrade_v0`（bound 升级）指：在严格 start_navigation 语境下，把“候选 + 确认 + 绑定依据”材料化为 **一个可被 future handoff 消费的 `destination_bound` 事实结构**。

升级 **不等于**：
- 有 `destination_candidate_v0`
- 有 `destination_confirmation_fact_v0`
- 文本像地点
- 语义层高置信（包括 `semantic_v2.confirm.yes`）

升级必须至少同时满足（写死最小集）：
1) **存在 destination_candidate_v0**（candidate_present=true 且 candidate_text 非空）  
2) **存在可接受的 destination_confirmation_fact_v0**（确认目标指向当前 candidate，而非新候选/否定/无关）  
3) **存在显式绑定依据或等价的稳定绑定依据**（主链可复核、可被后续模块消费）  
   - v0 口径：优先以 `proposal.place_id / destination_id / target_id / reference_id` 这类 **显式 id 型字段**作为绑定依据  
4) **当前无明显歧义/冲突**（例如 `semantic_v2.ambiguities` 非空或 `requires_followup=true` 只能作为“仍需确认”的辅助观察信号；一旦判定歧义未消除，则不得升级）  
5) **升级后形成 handoff 可消费的稳定字段结构**（见 §F）

---

## D. 升级条件分层（至少三类）

### D1. 明确不能升级（必须停留在 candidate / confirmation）

任一成立即 **不能升级**：
- **只有 candidate**：存在 `destination_candidate_v0`，但没有可接受的 `destination_confirmation_fact_v0`
- **只有 confirmation**：出现确认型话语，但不存在 `destination_candidate_v0`（No Fabrication：不得凭空假设确认对象）
- **没有绑定依据**：proposal 中没有任何 `place_id/destination_id/target_id/reference_id`（或等价可复核字段），仅凭文本/语义/记忆/视觉不得补出 id
- **仍存在歧义/需追问线索未解除**：例如语义辅助观察到 `ambiguities` 或 `requires_followup=true`，或候选本身明显不唯一
- **只有辅助信号“看起来像”**：例如 `semantic_v2.confirm.yes`、历史常去地点、视觉摘要提示；这些都不能替代升级依据

结论（写死）：
- 上述任何场景都不得写出 `destination_bound`，只能停留在 `destination_candidate_v0` / `destination_confirmation_fact_v0` / `destination_bound_check_v0` 的只读观测层。

### D2. “升级前提已具备，但仍不自动升级”的场景（写死）

满足：
- `destination_candidate_v0` 存在
- `destination_confirmation_fact_v0` 存在（确认型）
- 但 **绑定依据仍不足**（缺 id 字段），或仍存在歧义/冲突观察

则：
- 只能视为“升级前提候选已接近”，但 **仍不能写出 destination_bound**
- 需要引入后续“绑定依据生成/注入”的独立机制（不在本专题实现；也不得偷用记忆/视觉/语义猜测补齐）

### D3. 可升级为 bound（未来条件，仍需写死纪律）

当且仅当同时满足：
- `proposal.task_action == "start_navigation"`
- `destination_candidate_v0.candidate_present == true`
- `destination_confirmation_fact_v0.confirmation_ready == true` 且确认目标指向“current destination candidate”
- proposal 中出现 **可复核且非空** 的显式绑定字段（`place_id/destination_id/target_id/reference_id` 之一，或未来被冻结的等价绑定字段）
- 无明显歧义/冲突（歧义未消除不得升级）

才允许升级（future）：
- 写出 `destination_bound`（结构见 §F）
- 供 future handoff 消费

---

## E. 主链事实 vs 辅助信号（分层写死）

### E1. 主链事实候选（允许参与 bound 升级规则判定的材料）

- `proposal.task_action == "start_navigation"`
- `result.metadata["destination_candidate_v0"]`
- `result.metadata["destination_confirmation_fact_v0"]`
- `result.metadata["destination_bound_check_v0"]`（其中的 `binding_key_seen` 是“显式绑定字段是否出现”的主链可复核结果）
- `proposal.place_id / destination_id / target_id / reference_id`（显式绑定字段本体）

### E2. 辅助信号（只能辅助观察，不可替代升级依据）

- `event.metadata["luna_voice_semantic_v2"]`：
  - `intent`（包括 `confirm.yes/no`）
  - `ambiguities`
  - `requires_followup`
- `VoiceV1SessionStateAnchor`（上下文线索）
- 视觉摘要 / V3 输入包
- 历史记忆 / 常用地点

写死结论：
- 辅助信号只能用于“是否仍需确认/是否存在歧义”的观测；不得单独触发升级，也不得用于补齐 binding id。

---

## F. 最小 destination_bound 结构建议（future；只设计不实现）

建议使用极小结构（克制，不做大 schema），例如：

```json
{
  "destination_bound": true,
  "binding_key": "destination_id",
  "binding_value": "dest_123",
  "binding_reason": "explicit_binding_field_present_and_confirmed_by_user",
  "bound_scope": "navigation_destination_bound_upgrade_v0"
}
```

约束（写死）：
- `binding_key/binding_value` 必须来自主链可复核的显式绑定字段（id 型），不得由语义/记忆/视觉推断生成。
- 不引入任何时空字段（timestamp/坐标/定位）。
- `destination_bound` 一旦写出，必须能被 future handoff 直接消费，且可离线复盘其来源（至少通过 `binding_key/binding_reason`）。

---

## G. handoff 消费边界（必须继续写死）

future `navigation_handoff_v0` 的消费纪律（写死）：
- **只能消费 `destination_bound`**（bound fact）。
- **不消费裸 `destination_candidate_v0`**。
- **不消费 `destination_confirmation_fact_v0`**。
- **不消费语义高置信候选/confirm intent**。
- **不消费视觉/记忆线索本身**。

---

## H. 当前明确禁止项（写死）

- 不允许因为 candidate + confirmation 同时存在就**自动**升级为 bound
- 不允许因为语义高置信（包括 `confirm.yes`）就补绑定依据或升级
- 不允许历史记忆直接替代绑定依据
- 不允许视觉摘要直接替代绑定依据
- 不允许把本专题做成地点解析/地点检索系统
- 不允许在本专题里顺手实现真实导航启动

---

## I. 推荐的最小未来落点（只选一个；只做设计不实现）

**唯一推荐落点**：在 `destination_bound_check_v0` 之后，增加一个只读的 `destination_bound_upgrade_eval_v0`。

- **输入（只读）**：
  - `destination_candidate_v0`
  - `destination_confirmation_fact_v0`
  - `destination_bound_check_v0`（尤其是 `binding_key_seen` 与 `needs_confirmation`）
- **输出（只写 metadata）**：
  - `metadata["destination_bound_upgrade_eval_v0"] = { eligible: true/false, reason: ... }`
- **硬边界**：
  - 不写 `destination_bound`
  - 不改 proposal / route / handoff / submit
  - 不接地图/记忆/视觉

为什么选这里：
- 连续性最好：`bound_check` 已把“绑定依据是否出现”与“歧义观察”压成一个最小事实层，upgrade_eval 只需再与 confirmation_fact 做组合判断即可。
- 最不容易失控：先评估 eligible，再由后续单独的 materialization 点决定是否真正写 bound（仍需更上位 gate/确认纪律约束）。

---

## J. 为什么现在还不能真实启动导航（必须单列）

- 现在只有 `destination_candidate_v0` / `destination_confirmation_fact_v0` / `destination_bound_check_v0` 等观测层，还没有 `destination_bound`。
- 当前没有被冻结并实现的“bound 升级规则 materialization”路径（只能评估，不能产出可消费 bound）。
- 当前 `navigation_handoff_v0` 也尚未实现“只消费 bound”契约下的真实执行入口（目前仍是 stub + 松散检查 `proposal.metadata` 文本）。
- 因此不能因为用户说“对”就进入真实导航启动（会违反 No Fabrication 与主链事实优先）。

---

## K. 下一步最小实现建议（只给 1 个方向）

**只建议一个方向**：先实现 `destination_bound_upgrade_eval_v0` 的只读评估器。

- 仅组合已有三层事实：candidate + confirmation_fact + bound_check（binding evidence）
- 输出 “eligible / not eligible + reason”
- 不写 bound、不改 handoff、不启动导航、不接地图/记忆/视觉

