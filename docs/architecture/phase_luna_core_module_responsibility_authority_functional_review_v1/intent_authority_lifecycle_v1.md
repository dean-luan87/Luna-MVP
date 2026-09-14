# Intent Authority and Lifecycle v1

## Authority matrix

| Operation | Proposer | Authoritative owner | Result |
|---|---|---|---|
| propose Intent | user/system/source modules, Brain, A, Task as an observation | Intent Governance | Potential/Intent Candidate |
| admit | Intent Governance after validation | Intent Governance | governed Intent identity/version |
| activate/coexist | Intent Governance under global constraints | Intent Governance | active/coexisting Intent ref |
| update | Intent Governance from governed candidate | Intent Governance | new Intent version |
| suspend/defer | Intent Governance, subject to Brain constraints | Intent Governance | lifecycle candidate/state |
| resume/reactivate | Intent Governance from valid prior version | Intent Governance | new active version/candidate |
| supersede | Intent Governance; Brain may request | Intent Governance | supersession relation |
| merge/split | Intent Governance candidate; Brain governs Concern consequences | Intent Governance for Intent state | governed relation or deferred candidate |
| terminate/close | Intent Governance under applicable global/Intent policy | Intent Governance | closed/superseded ref |

Brain can request or constrain a change, but must not mutate an Intent record
directly. A, Task, Role, Context and other sources can propose changes but do
not admit them. The current lifecycle type names are candidate vocabulary
(`POTENTIAL`, `FORMING`, `ACTIVE_CANDIDATE`, `SUPPRESSED`, `DORMANT`, and
others); this review does not create or promote new enums.

## Target lifecycle

`candidate → admitted → active/coexisting → suspended/deferred or temporarily
dominant → superseded/terminated/closed`.

Lifecycle semantics belong to Intent Governance. Loop may persist the supplied
Intent ref/version and mechanical consequence, but does not infer a lifecycle
transition.
