# Stage 09 — Eino Adapter Decision

> **Decision:** ADOPT Eino v0.9.19 behind runtime adapter boundary.

## Evidence

As of September 2026:

```text
v0.9.19 = stable release
v0.10.x = pre-release line
```

Eino supports:

```text
Chain
Graph
Workflow
ChatModel
Tool
Retriever
```

Stage 09 uses only composition.

## Why Eino

- Go-native framework;
- explicit structured composition;
- aligns with current engineering direction;
- framework can remain an adapter;
- future model/tool components can be added without changing domain contracts.

## Why not Eino ADK/ReAct now

Stage 09 clinical reasoning core requires:

```text
closed inputs
bounded sequence
deterministic safety
no ambient tools
```

Open-ended agent behavior adds unnecessary authority and failure modes.

## Adapter invariant

Only:

```text
internal/platform/runtime/eino
```

may import:

```text
github.com/cloudwego/eino/*
```

No domain package may depend on Eino types.

## Upgrade policy

Framework upgrade must rerun:

```text
go test ./...
go test -race ./...
Stage-08 evaluation
Stage-09 runtime smoke/integration tests
```

before acceptance.
