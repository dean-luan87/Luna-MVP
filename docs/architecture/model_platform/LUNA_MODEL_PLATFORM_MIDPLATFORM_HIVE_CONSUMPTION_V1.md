# Luna 中台如何消费蜂巢建议 v1

> 权力关系：**蜂巢**负责评分与建议；**中台**负责消费建议、做治理决策；**个体 Luna**不参与全局模型决策；**图书馆**不直接改线上。  
> 蜂巢不是上线器，**中台才是执行治理器**。  
> 配套：`LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md`、`LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`、宪法 **第十三条**。

---

## 一、总原则

**原则：蜂巢建议不是命令，中台消费不是照单全收。**

蜂巢可以说：

- 某模型该降级  
- 某模型该限域  
- 某模型该灰度试跑  

但中台**不能**因蜂巢一句建议就直接生效。

中台必须先判断：

1. 建议是否合规  
2. 建议是否有足够证据  
3. 建议是否需要影子验证  
4. 建议是否触发人工确认  
5. 建议是否会影响主链安全  

---

## 二、中台消费蜂巢建议的四层处理链

中台收到蜂巢建议后，**固定**走 4 层。

### 1. 接收层

**作用**

- 收下蜂巢建议对象  
- 校验结构完整性  
- 记录建议来源  

**输入对象**：`Hive Model Recommendation`（见 `LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`）

**输出对象**：**Recommendation Intake Record**

**本层只解决**：这条建议是不是**合法格式的建议**。

**本层不解决**：对不对、要不要执行。

---

### 2. 审核层

**作用**

- 检查建议是否违反中台治理规则  
- 检查是否越权  
- 检查是否与当前运行状态冲突  

**审核问题**包括但不限于：

- 建议对象是否是**已注册**模型  
- 推荐动作是否在**允许范围**内  
- 是否触发**一票否决**规则  
- 是否与当前**主链状态**冲突  
- 是否需要**影子验证**  

**本层解决**：这条建议有没有**资格**进入决策层。

---

### 3. 决策层

**作用**

- 决定采纳、部分采纳、延后、拒绝  
- 决定采用哪种执行模式  

**可选决策结果**（建议固定枚举）：

| 结果 | 含义 |
|------|------|
| `accept_shadow_only` | 仅采纳为 shadow |
| `accept_partial` | 部分采纳 |
| `accept_with_constraints` | 带约束采纳 |
| `defer_for_more_data` | 延后（补数据） |
| `reject` | 拒绝 |

**本层解决**：中台**准备怎么对待**这条建议。

---

### 4. 执行层

**作用**

- 真正修改中台治理配置  
- 发起灰度、限域、降级、熔断等  
- **写入变更记录**  

**执行动作**包括但不限于：

- 调整模型优先级  
- 修改 `allowed_task_domains`  
- 开启 shadow only  
- 从主链移出  
- 改为 backup  
- 触发回退  

**本层解决**：已采纳的建议如何**安全落地**。

---

## 三、蜂巢建议的五种消费结果

中台对单条建议的终态**不应**只有「采纳 / 拒绝」两种；建议固定 **5 类**：

| # | 结果 | 适用场景 |
|---|------|----------|
| 1 | **全量采纳** | 风险低、证据充分、不影响主链安全；已在影子或历史中验证过。例：experiment → backup |
| 2 | **带约束采纳** | 方向对但不能完全放开；须加限制。例：仅某任务域、仅 shadow、仅后台 |
| 3 | **部分采纳** | 一部分合理、一部分过激。例：同意 `restrict_scope`，不同意直接退役 |
| 4 | **延后采纳** | 样本不足、证据不够、需继续观察。例：再看一周、先补 shadow 数据 |
| 5 | **明确拒绝** | 越权、证据不足、与主链安全冲突、明显系统风险 |

---

## 四、中台判断维度（至少 6 维）

| 维度 | 看什么 |
|------|--------|
| **1. 建议合法性** | `recommendation_type` 是否合法；`suggested_action` 是否允许；`suggested_constraints` 是否可执行 |
| **2. 证据充分性** | 样本量、时间范围；是否仅来自单一个体；是否有图书馆记录支持 |
| **3. 风险等级** | 是否影响主链、实时能力、错误面 |
| **4. 回退可行性** | shadow 易撤回；直接换主模型难撤回 |
| **5. 当前运行状态兼容性** | 如主链已在降级态，是否不宜再切模型 |
| **6. 策略优先级** | 高优先级风控 vs 低成本优化，处理强度不同 |

