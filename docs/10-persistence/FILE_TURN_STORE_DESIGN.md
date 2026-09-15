# File Turn Store Design

> **Status:** Stage-10 minimum-sufficient adapter  
> **Production readiness:** NO

## Layout

One final canonical file per Turn.

Filename:

```text
sha256(TurnID).json
```

Turn ID never becomes a filesystem path.

## Permissions

```text
store dir = 0700
record    = 0600
```

## Create

```text
temp
→ write
→ fsync
→ hard-link(final)
→ fsync directory
```

Existing final path:

```text
load
→ verify integrity
→ same semantic request = idempotent
→ different = conflict
```

## Update

```text
temp
→ write
→ fsync
→ rename over canonical file
→ fsync directory
```

## Integrity

Envelope:

```text
schema_version
record_digest
record
```

`record_digest` detects inconsistent bytes.

## Result artifacts

Stage 10 v0.2 adds a sibling local immutable artifact adapter:

```text
fileartifact.Store
```

It stores payload bytes by SHA-256 and maintains an immutable bucket/key index.

```text
same bucket/key + same bytes
→ idempotent

same bucket/key + different bytes
→ conflict

read
→ SHA-256 + size verification
```

`fileturn.Store` may persist `result_ref` so a future runtime can replay or verify
large payloads without making the Turn record the blob owner.

## Important limitation

This adapter depends on Stage-10 topology:

```text
one application process
one writer
local filesystem
```

It is deliberately not a distributed lock manager.
