# Field Kernel Reducer Boundary v1

Field Kernel may query, organize, represent, compare, and observe references. Reducer alone mutates Field State.

`Field Event Candidate -> Admission -> Admitted Event -> Reducer -> Field State` is the only write path. Kernel cannot admit Event, reduce candidate, update State/Snapshot/History, or rewrite temporal validity.
