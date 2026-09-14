# B2 Design History & Decision Rationale

This document records **why** B2 evolved the way it did.
It is not a changelog, not a performance report, and not a roadmap.

Its purpose is to:
- Explain past failures
- Prevent design regression
- Serve as a reference for future architectural decisions

---

## Evolution Summary (Judged by DCS)

| Version | DCS | Status | Core Question Being Asked |
|--------|-----|--------|---------------------------|
| v0.1 | 16 | FAIL | What changed in the world? |
| v0.2 | 34 | FAIL | Which factors changed? |
| v0.3 | 61 | WARNING | Should we react to this change? |
| v0.4 | 92 | PASS | What happens if C does nothing? |

⚠️ **This table is an anchor. No architectural discussion can bypass it.**

---

## Version-by-Version Analysis

### v0.1 – World Descriptive System (DCS: 16)

**Core Question:** "What changed in the world?"

**Failure was inevitable because:**
- No concept of Gate
- Vision assumed to be truth
- World description instead of behavior projection
- No resistance to view pollution
- No concept of silence as a valid outcome

**Key Violations:**
- Gate: 0/25 (No gate mechanism existed)
- Evidence: 3/15 (Instant evidence, no lifecycle)
- Trigger: 4/15 (Trigger without behavior consequence)
- Impact: 2/20 (WORLD/SCENE used, world description)
- Trace: 5/15 (No reversible logic)
- Timeline: 2/10 (NO_OP pollution, no restraint)

**Diagnosis:**
This version answered the wrong question. It was designed to describe the world, not to project behavioral consequences.

**What v0.1 was asking:**
> "What happened in the world?"

**What v0.4+ asks:**
> "What happens if C does nothing?"

---

### v0.2 – Factor Decomposition (DCS: 34)

**Core Question:** "Which factors changed?"

**Improvements:**
- Introduced factors (PATH, PEOPLE, EVENT, ENV)
- Factor-based decomposition
- Partial separation of concerns

**Structural issues:**
- Factors treated as instant truth
- Trigger based on confidence, not consequence
- Still no Gate mechanism
- WORLD_SHIFT still present in decision logic

**Key Violations:**
- Gate: 0/25 (Still no gate)
- Evidence: 8/15 (Factors exist but no lifecycle)
- Trigger: 8/15 (Confidence-based, not consequence-based)
- Impact: 5/20 (WORLD_SHIFT still used)
- Trace: 8/15 (Better logging but not reversible)
- Timeline: 5/10 (Slightly better restraint)

**Diagnosis:**
Better structure, but still answering "what changed" rather than "what happens if we don't act."

---

### v0.3 – Early Behavior Awareness (DCS: 61)

**Core Question:** "Should we react to this change?"

**Key progress:**
- Evidence aggregation introduced
- Partial temporal awareness
- Beginning to consider "should we act"
- Removal of some WORLD-level semantics

**Blocking issues:**
- WORLD_SHIFT still present in some paths
- Silence not understood as a valid action
- No Gate mechanism
- Evidence lifecycle incomplete (no DEGRADED/DROPPED)

**Key Violations:**
- Gate: 5/25 (Awareness but no mechanism)
- Evidence: 10/15 (Aggregation exists but lifecycle incomplete)
- Trigger: 12/15 (Better consequence awareness)
- Impact: 15/20 (WORLD_SHIFT reduced but not eliminated)
- Trace: 10/15 (Better traceability)
- Timeline: 9/10 (Much better restraint)

**Diagnosis:**
Moving in the right direction, but still missing the fundamental question shift and Gate protection.

---

### v0.4 – Behavior Projection System (DCS: 92)

**Core Question:** "What happens if C does nothing?"

**Key shifts:**
- Gate introduced as reality filter
- Impact replaces world description
- Silence (NO_OP) is a first-class outcome
- Evidence lifecycle complete (OBSERVING → CONFIRMED → DEGRADED → DROPPED)
- Full traceability to time and frame
- Timeline restraint (NO_OP excluded)

**Key Achievements:**
- Gate: 25/25 (Full gate mechanism)
- Evidence: 15/15 (Complete lifecycle)
- Trigger: 15/15 (Consequence-based)
- Impact: 20/20 (Behavior projection only)
- Trace: 15/15 (Full reversibility)
- Timeline: 2/10 (Minor issues with restraint)

**Diagnosis:**
This is the first version aligned with human perception logic. It asks the right question and has the mechanisms to answer it safely.

**What v0.4 achieved:**
> "If C continues current behavior, what happens in the next 3 seconds?"

This is fundamentally different from describing the world.

---

## Non-regression Principles

The following principles MUST NOT be violated:

1. **B never describes the world, only behavior impact**
   - No WORLD/SCENE semantics
   - Impact must answer: "What happens if C does nothing?"

2. **Gate precedes all judgments**
   - Gate evaluation must occur before any trigger/impact
   - No judgment without gate protection

3. **Silence is a valid and necessary outcome**
   - NO_OP is not a failure
   - NO_OP must have a reason
   - NO_OP must not pollute timeline

4. **B may only intervene C on confirmed safety risks**
   - FORCE_ALERT is the only intervention-level action
   - All other actions are suggestions
   - Evidence must be CONFIRMED before intervention

5. **All judgments must be traceable to time and frame**
   - Every impact must be traceable to a specific second and frame
   - Every silence must have a reason
   - Every violation must be locatable

📌 **This section is a "constitution", not a suggestion.**

---

## Design Philosophy Evolution

### v0.1–v0.3: The Wrong Question

These versions were asking:
> "What changed in the world?"

This led to:
- View pollution (camera shake = false world change)
- Over-reaction (every change = action required)
- World description (WORLD_SHIFT, SCENE_CHANGE)
- No silence mechanism

### v0.4+: The Right Question

v0.4+ asks:
> "What happens if C does nothing?"

This requires:
- Gate (filter view pollution)
- Evidence lifecycle (confirm before acting)
- Behavior projection (not world description)
- Silence as first-class outcome

---

## Lessons Learned

1. **The question matters more than the answer**
   - v0.1–v0.3 had good implementations of the wrong question
   - v0.4+ has the right question, even if implementation is still evolving

2. **Gate is not optional**
   - Without gate, system is "blind" to view pollution
   - Gate is the foundation, not an optimization

3. **Evidence must mature**
   - Instant evidence = false positives
   - Lifecycle (OBSERVING → CONFIRMED) is essential

4. **Silence is not failure**
   - Most of the time, B should be silent
   - Silence with reason is correct behavior

5. **Traceability is non-negotiable**
   - Every decision must be reversible
   - Every silence must be explainable

---

## Future Considerations

When evaluating future changes, ask:

1. Does this change answer "what happens if C does nothing?"
2. Does this respect Gate protection?
3. Does this maintain evidence lifecycle?
4. Does this preserve traceability?
5. Does this treat silence as valid?

If any answer is "no", the change violates non-regression principles.

---

## Document Maintenance

This document must be updated when:
- A new version achieves DCS ≥ 85
- A non-regression principle is violated (and then fixed)
- A fundamental design shift occurs

This document must NOT be updated for:
- Performance improvements
- Bug fixes (unless they reveal design issues)
- Feature additions (unless they change core question)

---

**Last Updated:** 2025-01-12
**Current Version:** v0.4 (DCS: 92)
