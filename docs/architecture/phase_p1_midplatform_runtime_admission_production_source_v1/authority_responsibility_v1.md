# Authority and responsibility

| Boundary | Retained authority | This phase's responsibility |
|---|---|---|
| Capability Governance | Capability/Slot and Capability↔Model lifecycle | supplies and validates its refs |
| Model Governance | model identity/declarations | supplies model/version/loader declarations |
| Provider Governance | Model↔Provider lifecycle and later Provider boundary | supplies compatibility declaration |
| Runtime Admission | executable eligibility assessment/candidate lifecycle | assesses the composed current inputs |
| Integration source | no canonical state authority | translation/composition correctness |
| A | local semantic consequence | unchanged |
| Brain Governance | global consequence | unchanged |

No new Manager, selector, scheduler, planner, or owner is introduced.
