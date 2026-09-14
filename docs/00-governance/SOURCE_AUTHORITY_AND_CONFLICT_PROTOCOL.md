# 09 — Source Authority & Conflict Protocol

## 1. Vấn đề

BioMarker có ít nhất bốn loại nguồn:

1. nguồn yêu cầu của chính BioMarker;
2. chuẩn clinical/safety/regulatory;
3. Mia semantic/design documents;
4. Mia current implementation skeleton.

Nếu xếp tất cả vào một danh sách "file A > file B > file C", ta gặp category error.

Ví dụ:

- load test không thể override clinical safety;
- skeleton mới hơn không tự override product scope;
- JSON Schema không tự override semantic meaning;
- old proposal không thể block later approved decision.

Do đó dùng **authority lanes**.

---

# 2. Knowledge labels bắt buộc

```text
[SOURCE FACT]
[REQUIREMENT]
[CONSTRAINT]
[APPROVED DECISION]
[PROPOSAL]
[IMPLEMENTATION CHOICE]
[ASSUMPTION]
[OPEN QUESTION]
[TEAM DECISION REQUIRED]
[DEFERRED]
[CONFLICT]
[EMPIRICAL EVIDENCE]
[REFERENCE EVIDENCE]
```

Không dùng:

```text
CONFIRMED
```

nếu không chỉ ra confirmed bởi authority nào.

---

# 3. Authority lanes

## Lane A — Product / Business Authority

Quyết định:

- user nào;
- intended use;
- product scope;
- business workflow;
- non-goals;
- acceptance outcome.

Precedence:

```text
Approved BioMarker requirement / owner decision
>
Accepted BioMarker ADR interpreting requirement
>
Current proposed product spec
>
Assumption
>
Reference product
```

Biolyzer nằm mặc định ở:

```text
REFERENCE PRODUCT
```

không phải requirement.

---

## Lane B — Clinical / Safety / Regulatory Authority

Quyết định:

- medical intended-use boundary;
- safety constraints;
- clinical data semantics khi standard applicable;
- legal/regulatory obligations;
- privacy/data governance.

Precedence phải theo jurisdiction/organization thực tế.

General rule:

```text
Applicable law / binding regulation / approved organizational safety policy
>
Approved clinical requirement
>
Accepted BioMarker safety ADR
>
Recognized standard/guidance applicable to the concern
>
Research/reference
>
Engineering inference
```

Experiment performance không có quyền ghi đè lane này.

---

## Lane C — Mia / Platform Integration Authority

Chỉ active khi BioMarker thực sự phải integrate với Mia concern tương ứng.

Precedence:

```text
Accepted/approved Mia external integration contract
>
Approved Mia platform decision
>
Canonical Mia semantic contract
>
Proposed Mia contract
>
Current Mia implementation behavior
>
Historical Mia proposal
>
Inference from code
```

Quan trọng:

> Internal Mia implementation chỉ trở thành BioMarker constraint nếu integration contract yêu cầu.

---

## Lane D — BioMarker Semantic / Architecture Authority

Quyết định:

- BioMarker domain semantics;
- state ownership;
- boundaries;
- lifecycle;
- runtime semantics.

Precedence:

```text
Accepted BioMarker ADR
>
Approved BioMarker semantic spec
>
Proposed BioMarker spec
>
Experiment-supported candidate
>
Assumption
>
Reference architecture
```

---

## Lane E — Machine Contract Authority

Quyết định exact serialized shape.

```text
Canonical machine-readable contract
>
Approved governing semantic decision
>
Proposed machine contract
>
Example payload
>
Implementation inference
```

Rule:

```text
machine-valid
≠
semantically correct
≠
authorized
≠
clinically safe
```

---

## Lane F — Empirical Evidence

Quyết định empirical claim:

- latency;
- throughput;
- extraction accuracy;
- crash behavior;
- retry behavior;
- memory;
- cost;
- mapping accuracy.

Precedence:

```text
reproducible experiment on relevant conditions
>
measured prototype
>
vendor/reference benchmark
>
reasoned estimate
>
intuition
```

Evidence lane có thể thay architecture hypothesis nhưng không tự sửa product/safety requirement.

---

