# Luna 蜂巢评分记录模板 + 评分结果模板 v1

> 与 `LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md`、宪法 **第十三条** 配套。  
> **目标**：蜂巢评分有固定输入、固定输出；中台可消费建议；**蜂巢不直接改线上**。

---

## 一、蜂巢评分体系的最小对象（3 个）

| 对象 | 英文名 | 回答 |
|------|--------|------|
| 蜂巢评分输入包 | **Hive Model Score Input Pack** | 拿什么来评分 |
| 蜂巢评分记录 | **Hive Model Score Record** | 这次评分得出了什么结论 |
| 蜂巢建议对象 | **Hive Model Recommendation** | 基于评分，建议中台怎么做 |

三者齐备后：

- 图书馆能喂数据  
- 白盒能提供留痕  
- 中台能接建议  
- **个体 Luna 不参与评分本体**  

---

## 二、Hive Model Score Input Pack（输入包）

蜂巢评分时吃的**原料包**；**不**生产新结论，只聚合来源。

### 最小字段

| 字段 | 说明 |
|------|------|
| `score_input_pack_id` | 输入包唯一标识 |
| `model_id` | 模型 |
| `model_version` | 版本 |
| `score_scope` | 见下 |
| `time_range` | 时间边界（必带） |
| `source_usage_records` | 引用 Usage 集合 |
| `source_quality_records` | 引用 Quality 集合 |
| `source_governance_records` | 引用 Governance 集合 |
| `source_library_records` | 图书馆记录（可选） |
| `source_whitebox_summaries` | 白盒摘要（可选） |
| `sample_size` | 样本量（**必带**） |
| `aggregation_note` | 聚合说明 |

### `score_scope`（评分范围）

| 取值 | 含义 |
|------|------|
| `task_specific` | 如只评「长语音任务拆解」 |
| `domain_specific` | 如只评「视觉语义」 |
| `global` | 全局表现 |

### `time_range`

防止评分无边界漂移。须明确例如：

- 最近 24 小时  
- 最近 7 天 / 30 天  
- 某次灰度期间  

### `sample_size`

**无样本量，评分无意义。**

### 输入包来源（聚合自）

1. **Usage Record** — 模型被怎么用  
2. **Quality Record** — 输出质量怎样  
3. **Governance Record** — 是否触发治理问题  
4. **Library Record** — 图书馆是否提炼共性问题  
5. **Whitebox Summary** — 白盒是否观察到明显异常模式  

---

## 三、Hive Model Score Record（评分记录）

蜂巢打分后的**结构化产物**；不是一句「80 分」。

### 最小字段

| 字段 | 说明 |
|------|------|
| `score_record_id` | 记录唯一标识 |
| `model_id` | 模型 |
| `model_version` | 版本 |
| `score_scope` | 与输入包一致 |
| `score_timestamp` | 评分时刻 |
| `overall_score` | 总分（**不可单独使用**） |
| `dimension_scores` | 六维，见下 |
| `score_explanations` | **结构化**原因，非仅自由文本 |
| `risk_flags` | 风险标记 |
| `positioning_result` | 定位建议（非最终执行动作） |
| `comparison_reference` | 对比参照（可选） |
| `confidence_level` | 蜂巢对本次结论的置信度 |
| `notes` | 备注 |

### `dimension_scores`（固定 6 维）

- `stability_score`  
- `quality_score`  
- `latency_score`  
- `cost_score`  
- `governance_friendliness_score`  
- `evolvability_score`  

### `score_explanations`（结构化示例）

- timeout 高  
- validator 通过率低  
- mixed 保留差  
- 非法映射偏多  
- fallback 率过高  

### `risk_flags`（示例）

- `high_timeout_risk`  
- `schema_instability_risk`  
- `governance_bypass_risk`  
- `cost_burst_risk`  

### `positioning_result`（建议固定枚举）

| 取值 | 含义 |
|------|------|
| `primary_candidate` | 主模型候选 |
| `backup_candidate` | 备份候选 |
| `shadow_only` | 仅 shadow |
| `background_only` | 仅后台 |
| `deprecated_candidate` | 淘汰候选 |

**说明**：此为蜂巢**定位建议**，不是中台已执行动作。

### `confidence_level`

样本少、新接入模型等场景须**低置信度**观察，避免乱给高结论。

---

## 四、Hive Model Recommendation（建议对象）

蜂巢给**中台**的建议输出；**不等于自动生效**。

### 最小字段

| 字段 | 说明 |
|------|------|
| `recommendation_id` | 建议唯一标识 |
| `model_id` | 模型 |
| `recommendation_type` | 见下 |
| `recommendation_priority` | 优先级 |
| `recommendation_reason` | 原因 |
| `based_on_score_record_id` | 关联的评分记录 |
| `suggested_action` | 建议动作描述 |
| `suggested_constraints` | 建议约束（结构化） |
| `requires_human_review` | 是否需人工 |
| `requires_shadow_validation` | 是否需 shadow 验证 |
| `notes` | 备注 |

### `recommendation_type`（建议固定）

| 取值 | 含义 |
|------|------|
| `promote` | 晋升 |
| `degrade` | 降级 |
| `restrict_scope` | 限域 |
| `keep_observing` | 继续观察 |
| `retire` | 退役 |
| `optimize_prompt` | 优化 prompt |
| `optimize_routing` | 优化路由 |
| `optimize_schema_contract` | 优化 schema 契约 |

### `suggested_action`（示例）

