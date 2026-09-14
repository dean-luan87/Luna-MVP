# Cognitive Behavior Candidate Information Value Alignment v1

## Information-aware candidates

Behavior Candidates may declare `information_gain_potential`, estimated cost, reversibility, and required evidence. This makes it possible for a later, separately governed layer to compare actions that progress a task with actions that safely reduce uncertainty.

For example, requesting illumination can be a low-cost, high-information candidate; entering an unknown area can be a higher-cost candidate with unresolved information benefit. These descriptions are uncertain evaluations, not decisions, instructions, or permission grants.

## Alignment rule

Information Value affects candidate description and future comparison only. It cannot cause observation execution, Action execution, or a State change. Exploration remains a candidate condition, never automatic Permission.
