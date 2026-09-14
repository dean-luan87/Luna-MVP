# Value & Utility Implementation Plan v1

This phase is Planning Only and Architecture Only.

1. Reuse the existing Drive/Value Core, Value Constitution, Attention value,
   Goal Priority, Exploration Impact, Self Resource Awareness, and Brain Value
   Constraint interfaces.
2. Add adapters that normalize those assets into Value Evaluation Candidate and
   Utility Evaluation Candidate contracts; do not create a parallel Value
   Manager or Decision Engine.
3. Keep Self as the source of resource and health context, Constitution as the
   hard constraint authority, and Brain as the later judgment authority.
4. Reserve Decision Arbitration, Utility Runtime, automatic scoring, and
   learning integration for later phases.
5. Validate any future implementation against the contracts and negative
   guards before activation.

No files outside this phase directory are changed. Mapping is preferred over
moving or deleting historical assets.
