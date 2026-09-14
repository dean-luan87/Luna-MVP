# Luna Engineering Phase Execution Role Standard v1

## Scope

This standard defines execution roles and stop authority for Luna engineering phases.

## Role A: Agent

Agent is responsible for:
- Reading phase input assets and required pre-read governance assets.
- Creating and modifying only in-scope phase files.
- Running authorized V0 static checks.
- Running authorized V1 controlled runner/result verifier only when explicitly allowed by Execution Mode and phase instruction.
- Providing exact user terminal commands for user-only verification steps.
- Stopping at the phase-defined agent stop status.

Agent is not allowed to:
- Run Final Phase Verifier by default.
- Declare GO before receiving complete user terminal V2 output and ChatGPT V3 audit.
- Treat V0 pass as phase pass.
- Treat V1 pass as final phase pass.
- Modify unrelated modules.
- Cross phase boundary.
- Enter next phase automatically.

## Role B: User Terminal

User Terminal is responsible for:
- Running Final Phase Verifier (V2).
- Running explicit runtime/migration/device commands assigned to user in phase instruction.
- Returning complete terminal output.

## Role C: ChatGPT

ChatGPT is responsible for:
- Reviewing phase definition and execution boundary.
- Reviewing Agent completion report.
- Reviewing user terminal V2 output.
- Checking boundary violations and side effects.
- Making final GO or BLOCKED decision.
- Deciding next phase.

## Standard Execution Flow

1. Agent reads repository governance standards and current phase instruction.
2. Agent identifies Execution Mode and verification authority (V0/V1/V2/V3).
3. Agent performs in-scope work and allowed checks.
4. Agent stops at WAITING_FOR_USER_TERMINAL_VERIFICATION (or blocked status before V2).
5. User Terminal runs Final Phase Verifier (V2) and shares full output.
6. ChatGPT performs V3 audit and issues final decision.

## Agent Stop Point

Agent must stop when one of the following is true:
- All in-scope artifacts and allowed checks are complete.
- A blocker requires user action or governance decision.
- User-only command execution is required.

Agent highest normal completion status:
- WAITING_FOR_USER_TERMINAL_VERIFICATION

## Final Decision Authority

- V0: readiness signal only.
- V1: component validation signal only.
- V2: user terminal verification output.
- V3: ChatGPT final authority.

Only user-executed V2 plus ChatGPT V3 audit can grant GO.

## Unverified No-GO Rule

Without complete V2 output and V3 audit:
- GO is forbidden.
- Final decision is not granted.

## Sufficient And Stop Condition

Agent must stop as soon as required scope is done.
No extra phase expansion is allowed.
