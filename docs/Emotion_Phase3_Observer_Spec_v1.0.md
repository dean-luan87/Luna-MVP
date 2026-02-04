# Emotion Phase-3 Observer Spec v1.0 (Frozen)

**文档状态：** 🔒 FROZEN  
**版本标记：** emotion.phase3.v1  
**修改规则：** 仅允许版本号升级，不允许语义扩展

---

## 0. 冻结声明
本文件用于锁死情感引擎 Phase-3 观察层（Observer）的工程语义与职责边界。  
冻结后，任何实现不得超出本文定义；新增字段必须升级 schema_version。

---

## 1. 角色定位（只读观察层）
Emotion Phase-3 是趋势观察层，不是决策器、不是行动器、不是建议器。  
它只描述情绪演化态势，不触发任何干预动作。

---

## 2. 输出结构（冻结）

### 2.1 枚举定义（1:1 迁移）
- **EmoAcceleration**  
  - INCREASING / STABLE / DECREASING / UNKNOWN
- **EmoCurvature**  
  - TOWARD_DISTRESS / STABLE / AWAY_FROM_DISTRESS / UNKNOWN
- **EmoIrreversibility**  
  - REVERSIBLE / LIKELY_IRREVERSIBLE / UNKNOWN

### 2.2 输出结构
```
{
  "acceleration": "INCREASING",
  "curvature": "TOWARD_DISTRESS",
  "irreversibility": "LIKELY_IRREVERSIBLE",
  "schema_version": "emotion.phase3.v1"
}
```

强约束：
- ❌ 不允许输出动作/建议字段
- ❌ 不允许携带决策结论
- ✅ 仅描述性信号

---

## 3. 输入依赖（白名单 / 黑名单）

### 3.1 允许输入（只读历史片段）
最近 N 轮对话的情绪快照（窗口化），例如：
- emotion_label（离散情绪类别）
- valence / arousal（维度值）
- conflict_markers（冲突/攻击性语言标记）
- self_harm_risk_flag（极端情绪标记）

### 3.2 明确禁止输入
- ❌ policy_decision（系统最终策略）
- ❌ authority / abilities（治理层）
- ❌ 咨询师/干预模块输出动作

---

## 4. 计算原则（冻结）
- 不预测“人会怎么想”
- 只做短窗趋势（变化率 / 方向变化 / 不可逆窗口）
- 数据不足/异常 → UNKNOWN（诚实失败）

---

## 5. 与“立场模块”的共存原则
- 立场：解释框架（观点差异）
- Phase-3 Observer：情绪态势（是否加速 / 转向 / 不可逆）
- 决策/干预层：唯一行动输出（Observer 不参与）

---

## 6. 非控制声明（冻结条款）
Emotion Phase-3 outputs are descriptive signals only.  
They must not directly trigger, modify, or override any intervention action.  
Any downstream influence, if ever introduced, must be mediated explicitly by the emotional policy layer, not by direct coupling.  
Emotion Phase-3 must remain read-only with respect to authority, decision, and instinct layers.

---

## 7. 冻结结论
- 仅增加情绪趋势“分辨率”
- 不增加系统权力
- 不改变安全边界
- 为未来因果/情感系统预留接口但不实现
