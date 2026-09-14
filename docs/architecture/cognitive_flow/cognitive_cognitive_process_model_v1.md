# Cognitive Cognitive Process Model v1

## Definition

A Cognitive Process Candidate is a bounded task such as “assess whether a vehicle may yield.” It references input evidence, Situation/Risk/Experience/Future Space module requests, process constraints, and Candidate Set output.

## Process flow

`Trigger -> Create Runtime Instance Candidate -> Create Snapshot Candidate -> Activate Modules Candidate -> Generate Candidate Set -> Evaluate Candidate -> Commit / Discard Candidate -> Close Process Candidate`.

Process != Decision. Process output != Action. Commit / Discard describes candidate lifecycle only and never grants execution or State authority.
