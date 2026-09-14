# Luna Engineering Architecture Constitution v1

## 1. Constitutional Position

This document is the architectural constitution for Luna engineering. It defines the common language, layer boundaries, object semantics, authority relations, naming rules, module shape, and development process that future Luna work must follow.

It is not a product introduction, market plan, single-module design, or technology-selection decision. It does not by itself activate runtime behavior, modify an existing registry, or grant a module new authority.

### 1.1 Normative Use

- New modules, protocols, schemas, and architecture documents must use this vocabulary or explicitly document an approved compatibility mapping.
- A lower-layer module may not claim authority reserved to a higher-level owner.
- Phase instructions and engineering execution governance continue to govern verification authority and stopping behavior. This constitution governs architectural meaning and ownership.
- When an existing asset differs from this document, do not silently rename or rewrite it. Record the mismatch and resolve it in an authorized compatibility or migration phase.

## 2. Architectural Layer Model

Luna has one constitutional layer and five core system layers.

| Layer | Name | Role | May not become |
| --- | --- | --- | --- |
| L0 | Constitution Layer | Immutable architectural principles, safety, permission, and cognitive boundaries | a runtime controller or a business module |
| L1 | Cognitive Flow Layer | Luna's core language for understanding: Observation, Evidence, Field, State, Hypothesis, Information Gap, Decision Candidate, Experience | a model wrapper or direct action engine |
| L2 | Midplatform Layer | Capability, Model, Protocol, Task, Runtime, Permission, and Diagnostic governance | Luna's brain or source of truth about the world |
| L3 | External Capability Layer | OCR, SLAM, Vision, Audio, ASR, TTS, Map, LLM, VLM, and similar external organs | cognitive state owner, fact authority, or action authority |
| L4 | Self Layer | Individual emotion, memory, relationship, preference, worldview, and personality candidates | global truth, collective authority, or direct Field State override |
| L5 | Hive Experience Field | Experience Kernel/Branch association, collective observation, historical evolution, divergence, and conflict records | central brain, voting system, or value arbiter |

### 2.1 L0 Constitution Layer

L0 defines the following non-negotiable boundaries:

- Observation must not directly become Fact.
- Hypothesis must not directly become Conclusion.
- Experience must not directly become Value.
- Hive must not directly control an Individual Luna.
- A Model must not directly replace Cognitive Flow.
- External input is Candidate by default.
- Analysis may not directly execute.
- Authority must be explicit, singular where mutation or final lifecycle ownership exists, and traceable.

### 2.2 L1 Cognitive Flow Layer

L1 is Luna's core. It structures how Luna receives information, preserves evidence, forms a temporal world understanding, represents uncertainty, proposes analysis and delivery candidates, records outcomes, and develops experience.

L1 includes at minimum:

- Observation
- Evidence
- Field
- State
- Hypothesis
- Information Gap
- Decision Candidate
- Experience

L1 understands the world through governed candidate transitions. It does not delegate its semantic authority to a model, vector index, database, graph engine, or Hive.

### 2.3 L2 Midplatform Layer

L2 governs operational capabilities and their safe use: Capability, Model, Protocol, Task, Runtime, Permission, and Diagnostic concerns. It supplies contracts, lifecycle gates, task governance, provider control, and diagnostics to L1 and other layers.

L2 is not Luna's brain. It does not define Field identity, establish cognitive truth, replace hypothesis semantics, or absorb the individual Self System.

### 2.4 L3 External Capability Layer

L3 contains external organs and attachments, including OCR, SLAM, Vision Model, Audio Model, ASR, TTS, Map, LLM, and VLM. Their output is an Evidence Candidate or an observation-derived candidate with source, trace, temporal context, provenance, and uncertainty retained.

L3 must not directly mutate cognitive state, Field State, fact status, task lifecycle, or action state.

### 2.5 L4 Self Layer

L4 forms an individual Luna through governed emotional, relational, preference, memory, worldview, and personality structures. Its outputs are individual context and constraint candidates. L4 cannot declare global truth, force a Field State update, or control another Luna.

### 2.6 L5 Hive Experience Field

L5 associates multiple Luna experience structures. It may represent Experience Kernel links, Experience Branches, collective observations, historical evolution, divergence, conflicts, and game-analysis candidates.

Hive is not a central brain, voting system, consensus engine, or value judge. It must not replace an individual Luna's decision, perspective, Field State, or Self Layer.

