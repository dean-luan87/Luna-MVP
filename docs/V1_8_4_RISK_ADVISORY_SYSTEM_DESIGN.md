# 1.8.4 危险评估与告知系统设计方案
（Risk Advisory System）

> 版本目标：  
> 构建一个**克制、可靠、可扩展**的危险评估与告知系统  
> ——只提示"危险态势上升"，不推断行为、不放大风险、不做安全承诺。

---

## 一、设计目标（Design Goals）

1. 仅做**危险评估与告知**，不做安全控制  
2. **警告 ≠ 真实危险 ≠ 事故预测**  
3. 只在**危险态势上升**时触发提醒  
4. 基于**空间关系与趋势**，不基于用户行为推断  
5. 为后续「世界模型 × 安全位置评估」预留接口

---

## 二、系统职责边界（硬约束）

### 系统负责
- 评估环境的危险程度
- 判断危险态势是否上升
- 在阈值触发时进行**一次性告知**

### 系统不负责
- 判断用户行为是否正确（坐 / 趴 / 探身）
- 判断用户是否"已经安全"
- 对静态危险进行持续警告
- 推断事故结果（如"会掉下去"）

---

## 三、核心概念分层（三层模型）

### 1. Hazard（环境危险评估层）【1.8.4 实现】

描述"**这个位置本身有多危险**"，与用户行为无关。

- 静态、客观
- 不随时间变化
- 来源：视觉 / 地图 / 规则

示例：
- 水体 + 无护栏 → HazardLevel = 高  
- 水体 + 有护栏 → HazardLevel = 中  
- 普通台阶 → HazardLevel = 低  

---

### 2. Safety Boundary（安全边界层）【接口预留】

描述"**哪些位置被认为是安全的**"。

- 护栏内侧 / 警戒线外 → Safe  
- 越过警戒线 / 护栏外侧 → Unsafe  
- 是否越界是**离散事件**

> 本版本仅预留接口，复杂判断交由后续世界模型。

---

### 3. Risk（态势风险层）【1.8.4 核心】

描述"**危险态势是否在上升**"，  
这是**唯一触发警告的依据**。

---

## 四、危险对象模型（RiskObject）

```json
{
  "risk_id": "lake_edge_001",
  "risk_class": "STATIC",
  "risk_type": "WATER_EDGE",
  "geometry": {
    "type": "LINE",
    "length_m": 25.0
  },
  "hazard_level": 0.8,
  "confidence": 0.9,
  "state": "DORMANT",
  "edge_distance_m": 3.2,
  "edge_trend": "STABLE"
}
```

### geometry 类型说明
- **POINT**：井盖、坑洞
- **LINE**：湖畔、护栏、台阶
- **AREA**：施工区、事故区

---

## 五、RiskLevel 计算模型（最终版）

**不包含时间累积项**

```
RiskLevel = HazardLevel × ProximityFactor × TrendFactor
```

### 因子说明
- **HazardLevel**：环境本身危险程度（静态）
- **ProximityFactor**：与危险边界的距离（越近越高）
- **TrendFactor**：是否在持续靠近危险边界
  - 靠近 → > 1
  - 静止 / 远离 → = 1

**不使用用户行为、不使用时间累积。**

---

## 六、警告触发原则（唯一合法条件）

### 触发任一即可
1. **RiskLevel 在短时间内显著上升**（ΔRisk > 阈值）
2. **越过 SafetyBoundary**（事件型触发，接口预留）

### 不触发的情况
- RiskLevel 长时间保持稳定
- 用户静止在危险区域内
- 危险存在但态势未恶化

**危险存在 ≠ 必须提醒**

---

## 七、警告策略（一次性、边界告知）

### 播报原则
1. 只描述空间关系，不描述行为
2. 只做提醒，不做结论
3. 一次触发，不持续骚扰

### 正确示例
- "您已接近湖边，请注意与边缘保持安全距离。"
- "前方是连续台阶，请注意脚下。"

### 禁止示例
- "有掉下去的危险"
- "请不要趴在护栏上"
- "您现在已经安全了"

---

## 八、危险区内逻辑（关键约束）

### 不再判断
- 是否进入危险区
- 停留时长

### 只判断
- 危险态势是否继续上升

### 允许情况
- 高 Hazard + RiskLevel 稳定 → 不再提醒
- 再次靠近边界 → RiskLevel 上升 → 可再次触发

---

