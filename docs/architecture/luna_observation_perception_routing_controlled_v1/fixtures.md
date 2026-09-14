# Controlled fixtures

The evaluation package covers:

- one demand and one resolution candidate;
- one demand with multiple candidates;
- independent demands;
- same-class candidates without deduplication;
- one capability candidate supporting multiple demands without merge;
- zero demand, missing mapping, no match, unavailable, and not-admitted cases;
- invalid resolution candidate and demand/capability lineage mismatch;
- Scenario 12 signage, human-flow, and both-route shapes;
- deterministic replay;
- malformed collection input, which must fail closed.

The fixtures use opaque controlled capability references. They do not infer
OCR, VLM, camera, SLAM, provider, or model routes from strings.
