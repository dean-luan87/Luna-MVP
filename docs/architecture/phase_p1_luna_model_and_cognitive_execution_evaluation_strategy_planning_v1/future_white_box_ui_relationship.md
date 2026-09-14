# Future White-box UI Relationship

## Current decision

No White-box UI is implemented or changed. The machine-readable evaluation
trace is the prerequisite surface.

## Separation

- Model Test Lens: model/capability result, metrics, failure modes, and
  candidate envelopes.
- Future White-box: cross-seam cognitive/execution trace, node states,
  evidence quality, sufficiency transitions, and handoff explanation.
- TestBoard: protected durable process/result/conclusion evidence.

The future UI may read all three through refs but must not own their lifecycle,
write runtime state, or infer unavailable nodes. A node marked planned or
unavailable must remain visually and machine-readably distinct from success.
