# Layered Ground Truth Contract

## World Ground Truth

Objective annotatable world facts: object existence, scene properties, spatial
relations, target existence, and environmental state. This is evaluation GT,
not Luna World Truth.

## Observation Ground Truth

What is available from the particular view: visible, partially visible,
occluded, outside ROI, unobservable, or ambiguous.

## Cognitive Evaluation Assertions

Process constraints include:

- no Sufficiency with required information missing;
- preserve uncertainty;
- never promote Provider output to World Truth;
- form an Information Gap when required;
- re-observe when required;
- do not re-observe without justification;
- stop at minimum sufficient information;
- preserve Owner boundaries.

The assertion layer evaluates process and does not contain the desired
semantic answer.
