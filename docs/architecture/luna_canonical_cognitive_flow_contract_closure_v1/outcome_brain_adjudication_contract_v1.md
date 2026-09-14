# Outcome Candidate → Brain Adjudication Contract v1

## Input contract

Outcome Evaluation supplies a reference-oriented adjudication input containing:

- `outcome_candidate_ref`, `outcome_version`;
- Goal, Concern and Grant refs;
- Decision, Task and Action Result refs;
- A Local Evaluation refs;
- Field and Current World consequence refs;
- evaluation status, partiality and uncertainty;
- Safety, Permission and Resource consequence refs;
- recommended follow-up candidates;
- source versions, provenance and trace refs.

## Boundary

Outcome Evaluation forms/evaluates the candidate. Brain performs final global evaluation/adjudication and Assimilation. Brain does not rerun Task, Action or A internals. Outcome does not close Concern or mutate Goal.

## Output contract

The Brain result may reference existing outcome vocabulary such as accept, partial accept, reject, defer, supersede, continue Concern, close Concern and follow-up required. It may emit governed Goal/Concern consequence refs, Intent impact candidates, Decision/Task candidates, MemoryCandidate/ExperienceCandidate refs and Loop mechanical command refs.

Brain output is a separate Brain Adjudication/Assimilation record. Brain does not directly mutate Intent, Task, Memory or Experience.

## Responsibility

Outcome Evaluation owns aggregation, missing refs, stale acceptance and uncertainty loss. Brain owns final acceptance/rejection, Concern closure, Goal impact and Assimilation. Loop only persists the authorized result.

