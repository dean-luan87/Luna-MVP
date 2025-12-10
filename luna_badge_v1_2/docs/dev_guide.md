# Development Guide

## Ask System Development Guide

### 1. How to define an AskSchema

```python
from task_engine.ask import AskSchema, AskSlot, AskSlotKind

schema = AskSchema(
    task_id="hospital_route",
    slots=[
        AskSlot(
            name="hospital_name",
            kind=AskSlotKind.REQUIRED,
            prompt_template="去哪家医院？"
        ),
    ]
)
```

### 2. How AskChain is built

```python
from task_engine.ask import AskChainBuilder

builder = AskChainBuilder()
plan = builder.build_chain(schema)
```

### 3. How AskChainRuntime executes

```python
from task_engine.ask import AskChainRuntime, AskManager
import time

ask_manager = AskManager()
effective_policy = schema.effective_retry_policy()
runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

# produce prompt
result, state = runtime.step(user_input=None, now_ts=int(time.time()))

# parse and advance
result, state = runtime.step(user_input="用户输入", now_ts=int(time.time()))
```

### 4. Running Demo

```bash
python3 scripts/demo_askchain.py
```

### 5. Testing Ask System

All Ask-related tests are under:

```
tests/v1_4_6a/
```

Run all Ask tests:

```bash
cd luna_badge_tests
pytest tests/v1_4_6a/ -v
```

---

## Other Development Topics

(Add more development guides here as needed)

