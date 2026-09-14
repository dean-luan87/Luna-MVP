# Attention Modality Priority v1

Attention may rank modality candidates such as visual, auditory, language,
tactile or future senses when those modalities are represented by existing
refs/contracts.

Example: if the relevant event is outside the visual field, auditory evidence
may receive a higher candidate priority. Attention still does not invoke the
microphone, camera, OCR, model or Provider.

No new modality enum is proposed. Existing modality labels remain input or
candidate vocabulary until a later canonical contract review reconciles them.

Modality priority is not Capability Resolution. The selected modality remains
subject to Capability Governance, Runtime Admission, Permission, Resource and
Safety policy.
