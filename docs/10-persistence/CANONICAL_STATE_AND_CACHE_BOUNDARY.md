# Canonical State vs Checkpoint vs Cache

> **Status:** CANDIDATE v0.1

The most important Stage-10 rule:

```text
checkpoint ≠ canonical Turn state
cache ≠ canonical Turn state
queue ≠ canonical Turn state
```

## Canonical

Answers:

```text
Was this logical Turn accepted?
Which semantic request does this Turn represent?
What is its canonical status?
Is there a canonical result?
Does it require recovery?
```

## Checkpoint

Future checkpoint answers:

```text
Where might execution resume?
```

A checkpoint may be stale or absent.

It cannot decide whether an external effect happened.

## Cache

Answers:

```text
Can I avoid recomputing/reloading this derived value?
```

Deleting cache must not erase logical execution truth.

## Queue

Future queue answers:

```text
Which work should be delivered?
```

Delivery count is not Turn identity.

This distinction is intentionally preserved before Stage 11/12.
