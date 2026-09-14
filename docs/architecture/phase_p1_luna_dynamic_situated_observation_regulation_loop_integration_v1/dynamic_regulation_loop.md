# Dynamic Regulation Loop

The regulation layer is a finite coordinator for candidate state changes. It
does not sleep, poll hardware, schedule background work, or issue actions.

For each explicit state in a controlled sequence it performs:

1. derive condition candidates from Self/Field/Target/Relation inputs;
2. evaluate the existing Capability Need, Feasibility, Gap, Adjustment,
   Opportunity, and Eligibility contracts;
3. enter `WAITING_FOR_CONDITION_CHANGE` when conditions are not feasible;
4. re-evaluate the same cognitive need at the next supplied state;
5. delegate to the existing eligibility-gated RapidOCR path only when the
   current state is eligible and the step is not intentionally deferred;
6. read the existing RuntimeObservation/Gateway/Evidence/A-Route/CState and
   Sufficiency result.

The finite cases cover one wait, multiple waits, an opportunity that is lost
before execution, and a Not Required exit. There is no autonomous loop beyond
the explicit state sequence.
