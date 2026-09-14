# Cognitive Runtime Isolation Model v1

Different processes, such as navigation, social understanding, and risk analysis, hold separate Runtime Instance and Snapshot Candidate references. Process A cannot modify Process B, Field State, Reducer State, Memory, Experience, Decision, Action, or Permission.

Cross-process communication, if needed, uses Signal and Candidate references through Orchestration and Candidate Integration. It is not shared mutable Runtime State.

Isolation != permanent separation: governed integration may preserve conflicting candidates with source/provenance boundaries.
