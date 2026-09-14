# Prohibited Behavior & Escalation Policy

> **Status:** PROPOSED v0.1  
> **Current clinical escalation policy:** DISABLED_PENDING_APPROVED_CLINICAL_POLICY

---

## 1. Prohibited current-MVP behavior

```text
diagnose disease
rule disease in/out as an AI authority
prescribe medication
start/stop medication
change dose
direct treatment
autonomous emergency triage
```

---

## 2. Why deterministic?

A prompt saying:

```text
"do not diagnose"
```

is useful but insufficient.

The final structured candidate must pass a policy gate that rejects prohibited semantic intent.

---

## 3. Abnormal flag vs diagnosis

Allowed controlled statement:

```text
"Observation X is outside the source-provided range."
```

Not allowed:

```text
"This proves disease Y."
```

---

## 4. Evidence association vs patient diagnosis

Potentially allowed:

```text
"Evidence Claim C reports an association between X and Y in the studied population."
```

Not allowed:

```text
"Therefore this patient has Y."
```

---

## 5. Critical/panic values

No approved threshold/escalation matrix was supplied.

Therefore:

```text
AI-generated urgent/emergency classification
→ REJECT
```

If the **source report itself** contains an explicit critical flag, Stage 07 may surface:

```text
"The source report marks this result as critical."
```

as a `measured_fact`, but current policy adds an explicit limitation because no approved autonomous escalation workflow is active.

This preserves the source assertion without inventing:

```text
emergency diagnosis
triage category
treatment action
```

A future approved policy may introduce deterministic escalation outside the model.

That future policy must define:

```text
measurement identity
method/specimen applicability
threshold/source
repeat/confirmation rule
escalation route
clinical owner
validation/evaluation evidence
```

---

## 6. More evidence needed

Allowed system outcome:

```text
NEED_MORE_EVIDENCE
```

This routes back to Stage 06.

It does not authorize Stage 07 to search.

---

## 7. Physician review

Every approved output remains:

```text
physician_review_required = true
```

for the current MVP.
