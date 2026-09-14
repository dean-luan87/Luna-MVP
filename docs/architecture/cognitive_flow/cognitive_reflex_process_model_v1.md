# Reflex Process Model v1

Reflex Processes describe bounded low-latency protection loops, such as battery protection, thermal protection, device anomaly detection, and basic safety signals.

They may emit a `reflex_signal_candidate` or `interrupt_candidate`; they may not create a world action, alter Goal/Value/Memory, claim truth, or bypass Neural Governance. Hardware protection remains local capability safety, not cognitive Decision.

Reflex status is a candidate observation. It can constrain future resource candidates but cannot directly allocate Attention or close a Brain objective.
