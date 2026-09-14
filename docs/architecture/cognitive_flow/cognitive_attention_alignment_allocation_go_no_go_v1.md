# Attention Alignment and Allocation Go/No-Go v1

## V0 static acceptance criteria

1. Allocation includes intent relevance, survival impact, temporal urgency,
   uncertainty, information value, and cost candidates.
2. Attention Allocation != Decision; priority is distinguished from importance.
3. Minimal sufficient information is preferred over complete observation.
4. Alignment evaluates support for Original Intent rather than model output.
5. Expansion, narrowing, replacement, attraction, and persistence drift exist
   only as candidates.
6. Feedback includes intent match, value, coverage, waste, missing information,
   drift, and improvement candidates.
7. Neural Resource Evaluation constrains allocation; Attention never allocates
   actual resources or changes frequency.
8. Only one cognitive objective is in scope; no multi-A, role, emotion, or
   long-lived task coordination is introduced.
9. No runtime, automatic strategy change, Provider call, Action, or State
   mutation is introduced.

## Verification ownership

Execution Mode: `Planning Only`; V0 is Agent-only, V1 is not permitted, V2 is
user-terminal only, and V3 is ChatGPT-only.

```bash
python3 docs/architecture/cognitive_reality_cognition_attention_alignment_allocation_v1/verify_cognitive_reality_cognition_attention_alignment_allocation_v1.py
```

`final_candidate_decision: COGNITIVE_REALITY_COGNITION_ATTENTION_ALIGNMENT_READY_WITH_NOTES`

`status: WAITING_FOR_USER_TERMINAL_VERIFICATION`
