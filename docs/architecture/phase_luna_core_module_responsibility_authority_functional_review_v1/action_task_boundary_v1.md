# Task → Action Boundary v1

Task may produce bounded Action candidates from an approved Decision and Task
constraints. Task does not execute, authorize around missing permission, select
a Provider or decide a retry. Action Governance validates source, target,
preconditions, duplicate boundary and current constraints before handoff.

Task completion and Action execution status remain separate facts.