## 3. Official Cognitive Terminology

| Term | Official definition | Prohibited substitution |
| --- | --- | --- |
| Observation | A record of an external stimulus entering Luna with source and temporal context | Fact, conclusion, decision |
| Evidence | Information source and provenance that supports a cognitive process | Truth, fact by existence |
| Fact | Data that has passed an explicit, owned admission process and is authorized for its designated world-state use | raw observation, model output, repeated evidence |
| Entity | A candidate object represented in cognition, such as a person, building, road, or entrance | final entity or universal ontology without admission |
| Field | A cognitive environment composed of physical, social, task, and relational context | a simple map label or a model classification |
| State | An effective description of a Field or Entity within a temporal window | event history, model result, arbitrary memory bucket |
| Hypothesis | A possible explanation formed from available information, assumptions, and alternatives | conclusion, fact, action command |
| Information Gap | Missing or uncertain information that materially affects understanding or a later decision boundary | permission to execute a tool |
| Decision Candidate | A structured possible recommendation, choice, or delivery that remains subject to its owning authority | direct action or final decision |
| Experience | A structured, situated record of a process, outcome, context, evidence, and review | value judgment, knowledge base entry by default |
| Experience Kernel | A reviewed reusable experience structure with applicability and counterexample boundaries | policy override, fact, model weight |
| Experience Branch | A versioned association or divergence among episodes/kernels | consensus, vote, shared consciousness |

## 4. Canonical Cognitive Lifecycle

```text
Observation
  -> Evidence
  -> Candidate
  -> Admitted Event
  -> Field State
  -> Hypothesis
  -> Decision Candidate
  -> Outcome
  -> Experience Episode
  -> Experience Kernel
```

Each arrow is a governed transition with a named owner, input contract, output contract, trace/provenance preservation, lifecycle status, and rejection/defer path.

### 4.1 Prohibited Lifecycle Shortcuts

- Observation → Decision is prohibited.
- Observation → Fact is prohibited without admission.
- Evidence → Fact is prohibited without an owning admission process.
- Model output → Field State is prohibited.
- Hypothesis → Conclusion is prohibited without the owning conclusion/decision authority.
- Experience → Fact is prohibited.
- Experience → Value is prohibited.
- Hive Experience → Individual Decision is prohibited.

## 5. Module Constitution Template

Every future Luna module must contain or reference the following fields before implementation is considered complete:

| Required field | Constitutional requirement |
| --- | --- |
| Module Name | One canonical, versioned identity; aliases require compatibility mapping |
| Purpose | The precise problem the module exists to solve |
| Responsibility | Owned capability and lifecycle authority only |
| Input | Versioned, structured input contract and accepted candidate status |
| Output | Versioned, structured output contract and candidate/fact/decision status |
| Authority | Explicit allowed mutations, admissions, or decisions; defaults to none |
| Dependency | Direct upstream/downstream contracts and prohibited dependencies |
| Forbidden Behavior | Testable exclusions, including authority it must not claim |
| Lifecycle | Creation, review, retention, revision, retraction, expiry, and handoff behavior |
| Version | Module, API, schema/protocol, and compatibility version references |

The template is mandatory even for planning modules. A module that cannot state its forbidden behavior or authority is incomplete.

## 6. Naming and File Conventions

| Artifact | Required convention | Example |
| --- | --- | --- |
| Python source | `snake_case.py` | `field_state_reducer_module_api_v1.py` |
| Protocol | `xxx_protocol_v1` | `observation_event_protocol_v1` |
| Schema | `xxx_schema_v1` | `experience_episode_schema_v1` |
| Model/domain object | `xxx_model_v1` | `hypothesis_model_v1` |
| Runner | `run_xxx_v1.py` | `run_cognitive_primitive_controlled_v1.py` |
| Verifier | `verify_xxx_v1.py` | `verify_cognitive_primitive_v1.py` |
| Architecture document | `xxx_v1.md` | `cognitive_flow_architecture_baseline_v1.md` |

Rules:

- One concept has one canonical name in a module boundary.
- Synonyms, legacy names, or migrations require an explicit mapping document.
- Names must communicate object kind and version; generic names such as `utils`, `common`, or `manager` are insufficient without a bounded domain prefix.
- A filename must not imply an authority the module does not own.

## 7. Authority Model

