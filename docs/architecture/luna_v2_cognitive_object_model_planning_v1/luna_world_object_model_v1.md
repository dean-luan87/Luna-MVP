# Luna V2 Cognitive Object Model Planning

## Object Model Purpose

This object model freezes Luna V2’s unified cognitive data language across World Substrate, Perspective, Living Field, Living Context, Meaning and Attachment, Subjective Causality, Developmental Memory and Personality, and Interaction.

Its purpose is to:
- unify Luna’s systems with a common data language while preserving explicit semantic object types
- support dynamic fields, temporal validity, perspectives, meaning, memory, emotion, and subjective causality
- preserve evidence tracking, revocation, and governance boundaries
- maintain candidate_only / not_fact semantics by default
- avoid flattening different semantic objects into a single untyped container

## Object Taxonomy

Luna V2 defines the following first-order object types:
- entity
- state
- event
- relation
- projection
- attachment
- belief
- request
- decision_candidate
- feedback

Each type is defined by ownership, lifecycle, and governance semantics.

### entity
- definition: a persistent or candidate-world object identity with stable core meaning
- ownership: data_owner + interpretation_owner
- long-lived: yes, when admitted as stable candidate or fact
- direct update: not directly updated; changes occur through lifecycle transitions or related state/event objects
- event driven: no, but entity evolution is recorded by events and revisions
- may become fact: only through governance admission; default candidate_only=true
- time validity: requires temporal_validity for active interpretation
- perspective scope: yes, entities are evaluated through perspective_scope

### state
- definition: a condition or attribute value attached to an entity, field, or projection
- ownership: interpretation_owner and execution_owner for updates
- long-lived: yes, as history or current interpretation
- direct update: no, state changes are triggered by events
- event driven: yes
- may become fact: only if supported by evidence and admission governance
- time validity: required
- perspective scope: required

### event
- definition: an occurrence, observation, or transition in the modeled world
- ownership: interpretation_owner and governance_owner
- long-lived: as historical record, yes
- direct update: no, events are immutable once recorded; revisions create supersession
- event driven: yes
- may become fact: candidate_only by default, admission requires evidence
- time validity: required
- perspective scope: required

### relation
- definition: a typed connection between objects
- ownership: interpretation_owner and governance_owner
- long-lived: yes, if maintained as structural knowledge
- direct update: no, relations are created and revised via events
- event driven: usually yes
- may become fact: candidate_only by default, fact admission requires evidence
- time validity: required for context-sensitive relations
- perspective scope: required when relation depends on stance or semantics

### projection
- definition: an interpretation or mapping of underlying substrate into a perspective-specific view
- ownership: perspective_owner and interpretation_owner
- long-lived: yes, as active view or historical projection
- direct update: no, projections are regenerated or revised by governance
- event driven: yes, changes when underlying substrate or perspective changes
- may become fact: no; projections remain interpretive
- time validity: required
- perspective scope: required

### attachment
- definition: an associative object linking meaning, memory, emotion, or context to target objects
- ownership: memory_owner, perspective_owner, and governance_owner
- long-lived: yes, as records of subjective attachment
- direct update: no, attachments are appended and revised with supersession
- event driven: yes
- may become fact: no for emotional and memory attachments; meaning attachments may be candidate admission only
- time validity: required
- perspective scope: required

### belief
- definition: a subjective causal or explanatory assertion
- ownership: interpretation_owner, perspective_owner
- long-lived: yes, as belief records and revisions
- direct update: no, requires revision records
- event driven: yes
- may become fact: no for subjective beliefs
- time validity: required
- perspective scope: required

### request
- definition: a call for observation, information, or action
- ownership: execution_owner and governance_owner
- long-lived: short-lived, lifecycle-bound
- direct update: no, request state changes via related events
- event driven: yes
- may become fact: no; requests are candidate objects
- time validity: required
- perspective scope: required

### decision_candidate
- definition: a candidate choice or recommendation without execution permission
- ownership: interpretation_owner, perspective_owner, governance_owner
- long-lived: maintained until admitted, rejected, or superseded
- direct update: no, revised through decision or feedback objects
- event driven: yes
- may become fact: no; decision candidates remain candidates
- time validity: required
- perspective scope: required

### feedback
- definition: evaluative or corrective commentary linked to candidate or active interpretation
- ownership: interpretation_owner, governance_owner
- long-lived: yes, as correction records
- direct update: no, appended and revised
- event driven: yes
- may become fact: no
- time validity: required
- perspective scope: required

## Core Cognitive Objects

### World Substrate
- SpaceAnchor
- PersonCandidate
- GroupCandidate
- ObjectCandidate
- InstitutionalRuleCandidate
- SocialConventionCandidate

