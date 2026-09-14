# Source Version, Correction & Retraction Policy

> **Status:** PROPOSED v0.1

---

## 1. Source lifecycle

Candidate states:

```text
active
corrected
expression_of_concern
retracted
unknown
identity_conflict
incomplete
```

---

## 2. NLM/PubMed behavior

NLM links:

```text
retracted publication
↔
retraction notice
```

and separately represents expressions of concern.

Stage 06 must preserve these states rather than treating all indexed citations as active support.

---

## 3. Crossref role

Crossref metadata may include:

```text
post-publication updates
Retraction Watch data
publisher metadata
```

This is useful corroborating metadata.

It does not replace source-specific verification.

---

## 4. Same identity, same digest

```text
idempotent retrieval
```

---

## 5. Same identity, different digest

### Explicit version/update metadata exists

Store a new source version.

Bundle pins exact version.

### No version/update explanation

```text
identity_conflict
```

Exclude from verified bundle until reconciled.

---

## 6. Retrieval corruption

Partial/incomplete download:

```text
incomplete
```

Do not compute canonical source digest as if content were complete.

---

## 7. Retraction handling

Default Stage 06 policy:

```text
retracted source
→ stored for provenance/history
→ not eligible as positive support
```

Retraction notice itself may be included as evidence about publication state.

---

## 8. Separation of Raw Artifact and Canonical Metadata Digests (EVID-020)

Raw source artifacts (e.g. raw binary PDF files, raw publisher streams) are hashed directly from raw byte sequences (`raw_content_sha256`).

Canonical metadata envelopes (JSON representations of `EvidenceSource`, `EvidenceClaim`, `EvidenceBundleSnapshot`) are hashed via canonical JSON profiles (`content_digest` / `canonical_payload_digest`).

Raw bytes are never serialized through JSON normalizers before hashing.

