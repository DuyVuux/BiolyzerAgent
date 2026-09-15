# Stage 09 — ai-studio Reference Reconciliation

> **Method:** BioMarker runtime derived first, ai-studio reference second.

The reference skeleton describes a mature platform where:

```text
Platform Harness
→ policy/context boundary
→ Eino adapter
```

and explicitly treats Eino as an in-memory graph execution adapter rather than the platform boundary.

## KEEP

```text
runtime adapter boundary
deterministic mock model
compile execution graph once
typed ports
framework isolation
safe structured output validation
```

## ADAPT

```text
ai-studio logical Run identity
→ BioMarker Turn identity

development/mock graph
→ Stage-09 deterministic model

Platform Harness around Eino
→ SingleProcessRuntime around Eino workflow
```

## REJECT for Stage 09

```text
Eino types in domain core
open-ended ReAct for clinical core
direct provider calls from domain packages
```

## DEFER

```text
PostgreSQL authoritative run state
DBOS
lease/fencing
durable model/tool invokers
artifact store
Redis live events
worker process
```

These solve distributed/durable failure modes not present in the current one-process no-side-effect workflow.
