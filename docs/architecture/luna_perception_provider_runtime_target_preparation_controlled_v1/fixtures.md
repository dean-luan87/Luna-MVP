# Controlled fixtures

The evaluation package contains 24 synthetic cases covering single and multiple providers, multiple compatibility candidates, same-class candidates, same-provider/multiple-demand lineage, no input, missing mapping, no match, unavailable/not-admitted providers, invalid lineage, duplicate mapping, optional/no model, all non-execution boundaries, Scenario 12 signage/flow/both, deterministic replay, and malformed tuple shape.

Scenario 12 remains abstract:

`signage compatibility → provider:controlled:scenario12:signage`

`human-flow compatibility → provider:controlled:scenario12:flow`

These refs come from explicit controlled mappings. They do not imply OCR, VLM, detector, SLAM, camera, provider binding, or execution.

Zero input and missing/invalid mappings never create fallback targets.
