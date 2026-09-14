# Cognitive Process Interrupt Candidate Model v1

An active or background process may report an `interrupt_candidate` when it observes an unexpected environment change, capability degradation, resource protection condition, or evidence conflict.

Required concepts: source process reference, reason, priority candidate, affected context, uncertainty, and trace. An interrupt is not preemption: it cannot directly seize Attention, cancel other processes, trigger an Action, or mutate State. Neural Governance arbitrates any later reallocation candidate.