- 进入主链灰度  
- 从主链降为备份  
- 仅允许某类任务调用  
- 仅允许图书馆后台使用  
- 停止面向用户  
- 增加 validator 约束  
- 收紧 timeout  

### `suggested_constraints`（示例）

- `allowed_task_domains`  
- `max_timeout_ms`  
- `mainline_forbidden: true`  
- `shadow_only: true`  
- `background_only: true`  

---

## 五、蜂巢评分记录文档模板（正文 7 段）

每张 **Hive Model Score Record** 正文建议按以下结构书写：

1. **评分对象** — 模型名、版本、评分范围、评分周期  
2. **样本信息** — 样本数、来源模块、来源任务域、是否含灰度样本  
3. **六维评分** — 稳定性、质量、时延、成本、治理友好度、可演化性  
4. **关键问题摘要** — 最拉分问题、最严重风险、是否存在一票否决  
5. **模型定位建议** — 主模型候选 / 备份 / shadow / 后台 / 淘汰  
6. **优化建议** — prompt、路由、schema、fallback、任务域收缩  
7. **结论置信度** — 高 / 中 / 低  

---

## 六、Score Result Summary（给中台的短结论）

蜂巢给中台的结果宜**短**，便于消费。

### 固定字段

| 字段 | 说明 |
|------|------|
| `overall_score` | 总分（仍须结合明细） |
| `positioning_result` | 定位建议 |
| `top_3_issues` | 三大问题 |
| `top_3_strengths` | 三大优势 |
| `primary_recommendation` | 一条主建议 |
| `confidence_level` | 置信度 |

即：**中台可读的摘要层**，与完整 `Hive Model Score Record` 并存。

---

## 七、一票否决项（5 条）

总分**不能**掩盖致命问题。以下任一条成立时，**即使其它维度尚可，也不得**作为**主模型**：

| # | 否决项 |
|---|--------|
| 1 | schema 不稳定 |
| 2 | timeout 率过高 |
| 3 | governance bypass 风险 |
| 4 | 非法映射率过高 |
| 5 | fallback 率长期过高 |

实现上应在 `score_record` / `risk_flags` 中可判定，并驱动 `positioning_result` 不得为「主链主用」语义。

---

## 八、蜂巢 vs 中台：如何作用（写死）

| 蜂巢做 | 中台做 |
|--------|--------|
| 评分 | 灰度 |
| 定位建议 | 升级 / 降级 |
| 优化建议 | 限域 |
| 风险提示 | 熔断 |
| | 退役 |

**蜂巢给建议，中台给决定。**

---

## 九、评分结果如何回流图书馆

评分**不只**给中台；**图书馆**须可消费：

- 某模型在 mixed 输入上持续差  
- 某模型在 clarification 上共性缺陷  
- 某模型在某任务域稳定超时  

沉淀为：

- 图书馆经验条目  
- 经验包  
- 测试用例建议  

**蜂巢评分记录须可被图书馆引用**（如 `score_record_id`、摘要字段）。

---

## 十、评分结果如何对白盒可见

白盒**不**展示全部评分细节，但至少展示：

- 当前模型**最近一次**蜂巢定位结果  
- 是否标记为**高风险**  
- 是否处于观察 / 降级 / shadow 状态  
- **关键问题摘要**（短）  

使用户/开发理解：**模型不是天然可信**；当前**治理状态**可感知。

---

## 十一、最小 JSON 示例

### Hive Model Score Record

```json
{
  "score_record_id": "hmsr_001",
  "model_id": "voice_task_parse_openai_v1",
  "model_version": "v1",
  "score_scope": "task_specific",
  "score_timestamp": "2026-04-01T10:00:00+08:00",
  "overall_score": 72,
  "dimension_scores": {
    "stability_score": 68,
    "quality_score": 79,
    "latency_score": 61,
    "cost_score": 74,
    "governance_friendliness_score": 83,
    "evolvability_score": 77
  },
  "risk_flags": [
    "high_timeout_risk"
  ],
  "positioning_result": "backup_candidate",
  "confidence_level": "medium"
}
```

### Hive Model Recommendation

```json
{
  "recommendation_id": "hmr_001",
  "model_id": "voice_task_parse_openai_v1",
  "recommendation_type": "restrict_scope",
  "recommendation_priority": "high",
  "recommendation_reason": "timeout rate is too high for real-time mainline use",
  "based_on_score_record_id": "hmsr_001",
  "suggested_action": "allow only background_analysis_or_shadow",
  "suggested_constraints": {
    "mainline_forbidden": true,
    "shadow_only": true
  },
  "requires_human_review": false,
  "requires_shadow_validation": true
}
```

### Score Result Summary（给中台）

```json
{
  "overall_score": 72,
  "positioning_result": "backup_candidate",
  "top_3_issues": [
    "high_timeout_rate",
    "p99_latency_spike",
    "mixed_preserve_regression"
  ],
  "top_3_strengths": [
    "high_validator_pass",
    "strong_governance_compliance",
    "stable_schema_output"
  ],
  "primary_recommendation": "restrict_scope_shadow_only_until_latency_improves",
  "confidence_level": "medium"
}
```

---

## 十二、一句话收束

**蜂巢评分记录解决「怎么评分」，蜂巢建议对象解决「评分后建议怎么表达」**；二者一起构成模型中台的全局评估与优化输入，但**都不直接替代中台裁决**。

---

## 下一步

- **已完成**：`LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md`。  
- **下一档**：见 `LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`、`LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md`。
