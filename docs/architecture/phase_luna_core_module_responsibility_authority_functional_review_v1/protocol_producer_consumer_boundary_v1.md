# Protocol Producer and Consumer Boundary v1

Producer owns correctness of the payload/state emitted against the declared
protocol version. Producer does not own protocol lifecycle unless it is also
the canonical protocol owner.

Consumer owns validation and interpretation of supported versions. It must not
silently reinterpret unsupported versions or treat a valid structure as valid
semantic meaning without its own contract.
