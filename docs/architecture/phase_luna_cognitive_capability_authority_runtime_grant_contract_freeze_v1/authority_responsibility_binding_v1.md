# Authority / Responsibility Binding

## Core rule

Authority implies responsibility. Responsibility cannot be assigned for an
outcome that the receiver had no authority to influence.

Every granted authority must carry:

- decision authority;
- execution responsibility;
- result receiver;
- error owner;
- expiry condition;
- revocation authority;
- trace and provenance.

## Binding table

| Granted authority | Decision authority | Execution responsibility | Result receiver | Error owner | Revocation authority |
|---|---|---|---|---|---|
| Concern admission | Brain | Brain | Brain | Brain | Brain |
| A local Need | A | A | A / Brain | A for local reasoning error | Brain, subject to grant |
| A B request | A within Brain grant | A for request scope | A | A for adoption/use | Brain or grant policy |
| B contingency reasoning | B within derived grant | B for requested result | A | B for bounded reasoning result; A for use | Brain/A per grant |
| Loop persistence | Loop mechanics | Loop engine | issuing A/Brain owner | Loop for mechanical failure | issuing governance |
| Loop pause/wait/resume mechanics | issuing A/Brain/Safety decision | Loop engine | issuing owner | Loop for mechanical failure | issuing governance |
| Capability Scope/Resolution/Provider mapping | Capability/Model Governance | Capability/Provider Governance | requester/governance | Capability owner | Capability Governance |
| Result assimilation | Brain | Brain | Brain | Brain | Brain |

## No orphan responsibility

The following are invalid:

- a Loop responsible for sufficiency because it stores a sufficiency ref;
- B responsible for final Need because B explored a scenario;
- Task responsible for cognitive continuation because it carries a requirement;
- Capability responsible for Goal success because it returned evidence;
- Provider responsible for World Truth because it produced output.

## Candidate-only limitation

This document defines metadata and accountability requirements. It does not
create an executable grant evaluator or mutate existing ownership.
