# Field Evolution Foundation Architecture Plan v1

The environment adaptation loop is: `Current Field View -> Field Event Candidate -> Admission + Temporal Validity -> Admitted Event -> Reducer -> Field State -> Temporal Evolution / Snapshot -> next Current Field View`.

Event is a possible change, not Fact. Reducer alone updates World State. Temporal Evolution describes the governed change afterward; it never creates State, predicts, or explains causality.
