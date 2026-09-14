# Cognitive Field Information Boundary v1

## Data boundary

Field Data Boundary classifies information as shared, scoped, restricted, or
unknown. It controls whether data may cross a Field boundary; it does not judge
the meaning of that data.

## Examples

Allowed shared fact:

```text
Battery Low → all active fields may receive a resource constraint candidate
```

Forbidden cross-field flow:

```text
Work Confidential File → Family Field
```

## Contract

Every cross-field reference requires source field, target field, data class,
permission context, purpose reference, validity, provenance, and redaction or
denial result. Information isolation does not create a Decision or modify Reality.

Unknown and denied data remain explicit; the boundary cannot replace missing data
with assumptions.
