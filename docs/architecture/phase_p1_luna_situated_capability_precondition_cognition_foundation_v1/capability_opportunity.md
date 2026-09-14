# Capability Opportunity and Eligibility

Opportunity is the generic counterpart of the existing Observation Window.
It is `OPEN` only when the Capability Need is `REQUIRED` and situated
feasibility is `FEASIBLE`. Unstable relation produces `UNSTABLE`; otherwise the
opportunity is `CLOSED`.

Eligibility is true only when all of the following candidate predicates hold:

`Capability Necessity = REQUIRED`
`AND Feasibility = FEASIBLE`
`AND Opportunity = OPEN`
`AND Capability Available = true`.

Therefore availability does not imply necessity or eligibility, and feasibility
does not imply availability. `eligible_now` remains separate from Provider
invocation, Model invocation, Task execution, and Action execution.

