# Memory Consolidation Model v1

Consolidation is an interface, not an executing algorithm:

```text
Experience Candidate
  -> importance evaluation
  -> validation and admission
  -> reinforcement / decay
  -> folding and compression
  -> Memory Candidate
  -> Pattern Candidate
```

Folding relates Episodes; compression preserves provenance, Field, time, confidence, and Unknown while reducing representation size. Decay lowers contextual influence rather than deleting historical truth. Removed means out of current influence, not destructive deletion.