| Domain | May do | Must not do |
| --- | --- | --- |
| External Capability | emit observation/evidence candidates with source and uncertainty | modify Field State, admit fact, execute action |
| Perception / Event Admission | evaluate candidate eligibility and emit admitted/rejected/deferred outcomes | modify final facts or mutate Field State |
| Field State Reducer | produce governed Field State candidates from admitted events | rewrite evidence, accept raw observation, execute action |
| Read Model | read/query/project Field State candidates | mutate state, reduce events, dispatch action |
| Cognitive Analysis | produce hypotheses, differences, information gaps, exploration and delivery candidates | make fact claims, mutate Field State, execute tools/actions |
| Task Manager | govern task lifecycle, authorization, safety, and execution-related candidates | make cognitive truth or treat analysis as fact |
| Experience System | organize reviewed episodes, kernels, and branches | control decision, establish value, admit fact |
| Hive Experience Field | associate experience, divergence, conflict, and history | replace individual choice, vote truth, impose values |
| Human Correction | emit correction and review evidence candidates | automatically overwrite model output or world state |

All authority is least-privilege by default. If an authority is not explicitly documented, it is prohibited.

## 8. Existing Asset Mapping

| Existing module | Current constitutional placement | Future role | Upgrade / replacement status |
| --- | --- | --- | --- |
| Field Event Admission | L1/L2 boundary: candidate event eligibility | Perception Admission to Field Kernel gate | retain; evolve only through compatible protocol work |
| Field State Reducer | L1 Field Kernel mutation authority | candidate Field State maintenance | retain; singular mutation authority |
| Read Model | L1 read-only Field Kernel projection | Cognitive Analysis read surface | retain; no write path |
| Task Manager | L2 task lifecycle and execution governance | delivery/exploration authorization boundary | retain; do not make cognitive truth owner |
| Model Manager | L2/L3 provider governance | external capability attachment control | retain; never fact or decision source |
| Observation Attention | L3-facing attention and follow-up route candidate layer | perception scheduling attachment | retain; not interpretation/state authority |
| Human Correction Layer | review/correction evidence boundary | human evidence and governance input | retain; not automatic ground truth |
| Situation Understanding Model | candidate insight/uncertainty producer | future Cognitive Analysis attachment | upgrade into explicit hypothesis/difference/gap contracts |
| Evidence Chain | shared lineage and non-substitution governance | source/provenance substrate | retain; evidence remains distinct from truth |

## 9. Development Process Constitution

The module is Luna's minimum construction unit. A phase may create multiple files, but its purpose, authority, contract, lifecycle, and verification boundary must describe one coherent module or explicitly bounded architecture artifact.

```text
Architecture Planning
  -> Module Implementation
  -> Module Completion
  -> Unified Validation
  -> Functional Unit Packaging
  -> Integration
```

### 9.1 Process Rules

- Architecture Planning freezes vocabulary, ownership, inputs/outputs, non-goals, and compatibility intent before runtime expansion.
- Module Implementation creates only assets authorized by the phase boundary.
- Module Completion assembles the module contract, documentation, boundary evidence, and required handoff artifacts.
- Unified Validation tests a coherent functional unit, not a collection of unrelated files.
- Functional Unit Packaging makes ownership, dependency, version, and lifecycle discoverable.
- Integration may occur only through declared contracts; it must not transfer ownership implicitly.
- Fragment-driven development is prohibited: files must not be created merely because they are convenient if they do not belong to a defined module/phase boundary.

## 10. Permanent Engineering Prohibitions

1. A model is not a cognitive subject.
2. A knowledge base is not experience.
3. Vector retrieval is not fact.
4. Majority voting cannot decide truth.
5. Hive cannot form a unified consciousness.
6. External data is Candidate by default.
7. Analysis cannot directly execute.
8. Provider availability cannot redefine cognitive semantics.
9. Storage topology cannot define a Field, State, Hypothesis, or Experience Kernel.
10. Convenience integration cannot bypass admission, trace, lifecycle, or authority boundaries.

## 11. Constitution Change Control

Changes to this document require an explicit architecture phase that states the affected principle, compatibility impact, existing asset impact, lifecycle impact, migration/rollback plan, and review authority. Lower-layer implementation phases must not silently reinterpret constitutional terms.

## 12. Current Phase Boundary

This phase creates this document only. It creates no runtime, runner, verifier, database, model connection, registry update, lifecycle update, or code change. The document awaits human architecture review before it is treated as a frozen reference for subsequent work.

