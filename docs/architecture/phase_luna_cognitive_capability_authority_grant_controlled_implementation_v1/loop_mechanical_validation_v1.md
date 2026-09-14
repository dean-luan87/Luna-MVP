# Loop Mechanical Validation

## Accepted operations

The controlled registry maps allowed mechanical commands to:

- persistence;
- state-version recording;
- reference recording;
- pause/wait/resume mechanics;
- final freeze;
- history archive;
- trace append.

## Validation order

1. command is inside Loop Capability Boundary;
2. receiver is a Loop Engine instance;
3. issuer A/B grant is active;
4. Loop mechanical grant is active;
5. Concern and Work match;
6. source state version matches;
7. Permission and Resource refs exist;
8. responsibility bindings are valid.

## Return boundary

Loop returns only mechanical state facts and supplied semantic refs. It never
synthesizes sufficiency, Need, Hypothesis validity, Replan, Capability choice,
Provider choice, Concern split/merge or result adoption.
