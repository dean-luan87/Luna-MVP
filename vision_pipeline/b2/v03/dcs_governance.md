# DCS Governance & Mandatory Rules

## DCS Role Definition

**DCS is not a performance metric.**
**DCS is a design integrity metric.**

A system with high accuracy but low DCS is considered unsafe.

---

## What DCS Measures

DCS measures:
- ✅ **Design consistency**: Does the system follow its architectural intent?
- ✅ **Boundary respect**: Does B respect its boundaries with C?
- ✅ **Traceability**: Can every decision be explained?
- ✅ **Silence validity**: Is silence treated as a valid outcome?

DCS does NOT measure:
- ❌ Model accuracy
- ❌ Performance (FPS, latency)
- ❌ Throughput
- ❌ User satisfaction

---

## Mandatory Usage Rules

### PR Requirements

**Any PR touching the following must include DCS evaluation:**
- B (B2) code
- C (C1) code
- Gate mechanism
- Trace system
- Timeline generation

### Merge Blocking Rules

1. **DCS < 85 blocks merge**
   - No exceptions
   - No "but it works" arguments
   - No "we'll fix it later" promises

2. **Any G-level violation blocks merge regardless of score**
   - G.FAIL.001 (World semantic leak) = immediate block
   - No override possible

3. **Fatal violations must be resolved**
   - Cannot merge with fatal violations
   - Warnings are acceptable but should be documented

### DCS Evaluation Process

1. **Run automated audit:**
   ```bash
   python vision_pipeline/b2/v03/b2_audit/audit_runner.py \
       traces/b2_runtime_trace_v05.jsonl
   ```

2. **Calculate DCS:**
   ```bash
   python vision_pipeline/b2/v03/b2_audit/dcs_runner.py \
       traces/b2_runtime_trace_v05.jsonl \
       timeline.jsonl
   ```

3. **Fill PR template:**
   - Use `PR_TEMPLATE_DCS.md`
   - Document manual scores (if any)
   - Explain any warnings

4. **Review DCS report:**
   - Check `b2_dcs_report.json`
   - Verify no fatal violations
   - Document any accepted warnings

---

## DCS Interpretation

### DCS Does Not Judge Intelligence

**DCS does not judge:**
- ❌ Whether the model is smart
- ❌ Whether the predictions are accurate
- ❌ Whether the system is useful

**DCS judges:**
- ✅ Whether the system obeys its architectural intent
- ✅ Whether boundaries are respected
- ✅ Whether decisions are traceable
- ✅ Whether silence is valid

### DCS Is About "Obedience to Design"

A system with:
- High accuracy + Low DCS = **Unsafe** (may work but violates design)
- Low accuracy + High DCS = **Safe but ineffective** (follows design but needs improvement)
- High accuracy + High DCS = **Ideal** (works correctly and follows design)

**The goal is high accuracy + high DCS, but DCS is non-negotiable.**

---

## DCS Score Interpretation

| Score | Grade | Meaning | Action |
|-------|-------|---------|--------|
| ≥ 90 | EXCELLENT | Design highly consistent | ✅ Merge |
| 85–89 | PASS | Acceptable, minor issues | ✅ Merge (with warnings) |
| 70–84 | WARNING | Design starting to drift | ⚠️ Fix before merge |
| < 70 | FAIL | Design integrity compromised | ❌ Block merge |

### Special Cases

**G-level violations:**
- Any G.FAIL.001 violation = immediate FAIL
- No score can override this
- Must be fixed before any merge

**Fatal violations:**
- Gate fail but still trigger = 0/25 Gate score
- Non-standard Impact enum = 0/20 Impact score
- These are design-level failures, not implementation bugs

---

## DCS vs. Other Metrics

### DCS vs. Accuracy

**Accuracy:** "Did the system predict correctly?"
**DCS:** "Did the system follow its design?"

A system can be:
- Accurate but low DCS (works but violates design)
- Inaccurate but high DCS (follows design but needs model improvement)

**Both matter, but DCS is non-negotiable for safety.**

### DCS vs. Performance

**Performance:** "How fast is the system?"
**DCS:** "Does the system respect its boundaries?"

Performance optimizations must not violate DCS principles.

### DCS vs. User Satisfaction

**User Satisfaction:** "Do users like it?"
**DCS:** "Is it architecturally sound?"

User satisfaction cannot override DCS requirements.

---

## Enforcement

### Automated Enforcement

- CI/CD must run DCS evaluation
- Merge blocked if DCS < 85
- Merge blocked if G-level violation exists

### Manual Review

- PR reviewer must check DCS report
- PR reviewer must verify no fatal violations
- PR reviewer must document any accepted warnings

### Escalation

- If DCS < 70, escalate to architecture team
- If G-level violation, escalate immediately
- No override without architecture team approval

---

## DCS Maintenance

### When to Update DCS Rules

DCS rules should be updated when:
- New design principles are established
- New violation patterns are discovered
- Architectural intent evolves (rare)

DCS rules should NOT be updated when:
- Performance requirements change
- User requirements change
- Model accuracy improves

### Rule Addition Process

1. Identify new violation pattern
2. Define rule (with rule_id)
3. Add to audit system
4. Update DCS scorer
5. Document in this file

---

## Common Violations and Fixes

### Gate Violations

**Violation:** Gate fail but still trigger
**Fix:** Ensure gate check before trigger
**Rule:** S1.GATE.003

### Evidence Violations

**Violation:** Single-frame CONFIRMED
**Fix:** Implement evidence lifecycle
**Rule:** S2.EVIDENCE.001

### Impact Violations

**Violation:** WORLD/SCENE semantics
**Fix:** Remove world description, use behavior projection
**Rule:** G.FAIL.001

### Trace Violations

**Violation:** NO_OP without reason
**Fix:** Always provide reason for NO_OP
**Rule:** S6.TRACE.001

---

## DCS Philosophy

**DCS is not about being right.**
**DCS is about being consistent with design intent.**

A system that:
- Follows its design = High DCS
- Violates its design = Low DCS

**Even if the design is wrong, DCS measures consistency, not correctness.**

(If the design is wrong, fix the design, then measure DCS again.)

---

## Document Authority

This document has the same authority as:
- Code review requirements
- Testing requirements
- Security requirements

**Violating DCS rules is as serious as introducing security vulnerabilities.**

---

**Last Updated:** 2025-01-12
**Authority:** Architecture Team
