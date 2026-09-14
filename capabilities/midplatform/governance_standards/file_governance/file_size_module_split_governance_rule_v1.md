# File Size and Module Split Governance Rule V1

## Thresholds

### Python

| Level | Lines | Action |
|-------|-------|--------|
| Suggest | ≤600 | OK |
| Warning | 800 | Plan split |
| Blocker | 1200 | Must split before merge |

### Markdown

| Level | Lines | Action |
|-------|-------|--------|
| Suggest | ≤800 | OK |
| Warning | 1200 | Plan split |
| Blocker | 1800 | Must split |

### JSON

- Large tables: use `index.json` + `detail/` shards  
- No monolithic unbounded JSON in standards

## Applies To

Standards, runners, verifiers, registry modules, test board writers.

## Usage Note

When a file approaches blocker threshold, open a split/refactor phase. Do not continue stacking into one file.

## Forbidden

- Single-file standards that exceed blocker limits  
- Mixing unrelated governance domains in one module
