# Durable Turn & Idempotency Model

> **Status:** CANDIDATE v0.1

## Identity

```text
logical key = TurnID
consistency check = IdempotencyKey + semantic request digest
```

Stage 10 does not use global arbitrary idempotency lookup.

## Same request

```text
same TurnID
same IdempotencyKey
same semantic digest
→ replay/join canonical Turn
```

## Conflict

```text
same TurnID
different key or semantic digest
→ conflict
```

No second logical execution is created.

## Concurrent duplicate

The current-process `flights` map coordinates waiters.

Canonical state still lives in durable storage.

```text
flights map = coordination
TurnStore   = authority
```

## Restart duplicate

No in-memory flight exists.

Terminal Turn:

```text
return canonical result
```

Nonterminal Turn:

```text
RECOVERY_REQUIRED
```

No blind execution.

## Revision

`revision` is persistence concurrency/history metadata.

It is not:

```text
Agent Config Version
clinical dataset version
timeline version
```
