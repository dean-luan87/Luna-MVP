# LUNA — WorldContextEvidence Write Readiness & Governance Definition v0

## Phase

- **Phase-WorldModel-WriteReadiness-001**

## Purpose

本阶段只定义：`WorldContextEvidenceCandidate` 在进入真实世界模型写入之前的 **准入、治理、回滚、防污染** 闸门。

它回答：

1. 哪些 candidate 允许进入写入评估
2. 哪些 candidate 只能暂存
3. 哪些 candidate 必须拒绝
4. 哪些 candidate 需要用户确认或多源验证
5. 哪些 candidate 可以短期写入
6. 哪些 candidate 可以长期写入
7. 写入后如何回滚
8. 过期、冲突、污染如何处理
9. 如何防止广告、低置信、幻想、谎言、欺诈信息污染世界模型

## Non-governance boundary（强制）

- 不实现 runtime
- 不真实写入世界模型
- 不上传蜂巢
- 不接推荐系统
- 不执行导航动作
- 不真实播报
- 不进入 SceneTask/Fusion/Output

## Inputs（上游事实）

当前上游已收口为 `closed_v0`（candidate-only offline skeleton）：

- Phase-WorldModel-ContextEvidence-004：GO / `world_context_evidence_status=closed_v0`
- 已有：
  - WorldContextEvidenceCandidate / CommercialActivityEvidenceCandidate / WorldChangeEventCandidate
  - observed_at / observed_where / spatiotemporal_anchor_ref
  - trust / lifecycle / world_model_policy
  - source_evidence_refs / source_reference_chain
  - no fabricated GPS
  - unknown anchor → requires_revalidation

## Core concepts

- **Write Readiness**：候选证据进入真实写入前的治理闸门（评估层）
- **Contamination guard**：污染防护（拒绝/隔离/降级/复核）
- **Rollback record**：回滚不是删除，而是状态迁移 + 证据保留
- **Write audit**：每一次评估与状态迁移必须可追溯（trace/replay/whitebox）

## Relationship with SceneDelta / ContextEvidence（关键分层）

- SceneDelta：只决定“变化语义”（新增/替换/移除/过期/冲突/重复/压缩），**不写世界模型**
- ContextEvidence：只包装 candidate + anchor/source alignment，**不写世界模型**
- Write Readiness：只给出“是否可写、写到哪里、是否隔离、是否回滚”的判定，**不直接执行写入**
- 真正写入由未来的 `WorldModel Commit Layer` 执行（不在本阶段）

