# Model Path and Integrity Boundary v1

Model Governance owns declared governed path and declared checksum metadata.
Filesystem supplies observed physical path/existence. Diagnostics supplies
observed checksum or integrity evidence. Runtime Admission compares supplied
evidence and determines admission.

`Declared checksum != observed checksum` is an integrity/admission input, not a
registry rewrite. Provider does not own checksums. The YOLO11n assets provide
repository evidence for declared/observed checksum separation and no automatic
download/install behavior.
