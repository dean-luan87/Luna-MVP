# Observation Gateway / Current World / Field Boundary v1

Gateway may emit `CurrentWorldUpdateCandidate` and `FieldEventCandidate`
handoff refs. It does not own Current World or Field state and does not write
either directly.

Target paths are `admitted Evidence refs → Current World candidate formation`
and `Evidence → Field Event candidate → Field admission → Field Reducer`.
