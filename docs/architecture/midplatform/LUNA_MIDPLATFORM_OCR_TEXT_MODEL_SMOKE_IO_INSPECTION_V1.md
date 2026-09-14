# Luna Midplatform — OCR / Text Model Smoke IO Inspection v1

## Scope

P2 model smoke + IO inspection only. No adapter skeleton. No world model assembly.

## Check Objects

- RapidOCR / PaddleOCR cached output
- Text region cached output
- OCR adapter stub
- Blocked paths (missing weight / dependency)

## Mapping Targets

- TextObservationCandidate
- TextRegionCandidate
- TextAnchorCandidate
- TextNormalizationCandidate
