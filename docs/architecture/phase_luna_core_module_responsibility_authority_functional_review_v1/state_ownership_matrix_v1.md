# State Ownership Matrix

| State | Intended owner | Representation in other modules | Mutation/transition owner | Loop role |
|---|---|---|---|---|
| Goal | Brain | refs in envelope/Task | Brain governance | record ref |
| Cognitive Concern | Brain | A/B work refs | Brain admit/split/merge | record work/Concern ref |
| A local reasoning state | A | candidate refs to Loop/Brain | A | persist refs/version |
| B local contingency state | B, bounded | A handoff/result refs | B inside request | record branch ref |
| Field State | Field Reducer | Context/Current World refs | Field owner | record ref |
| Context | Context Foundation | envelope/State Formation refs | Context owner | record ref |
| Current World | State Formation candidate + source world refs | A/B envelope | source/formation candidate | record ref |
| Intent | Intent Governance | A/Task refs | Intent owner | record ref |
| Task lifecycle | Task Manager | envelope/A refs | Task Manager | record ref |
| Attention plan | Attention Governance | Observation/A refs | Attention policy owner | record ref |
| Capability catalog/asset | Capability/Model Governance | A/Runtime Admission refs | respective source owner | record ref |
| Runtime admission | admission governance candidate | Provider/A refs | evidence-bound adapter | record admission ref |
| Loop lifecycle | Loop | A/Brain supplied semantics | Loop mechanics | owns mechanical state |
| Outcome | Brain/global governance with source candidates | Loop/A refs | governance acceptance | record outcome ref |

Main duplication risk is not every reference; it is copying authoritative values into a second mutable owner. Current World and A/B envelopes must remain candidate/ref-based.
