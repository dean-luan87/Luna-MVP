# Cognitive Attention Competition and Arbitration Go/No-Go v1

## Required checks

- Attention Resource has Available Capacity, Current Allocation, Reserved
  Capacity, and Recovery Capacity.
- Attention Source includes Survival Attention, Goal Attention, Field Attention,
  Maintenance Attention, Exploration Attention, and External Demand Attention.
- Priority considers Survival Impact, Goal Relevance, Field Relevance, Temporal
  Urgency, Information Value, Uncertainty Reduction, and Resource Cost.
- Competition records simultaneous Attention Requests and preserves deferred
  requests.
- Arbitration distinguishes Mandatory Attention, Competitive Attention, and
  Opportunistic Attention.
- New Evidence can create an Attention Interrupt Request and a Resource
  Reallocation Candidate, not an Action.
- Lifecycle includes Created, Allocated, Maintained, Decayed, Released, and
  Archived.
- Persistence distinguishes Persistent, Temporary, and Interruptive attention.
- Attention Candidate → Brain Evaluation → Decision preserves Brain authority.

## Explicit prohibitions

This architecture-only phase has No Emotion Runtime, No Role Runtime, No Social
Field Runtime, No B Route, No Prediction, No Decision, No Action, No real model
call, No Camera, No OCR, No SLAM, No Hardware Runtime, no automatic frequency
adjustment, no Scheduler implementation, and no online learning.

The agent performs V0 static checks only, does not run the Final Phase Verifier,
and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`. The user must execute
the phase verifier and return all required sections.

Reserved Capacity and Temporal Urgency are required terms. New Evidence may
produce a Resource Reallocation Candidate. No Social Field Runtime and No real
model call are enabled. This phase has no automatic frequency adjustment.

No real model call is permitted.
