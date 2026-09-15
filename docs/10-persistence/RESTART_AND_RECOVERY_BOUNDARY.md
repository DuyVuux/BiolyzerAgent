# Restart & Recovery Boundary

> **Status:** CANDIDATE v0.1

Stage 10 solves:

```text
remember canonical Turn across restart
```

Stage 10 does NOT solve:

```text
what exactly happened if process crashed mid-execution
```

## Known windows

### W0 — before durable ACCEPTED

Safe observation:

```text
no canonical Turn exists
```

Retry can attempt a new reservation.

### W1 — after ACCEPTED, before workflow completion

After restart:

```text
RECOVERY_REQUIRED
```

Stage 10 does not infer whether execution started.

### W2 — workflow completed in memory, before durable terminal commit

After restart:

```text
RECOVERY_REQUIRED
```

Result may have been computed but is not canonical.

### W3 — terminal commit durable, response lost

After restart:

```text
same Turn
→ canonical result replay
→ no workflow execution
```

Stage 11 must inject failures around W0–W3 and decide safe retry/reconcile policy.

External side effects introduce additional unknown windows that Stage 10 intentionally does not solve.