### Living Field
- FieldDefinition
- FieldInstance
- FieldState
- FieldRelation
- FieldEvent
- FieldTimeline
- TemporalValidity
- ActiveFieldProjection

### Perspective
- PerspectiveDefinition
- PerspectiveState
- PerspectiveWeight
- PerspectiveConflict
- PerspectiveSelectionCandidate

### Living Context
- LivingContext
- ContextSignal
- ContextSnapshot
- ExperienceRecord

### Meaning / Memory / Emotion
- MeaningAttachment
- MemoryAttachment
- EmotionAttachment
- ContextTrigger

### Subjective Causality
- CausalCandidate
- SubjectiveCausalBelief
- EmotionalAssociation
- NarrativeExplanation

### Development
- FieldGrowthProfile
- PerspectivePreference
- PersonalityDevelopmentCandidate
- CognitiveRevision

### Interaction
- ExpectationCandidate
- AttentionCandidate
- InteractionDecisionCandidate
- FeedbackCandidate
- ObservationRequest

## Unified World Object Envelope

All core objects share a common World Object Envelope with the following fields:
- object_id
- object_type
- schema_version
- lifecycle_status
- owner_scope
- source_scope
- perspective_scope
- field_scope
- temporal_validity
- confidence
- evidence_refs
- trace_refs
- governance_refs
- candidate_only
- not_fact
- created_at
- updated_at
- revision
- supersedes_ref
- revoked
- revocation_reason
- unresolved_fields
- extension_data

Key envelope rules:
- candidate_only defaults to true
- not_fact defaults to true
- revoked objects cannot continue to participate in ActiveFieldProjection
- extension_data is only for sanctioned extensions and may not bypass formal fields or governance rules

## Ownership Model

Ownership is explicitly partitioned:
- data_owner: owns source evidence and raw content
- interpretation_owner: owns semantic mapping and object typing
- execution_owner: owns action execution and runtime permission requests
- governance_owner: owns admission, revision, and revocation authority
- perspective_owner: owns perspective-specific projections and weights
- memory_owner: owns memory ties and recall associations

Provider boundaries:
- Providers may own raw evidence or provider candidate objects only
- Providers do not own final interpretation or admission authority

## Temporal Model

The model supports:
- valid_from
- valid_until
- recurrence
- expected_duration
- observed_at
- asserted_at
- expired_at
- temporal_confidence
- refresh_policy

## Perspective Model

The model supports:
- primary_perspective
- secondary_perspectives
- mandatory_safety_constraint
- perspective_weights
- suppressed_perspectives
- perspective_conflicts
- selection_reason
- task_ref
- emotion_modulation_ref
- personality_preference_ref

Safety semantics:
- safety is not a normal overridable perspective
- only one primary_perspective is allowed
- multiple secondary_perspectives are permitted
- perspective selection changes interpretation weight, not physical reality
- emotion can modulate perspective but cannot override mandatory safety constraints

## Reality Source Model

Supported reality sources:
- physical
- institutional
- social
- personal

Each source type carries:
- source_scope
- perspective_owner
- applicability_scope
- temporal_validity
- evidence_refs
- confidence
- revocation route

## Candidate and Fact Boundary

The model explicitly states:
- model outputs may only enter candidate status
- personal reality may not automatically become public fact
- subjective causal belief may not become objective fact
- emotion attachment may not be treated as environmental fact
- active projection does not rewrite underlying substrate
- decision candidate does not equal execution permission

## Lifecycle and Revision

Lifecycle states:
- proposed
- observed
- admitted_candidate
- active_candidate
- suspended
- expired
- superseded
- revoked
- archived

Transition rules:
- evidence is required for transitions from observed to admitted_candidate, active_candidate, and archived in some cases
- owner approval is required for revoked, suspended, and superseded transitions when governed
- only active_candidate may participate in controlled runtime eligibility
- suspended, expired, superseded, revoked objects are not written into long-term canonical memory without a separate archival candidate process

## Object Relations

Allowed relation categories include:
- contains
- belongs_to
- adjacent_to
- overlaps
- inherits_rules_from
- temporarily_overrides
- transitions_to
- named_by
- used_as
- perceived_by
- meaningful_to
- emotionally_attached_to
- remembered_through
- triggered_by
- supported_by
- contradicted_by
- conflicts_with
- coexists_with
- supersedes
- derived_from

## Engineering Principles

Frozen principles:
- Concept First
- Schema Second
- Protocol Third
- Runtime Fourth
- Provider Last
- Event before state mutation
- Projection does not rewrite substrate
- Safety overrides perspective
- Multiple perspectives may coexist
- Uncertainty must remain explicit
- No silent candidate-to-fact promotion

## Stop Conditions

This phase does not implement runtime, database, graph databasing, model training, or production activation. It does not migrate directories or modify existing existing code. It creates metadata-only planning artifacts.
