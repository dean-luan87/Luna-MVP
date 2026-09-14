# Cognitive Entity Identity Model v1

## Purpose

Entity Identity identifies a particular embodiment node and its bounded operational profile. It establishes protocol ownership, capability provenance, and trust context without creating a personal identity or independent cognitive subject.

```text
EntityIdentityCandidate {
  entity_id,
  embodiment_type,
  capability_profile,
  resource_profile,
  connection_state,
  trust_state,
  owner_brain_reference,
  protocol_compatibility,
  trace
}
```

| Field | Meaning | Boundary |
|---|---|---|
| `entity_id` | Stable entity-node reference. | Not a persona/name claim. |
| `embodiment_type` | Glass, Badge, Watch, Home, Robot, Cloud node, or future category. | Does not grant independent agency. |
| `capability_profile` | Advertised local capability roles and limits. | Availability does not imply execution. |
| `resource_profile` | Local resource/health limits. | Does not set Brain priorities. |
| `connection_state` | Protocol/network channel condition. | Does not change Brain state. |
| `trust_state` | Admission/protocol/trust status for bounded participation. | Not truth or value authority. |
| `owner_brain_reference` | Reference to the sole cognitive-owner boundary. | Does not duplicate Brain memory. |

## Frozen distinction

`Entity Identity ≠ Personality`  
`Entity Identity ≠ Brain Identity`  
`Entity Identity ≠ Memory ownership`

Local identity data may support discovery, protocol compatibility, trace provenance, and secure routing. It must not be used to generate a Goal, persistent value system, or independent long-term experience.
