# Runner / Verifier Modes

## Structural mode

Structural mode runs only the adapters with synthetic provider-shaped input.
It must report:

- `actual_provider_response=false`;
- `provider_invocation=false`;
- candidate-only and mutation guards;
- trace/provenance/version continuity;
- negative case results.

## Real-provider mode

Real mode requires a user-supplied JSON input containing governed request
refs, including `goal_ref` and `concern_ref`, but no semantic assessment.
It requires `--mode real`, a local image, `ROBOFLOW_API_KEY`, the Inference
Server base URL, `ROBOFLOW_WORKSPACE`, `ROBOFLOW_WORKFLOW_ID`, and explicit
workflow output mappings. Luna's narrow A-owned bridge forms only evidence
coverage candidates for Hypothesis/Sufficiency/Information Gap; it does not
answer the exit question or create a Decision.

The real cycle stops after the first provider response and Luna cognitive
formation. A Next Observation candidate or Decision Governance handoff is
returned for review and is not executed automatically.

The verifier also checks source wiring so a fake native fixture cannot be
counted as a real result, the official SDK transport was used, and the
provider/workflow/model provenance remains attached to normalized Evidence.
