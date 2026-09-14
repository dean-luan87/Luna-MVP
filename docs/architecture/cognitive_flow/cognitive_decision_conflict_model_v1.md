# Decision Conflict Model v1

## Definition

Decision Conflict Candidate represents that two or more Decision Candidates cannot currently be compared or resolved without losing relevant constraints. For example, a high-reward/high-risk option and a low-reward/low-risk option may both remain valid candidates.

Conflict is not failure, an exception, or an instruction to choose a compromise. It is information that can support future request-more-information, delay, alternative-path, or human-assistance candidates.

## Preservation rule

Conflicts retain references to the competing candidates, value dimensions, missing evidence, uncertainty, provenance, and trace. Candidate formation may not collapse a conflict into an automatic winner.