## 九、时间变量的最终角色定义
- ❌ 不用于风险累积
- ❌ 不用于"结束判断"
- ✅ 仅用于：
  - 去抖（防止连续抖动触发）
  - 冷却（同一 RiskObject 的最小提醒间隔）

---

## 十、状态机（最小可用）

| 状态 | 含义 |
|------|------|
| DORMANT | 已感知，不提醒 |
| WARNED | 已触发过一次提醒 |
| COOLDOWN | 冷却期，防重复 |

**无"已安全 / 已结束"状态**

---

## 十一、与世界模型的接口约定（未来）

世界模型可提供：
1. **更精细的 HazardLevel**
   - 护栏有无、高度、完整性
2. **SafetyBoundary 定义**
   - 护栏内外、警戒线
3. **环境结构稳定性判断**

**世界模型只输出结构与属性，不直接参与播报决策。**

---

## 十二、设计精神（一句话）

> 我们评估危险，不预测事故；  
> 我们提醒态势上升，不干扰静态存在；  
> 我们告知边界，不替用户做选择。

---

## 十三、与 v1.8.3 的衔接

### v1.8.3 已有能力
- ✅ `RiskAssessor`：基础风险评估（LV2/LV1）
- ✅ `ThreatAssessment`：威胁语义标注
- ✅ `RiskConfig`：参数化配置
- ✅ `DecisionController`：决策调度（`bypass_speech_gate`, `wait_mode`）

### v1.8.4 新增能力
- ✅ `RiskObject`：危险对象模型
- ✅ `HazardLevel`：环境危险评估
- ✅ `RiskLevel` 计算：HazardLevel × ProximityFactor × TrendFactor
- ✅ 态势上升检测：ΔRisk > 阈值
- ✅ 状态机：DORMANT → WARNED → COOLDOWN
- ✅ 警告策略：一次性、边界告知

### 衔接点
- v1.8.3 的 `assess_risk()` 输出 `RiskResult`
- v1.8.4 的 `evaluate_risk_advisory()` 基于 `RiskResult` 和 `RiskObject` 计算 `RiskLevel`
- v1.8.4 的警告触发基于 `ΔRisk`，而非 `RiskLevel` 绝对值

---

## 十四、实现优先级

### Phase 1：核心模型（必须）
1. `RiskObject` 数据模型
2. `HazardLevel` 计算（基于现有 `RiskConfig`）
3. `RiskLevel` 计算（HazardLevel × ProximityFactor × TrendFactor）
4. 态势上升检测（ΔRisk）

### Phase 2：状态管理（必须）
1. 状态机实现（DORMANT → WARNED → COOLDOWN）
2. 冷却期管理
3. 去抖逻辑

### Phase 3：警告策略（必须）
1. 警告文本生成（只描述空间关系）
2. 一次性触发逻辑
3. 与 `DecisionController` 集成

### Phase 4：接口预留（可选）
1. `SafetyBoundary` 接口定义
2. 世界模型接口约定
3. 扩展点文档

---

## 十五、技术债务与风险

### 技术债务
- ⚠️ `HazardLevel` 计算依赖视觉识别精度（当前为关键词匹配）
- ⚠️ `ProximityFactor` 需要距离估计（当前为 `motion_state.estimated_distance`）
- ⚠️ `TrendFactor` 需要运动趋势判断（当前为 `motion_state.is_moving_towards_edge`）

### 风险
- ⚠️ 误报：RiskLevel 计算不准确导致频繁触发
- ⚠️ 漏报：态势上升检测阈值设置不当
- ⚠️ 性能：RiskObject 管理可能带来内存开销

---

## 十六、测试策略

### 单元测试
- `RiskLevel` 计算正确性
- 态势上升检测（ΔRisk）
- 状态机转换

### 集成测试
- 与 `DecisionController` 集成
- 警告触发时机
- 冷却期管理

### 场景测试
- 接近危险边界（态势上升）
- 静止在危险区域（不触发）
- 远离危险边界（不触发）
- 冷却期内的重复触发（被抑制）

---

## 十七、后续扩展方向

1. **世界模型集成**
   - 更精细的 `HazardLevel` 计算
   - `SafetyBoundary` 定义
   - 环境结构稳定性判断

2. **多危险对象管理**
   - 危险对象优先级
   - 危险对象合并
   - 危险对象生命周期

3. **用户行为学习**
   - 用户对警告的响应
   - 个性化阈值调整
   - 警告频率优化


