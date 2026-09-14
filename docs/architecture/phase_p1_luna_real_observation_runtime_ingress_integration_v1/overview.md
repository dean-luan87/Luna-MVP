# Real Observation Runtime Ingress Integration v1

This phase enables an already-produced external observation result to enter
the existing Luna Observation Gateway under `LIVE_RUNTIME`. It does not invoke
a provider, model, sensor, camera, OCR engine, SLAM engine, or downstream
Decision/Task/Action runtime.

The path is:

`runtime observation envelope → Observation Gateway → Evidence Candidate → A-Route → Cognitive State Formation`

The existing replay and synthetic paths remain separate and unchanged in
meaning.
