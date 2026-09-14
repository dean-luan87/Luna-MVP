# Cognitive Module Encapsulation Matrix v1

| Subsystem view | Encapsulated existing modules | Input focus | Output focus | Must stay outside |
|---|---|---|---|---|
| Perception & Situation | field/primitive/concept/relationship/situation/affordance | Field/observation | Field/Situation/Affordance candidates | Goal, Decision, Action |
| Context & Intent | state/context/intent/goal/task-role refs | Situation/Human/task | Context/Intent/Goal candidates | Value override, Decision |
| Attention & Resource | attention/gap/value/sufficiency/time/resource/depth/mode | Context/Goal/Risk/Resource | attention/investment/path-need candidates | Runtime scheduler, Action |
| Reasoning & Future | routing/hypothesis/belief/causality/counterfactual/future/preparation | high-value unknown/risk | explanation/future candidates | simulation truth, Decision |
| Evaluation & Decision Support | constraint/behavior/value/optimization/conflict/decision candidate/commitment | candidate/future/constraint space | decision-support candidates | Future Decision, permission, Action |
| Experience & Evolution | outcome/experience/compression/representation/population/culture/gene pool | outcome/history/feedback | experience/evolution/guidance candidates | Memory/Hive write, learning runtime |
| Governance | constitution/contracts/admission/drift/reducer boundary | boundary/validation refs | review/admission candidates | Runtime gate, State owner |

Field, Reducer, future Emotion, and future Hive are independent boundaries. Encapsulation is a documentation view, not a source-code package, ownership transfer, or authority merge.
