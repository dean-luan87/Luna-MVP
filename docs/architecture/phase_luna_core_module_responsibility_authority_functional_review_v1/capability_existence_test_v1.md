# Capability Governance Existence Test v1

| Architecture | Result |
|---|---|
| Capability owned by Brain | Reject: Brain governs global constraints, not technical capability taxonomy. |
| Capability owned by A | Reject: A owns Need and cognitive meaning, not implementation portability. |
| Capability owned by Task | Reject: Task organizes execution; it must not route model/provider implementations. |
| Capability owned by Model Manager | Reject: Model Manager owns assets and mappings, not logical capability identity. |
| Capability owned by Provider Governance | Reject: Provider is one execution implementation, not the functional abstraction. |
| Independent Capability Governance | **Preferred:** portable logical abstraction and testable scope/resolution boundary. |
| Capability as simple registry only | Insufficient: registry alone cannot govern scope, resolution, mapping and handoff. |

Capability Governance is justified because one functional capability may map to
multiple models/providers, one model may support multiple capabilities, and
logical requirements must remain independent from runtime availability.

Final disposition: NARROW, retaining the independent logical governance
boundary without creating a new runtime Manager.
