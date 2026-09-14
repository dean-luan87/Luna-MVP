# Luna Phase Instruction Template v1

## 当前阶段判断

- Phase: <Phase-Id>
- Stage: <Stage-Name>
- Execution Mode: <Mode-Id>
- Previous Phase: <Phase-Id>
- Previous Phase Decision: <Decision-Token>

## 当前工作内容描述

- In scope:
  - <item>
- Out of scope:
  - <item>

## 适可而止条件

- 完成 Required Final Files。
- 完成 Allowed Agent Checks。
- 达到 Agent Stop Point 后立即停止。

## 🟢 Agent 执行

- Required Pre-Read:
  - <repo-relative path>
- Target Directory:
  - <repo-relative path>
- Required Final Files:
  - <repo-relative path>
- Required Checks:
  - <V0/V1 scoped checks>
- Negative Guards:
  - <forbidden shortcut list>

Verification Authority:

V0 Static Checks:
Agent Allowed:
- <allowed static checks>

V1 Controlled Component Validation:
Agent Allowed / Not Allowed:
- Allowed: <only if mode authorizes>
- Not Allowed: <if mode forbids>

V2 Final Phase Verification:
User Terminal Only:
- exact command: <python docs/architecture/.../verify_...py>

V3 Final Audit And Decision:
ChatGPT Only

Validation Result Authority:
- V0 does not grant GO.
- V1 does not grant GO.
- Only user-executed V2 plus ChatGPT V3 audit can grant GO.

## 🟡 用户终端执行

- Required commands:
  - <exact command 1>
  - <exact command 2>
- Return full terminal output including verifier sections.

## 🔵 ChatGPT 审核与最终裁决

- Review phase boundary and execution mode authority.
- Review Agent completion report.
- Review user terminal V2 output.
- Issue GO or BLOCKED.
- Decide next phase.

## Agent Stop Point

- Current status contract: WAITING_FOR_USER_TERMINAL_VERIFICATION

## Completion Report Format

- Pre-read findings
- Created files
- Modified files
- Governance coverage
- Static checks
- Boundary confirmation
- Known blockers
- User terminal commands
- Current status

---

## Example A: Planning Only

- Execution Mode: Planning Only
- Agent Allowed: V0 only
- Agent Not Allowed: any runner/verifier execution beyond V0
- Agent Stop Point: WAITING_FOR_USER_TERMINAL_VERIFICATION

## Example B: Controlled Skeleton

- Execution Mode: Controlled Skeleton Implementation
- Agent Allowed: V0 + explicitly authorized skeleton runner/result verifier
- Agent Not Allowed: real runtime, final phase verifier
- Agent Stop Point: WAITING_FOR_USER_TERMINAL_VERIFICATION

## Example C: Controlled DryRun

- Execution Mode: Controlled DryRun
- Agent Allowed: V0 + authorized dryrun runner/result verifier
- Agent Not Allowed: final phase verifier, real state mutation
- Agent Stop Point: WAITING_FOR_USER_TERMINAL_VERIFICATION

## Example D: Remediation

- Execution Mode: Remediation
- Agent Allowed: fix failed items only, V0 and authorized rechecks
- Agent Not Allowed: weakening checks, renaming to hide failures, final phase verifier
- Agent Stop Point: WAITING_FOR_USER_TERMINAL_VERIFICATION
