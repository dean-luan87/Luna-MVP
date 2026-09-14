# Cognitive Flow Module Boundary Matrix v1

| Module / domain | Responsibility | Inputs | Outputs | Forbidden behavior | Dependencies |
| --- | --- | --- | --- | --- | --- |
| Perception Admission | Normalize external observations and evidence candidates | OCR/SLAM/ASR/TTS-facing observations, user input, model output candidates | Observation Event, Evidence Reference, admission decision | write Field State, make facts, invoke action | Evidence Chain, Field Event Admission |
| Field Event Admission & Temporal Validity | Decide candidate eligibility for Reducer | event candidate, evidence/source/trace, explicit time policy | admitted/rejected/deferred/duplicate/expired/out-of-order candidate | mutate state, call Reducer, call model, use real store | Perception Admission, temporal protocol |
| Field State Reducer | Maintain candidate Field State from admitted events | admitted events, temporal/policy/conflict snapshots | Field State candidate, provenance, read projection candidate | accept raw event, fact admission, action, provider call | Admission, temporal validity |
| Field State Read Model | Provide read-only Field State projection/query | Field State candidate, scoped query | read result/projection | mutate state, reduce events, dispatch downstream action | Field Kernel only |
| Cognitive Analysis | Produce hypotheses, differences, gaps, alternatives | Field reads, evidence refs, task/self constraints | Hypothesis, Difference Point, Information Gap, Exploration/Delivery candidates | claim fact, modify Field State, directly execute tools/actions | Read Model, Evidence Chain, Task context |
| Experience System | Record reviewed episodes and abstract reusable kernels | outcome events, delivery refs, hypotheses, evidence, review | Episode/Kernel/Branch candidates | value judgment, policy mutation, fact admission | Outcome Event, Evidence Chain, Human review |
| Luna Self System | Maintain individual perspective, relationship, emotion, worldview candidates | self-context events, experience refs, explicit user/owner constraints | self-context/perspective constraints | global truth, direct Field State override, Hive control | Experience System, Human/owner governance |
| Hive Experience Field | Associate cross-Luna experience branches and conflicts | explicitly shared episode/kernel/branch refs | links, divergence/conflict/game-analysis candidates | vote, impose consensus, make decision, overwrite local value | Experience System, sharing/consent governance |
| Task Manager | Own task lifecycle and execution-gate candidates | task candidates, safety/owner approvals, cognitive delivery candidates | task guidance/authorization outcome candidates | treat analysis as fact, execute unapproved action | Cognitive Delivery, owner/safety governance |
| Model Manager | Govern provider/capability access | bounded capability request candidate | model output candidate, capability status | fact source, action controller, Field owner | Perception Admission / Cognitive Analysis request boundary |
| Observation Attention | Prioritize observation and propose follow-up routes | region/scene candidates, task context, corrections | attention/route candidate | call model directly, write fact/state, navigate | Perception attachments, Task context |
| Human Correction | Capture structured human correction and review evidence | correction input, target refs, rationale | correction/review/training-signal candidates | overwrite model/Field State, become ground truth automatically | Evidence Chain, review governance |

## Boundary Assertions

- OCR, SLAM, ASR, TTS, and model outputs are external organ/attachment outputs; none may modify Field State.
- An LLM can produce a candidate explanation or hypothesis only; it cannot directly generate a fact, conclusion, or action.
- A model cannot control action. Cognitive Delivery still requires Task/owner/safety governance before any execution boundary.
- Hive can associate divergence and conflict but cannot directly intervene in a local decision.
- No module may bypass the Event Admission → Reducer → Read Model ownership chain for current world-state maintenance.

## Permitted Influence Chain

```text
candidate observation -> evidence -> admitted event -> Field State candidate
-> analysis candidate -> authorized delivery/task boundary -> outcome candidate
-> reviewed experience candidate
```

Each transition has its own owner. “Influence” means a bounded input to the next owner, never transfer of authority.

