# Phase Contract

## In scope

- supplement the prior Dataset Registry asset audit;
- plan P0/P1/P2 Evaluation Strategy;
- define orthogonal Test Case Taxonomy;
- plan machine-readable White-box Evaluation Trace;
- plan Execution Profile, Model Fit Profile, model/version comparison, and
  Cognitive Burden metrics;
- define failure/gap taxonomy and Dataset Registry relationship;
- propose later schema revisions and implementation roadmap.

## Out of scope

- Dataset Registry implementation or real Dataset registration;
- White-box UI;
- model/provider/Roboflow execution or API calls;
- data acquisition, benchmark execution, training, annotation automation;
- runtime binding changes, automatic model selection, Scheduler, or Planner;
- promotion of evaluation results to World Truth or runtime policy.

## Required boundary

The Evaluation subsystem remains offline/evaluation-only. Existing model,
capability, provider, observation, evidence, A, Decision, Task, Action, Field,
and Brain authorities remain unchanged.

## Stop condition

Stop after the planning documents and static checks are complete. The next
phase requires review of schema revisions, MUEP object-detection vocabulary,
dataset ownership, and cognitive-trace observability before implementation.
