# M 层 v0 规格（行为绑定，shadow-only）

## 定位

- **M 层** = 把「G 层选出来的 winner」翻译成「如果要做，会做什么」；当前**只算、不做、不发声（shadow-only）**。
- K = 想干什么；L = 围绕什么对象；**M = 如果真的要干，会采取什么行动形态**。

## 在主线中的位置

```
A Eligibility → B–F 世界与节律 → G Arbitration → K Intent → L Slot
  → M Action Plan（本层，仅写 trace）→ N Outcome（后续）
```

- M 不做决策、不影响仲裁、不触发执行；仅为语义→行为的确定性映射。

## 输入 / 输出（v0）

**输入**（同一条 arbitration 记录）  
- `winner_type`（SAFETY / NAVIGATION / ENV_AWARENESS / TASK_STATE）  
- `k.intent`  
- `l.slot_type`、`l.slot`  
- `context`（只读：level / pal / vc / complexity）

**输出**（ActionPlan，仅写 trace）  
- `action_type`: SAY | WARN | GUIDE | IGNORE | NONE  
- `modality`: VOICE | HAPTIC | VISUAL | NONE  
- `urgency`: LOW | MEDIUM | HIGH  
- `content_hint`: 语义占位字符串或 null  
- `constraints`: 约束 dict（v0 可为空）  
- **`apply_now`**: v0 **恒为 false**（shadow-only）

## 映射规则（v0 最小集）

| 条件 | action_type | modality | urgency | content_hint |
|------|-------------|----------|---------|--------------|
| winner_type == SAFETY | WARN | VOICE | HIGH | safety_alert |
| winner_type == NAVIGATION | GUIDE | VOICE | MEDIUM | navigation_guidance |
| winner_type == ENV_AWARENESS | SAY | VOICE | LOW | environment_observation |
| winner_type == TASK_STATE | SAY | VOICE | LOW | task_state_update |
| 无 winner / intent=NONE | NONE | NONE | LOW | null |

## shadow-only 约束（冻结点）

- **v0 强约束**：`apply_now` 恒为 false；不调用 TTS、不写执行队列、不影响下一 tick。  
- **允许**：写 trace、写 metrics、用于回放/验收/对照。

## Trace 结构

在 arbitration 行中新增 `"m"`，例如：

```json
"m": {
  "action_type": "SAY",
  "modality": "VOICE",
  "urgency": "LOW",
  "content_hint": "environment_observation",
  "constraints": {},
  "apply_now": false
}
```

无 winner 时示例：

```json
"m": {
  "action_type": "NONE",
  "modality": "NONE",
  "urgency": "LOW",
  "content_hint": null,
  "constraints": {},
  "apply_now": false
}
```

## 验收标准（5 条）

1. **出现性**：arbitration > 0 时，M 必定存在。  
2. **一致性**：同一 (winner_type, intent, slot_type) → M 输出稳定。  
3. **不越权**：M 不改变 control / rhythm / engagement。  
4. **安全显式**：SAFETY → WARN + HIGH。  
5. **shadow-only**：`apply_now` 全为 false。

满足即视为 M v0 封板。

## 实现与验收

- 实现：`intervention/action_mapper_m_v0.py`（`ActionMapperM_v0.decide`）。  
- 接入：main 在两处写 arbitration 时同时计算 M 并传入 `log_arbitration_event(..., m=m_result.to_trace_dict())`。  
- 验收：`python3 tools/check_kl_trace.py logs/a3_trace.jsonl` 可查看含 m 的条数及 apply_now 是否全为 false。
