# Validate-Once Reference Governance Standard V1

## Principle

`validate_once_reference_review_ok`

After a shared protocol or standard passes canonical validation once, subsequent failures in referencing modules default to **implementation issues**, not protocol re-audit.

## Re-validate Only When

- Protocol version changes  
- Canonical path changes  
- Reference drift detected  
- Explicit standard patch phase

## Usage Note

Reference phases should check drift (`reference_path`, `version`, `protocol_id`), not re-run full protocol validation every time.

## Forbidden

- Repeated full protocol audit without drift  
- Blaming protocol when reference is stale or wrong
