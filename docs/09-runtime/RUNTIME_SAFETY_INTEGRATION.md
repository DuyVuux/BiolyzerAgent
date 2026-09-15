# Stage 09 — Runtime Safety Integration

## 1. Model output is untrusted

```text
CandidateGenerator
→ ReasoningCandidate
```

never goes directly to transport.

## 2. Output-shape preflight

Before deterministic safety evaluation, Stage 09 validates the candidate's minimum structured shape:

```text
schema_version
candidate_id
statement_id
statement_class
statement text
```

This is the single-process adaptation of ai-studio's output-validation funnel. It catches malformed model output before clinical safety semantics are evaluated.

## 3. Safety flow

```text
Candidate
→ deterministic Evaluator
→ SafetyDecision
→ SafeReasoningOutput?
```

`reject` and `defer` return no SafeReasoningOutput.

## 4. Runtime success ≠ safety approval

Example:

```text
workflow runs successfully
candidate says diagnosis
safety verdict = reject
runtime status = completed
```

This is correct.

The runtime completed its job of safely evaluating the candidate.

## 5. Current production-shape evaluator

The Go evaluator implements Stage-07 core restrictions:

```text
prohibited statement classes
prohibited inference modes
ambient actions
unknown/unverified/reconciliation clinical refs
candidate terminology in interpretation
unsupported/conflicted evidence
missing-context disclosure
critical source signal limitation
review basis
```

Stage 08 remains the evaluation authority for gate quality.

## 6. Physician review

Every surfaced `SafeReasoningOutput` contains:

```text
physician_review_required = true
```

plus exact snapshot/bundle/reference/policy basis.
