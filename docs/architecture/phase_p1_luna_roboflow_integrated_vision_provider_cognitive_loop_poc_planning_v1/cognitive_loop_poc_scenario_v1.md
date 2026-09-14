# Primary Cognitive-Loop PoC Scenario

## Goal

`Find the likely exit from the current room/environment.`

## Observable scenario, without answer encoding

1. Brain supplies Goal/Concern/Grant and a valid Working Envelope.
2. A produces a local Cognitive Requirement for exit-relevant visual
   information; it does not choose Roboflow or a physical model.
3. Attention/Observation forms a bounded request for object detection and,
   where signage is visible, OCR evidence.
4. Governed Capability/Model/Runtime/Provider records admit a candidate
   external observation path.
5. Roboflow returns provider-native detections and optional OCR output.
6. The adapter maps detections/text to separate candidate evidence records.
   Multiple doors, signs, weak labels and conflicts remain separate.
7. Gateway/evidence handling preserves source, frame, ROI, workflow/model,
   confidence, uncertainty, trace, provenance and versions.
8. Current World is updated only as a candidate representation; Field Event
   is emitted separately only when an operational transition is proposed.
9. Cognitive State Formation/A consumes the candidates, creates or revises
   hypotheses, and evaluates sufficiency.
10. If insufficient, the information-gap detector and re-observation policy
    produce a targeted OCR/region/observation request. If sufficient, A may
    produce a Decision candidate. Neither result is hardcoded by the fixture.

## Required ambiguity

The input must permit at least two plausible door/sign candidates and allow
low confidence, missing text, stale evidence, and detection/OCR disagreement.
The test oracle checks structural routing, evidence preservation, hypothesis
revision capability and sufficiency/re-observation behavior. It must not
assert a preselected exit label.

## Success is not “correct answer”

The PoC succeeds structurally when real external evidence can be traced into
Luna evidence and returned to A as either a bounded next-observation request
or a Decision candidate, while all authority and candidate-only guards hold.