## Lane G — Reference Architecture

Mia skeleton thuộc lane này **mặc định**.

Reference answers:

> "Một hệ thống mạnh khác đã giải problem này như thế nào?"

Không tự trả lời:

> "BioMarker bắt buộc phải làm y như vậy."

---

# 4. Conflict classification

Trước khi resolve, classify conflict.

## C1 — True semantic conflict

Hai source cùng authority lane nói hai meaning incompatible.

Ví dụ:

```text
Spec A: one session pins exact config version.
Spec B: active session always uses latest config.
```

Cần authority/ADR.

## C2 — Maturity evolution

Old source defer feature, later implementation có feature.

Không nhất thiết conflict.

Example:

```text
old: distributed queue DEFER
later skeleton: DBOS exists
```

Interpretation:

> project maturity/evidence changed.

## C3 — Scope difference

Mia general platform cần feature mà BioMarker MVP chưa cần.

Không phải conflict.

## C4 — Representation conflict

Semantic spec và schema khác nhau.

Semantic authority quyết meaning; schema có thể drift.

## C5 — Empirical assumption failure

Experiment bác assumption.

Update hypothesis/ADR; không gọi source "sai" nếu source chỉ là assumption.

## C6 — Authority conflict

Business owner và engineer proposal khác nhau.

Engineer proposal không thắng.

---

# 5. Resolution algorithm

```text
1. STOP the affected decision
2. State exact conflicting statements
3. Classify each statement:
   - lane
   - status
   - scope
   - date/maturity
4. Determine whether they truly govern the same concern
5. Check accepted decisions/contracts in that lane
6. If resolved → follow authority and mark stale source
7. If unresolved:
   - continue independent work
   - record OPEN QUESTION / TEAM DECISION REQUIRED
   - use reversible local assumption only if safe and necessary
8. Never rewrite history:
   - preserve that old source was correct for its state if applicable
9. Add revisit trigger
```

---

# 6. Mia-specific rule

Historical Mia docs explicitly used:

```text
PROPOSAL ≠ APPROVED DECISION
TARGET ARCHITECTURE ≠ IMPLEMENTED SYSTEM
```

Current skeleton, ngược lại, là evidence của implementation.

Khi đối chiếu:

```text
Mia historical doc
→ why / semantic intent / unresolved decisions

Mia skeleton
→ how / implementation mechanics / later maturity evidence

BioMarker
→ own requirement + own evidence + own decision
```

---

# 7. Example: DBOS

Historical Mia runtime spec từng defer:

- generic async job platform;
- distributed queue topology;
- advanced leases/workflow engine.

Current skeleton có DBOS.

Correct interpretation:

```text
NOT:
Historical doc wrong.

NOT:
BioMarker must use DBOS.

BUT:
Mia later acquired requirements/evidence that justified a durable execution mechanism.
```

BioMarker action:

```text
H-xxxx
single-process is sufficient initially

Stage 11:
fault injection

Stage 12:
if hypothesis false, evaluate DBOS and alternatives
```

---

# 8. Example: signed manifest

Mia skeleton:

```text
definition
→ canonical
→ hash
→ Ed25519 signature
→ manifest pin
```

BioMarker không adopt ngay.

First ask:

- reproducibility requirement?
- mutable config risk?
- audit requirement?
- supply-chain/approval requirement?
- untrusted authoring?
- worker must verify offline artifact?

Decision nằm Stage 13.

---

# 9. Red flags

Nếu AI viết:

> "Mia uses PostgreSQL, therefore BioMarker will use PostgreSQL."

→ violation.

Nếu AI viết:

> "FHIR is healthcare standard, therefore database schema will be FHIR resources."

→ violation.

Nếu AI viết:

> "Experiment is fast, therefore safety validation is unnecessary."

→ violation.

Nếu AI viết:

> "Skeleton has JWT, so AuthN is JWT."

→ violation unless upstream contract approves.

---

# 10. Conflict record minimum fields

```text
Conflict ID
Concern
Statement A
Source A / lane / status
Statement B
Source B / lane / status
True conflict?
Scope difference?
Maturity difference?
Decision authority
Temporary action
Blocked work
Independent work allowed
Revisit trigger
Resolution
```
