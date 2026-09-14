# Phase-Fusion-001 — Map × Vision × Memory Conflict Policy v0（冲突策略冻结）

**目的**：写死地图、视角、记忆冲突时的优先级与保守处理规则，确保“实时视角风险不得被地图或记忆覆盖”，且冲突只产生候选不触发执行。  
**性质**：policy；candidate-only；不放权。  

---

## 1) 写死的优先级规则（必须全部成立）

1. **Vision risk beats map convenience**  
   - 若 `vision_anchor_signal.risk_anchor` 表示高风险，则不得因为地图路线正常而继续推进（必须输出 `stop/slow_down/ask_for_help` 等候选）。
2. **Vision passability beats stale memory**  
   - 若记忆认为可通行，但当前视角显示不可通行/风险高，以视角为准。
3. **Map guides macro route only**  
   - 地图只指导目标方向与宏观路径，不直接决定局部通行。
4. **Memory optimizes repeated tasks only**  
   - 记忆只作为重复任务优化候选，不得覆盖实时风险信号。
5. **Conflict produces candidate, not execute**  
   - 冲突处理只输出 `fusion_decision_candidate`，且 `allows_execute_now=false`。
6. **Low confidence degrades**  
   - 任一核心来源低置信且影响安全时，输出 `conservative_degraded` 或 `need_human_help` 候选。

---

## 2) 冲突类型枚举（v0）

- `map_vs_vision`
- `memory_vs_vision`
- `map_vs_memory`
- `multi_source_conflict`
- `none`

---

## 3) 冲突解决输出要求（v0）

每次冲突解决必须输出：
- `conflict_detected=true`
- `conflict_type` 命中上述枚举
- `selected_basis` ∈ {`vision_anchor`, `map_macro_constraint`, `memory_optimizer`, `conservative_degraded`, `need_human_help`}
- `candidate_action_type`（continue/slow_down/stop/ask_for_help/reroute_candidate/orientation_check/wait）
- `reason_codes`（至少包含冲突来源与保守性原因）
- `allows_execute_now=false`（硬写死）

---

## 4) 明确禁止（Hard Denylist）

以下任一出现即 no-go：
- 地图或记忆覆盖实时高风险视角信号（unsafe override）
- 冲突不可识别（conflict_detected=false 但实际存在冲突）
- 低置信度强行推进 `continue`
- 任何 `allows_execute_now=true` 或等价执行放权语义

