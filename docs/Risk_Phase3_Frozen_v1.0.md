📄 Risk Phase-3（Acceleration / Curvature）

冻结设计文档 v1.0

文档状态：🔒 FROZEN  
生效版本：Risk Layer v3  
最后修改：仅允许版本号升级，不允许语义扩展

---

## 0. 冻结声明（必须先读）

本文件用于锁死 Risk Phase-3 的工程语义与职责边界。  
在本文件冻结前，不允许进入 Phase-3 工程实现。

冻结后：
- 任何 Phase-3 的实现 不得超出本文定义  
- 任何新增字段 / 行为 必须升级 schema_version

---

## 1. Phase-3 的唯一目标（不可变）

Phase-3 的目标不是预测未来，也不是做决策，而是：

判断风险是否正在以“不可忽略的趋势”恶化。

Phase-3 只回答一个问题：

如果当前态势继续，风险是不是正在更快、更难逆转地逼近？

---

## 2. Phase-3 在系统中的位置（冻结）

World Snapshot（事实）  
   ↓  
Risk Phase-1（静态风险）  
   ↓  
Risk Phase-2（相对速度 / VO）  
   ↓  
Risk Phase-3（趋势感知）  
   ↓  
【只写入 bc_snapshot / DebugView / RA-View】

严格禁止：
- ❌ Phase-3 不得影响 C 决策  
- ❌ Phase-3 不得影响 BC 裁决  
- ❌ Phase-3 不得影响 Authority  
- ❌ Phase-3 不得写回 system_snapshot

---

## 3. Phase-3 的输入约束（冻结）

### 3.1 允许输入（仅限）

Phase-3 只允许读取：
- Phase-2 Risk 输出：
  - risk.present
  - risk.level
  - risk.time_to_risk
  - risk.vo.*
- 最近 N 帧 Risk 历史（N ∈ [3,5]）

### 3.2 明确禁止输入
- ❌ decision / selected_result / reason  
- ❌ authority / abilities  
- ❌ c_decision  
- ❌ 模型输出 / 世界模型原始感知  
- ❌ 情绪 / 意图 / 因果信息

---

## 4. Phase-3 的子模块（冻结为 3 个）

### 4.1 Risk Acceleration（风险加速度）

定义  
判断风险逼近速度是否在加快。

计算  

Δt = time_to_risk(t-1) - time_to_risk(t)  
acc = Δt / Δtime

输出枚举（冻结）
- INCREASING
- STABLE
- DECREASING
- UNKNOWN

规则
- 单帧异常 → 忽略  
- 波动过大 → UNKNOWN  
- 数据不足 → UNKNOWN

---

### 4.2 Curvature Toward Risk（路径曲率趋势）

定义  
判断运动方向是否“越来越指向风险区域”。

输出枚举（冻结）
- TOWARD_RISK
- STABLE
- AWAY_FROM_RISK
- UNKNOWN

约束
- 不做完整轨迹预测  
- 不推断他方意图  
- 只判断趋势方向

---

### 4.3 Irreversibility Hint（不可逆提示）

定义  
判断风险是否已进入“物理上难以缓解”的阶段。

输出枚举（冻结）
- REVERSIBLE
- LIKELY_IRREVERSIBLE
- UNKNOWN

允许触发条件（满足任一）
- 剩余时间 < 最小制动时间  
- time_to_risk 连续下降 + 速度上升  
- 可用转向不足以脱离风险区

---

## 5. Phase-3 的输出结构（冻结）

```
"risk": {
  "present": true,
  "level": "HIGH",
  "time_to_risk": 1.8,
  "vo": {...},
  "phase3": {
    "acceleration": "INCREASING",
    "curvature": "TOWARD_RISK",
    "irreversibility": "LIKELY_IRREVERSIBLE",
    "schema_version": "risk.phase3.v1"
  }
}
```

强 invariant
- ❌ 不允许新增字段  
- ❌ 不允许输出动作 / 建议  
- ❌ 不允许修改 risk.level  
- ❌ 不允许覆盖 Phase-2 结果

---

## 6. 失败哲学（冻结）

情况 | 行为
--- | ---
数据不足 | UNKNOWN
噪声过大 | UNKNOWN
异常 | UNKNOWN
不确定 | UNKNOWN

Phase-3 宁可沉默，不可误导。

---

## 7. 与 C 本能层的隔离条款（冻结）

### 7.1 职责区分
- C：即时本能反射（Stop / Hold / Takeover）
- Phase-3：趋势观察（不触发动作）

### 7.2 工程强约束
- CController.decide() 不得读取 risk.phase3  
- system_snapshot 不得包含 risk.phase3

示例断言：

```
assert "phase3" not in system_snapshot.get("risk", {})
```

---

## 8. Phase-3 的非目标声明（冻结）

Phase-3 不是：
- ❌ 预测系统  
- ❌ 决策系统  
- ❌ 因果推理系统  
- ❌ 行为规划系统

Phase-3 是：

短时风险趋势感知层（Trend-Only）

---

## 9. 冻结结论
- Phase-3 只增加风险“分辨率”
- 不增加系统权力
- 不改变安全边界
- 为未来因果 / 情感系统预留接口但不实现

本文档冻结后，方可进入 Phase-3 工程实现。

---

## 10. Phase-3 非控制声明（冻结条款）

**Non-Control Declaration (Phase-3)**  
Phase-3 outputs are descriptive safety signals only.  
They must not directly trigger, modify, or override any control action.  
Phase-3 must not emit STOP / HOLD / TAKEOVER or equivalent action semantics.  
Any downstream influence, if ever introduced, must be mediated explicitly by BC policy, not by direct coupling.  
Phase-3 must remain read-only with respect to authority, decision, and instinct layers.
