# Producer Compatibility

The previous governed-record producer now reads:

- the Capability Registry `slots` declaration;
- the YOLO11n Model Registry entry;
- the Capability↔Model binding registry;
- the YOLO Provider Registry entry;
- the Model↔Provider binding registry.

The expected remaining missing set is:

```text
RUNTIME_ADMISSION_PRODUCTION_SOURCE
```

This discovery is source-based and does not use scenario IDs, fixture
records, or hardcoded success values.

