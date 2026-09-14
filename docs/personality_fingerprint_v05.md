# Personality Fingerprint v0.5 (Base)

## Purpose
Provide a cross-trace, read-only behavioral summary for analysis and future engines.

## Generation
- Generated **ONLY** during Trace Audit / DCS stage
- **NOT** available in runtime (B / Gate / C)

## Scope
- Statistical facts only
- No semantic interpretation
- No thresholds or judgments

## Prohibited
- ❌ Runtime usage
- ❌ Decision making
- ❌ Gate or Control influence
- ❌ Personality / emotion naming

## Future
Higher-level personality or emotional models must consume this as input,
not extend or modify it in-place.

---

## Schema (Frozen)

```json
{
  "personality_fingerprint": {
    "window": {
      "duration_sec": 401.8,
      "frame_count": 12048
    },
    "gate_profile": {
      "active_ratio": 0.985,
      "read_only_ratio": 0.015,
      "suspended_ratio": 0.0,
      "state_switch_per_min": 0.73
    },
    "decision_profile": {
      "tick_per_min": 0.0,
      "no_op_ratio": 1.0,
      "meaningful_decisions": 0
    },
    "stability_profile": {
      "avg_stability_score": 0.91
    }
  }
}
```

---

## Implementation

- **Generator**: `tools/personality_fingerprint_v05.py` → `build_personality_fingerprint()`
- **Integration**: `tools/run_trace_audit.py` (Trace Audit stage only)
- **Output**: `artifacts/personality_fingerprint_v05.json`
- **Display**: `viewer/trace_viewer_v05_dashboard.html` (read-only, no interpretation)

---

## Version

- **Current**: v0.5 (Frozen)
- **Date**: 2025-01-14
- **Status**: ✅ Implemented
