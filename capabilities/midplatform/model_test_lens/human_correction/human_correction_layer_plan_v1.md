# Human Correction Layer V1 — Planning Document

**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-Planning-v1-001`  
**Layer ID:** `HumanCorrectionLayerV1`  
**Status:** Planning only（本阶段不实现 UI、不跑模型、不修改 envelope / runner）

## 上游

- Luna Observation Lens V1 Closure GO  
- `LunaObservationLensV1TemplateStandard`  
- `TestBoardProtectedArtifactRuleV1`

## 核心定义

**Human Correction Layer（人工指错层 / 人工纠错层）** 是 Luna 观察镜中让用户对模型结果进行结构化指错的入口。

用户流程：

```
看 HUD 结果 → 点对象胶囊 / 画面区域 / 右侧判断
→ 标记「这里有问题」→ 选择错误类型 → 写一句修正说明
→ 保存为 correction record
```

产出进入：

- correction candidate  
- review evidence  
- test improvement signal  
- future training / prompt / adapter / model eval candidate  

**不是：** 直接修改模型结果、把用户说法写成事实、自动训练数据、自动 ground truth。

## 第一版纠错类型（10 类）

| correction_type | 中文 | MobileSAM 优先级 |
|-----------------|------|------------------|
| false_positive | 误识别 | 中 |
| false_negative | 漏识别 | **高** |
| wrong_label | 标签错误 | **高** |
| boundary_inaccurate | 边界不准 | **高** |
| confidence_mismatch | 置信度不合理 | 中 |
| task_relevance_error | 任务相关性错误 | **高** |
| risk_assessment_error | 风险判断错误 | 中 |
| recommendation_error | 建议不合理 | 中 |
| duplicate_or_overlapping_detection | 重复/重叠识别 | 低 |
| unclear_need_review | 不确定需复核 | 中 |

MobileSAM 场景重点：**漏识别、区域不准、标签不可信、任务相关性错误、需 Detection/OCR 复核**。

## UI 集成规划（执行阶段，本阶段仅规划）

**不得改变 Luna Observation Lens V1 主体布局。**

| 入口 | 位置 | 行为 |
|------|------|------|
| 对象胶囊 | chip 尾部 `[指错]` | 预选 object target |
| HUD 画面 | 点击框/mask/编号 | 右侧出现「标记问题」 |
| 空白区域 | 点击画面空白 | 标记「漏识别」 |
| 右侧面板 | 底部 `[指出问题]` | 对事实/风险/建议指错 |
| 底部 Drawer | 新增「纠错」tab | 默认折叠；列表/编辑/导出 |

开发者模式可查看 correction record JSON；默认用户不可见 raw JSON。

## Schema 产物

| 文件 | 用途 |
|------|------|
| `human_correction_record_schema_v1.json` | 纠错记录结构 |
| `human_correction_target_schema_v1.json` | 纠错目标指向 |
| `human_correction_feedback_taxonomy_v1.json` | 类型 / 严重度 / 原因假设 |
| `human_correction_training_signal_schema_v1.json` | 训练/复测候选信号 |
| `human_correction_types_v1.py` | Python 枚举与边界常量 |

## 边界（强制）

### 禁止

- 纠错直接覆盖模型输出  
- 纠错直接修改 envelope  
- 纠错写 fact / semantic / registry  
- 纠错触发 runtime / output adapter / navigation / speech  
- 纠错自动进入训练或成为 reward / ground truth  
- 删除原始模型输出或 TestBoard  

### 允许

- 生成 correction candidate  
- 生成 training signal / hard case / regression test candidate  
- 写 TestBoard（protected / non-deletable）  
- 导出 correction JSON  
- 开发者模式查看 record  

## TestBoard 关系

每条 correction session 必须关联 TestBoard：

- `correction_session_record`  
- `correction_record`  
- `correction_summary`  
- `correction_artifact_refs`  

## Future Training / 强化学习

Human Correction Layer 产生：

- `training_signal_candidate`  
- `hard_case_candidate`  
- `regression_test_candidate`  
- `failure_pattern_candidate`  

进入训练或强化前必须经过：

1. owner review  
2. sensitive data review  
3. data quality review  
4. task relevance review  
5. consent review（如涉敏感数据）  

## 下游：中台纠错分析（Single Model Interaction Validation 对齐）

原始纠错 **不得** 直接进入训练管线。须经：

```
Human Correction Raw → Midplatform Analysis → Correction Taxonomy → Routing Decision
```

归因四类：模型问题 / 任务策略 / 关注度优先级 / 用户偏好（+ 环境限制）。

详见：
- `schemas/human_correction/correction_attribution_taxonomy_v1.json`
- `schemas/human_correction/correction_routing_policy_v1.json`
- `human_correction/correction_midplatform_analyzer_v1.py`

## 下游执行阶段

**Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-UI-Execution-And-Post-Review-v1-001**

在对象胶囊、HUD、右侧面板、底部纠错 drawer 实现「指错」入口。

## 引用

- `schemas/human_correction/human_correction_record_schema_v1.json`  
- `governance_standards/.../human_correction_layer_governance_standard_v1.md`  
- `standards/ui/luna_observation_lens_v1_template_standard.md`
