# Stage 09 — Runtime Execution Contract

## 1. Distinctions

```text
Turn ID ≠ Idempotency Key
logical Turn ≠ physical function invocation
Runtime result ≠ public physician-facing API response
structurally valid JSON ≠ trusted clinical input
```

## 2. Request

`RuntimeExecutionRequest` pins:

```text
turn_id
idempotency_key
correlation_id?
deadline_ms?
clinical snapshot
timeline snapshot?
frozen evidence bundle
closed clinical references
reasoning/safety policy digests
user question
```

## 3. Result

Status:

```text
completed
failed
cancelled
```

A completed execution may still contain:

```text
SafetyDecision = reject/defer
```

because runtime completion and clinical safety approval are different axes.

## 4. Idempotency

Same Turn identity + same serialized semantic request:

```text
reuse in-process result
```

Same Turn identity + changed request:

```text
IDEMPOTENCY_CONFLICT
```

No second generation occurs.

## 5. Deadline

`deadline_ms` produces a child Go context.

Cancellation propagates through:

```text
SingleProcessRuntime
→ Eino workflow
→ CandidateGenerator
```

Current no-tool workflow has no external side effect to roll back.

## 6. Error privacy

Runtime error payload returns:

```text
safe code
safe message
```

not raw clinical payload, provider secret, chain-of-thought or stack trace.
