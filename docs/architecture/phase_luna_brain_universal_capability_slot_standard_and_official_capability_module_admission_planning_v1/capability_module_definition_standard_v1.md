# Capability Module definition standard

A Capability Module is the capability-level definition that Luna may possess.
It is separate from the Slot that hosts it and from the implementation that
realizes it.

The Module contract may reference:

- module identity/name/domain/purpose
- problem classes
- origin and requirement classification
- capability and implementation versions
- input/output/evidence contracts
- provider/model/implementation resources
- resource, permission, dependency, and compatibility references
- integrity/signature and provenance references
- lifecycle, degradation, rollback, and recovery policies
- Brain Self description and contribution description
- knowledge dependency/interface references
- minimum baseline references where applicable

The list is a semantic contract boundary, not a requirement that every field
be placed in one runtime object.
