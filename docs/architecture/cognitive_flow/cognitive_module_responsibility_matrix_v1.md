# Cognitive Module Responsibility Matrix v1

| Module | Purpose | Input | Output | Authority boundary | Forbidden responsibility |
|---|---|---|---|---|---|
| Field Understanding | represent current environmental candidates | primitive, concept, context, temporal/spatial refs | field/view candidates | organize candidate references | fact/state/memory/decision/action |
| Situation Understanding | interpret what may be occurring | field, relations, context, experience/knowledge refs | situation candidates | environment interpretation only | context/fact/decision/action |
| Context Management | describe Luna's current cognitive stance | field/view, survival, task, attention, uncertainty refs | context/state candidates | candidate coordination only | field/state mutation, memory, decision/action |
| Intent Understanding | interpret why a goal may matter | language/behavior/context/situation/goal refs | intent candidates | candidate purpose support | command/goal/decision/action/emotion |
| Goal Understanding | interpret desired results and constraints | user/context/situation/mission/capability refs | goal/subgoal/constraint candidates | desired-result representation | plan/command/decision/action |
| Affordance Understanding | represent possible opportunities/limits | field/situation/context/goal/capability refs | affordance candidates | possible use/limitation only | behavior/permission/decision/action |
| Capability Awareness | represent current possible capability/limits | affordance/context/state/resource/experience refs | capability candidates | behavior-boundary support | authority/identity/permission/action |
| Cognitive Routing | select candidate cognitive path/objective/resources | context/intent/goal/gap/risk/time/resource refs | route/objective candidates | A/B path candidate only | answer/runtime/decision/action |
| Reasoning | support causal, counterfactual, hypothesis evaluation | route, causality, field/context/future refs | reasoning/deep candidates | explanation and possible-world support | fact/simulation/decision/action |
| Future Space | maintain possible futures and branches | hypothesis/belief/causal/counterfactual refs | future branch candidates | uncertainty-space support | prediction truth/decision/action |
| Optimization | compare candidate value under constraints | future/behavior/goal/survival/resource refs | utility/satisfaction candidates | candidate evaluation | optimal truth/decision/action |
| Decision Candidate | form option/choice and trade-off space | behavior/value/constraint/commitment refs | decision option candidates | future-decision input only | actual decision/action/permission |
| Experience | retain outcome-linked historical candidate patterns | outcome/context/decision/action trace refs | experience/guidance candidates | historical pattern support | memory/fact/rule/automatic learning |
| Compression | form minimum sufficient internal representations | field/event/experience/knowledge/situation traces | representation candidates | compression/decompression support | data store/knowledge truth/language/memory |
| Representation Evolution | strengthen/weaken/revise representation candidates | experience/validation/pressure/value refs | evolution/mutation/aging candidates | adaptation consideration | self rewrite/capability growth/state mutation |
| Population Evolution | govern individual-to-population pattern candidates | individual representations/validation refs | culture/gene-pool candidates | propagation/validation support | central control/automatic learning/individual override |

No module may combine Understanding, Decision, Action, and Authority in one responsibility.
