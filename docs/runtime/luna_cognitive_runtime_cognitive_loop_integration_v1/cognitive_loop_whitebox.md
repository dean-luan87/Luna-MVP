# Cognitive Loop Integration Whitebox

The integration deliberately stops at a Decision Candidate. The placeholder Brain boundary returns `unresolved_candidate` with confidence `0.0`; this is a transport contract, not reasoning. No Action Command, Reality Change, Memory Mutation, Goal Mutation, or direct provider output is produced.

The State Update Boundary writes only the runtime-owned candidate projection. Workspace and Attention adapters keep ephemeral context and candidates; they do not write Reality. The Feedback Placeholder records that a future action result is required and does not execute an action or learning step.
