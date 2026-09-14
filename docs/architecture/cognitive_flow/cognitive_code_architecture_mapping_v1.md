# Cognitive Architecture Code Mapping v1

| Architecture capability | Current code location | Baseline status |
| --- | --- | --- |
| Candidate contract | `cognitive/contracts/candidate.py` | Present; immutable candidate container |
| Signal contract | `cognitive/contracts/signal.py` | Present; immutable decoupled signal container |
| Cognitive snapshot | `cognitive/contracts/snapshot.py` | Present; immutable cycle view |
| Candidate-only governance | `cognitive/governance/reducer_boundary.py` | Present; rejects requested State mutation |
| Cognitive tick | `cognitive/runtime/tick.py` | Present; declared trigger/tick contract |
| Controlled cognitive flow | `cognitive/runtime/controlled_execution.py` | Present; synthetic-only validation skeleton |
| Snapshot continuity | `cognitive/runtime/state_transition.py` | Present; synthetic-only transition skeleton |
| Trace and validation | `cognitive/validation/` | Present; controlled synthetic validation assets |
| Evidence / Perception runtime | — | Planning only |
| World / Context runtime | — | Planning only |
| Attention Controller | — | Planning only |
| Cognitive Kernel | — | Planning only |
| Organization Layer | — | Planning only |
| Capability Composition | — | Planning only |
| Resource Modulation | — | Planning only |
| Process Composer | — | Planning only |
| Workspace / Simulation runtime | — | Planning only |
| Experience / Evolution runtime | — | Planning only |

## Interpretation

“Planning only” means no code package exists and no runtime behavior is implied. A missing package is expected at this baseline; it is not evidence that a planning document has been implemented.

