# Attention Spatial / Object Focus v1

Attention may produce candidate refs for:

- object or entity target;
- region/ROI;
- spatial focus;
- focus score and risk score;
- persistence/decay;
- expected evidence type.

Existing Observation Attention assets support region IDs, priority levels,
uncertainty tags, motion-state candidates and follow-up route refs. These are
candidate focus data, not object identity, motion Truth, Field state or
navigation instruction.

Attention must preserve source geometry/evidence refs and provenance. A
candidate focus cannot promote a prompt label, segmentation label or single
frame observation into fact.
