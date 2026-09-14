# Evidence Bundle Snapshot

> **Status:** PROPOSED v0.2 (SURGICALLY HARDENED)

---

## 1. Purpose

A physician-facing explanation must be reproducible.

Therefore Stage 07 should not receive:

```text
search query + mutable web
```

It receives:

```text
EvidenceBundleSnapshot
```

---

## 2. Snapshot includes

```text
bundle_id
experimental_content_sha256
question
timeline_snapshot_id?
frozen_at?
retrieval_policy_version
processing_profile:
  profile_id
  retrieval_policy (PolicyDescriptor: id, version, digest)
  source_selection_policy (PolicyDescriptor: id, version, digest)
  claim_schema (SchemaDescriptor: id, version, digest)
  entailment_policy (PolicyDescriptor: id, version, digest)
  claim_extractor?
  entailment_model?
query intents
retrieval_attempt_ids
selected exact source versions
selected claims
claim-source links
conflicts
limitations
status
```

---

## 3. Freeze & Closure semantics (EVID-017 & EVID-018)

After bundle creation:

```text
selected_sources
selected_claims
claim_source_links
processing_profile
```

are strictly immutable for that bundle.

### EVID-017: Closed Dependency Scope
A frozen `EvidenceBundleSnapshot` has closed dependency scope. Any change to a policy version, policy digest, schema digest, or model version requires a NEW bundle snapshot.

### EVID-018: Late Retrieval Isolation
If a physical retrieval attempt finishes after `frozen_at`, it CANNOT mutate the current frozen bundle. It is preserved in retrieval history as a candidate for a future evidence refresh bundle.

---

## 4. Deterministic experiment identity

Stage 06 experiment uses deterministic sorted JSON + SHA-256.

This demonstrates:

```text
same logical content + policy digest
→ same experimental bundle ID
```

It is not the final cross-language production canonicalization profile. Production profile remains Stage 13.

---

## 5. No ambient retrieval

Stage 07 interface contract:

```text
reason(bundle)
```

not:

```text
reason(question) + freely browse
```

This sharply reduces evidence drift, eliminates race conditions, and makes clinical evaluation possible.

---

## 6. Bundle status

```text
verified
conflicted
incomplete
```

`verified` means bundle structural, closure, and integrity gates passed.
It does not mean the scientific proposition is clinically certain.
