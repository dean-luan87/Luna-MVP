# Intent Alignment Evaluation Model v1

## Evaluation question

“Does the evidence and resulting Situation support the Original Purpose within
the Intent Contract boundary?”

## Candidate dimensions

| Dimension | Candidate question |
|---|---|
| Purpose coverage | does obtained evidence address the original cognitive need? |
| Non-negotiable coverage | are mandatory evidence categories represented or explicitly missing? |
| Boundary fidelity | did interpretation remain inside allowed range and avoid forbidden transformation? |
| Evidence relevance | does returned evidence support the request rather than a local proxy? |
| Uncertainty preservation | are gaps, conflict, and unavailable capability retained? |
| Resource proportionality | did organization remain proportionate to the bounded purpose? |

## Output

`Intent Alignment Evaluation Candidate` contains alignment score candidate,
coverage gaps, drift candidates, uncertainty, and trace references.

Value is not Truth, and alignment score is not cognitive completion, Decision,
Action, permission, or State mutation. Brain retains final evaluation.

