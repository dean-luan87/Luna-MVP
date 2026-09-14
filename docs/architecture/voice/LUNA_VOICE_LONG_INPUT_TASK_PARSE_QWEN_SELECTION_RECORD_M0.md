# 长语音任务拆解（long_voice_task_parse）— Qwen 选型记录 M0（可审计）

## 结论（定案）

- **当前主选（primary_candidate）**：`qwen-plus`
- **速度型备选（backup_candidate）**：`qwen-turbo`
- **淘汰（deprecated_candidate）**：`qwen3.5-flash`

## 范围（写死）

只评估一张任务卡：

- **role_type**：`production`
- **task_domain**：`long_voice_task_parse`

只验证“长语音任务拆解”模型链路，不接：

- tools
- 图书馆 / 蜂巢
- recommendation 自动消费
- 自动升降级 / 自动切模型（除 provider 内通道超时回退）
- 第二家供应商

主链不改的部分（保持不变）：

- schema（`voice_task_parse_v1_1`）
- validator / builder
- fallback 规则链语义与统计口径

## 固定 smoke（不允许改）

1. 先去商场，再找便利店买点吃的
2. 我今天有点不舒服，先带我去最近的医院吧
3. 帮我自动挂号
4. 带我去医院

## 固定验收口径（不允许改）

每条输入输出：

- JSON 成功/失败
- validator 通过/失败
- fallback 是/否
- task_plan_v1 有/无
- 耗时 ms（e2e）

总汇总输出：

- 纯 JSON 成功率
- validator 通过率
- fallback 触发率
- 平均 e2e 耗时
- mixed 下 non_task_payload 是否保留（“不舒服”）

## 证据链（关键结果）

### M0-最终（v3）— 达标轮（单模型分别跑）

#### qwen-plus（主选）

- **JSON**：100%
- **validator**：100%
- **fallback**：0%
- **avg e2e**：约 10s（< 15s）
- **mixed non_task_payload**：True
- **通道**：4/4 `responses`（无 120s timeout 污染）

#### qwen-turbo（速度型备选）

- **JSON**：100%
- **validator**：100%
- **fallback**：0%
- **avg e2e**：约 4.5s
- **mixed non_task_payload**：True
- **unsupported_register**：输出 `unsupported_or_reject` 且 `task_candidates=[]`（不再出现 `task_control.*`）

#### qwen3.5-flash（淘汰）

- **avg e2e**：> 25s
- **输出过肥**：output tokens 显著偏高
- 结论：不再投入前台主链优化

## 因果关系（为何“不是拍脑袋”）

- **mixed 丢失**：通过 prompt 的 mixed 硬约束修复（保住“我今天有点不舒服”）
- **qwen-turbo mapping 纪律**：通过 turbo 专用 prompt 固定 unsupported 输出与禁止 `task_control.*` 修复
- **qwen-plus 120s 通道污染**：通过 provider 级最小修复（缩短 Responses 单次 HTTP timeout，失败尽快切换 Chat Completions）消除超时污染

## 中台状态写入建议（执行态）

- 路由策略：`long_voice_task_parse` → primary=`qwen-plus`，fallback=`qwen-turbo`，rule_chain 仍为最终兜底
- registry 标注：
  - `qwen-plus`：allowed_in_mainline=true
  - `qwen-turbo`：allowed_in_mainline=true（但定位为 backup_candidate）
  - `qwen3.5-flash`：allowed_in_mainline=false / deprecated_candidate

**已落档（代码）**：`mid_platform/model_governance/routing/policies/voice_long_voice_task_parse_policy_m0.py`、  
`mid_platform/model_governance/registry/cards/voice_long_voice_task_parse_registry_cards_m0.py`。  
**Provider 默认档 optimized** 与 **主链三线路线图**：见 `LUNA_VOICE_QWEN_EXTERNAL_PROVIDER_AB_DECISION_M0.md`、`LUNA_VOICE_LONG_VOICE_TASK_PARSE_MAINLINE_ROADMAP_M1.md`。

