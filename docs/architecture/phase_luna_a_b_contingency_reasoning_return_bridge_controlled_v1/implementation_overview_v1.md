# Implementation Overview

The package reuses the prior Cognitive Authority Grant, derived-grant, responsibility-binding, A semantic authority, and Loop mechanical-boundary candidates. It adds only a bounded integration seam.

Flow:

`A uncertainty trigger → A request → derived B grant → bounded B envelope → B result → A handoff → A evaluation`.

The implementation is synthetic and candidate-only. Existing A, Dynamic Flow, and Loop engines are not rewritten.
