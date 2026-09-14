# Real Input adapter cutover

The Real Input adapter still invokes the existing Dynamic Flow engine as a computation source. It now creates a compatibility output and uses the A semantic bundle for downstream final Need, sufficiency, final disposition, and next-step values.

The legacy `dynamic_output` is retained in the result for reverse tracing and old fixture compatibility. This is not direct downstream semantic authority consumption.
