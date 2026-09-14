# Negative guards

The controlled evaluation fail-closes for malformed Evidence, missing context
or field references, empty lineage, insufficient/stale input, non-admitted
events, invalid governance authority/responsibility records, and invalid
temporal transitions.

It explicitly guards against:

- direct Evidence, Context, Gateway, Provider, or FPO Field mutation;
- direct reducer bypass and reduction of non-admitted events;
- Context as a Truth source;
- Evidence or Field State as absolute World Truth;
- last-write-wins or fabricated conflict winners;
- silent correction without a correction reference;
- deletion of historical references on reopen;
- automatic Scenario 12 semantic interpretation or merge;
- Memory, Experience, Decision, Task, Action, or new Observation Demand;
- Provider/Model/network/subprocess/thread/socket execution.

The Governance Backbone is reused for rule resolution, preflight,
postflight, authority/responsibility consistency, and unified final-decision
calculation. Negative governance fixtures are malformed records, not
case-name special cases.
