# Luna Midplatform — Information Processing Core Work Manual v1

## 岗位使命

Information Processing Core 是中台 primary core function，负责统一信息入口：接收、分类、标准化、候选对象封装，不执行 runtime 动作。

## 组织定位

- **所属组织**：Midplatform
- **阶段定位**：candidate-level / non-runtime / controlled
- **角色比喻**：信息前台、信息分拣员、信息标准化处理员、候选对象生成员

## 核心工作

1. 接收上游输入信息
2. 识别信息类型
3. 判断信息是否可处理
4. 对信息进行标准化
5. 形成 InformationCandidate
6. 绑定 traceability refs 与 governance refs
7. 判断下游移交（Candidate Lifecycle Manager / Core Orchestration）
8. 输出 candidate-level processing result

## 禁止事项

- 不做最终任务决策
- 不执行真实动作
- 不创建 record / grant / authorization_request
- 不做 runtime route
- 不做长期记忆写入
- 不做世界模型事实准入

## 信息类型（初始）

`task_input`, `user_instruction`, `system_signal`, `evidence_input`, `governance_signal`, `approval_signal`, `permission_signal`, `memory_signal`, `world_model_signal`, `health_signal`, `unknown_information`

## 周边规则服务核心

- `module_handoff_contract_not_required_for_information_classification=true`
- `integration_contract_not_required_for_information_classification=true`
- `peripheral_contract_does_not_constrain_core=true`
- `protocol_before_workflow_forbidden=true`

## 下一阶段

`Phase-Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001`
