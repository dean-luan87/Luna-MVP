# B / C Boundary Assumptions (v1)

This document records **reviewed and accepted assumptions**
about the boundary between B (world observer) and C (real-time navigator).

These assumptions are not hypotheses.
They define the contract between B and C.

Any future change MUST explicitly reference this document.

---

## 1. Frequency Mismatch Is Intentional

**Assumption**
B and C operate at different frequencies by design.
- C reacts to the present (real-time, short range)
- B observes the future (delayed, long range)

**Invariant**
- B and C MUST share the same time and position reference
- Synchronization is NOT required, alignment is

**Rationale**
Human perception also operates asynchronously.
Consistency is achieved through shared reference, not identical timing.

**Status:** ACCEPTED  
**Revisit Phase:** Phase 3 (Learning & Evolution)

---

## 2. B Is System-Awakened, Not Self-Driven

**Assumption**
B does not decide when to run.
- B may remain read-only for long periods
- B may be awakened late
- Safety responsibility remains valid even under delayed activation

**Invariant**
- B's first objective is safety parity with C
- World modeling completeness is always secondary

**Rationale**
Running B continuously is a system scheduling problem,
not a cognitive requirement.

**Status:** ACCEPTED  
**Revisit Phase:** Phase 3

---

## 3. B Never Confirms Risk, Only Signals It

**Assumption**
B does not verify risks.
- B signals potential risks
- C and the user confirm them
- Risk confirmation requires proximity and action

**Invariant**
- All B outputs must be deniable suggestions
- Only one intervention class exists: confirmed safety impact

**Rationale**
B's view is limited and probabilistic.
Confirmation without proximity would be irresponsible.

**Status:** ACCEPTED  
**Revisit Phase:** NEVER (Hard Boundary)

---

## 4. Conservative C Is Acceptable in Early Phases

**Assumption**
C may behave overly conservatively.

**Invariant**
- Safety > Comfort > Efficiency
- Overreaction is preferable to underreaction in early versions

**Rationale**
Adaptation and learning will address conservatism later.
This is not a structural flaw.

**Status:** ACCEPTED  
**Revisit Phase:** Phase 3

---

## 5. Silence Requires No Immediate Explanation

**Assumption**
The system does not explain whether silence means "no detection" or "no warning".

**Invariant**
- NO_OP / SILENT is a valid and final outcome
- User explanation is deferred

**Rationale**
Different users require different feedback styles.
This must be learned, not hard-coded.

**Status:** ACCEPTED  
**Revisit Phase:** Phase 3

---

## 6. System Time Is the Only Time

**Assumption**
All B–C communication uses system time.

**Invariant**
- No alternative time sources are accepted
- Any mismatch is a synchronization bug

**Rationale**
A single time authority is required for accountability.

**Status:** ACCEPTED  
**Revisit Phase:** NEVER

---

## 7. B and C Evolve Orthogonally

**Assumption**
B and C do not compete in capability.
- C improves immediacy and execution
- B improves foresight and abstraction

**Invariant**
- No capability substitution
- No authority escalation

**Rationale**
Present and future cognition evolve independently.

**Status:** ACCEPTED  
**Revisit Phase:** Phase 3

---

## Document Authority

This document has the same authority as:
- Code review requirements
- Testing requirements
- Security requirements

**Violating these assumptions is as serious as introducing security vulnerabilities.**

---

## Change Process

To modify any assumption:
1. Propose change with explicit rationale
2. Get architecture team approval
3. Update this document
4. Update all affected code
5. Update DCS rules if necessary

**No assumption can be violated "temporarily" or "for testing".**

---

**Version:** v1  
**Last Updated:** 2025-01-12  
**Authority:** Architecture Team
