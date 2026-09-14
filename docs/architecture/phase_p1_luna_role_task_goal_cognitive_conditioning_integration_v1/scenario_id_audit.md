# Scenario ID audit

In the controlled replay branch, `scenario_id` is retained only for trace,
candidate, provenance, and execution identity namespaces. Attention selection,
Evidence relevance, Hypothesis state, Current World kind, and Sufficiency are
derived from supplied conditioning/evidence inputs. The pre-existing
`SYNTHETIC_CONTROLLED` branch retains its historical scenario fixture behavior
for backward compatibility.
