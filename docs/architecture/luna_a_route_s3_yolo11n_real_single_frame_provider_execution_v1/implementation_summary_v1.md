# Implementation summary

Added a bounded single-frame wrapper under the existing Field Perception
Orchestrator integration owner. The wrapper consumes the existing
YOLO11n external provisioning/admission result, creates the existing bounded
Vision provider admission candidate, and calls the existing local YOLO
provider adapter exactly once.

Provider output remains canonical candidate evidence and an Observation
Gateway handoff candidate. Raw frame bytes are not written to artifacts.
Synthetic S3 regression remains available and is executed before the
optional real case.
