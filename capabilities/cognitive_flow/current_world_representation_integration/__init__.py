"""A2 Current World Representation fixture integration.

Provides simulation-only integration fixtures, reference envelopes, and
contract validation for the Current World Representation chain.

This package does not execute a real Reducer, Read Model, database, network,
model, or production runtime.
"""

from .current_world_representation_envelope_v1 import (
    CurrentWorldRepresentationEnvelopeV1,
)
from .integration_dryrun_v1 import run_controlled_integration_dryrun_v1
from .integration_types_v1 import CurrentWorldRepresentationIntegrationDryRunResultV1

__all__ = (
    "CurrentWorldRepresentationEnvelopeV1",
    "CurrentWorldRepresentationIntegrationDryRunResultV1",
    "run_controlled_integration_dryrun_v1",
)
