# Cognitive Perception Adapter Validation v1

## V0 validation cases

| Case | Candidate input | Required outcome | Prohibited outcome |
| --- | --- | --- | --- |
| OCR ambiguity | `星巴克` may be recognized as `星巴刻` | uncertain Visual Evidence Candidate with source/trace | reality/location fact or navigation action |
| VLM uncertainty | `possibly airport` | Situation Candidate support with uncertainty | Situation Fact |
| SLAM spatial output | position/space structure candidate | Spatial Evidence Candidate for later evaluation | direct route planning |
| language input | user utterance | Language Evidence Candidate for Intent/Goal support | goal command or decision |
| audio output | speech/sound candidate | Audio Evidence Candidate with ambiguity | fact or action |

## Static criteria

Every path must terminate in Candidate/Evidence Admission/Cognitive Information Field support only. No real capability is run in this phase.