---

## 五、中台执行动作清单（固定 8 种）

中台最终动作须**预定义**，不得自由发挥。

| # | 动作 | 说明 |
|---|------|------|
| 1 | **Promote** | experiment / shadow → backup 或特定域主模型候选 |
| 2 | **Degrade** | primary → backup / shadow / background_only |
| 3 | **Restrict Scope** | 收紧任务域、禁止前台、仅图书馆后台等 |
| 4 | **Expand Scope** | 扩大范围但**不能**一步无限放开；如单域→双域、后台→shadow |
| 5 | **Force Shadow** | 强制仅影子，不准主链生效 |
| 6 | **Retire** | 停止调用，退役/废弃 |
| 7 | **Tune Governance** | 不改模型本体，改治理：timeout、schema、clarification、fallback 条件 |
| 8 | **Observe More** | 暂不动模型，继续采集 |

---

## 六、Model Governance Decision Record（治理决策记录）

消费建议后**必须留痕**，否则蜂巢建议不可追踪。

### 最小字段

| 字段 | 说明 |
|------|------|
| `decision_record_id` | 决策记录唯一标识 |
| `recommendation_id` | 关联蜂巢建议 |
| `model_id` | 模型 |
| `decision_result` | 与第三节五类结果对齐或可映射 |
| `decision_reason` | 原因 |
| `decision_constraints` | 中台实际施加的约束 |
| `decision_timestamp` | 时间 |
| `effective_scope` | 生效范围（如 shadow_only） |
| `rollback_plan` | 回滚方案 |
| `requires_followup_review` | 是否需复核 |
| `notes` | 备注 |

**可查**：某条建议是否采纳、为何、加了何限制、能否回滚。

---

## 七、中台消费红线（须更谨慎）

| 红线 | 要求 |
|------|------|
| **1. 主链主模型切换** | 不得直接全量采纳；须至少影子验证**或**人工确认 |
| **2. fallback 路径变更** | 不能直接改；影响底线能力 |
| **3. 安全规则放宽** | 减少 schema、减少 clarification、放宽风险阻断等 — **默认拒绝**，除非强证据与专项评审 |
| **4. 跨主体权限扩张** | 如图书馆后台模型进个体主链 — **高等级审核** |

---

## 八、闭环顺序（写死）

1. 个体 Luna 使用模型  
2. 白盒记录  
3. 图书馆提炼  
4. 蜂巢评分与生成建议  
5. **中台消费建议**  
6. 中台执行治理动作  
7. 新状态再回流个体 Luna  

**关键点**：蜂巢**不直接**碰个体 Luna；**必须**经中台。链断则模型治理乱。

---

## 九、最小 JSON 示例

### Recommendation Intake（接收层）

```json
{
  "recommendation_id": "hmr_001",
  "model_id": "voice_task_parse_openai_v1",
  "recommendation_type": "restrict_scope",
  "intake_status": "accepted_for_review",
  "intake_timestamp": "2026-04-01T12:00:00+08:00"
}
```

### Model Governance Decision Record

```json
{
  "decision_record_id": "mgdr_001",
  "recommendation_id": "hmr_001",
  "model_id": "voice_task_parse_openai_v1",
  "decision_result": "accept_with_constraints",
  "decision_reason": "timeout risk is high; model allowed only in shadow mode",
  "decision_constraints": {
    "mainline_forbidden": true,
    "shadow_only": true,
    "allowed_task_domains": ["long_voice_task_parse"]
  },
  "effective_scope": "shadow_only",
  "rollback_plan": "revert to previous registry state",
  "requires_followup_review": true
}
```

---

## 十、最短可执行规则（5 条）

1. 蜂巢建议**不得直接生效**  
2. 中台**必须**审查蜂巢建议  
3. 中台可全量采纳、带约束采纳、部分采纳、延后、拒绝  
4. 涉及主链、fallback、安全放宽的建议须**高等级处理**  
5. 所有消费决定**必须留痕、可回滚**  

---

## 十一、一句话收束

**蜂巢负责提出「模型该怎么变」，中台负责决定「模型能不能这么变、何时这么变、以什么限制条件这么变」。**

至此，与注册卡、任务卡、职责矩阵、蜂巢评分、蜂巢建议形成**完整闭环**。

---

## 下一步

- **已完成**：`LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`（宪法第十四条）；**全景总表** `LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md`。
