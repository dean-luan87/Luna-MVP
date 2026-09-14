# Cognitive Visual Evidence Adapter Model v1

## Future input

`Camera Frame / Vision Model Output -> Visual Evidence Candidate`

Candidate categories may include Object Candidate, Scene Candidate, Text Candidate, and Spatial Candidate.

## Required candidate envelope

- source capability and model/version reference;
- time, space, and observation-context reference;
- raw-output reference rather than a fact claim;
- object/scene/text/spatial candidate payload;
- confidence candidate, uncertainty, contradiction indicators, provenance, and trace; and
- `candidate_only=true`, `not_fact=true`, `decision_authorized=false`, `action_authorized=false`.

OCR error example: a text candidate such as `星巴刻` remains an uncertain Visual Evidence Candidate. It cannot mutate Reality, promote a location fact, or issue a navigation instruction.
