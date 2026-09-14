# Luna Capability Assessment Model v1

## Assessment Dimensions

| dimension | governance question | non-authorizing result |
| --- | --- | --- |
| reliability | are declared behavior, validation evidence, and known limitations sufficiently explicit? | reliability signal, not activation or Fact authority |
| traceability | can input, output, source, Contract, version, and limitation lineage be retained? | traceability status, not permission grant |
| compatibility | do Protocol, input/output Contract, consumer, and dependency references remain compatible? | compatibility candidate, not Registry write |
| risk | what boundary, misuse, side-effect, provenance, or deprecation risks are present? | risk warning/block candidate, not automatic denial override |
| resource cost | what bounded computation, dependency, latency, or operational cost is declared? | resource planning signal, not a Runtime scheduler |
| learning value | does the Capability produce a reviewable candidate signal with evidence and uncertainty? | learning-review relevance only, never Memory/Training write |

## Assessment Rules

- Assessment dimensions may be extended for a Capability family if their source, interpretation, traceability, and authority boundary are declared.
- No single dimension is a universal score or automatic approval rule.
- A strong reliability, compatibility, or learning-value signal cannot override Protocol incompatibility, denied Permission, constitutional boundary, or missing provenance.
- Assessment produces evidence, recommendations, warnings, or candidate classifications only. It does not activate, register, grant permission, run a Capability, or modify State.

## Diagnostics Boundary

Diagnostics may detect, report, and recommend from assessment evidence: Capability drift, Contract mismatch, dependency risk, contextual incompatibility, resource concerns, and Deprecated usage. Diagnostics cannot activate, upgrade, grant permission, register, retire, or auto-remediate a Capability.

