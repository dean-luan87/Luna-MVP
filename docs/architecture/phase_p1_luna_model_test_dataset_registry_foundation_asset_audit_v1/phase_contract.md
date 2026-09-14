# Phase Contract

## In scope

- static inventory of model testing/evaluation/dataset/benchmark/sample/GT/
  provenance assets;
- ownership and source-of-truth analysis;
- reuse/gap matrix;
- recommendation for a generic evaluation-only Dataset Registry;
- minimum next-phase schema contract.

## Out of scope

- downloading or importing public datasets;
- runtime dataset loading, data lakes, training, annotation generation, or
  benchmark execution;
- model/provider/Roboflow changes;
- Test Lens UI changes;
- automatic human-correction-to-GT promotion;
- canonical Field, Current World, Evidence, or cognitive-flow changes.

## Static safety statement

No Runner, Verifier, pytest, benchmark, model inference, network request, or
dataset acquisition was performed for this phase. No static verifier was
created.

## Required next-phase boundary

The next implementation phase may create the evaluation-only registry under
`capabilities/evaluation/dataset_registry/`, after a focused design review.
It must first reuse the four proposed declarations and existing Test Lens,
Evaluation Report, MUEP, and TestBoard contracts. It must not register the
RF-DETR image or any public dataset without explicit provenance/annotation
status.

## Stop condition

Stop at this audit. Do not implement the registry until ownership, schema
reuse, MUEP object-detection vocabulary, media-reference normalization, and
ground-truth review semantics are accepted for the next phase.
