# BioMarker Agent — Project Skeleton & Monorepo Architecture

> **Status:** PROPOSED TARGET SKELETON v0.1  
> **Project:** BioMarker Agent  
> **Purpose:** Định nghĩa skeleton chuẩn cho repository mới, phục vụ đồng thời **học kiến trúc**, **thực nghiệm**, **build sản phẩm**, **đánh giá AI/clinical quality**, và **tích hợp có kiểm soát với ai-studio Platform** về sau.  
> **Important:** Tài liệu này là **target repository structure**, không có nghĩa mọi thư mục phải được tạo ngay từ Stage 0. Mỗi phần phải được materialize khi Stage tương ứng chứng minh cần.

---

# 1. Mục tiêu thiết kế skeleton

Repository này không được xây theo cách:

```text
copy ai-studio
→ đổi tên
→ xóa bớt
→ thêm biomarker
```

Hướng đúng:

```text
BioMarker problem
        ↓
derive architecture from first principles
        ↓
experiment / benchmark
        ↓
materialize minimum code structure
        ↓
compare with ai-studio reference architecture
        ↓
KEEP / ADAPT / REJECT / DEFER
        ↓
ADR
        ↓
evolve repository
```

Skeleton vì vậy phải đạt đồng thời các mục tiêu:

1. **Dễ học** — nhìn cây thư mục phải hiểu system đang chia boundary thế nào.
2. **Dễ mở rộng** — có chỗ rõ cho Web, API, contracts, evaluation, experiments và infrastructure.
3. **Không over-engineer** — không tạo Worker, Queue, Durable Runtime, Redis, MCP, Compiler hoặc Kubernetes khi chưa có requirement.
4. **Polyglot-friendly** — hỗ trợ TypeScript/React và Go trong cùng monorepo.
5. **Contract-first** — API/schema nằm ở vị trí canonical, không bị chôn trong một implementation.
6. **Evaluation-first** — `evals/` là first-class citizen, tách khỏi unit/integration test.
7. **Clinical safety first-class** — Security và Clinical Safety là hai concern khác nhau.
8. **AI-assisted nhưng engineer-owned** — repository có governance rõ cho AI coding agents.
9. **ai-studio-compatible nhưng ai-studio-independent** — không khóa BioMarker vào implementation nội bộ của ai-studio trước Stage 15.
10. **Production path rõ nhưng không giả vờ production-ready.**

---

# 2. Những điểm không nên sao chép nguyên xi từ `ai-studio`

Skeleton `ai-studio` hiện tại là một **Durable Agent Platform đã trưởng thành**, chứa nhiều lời giải production/runtime như:

```text
DBOS
worker
lease
fencing
durable invokers
manifest compiler
attestation
registry
MCP
Redis Streams
object store
Run FSM
```

Đó là reference architecture có giá trị rất cao, nhưng không phải skeleton tối ưu cho BioMarker ở ngày đầu.

## 2.1. `internal/` đang quá lớn về mặt nhận thức

Ví dụ conceptual:

```text
internal/
├── durable/
├── harness/
├── platform/
│   ├── compiler/
│   ├── contracts/
│   ├── einoadapter/
│   ├── registry/
│   ├── runtimecore/
│   └── store/
├── patterns/
├── providers/
...
```

Cấu trúc này hợp lý khi platform đã có các subsystem trên.

Nhưng với BioMarker mới:

> Người đọc dễ thấy **technology layers** trước khi thấy **domain boundaries**.

BioMarker phải ưu tiên nhìn thấy:

```text
ingestion
observation
normalization
timeline
evidence
analysis
safety
```

trước.

---

## 2.2. Platform concern và product concern cần tách rõ hơn

BioMarker không nên để clinical logic nằm trong một namespace kiểu:

```text
internal/platform/
```

Clinical domain là business/domain core, không phải platform utility.

---

## 2.3. Không tạo infrastructure trước khi có failure mode

Các component như:

```text
worker
DBOS
lease
fencing
Redis
manifest compiler
attestation
```

chỉ được materialize khi Stage tương ứng chứng minh chúng cần thiết.

---

## 2.4. Evaluation phải là top-level concern

AI Studio có eval trong product reference package.

BioMarker cần mạnh hơn:

```text
evals/
```

phải là top-level citizen vì:

```text
software correctness
≠
clinical/AI quality
```

---

# 3. Architecture stance của repository

## 3.1. Monorepo — nhưng không phải monolith

Ta chọn:

> **Polyglot Monorepo**

Repository chứa:

```text
Frontend
Backend
Contracts
Experiments
Evaluations
Documentation
Infrastructure
```

nhưng mỗi boundary vẫn rõ.

---

## 3.2. Một Go module trước, không multi-module sớm

Baseline:

```text
repository root
└── go.mod
```

Toàn bộ Go production code ban đầu dùng **một Go module**.

Không tạo `go.work` chỉ để repository trông “enterprise”.

`go.work` chỉ xuất hiện khi repository thật sự có **nhiều Go modules cần phát triển đồng thời**.

Lý do:

```text
one Go module
→ simpler dependency graph
→ simpler refactor
→ simpler tooling
→ fewer accidental boundaries
```

Multi-module là một architectural choice, không phải badge maturity.

---

## 3.3. pnpm quản lý JS/TS dependency

Dùng:

```text
pnpm
```

cho:

```text
apps/web
packages/*
tooling JS/TS
```

Root có một lockfile:

```text
pnpm-lock.yaml
```

Internal JS/TS packages phải dùng:

```text
workspace:*
```

khi tham chiếu lẫn nhau.

---

## 3.4. Turborepo quản lý task graph

Dùng:

```text
turbo
```

để thống nhất:

```text
dev
build
lint
typecheck
test
```

trên các workspace packages.

Turborepo là **build/task orchestrator**, không phải runtime architecture.

Không được suy:

```text
uses Turbo
→ must be microservices
```

---

## 3.5. Không thêm Makefile + Taskfile + Justfile cùng lúc

Root command surface ban đầu là:

```text
pnpm <task>
```

và với công việc Go chuyên biệt vẫn có thể chạy trực tiếp:

```text
go test ./...
go vet ./...
go run ./apps/api
```

Chỉ thêm Make/Task/Just nếu sau này có concrete cross-language workflow mà `package.json + turbo` giải quyết kém.

---

# 4. Target repository tree

Ký hiệu:

```text
[CORE]        Nên tồn tại từ sớm.
[STAGE-x]     Chỉ materialize từ Stage tương ứng.
[OPTIONAL]    Chỉ tạo khi requirement xuất hiện.
[GENERATED]   Không được sửa tay nếu được sinh từ canonical source.
[LOCAL]       Không commit dữ liệu runtime/local nhạy cảm.
```

```text
biomarker/
│
├── README.md                                  # [CORE] Entry point ngắn gọn của repository
├── CONTRIBUTING.md                            # [CORE] Quy trình branch, commit, review, test
├── AGENTS.md                                  # [CORE] Entry point cho AI coding agents
│
├── package.json                               # [CORE] Root JS/TS task surface + Turbo
├── pnpm-workspace.yaml                        # [CORE] pnpm workspace definition
├── pnpm-lock.yaml                             # [CORE] Single JS/TS lockfile
├── turbo.json                                 # [CORE] Task graph / cache policy
├── .npmrc                                     # [CORE] pnpm policy; không override linker vô cớ
├── .node-version                              # [CORE] Pin Node runtime được team approve
│
├── go.mod                                     # [STAGE-9] Một Go module cho production runtime
├── go.sum                                     # [STAGE-9] Go dependency integrity
│
├── .editorconfig                              # [CORE] Editor-independent whitespace baseline
├── .gitattributes                             # [CORE] Line endings / text normalization
├── .gitignore                                 # [CORE] Build/runtime/local-sensitive exclusions
├── .env.example                               # [STAGE-9] Placeholder-only environment contract
│
├── eslint.config.js                           # [STAGE-13/14] JS/TS lint config khi Web xuất hiện
├── prettier.config.mjs                        # [STAGE-13/14] Formatting policy
├── tsconfig.base.json                         # [STAGE-13/14] Shared TypeScript compiler baseline
│
├── docs/                                      # [CORE] Human-readable source-of-truth
│   │
│   ├── 00-governance/
│   │   ├── AI_ZIP_GENERATION_RULES.md
│   │   ├── SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md
│   │   ├── ARCHITECTURE_HYPOTHESIS_REGISTER.md
│   │   ├── AI_STUDIO_REFERENCE_LEDGER.md
│   │   └── MASTER_ROADMAP.md
│   │
│   ├── 01-product/
│   │   ├── PRODUCT_CONTEXT.md
│   │   ├── INTENDED_USE_AND_SAFETY_ENVELOPE.md
│   │   ├── USERS_USE_CASES_AND_NON_GOALS.md
│   │   └── ASSUMPTIONS_OPEN_QUESTIONS.md
│   │
│   ├── 02-domain/
│   │   ├── BIOMARKER_DOMAIN_MODEL.md
│   │   ├── LAB_REPORT_INGESTION_SPEC.md
│   │   ├── OBSERVATION_NORMALIZATION_SPEC.md
│   │   ├── TERMINOLOGY_MAPPING_SPEC.md
│   │   ├── LONGITUDINAL_TIMELINE_SPEC.md
│   │   ├── EVIDENCE_MODEL_SPEC.md
│   │   └── BIOMARKER_REPORT_SPEC.md
│   │
│   ├── 03-architecture/
│   │   ├── SYSTEM_ARCHITECTURE.md
│   │   ├── COMPONENT_BOUNDARIES.md
│   │   ├── DATA_FLOW.md
│   │   ├── STATE_OWNERSHIP.md
│   │   ├── RUNTIME_ARCHITECTURE.md
│   │   └── AI_STUDIO_INTEGRATION.md
│   │
│   ├── 04-security/
│   │   ├── SECURITY_AND_PRIVACY.md
│   │   ├── DATA_CLASSIFICATION.md
│   │   ├── DATA_RETENTION.md
│   │   ├── THREAT_MODEL.md
│   │   └── SECURITY_TEST_MATRIX.md
│   │
│   ├── 05-safety/
│   │   ├── CLINICAL_SAFETY_REQUIREMENTS.md
│   │   ├── CLINICAL_RISK_REGISTER.md
│   │   ├── SAFETY_GATE_SPEC.md
│   │   ├── CLAIM_GROUNDING_POLICY.md
│   │   └── HUMAN_ESCALATION_POLICY.md
│   │
│   ├── 06-evaluation/
│   │   ├── EVALUATION_STRATEGY.md
│   │   ├── EXTRACTION_EVALUATION.md
│   │   ├── NORMALIZATION_EVALUATION.md
│   │   ├── EVIDENCE_EVALUATION.md
│   │   ├── REASONING_EVALUATION.md
│   │   └── SAFETY_EVALUATION.md
│   │
│   ├── 07-decisions/
│   │   ├── DECISION_INDEX.md
│   │   └── adr/
│   │       └── ADR-XXXX-*.md
│   │
│   ├── 08-operations/
│   │   └── ...                                # [STAGE-15] Runbooks khi có production ops
│   │
│   └── 99-ai/
│       ├── AI_CONTEXT.md
│       └── READ_ORDER.md
│
├── contracts/                                 # Canonical machine-readable cross-boundary contracts
│   │
│   ├── openapi/
│   │   ├── openapi.yaml                       # [STAGE-14]
│   │   └── examples/
│   │
│   ├── schemas/
│   │   ├── clinical/
│   │   │   ├── lab-report.schema.json
│   │   │   └── biomarker-observation.schema.json
│   │   ├── evidence/
│   │   │   └── evidence-claim.schema.json
│   │   └── analysis/
│   │       └── biomarker-report.schema.json
│   │
│   └── fhir/
│       ├── README.md
│       └── mappings/                           # BioMarker domain ↔ FHIR mappings, nếu integration cần
│
├── experiments/                               # Disposable/reproducible technical investigations
│   │
│   ├── README.md
│   ├── stage-03-ingestion/
│   ├── stage-04-normalization/
│   ├── stage-06-evidence/
│   ├── stage-07-reasoning-safety/
│   ├── stage-09-runtime/
│   ├── stage-11-failure-recovery/
│   └── stage-12-durability/
│
├── evals/                                     # AI/clinical quality evaluation — không phải unit tests
│   │
│   ├── README.md
│   ├── datasets/
│   │   ├── extraction/
│   │   ├── normalization/
│   │   ├── evidence/
│   │   └── safety/
│   │
│   ├── rubrics/
│   ├── scorers/
│   ├── harness/
│   └── reports/                               # Generated eval reports; commit policy phải explicit
│
├── testdata/                                  # Chỉ synthetic/de-identified fixtures được phép commit
│   │
│   ├── synthetic/
│   │   ├── lab-reports/
│   │   └── expected/
│   └── README.md
│
├── apps/                                      # Deployable processes / user-facing applications
│   │
│   ├── web/                                   # [STAGE-14] React/Vite TypeScript application
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── tsconfig.json
│   │   ├── index.html
│   │   │
│   │   └── src/
│   │       ├── app/                           # App bootstrap/router/providers
│   │       ├── routes/                        # Route-level composition
│   │       ├── features/
│   │       │   ├── upload/
│   │       │   ├── analysis/
│   │       │   ├── report/
│   │       │   └── chat/
│   │       ├── components/                    # App-level reusable components
│   │       ├── lib/                           # API/auth/helpers; không chứa business core
│   │       ├── styles/
│   │       └── main.tsx
│   │
│   ├── api/                                   # [STAGE-9+] Go deployable API
│   │   ├── package.json                       # Turbo task adapter ONLY
│   │   └── main.go                            # Thin composition root
│   │
│   └── worker/                                # [STAGE-12 CONDITIONAL]
│       ├── package.json                       # Turbo task adapter ONLY
│       └── main.go
│
├── internal/                                  # [STAGE-9+] Go implementation; bounded by root Go module
│   │
│   ├── ingestion/                             # document → extracted observations
│   │   ├── domain.go
│   │   ├── service.go
│   │   ├── ports.go
│   │   └── ...
│   │
│   ├── observation/                           # canonical clinical observation semantics
│   ├── normalization/                         # terminology/unit/range normalization
│   ├── timeline/                              # longitudinal biomarker state
│   ├── evidence/                              # evidence retrieval + provenance
│   ├── analysis/                              # orchestration of analysis pipeline
│   ├── safety/                                # deterministic safety / policy boundary
│   │
│   └── platform/                              # Technical adapters ONLY
│       ├── http/
│       ├── persistence/
│       ├── objectstore/
│       ├── model/
│       ├── telemetry/
│       └── runtime/                            # Eino adapter khi Stage 9 quyết định
│
├── packages/                                  # pnpm-managed reusable JS/TS packages
│   │
│   ├── api-client/                            # [STAGE-14] Typed client derived from OpenAPI
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── ui/                                    # [OPTIONAL] Chỉ khi có >=2 UI consumers
│   │   ├── package.json
│   │   └── src/
│   │
│   ├── eslint-config/                         # [OPTIONAL] Khi cần share config
│   │   └── package.json
│   │
│   └── typescript-config/                     # [OPTIONAL] Khi có nhiều TS packages
│       └── package.json
│
├── tests/                                     # Cross-boundary / system-level verification
│   │
│   ├── contracts/
│   ├── integration/
│   ├── security/
│   └── e2e/
│
├── tools/                                     # Developer tooling có semantics riêng
│   │
│   ├── contract-check/
│   ├── fixture-builder/
│   └── eval-runner/
│
├── scripts/                                   # Small glue scripts only; không chứa business logic
│   ├── verify-repo.*
│   └── check-no-sensitive-data.*
│
├── infra/                                     # [STAGE-GATED] Development/deployment infrastructure
│   │
│   ├── local/
│   │   └── compose.yaml                       # Chỉ khi Stage cần DB/object store/etc.
│   │
│   └── deployment/                            # [STAGE-15]
│       └── ...
│
├── .agents/                                   # Project-specific AI governance only
│   │
│   ├── rules/
│   │   ├── source-discipline.md
│   │   ├── clinical-data-safety.md
│   │   └── repository-boundaries.md
│   │
│   └── workflows/
│       ├── stage-package.md
│       ├── code-review.md
│       └── verification.md
│
└── var/                                       # [LOCAL / GITIGNORED]
    ├── uploads/
    ├── artifacts/
    └── tmp/
```

---

# 5. Cây thư mục KHÔNG được tạo đầy đủ ngay lập tức

Skeleton trên là **target map**.

Day-0 repository chỉ nên materialize phần có evidence:

```text
biomarker/
├── README.md
├── CONTRIBUTING.md
├── AGENTS.md
├── package.json
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── turbo.json
├── .npmrc
├── .node-version
├── .editorconfig
├── .gitattributes
├── .gitignore
├── docs/
├── contracts/             # chỉ schema nào đã được Stage tạo
├── experiments/
├── evals/
└── testdata/
```

Không tạo empty folders chỉ để “đúng skeleton”.

Ví dụ:

```text
apps/worker/
```

**không tồn tại** cho đến khi Stage 12 chứng minh background/durable execution cần thiết.

---

# 6. Root `package.json`

Root `package.json` là:

```text
workspace task surface
+
tooling dependencies
+
Turbo entry point
```

Nó **không chứa application dependencies** như React.

Proposed shape:

```json
{
  "name": "biomarker",
  "private": true,
  "version": "0.0.0",
  "packageManager": "pnpm@<EXACT_APPROVED_VERSION>",
  "engines": {
    "node": "<APPROVED_NODE_RANGE>"
  },
  "scripts": {
    "dev": "turbo run dev --parallel",
    "build": "turbo run build",
    "lint:js": "turbo run lint",
    "lint:go": "go vet ./...",
    "lint": "pnpm lint:js && pnpm lint:go",
    "typecheck": "turbo run typecheck",
    "test:js": "turbo run test",
    "test:go": "go test ./...",
    "test": "pnpm test:js && pnpm test:go",
    "check": "pnpm lint && pnpm typecheck && pnpm test"
  },
  "devDependencies": {
    "turbo": "<EXACT_APPROVED_VERSION>"
  }
}
```

## Important

Không dùng:

```json
"latest"
```

trong committed project configuration.

Khi materialize project:

```text
check approved/current version
→ pin exact version
→ commit pnpm-lock.yaml
```

Không copy version từ tài liệu này sau nhiều tháng.

---

# 7. `pnpm-workspace.yaml`

Baseline:

```yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tools/*"
```

Nếu dùng pnpm catalogs sau khi dependency graph đủ lớn:

```yaml
catalog:
  typescript: "<approved-version>"
  react: "<approved-version>"
  react-dom: "<approved-version>"
```

Lợi ích:

```text
one declared version
→ multiple packages
→ less dependency drift
```

Không cần catalog hóa dependency chỉ có một consumer.

---

# 8. `turbo.json`

Proposed baseline:

```json
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "dev": {
      "cache": false,
      "persistent": true
    },
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".out/**"]
    },
    "lint": {
      "dependsOn": ["^lint"]
    },
    "typecheck": {
      "dependsOn": ["^typecheck"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    },
    "e2e": {
      "cache": false
    }
  }
}
```

## Không cache bừa

Các task có external/non-deterministic behavior như:

```text
live LLM tests
clinical research calls
E2E against mutable services
```

không được cache như deterministic build task.

---

# 9. Go + Turbo integration

Go dependency authority:

```text
go.mod
go.sum
```

pnpm không được quản lý Go dependencies.

Để `turbo dev/build` có thể nhìn thấy Go deployable, `apps/api/package.json` được phép tồn tại như **task adapter**:

```json
{
  "name": "@biomarker/api",
  "private": true,
  "scripts": {
    "dev": "cd ../.. && go run ./apps/api",
    "build": "cd ../.. && go build -o ./apps/api/.out/api ./apps/api"
  }
}
```

Điều này có nghĩa:

```text
package.json
= task registration for Turbo

go.mod
= Go dependency authority
```

Không được thêm Go library vào npm dependency.

---

# 10. Khi nào dùng `go.work`?

Không tạo mặc định.

Tạo khi:

```text
repository có >= 2 Go modules
AND
developer cần edit/test chúng cùng lúc
```

Ví dụ tương lai:

```text
apps/api/go.mod
modules/clinical/go.mod
modules/runtime/go.mod
```

lúc đó root có thể dùng:

```text
go.work
```

Đây là reason-driven adoption.

Không chuyển sang multi-module chỉ vì repository lớn.

---

# 11. Application boundary

## 11.1 `apps/`

Rule:

> `apps/` chứa **deployable process** hoặc **user-facing application**.

Ví dụ:

```text
apps/web
apps/api
apps/worker
```

Không đặt ở đây:

```text
clinical domain library
JSON schema
shared React components
experiment
```

---

## 11.2 `internal/`

Rule:

> `internal/` chứa Go implementation không phải reusable public module.

Nhưng khác `ai-studio`, BioMarker chia **domain-first**:

```text
internal/
├── ingestion/
├── observation/
├── normalization/
├── timeline/
├── evidence/
├── analysis/
├── safety/
└── platform/
```

Không bắt đầu từ:

```text
controller/
service/
repository/
model/
utils/
```

vì cấu trúc đó làm mất domain language.

---

# 12. Bounded Context design

Mỗi domain package có thể tiến hóa theo shape:

```text
internal/evidence/
├── domain.go
├── service.go
├── ports.go
├── errors.go
└── *_test.go
```

Không bắt buộc mỗi package có đủ các file trên.

Ví dụ nhỏ có thể chỉ:

```text
normalization.go
normalization_test.go
```

Nguyên tắc:

> Boundary đúng trước, abstraction sau.

---

# 13. `platform/` có nghĩa rất hẹp

`internal/platform/` chỉ chứa technical adapters:

```text
HTTP
database
object storage
LLM provider
telemetry
runtime adapter
```

Nó không được chứa:

```text
how to interpret LDL
how to normalize ALT
how to build biomarker timeline
how to rank clinical evidence
clinical safety rule
```

Nếu code có clinical meaning, nó không phải platform code.

---

# 14. `contracts/` là canonical cross-language boundary

Không nhét canonical schemas vào:

```text
apps/api/internal/...
```

vì Web, eval harness, fixtures hoặc future ai-studio integration đều có thể cần đọc chúng.

Baseline:

```text
contracts/
├── schemas/
├── openapi/
└── fhir/
```

## Source relationship

```text
semantic spec
        ↓
machine-readable contract
        ↓
generated types/client
        ↓
implementation
```

Không đảo:

```text
TypeScript interface
→ suy ra OpenAPI
→ viết docs để hợp thức hóa
```

trừ khi ADR explicitly chọn code-first contract generation.

---

# 15. `packages/` không được trở thành `shared/` dump

Không tạo:

```text
packages/common
packages/shared
packages/utils
```

nếu không có semantic boundary.

Allowed examples:

```text
packages/api-client
packages/ui
packages/eslint-config
packages/typescript-config
```

Một package chỉ tồn tại nếu có:

```text
clear owner
clear consumers
clear public API
```

---

# 16. Frontend organization

`apps/web` dùng **feature-oriented architecture**.

```text
src/
├── app/
├── routes/
├── features/
│   ├── upload/
│   ├── analysis/
│   ├── report/
│   └── chat/
├── components/
├── lib/
└── styles/
```

Không gom toàn bộ thành:

```text
components/
hooks/
services/
utils/
pages/
```

khi project lớn, vì domain feature bị phân mảnh theo technical type.

---

# 17. `experiments/` khác `src/`

Experiment trả lời câu hỏi.

Ví dụ:

```text
Can parser X extract lab table Y accurately?
```

Production code cung cấp capability ổn định.

Một experiment:

```text
experiments/stage-03-ingestion/
```

được phép:

```text
throw-away
compare multiple approaches
measure
fail
```

Nhưng không được âm thầm trở thành production dependency.

Promotion flow:

```text
Experiment
→ Result
→ Decision
→ Production design
→ Implementation
```

---

# 18. `evals/` khác `tests/`

## Tests

Chứng minh:

```text
software behaves according to contract
```

Ví dụ:

```text
Tenant B cannot read analysis of Tenant A
invalid unit is rejected
API returns typed error
```

## Evals

Đo:

```text
AI / clinical behavior quality
```

Ví dụ:

```text
biomarker extraction recall
LOINC mapping accuracy
claim grounding
citation entailment
unsupported clinical claim rate
```

Không dùng unit-test coverage thay thế eval quality.

---

# 19. Test strategy

## Unit tests

Ưu tiên colocate:

```text
internal/normalization/normalization.go
internal/normalization/normalization_test.go
```

Không tạo root:

```text
tests/unit/
```

chỉ để di chuyển test xa code.

## Root `tests/`

Dành cho cross-boundary behavior:

```text
tests/
├── contracts/
├── integration/
├── security/
└── e2e/
```

---

# 20. Clinical test data policy

Repository chỉ commit:

```text
synthetic
explicitly de-identified
approved test fixtures
```

Không commit:

```text
real patient PDF
PHI/PII
production API response
production logs
access tokens
```

Local sensitive-like development artifacts nằm:

```text
var/
```

và bị gitignore.

---

# 21. Security và Clinical Safety phải tách riêng

## Security hỏi

```text
Ai được đọc dữ liệu?
Ai được sửa?
Tenant/patient nào sở hữu resource?
Secret có bị leak không?
```

## Clinical Safety hỏi

```text
Interpretation có unsupported claim không?
Agent có biến correlation thành diagnosis không?
Critical result có được xử lý đúng policy không?
System có biết khi nào không đủ context không?
```

Hai domain này liên quan nhưng không đồng nghĩa.

Vì vậy:

```text
docs/04-security/
docs/05-safety/
```

được tách.

---

# 22. `tools/` khác `scripts/`

## `scripts/`

Small glue:

```text
verify repo
check generated files
local bootstrap
```

Nếu một script bắt đầu có:

```text
domain types
complex state
tests
versioned behavior
public contract
```

nó nên thành tool thật.

## `tools/`

Developer-facing software:

```text
contract-check
fixture-builder
eval-runner
```

Tool có thể có package/module/tests riêng.

---

# 23. AI governance

Không sao chép toàn bộ `.agents/` khổng lồ của AI Studio.

BioMarker chỉ giữ project-specific rules:

```text
.agents/
├── rules/
│   ├── source-discipline.md
│   ├── clinical-data-safety.md
│   └── repository-boundaries.md
└── workflows/
    ├── stage-package.md
    ├── code-review.md
    └── verification.md
```

Global/general coding skills nên để ở environment/tooling của engineer nếu có thể.

Mục tiêu:

```text
project repo
≠ AI knowledge warehouse
```

---

# 24. Root `AGENTS.md`

`AGENTS.md` nên là AI entry point dưới ~2–4 trang.

Nó phải nói:

```text
What project is this?
What must be read first?
Which sources are canonical?
What must never be assumed?
Where can code be created?
Which commands verify work?
What data must never be logged/committed?
```

Không duplicate toàn bộ architecture docs vào `AGENTS.md`.

---

# 25. Infrastructure policy

Không tạo ngày đầu:

```text
k8s/
helm/
terraform/
redis/
queue/
worker/
```

Stages tạo infrastructure theo evidence.

Ví dụ:

```text
Stage 10 proves PostgreSQL needed
→ infra/local/compose.yaml adds PostgreSQL

Stage 12 proves durable worker needed
→ apps/worker
→ queue/runtime dependency

Stage 15 selects deployment environment
→ infra/deployment/
```

---

# 26. Không tạo `services/` song song với `apps/`

Tránh:

```text
apps/api
services/analysis
services/evidence
```

khi chúng vẫn chạy trong cùng process.

Ban đầu dùng:

```text
apps/api
    ↓
internal/analysis
internal/evidence
```

Chỉ extract một independent deployable khi có evidence như:

```text
independent scaling
independent failure domain
independent lifecycle
security boundary
team ownership
different runtime/toolchain
```

Khi đó nó trở thành một `apps/<deployable>` mới hoặc architecture được ADR điều chỉnh.

---

# 27. Generated code policy

Generated artifacts phải phân biệt rõ.

Ví dụ:

```text
contracts/openapi/openapi.yaml
        ↓
packages/api-client/src/generated/
```

Source of truth:

```text
OpenAPI
```

Generated TypeScript không được sửa tay.

Generated code phải có header/comment nếu generator hỗ trợ:

```text
DO NOT EDIT — generated from ...
```

---

# 28. Dependency policy

Một dependency mới phải trả lời:

```text
Why needed?
Which problem?
Why standard library/current stack insufficient?
Who owns it?
What is its update policy?
```

Không thêm package chỉ vì boilerplate ngắn hơn.

Root không được chứa application dependencies:

```text
react
zod
tanstack-query
```

nếu chỉ `apps/web` dùng chúng.

Chúng thuộc:

```text
apps/web/package.json
```

---

# 29. Naming rules

## Directories

```text
kebab-case
```

cho JS/tooling/docs folder khi cần nhiều từ:

```text
api-client/
contract-check/
```

Go package:

```text
lowercase
```

không underscore nếu không cần.

## Documents

Canonical design docs:

```text
UPPER_SNAKE_CASE.md
```

Ví dụ:

```text
SYSTEM_ARCHITECTURE.md
CLINICAL_SAFETY_REQUIREMENTS.md
```

ADRs:

```text
ADR-0001-short-title.md
```

## Environment variables

Prefix project-specific:

```text
BIOMARKER_...
```

Không dùng generic:

```text
TOKEN
URL
KEY
```

---

# 30. Environment configuration

`.env.example` chỉ chứa:

```text
VARIABLE_NAME=
# explanation
```

Không chứa:

```text
real key
real token
production endpoint with credential
```

Application startup phải:

```text
parse
→ validate
→ fail explicitly
```

Không silent default security-sensitive values.

---

# 31. Local runtime data

Dùng:

```text
var/
```

cho:

```text
uploads
temporary files
generated artifacts
local runtime state
```

`var/` mặc định gitignored.

Không dùng:

```text
tmp/
data/
uploads/
```

rải rác ở nhiều nơi.

---

# 32. Recommended `.gitignore` categories

Ít nhất phải cover:

```text
# Node
node_modules/
.pnpm-store/
.turbo/
dist/
coverage/

# Go
*.test
*.out

# App build
**/.out/

# Environment
.env
.env.*
!.env.example

# Local runtime data
var/

# IDE
.idea/
.vscode/*
!.vscode/extensions.json
!.vscode/settings.json

# OS
.DS_Store

# Generated local reports if policy says non-committed
evals/reports/local/
```

Không ignore canonical fixtures hoặc contracts vô ý.

---

# 33. Recommended `.npmrc`

Conservative baseline:

```ini
engine-strict=true
strict-peer-dependencies=true
```

Không override:

```text
node-linker
hoist-pattern
public-hoist-pattern
```

nếu chưa có dependency compatibility reason.

pnpm defaults nên được giữ khi đủ.

---

# 34. Recommended web stack placement

Nếu Stage 14 giữ React/Vite:

```text
apps/web/
├── package.json
├── vite.config.ts
├── tsconfig.json
└── src/
```

Không cài frontend dependency ở root.

Ví dụ:

```text
React
React DOM
TanStack Query
router
form library
```

đều thuộc `apps/web`.

---

# 35. Where Eino belongs

Nếu Stage 9 chọn Go + Eino:

```text
internal/platform/runtime/eino/
```

hoặc tương đương adapter boundary.

Không để:

```text
Eino graph types
```

lan xuyên:

```text
observation
evidence
safety
timeline
```

Domain core phải hiểu:

```text
domain inputs / outputs
```

chứ không hiểu framework runtime.

Nguyên tắc:

```text
BioMarker domain
        ↓
runtime port
        ↓
Eino adapter
```

không phải:

```text
BioMarker domain
= Eino graph
```

---

# 36. Where ai-studio integration belongs

Không đưa ai-studio-specific types vào domain core.

Tương lai:

```text
internal/platform/ai-studio/
```

hoặc một adapter package tương đương.

Flow:

```text
ai-studio contract
    ↓
ai-studio adapter
    ↓
BioMarker application/domain
```

Như vậy:

```text
BioMarker core
```

vẫn test/run độc lập.

---

# 37. Evolution theo 16 Stage

| Stage | Repository evolution chính |
|---|---|
| **0** | root governance/tooling + docs structure |
| **1** | `docs/01-product` |
| **2** | `docs/02-domain` + first `contracts/schemas` |
| **3** | `experiments/stage-03-ingestion` + testdata |
| **4** | normalization experiments/contracts |
| **5** | timeline/domain semantics |
| **6** | evidence experiments + schemas |
| **7** | reasoning/safety experiment |
| **8** | `evals/` becomes executable |
| **9** | `go.mod`, `apps/api`, `internal/*`, Eino decision |
| **10** | persistence adapters + migrations + local infra if needed |
| **11** | failure/retry experiments + tests |
| **12** | `apps/worker` / durable infrastructure only if justified |
| **13** | config/version/reproducibility contracts |
| **14** | `apps/web`, OpenAPI, `packages/api-client`, security/API |
| **15** | ai-studio adapter + deployment/operations closure |

---

# 38. What Stage 0 repository should actually contain

Ngay bây giờ, nếu materialize repository, tôi khuyên chỉ:

```text
biomarker/
├── README.md
├── CONTRIBUTING.md
├── AGENTS.md
├── package.json
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── turbo.json
├── .npmrc
├── .node-version
├── .editorconfig
├── .gitattributes
├── .gitignore
│
├── docs/
│   └── 00-governance/
│       ├── AI_ZIP_GENERATION_RULES.md
│       ├── SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md
│       ├── ARCHITECTURE_HYPOTHESIS_REGISTER.md
│       ├── AI_STUDIO_REFERENCE_LEDGER.md
│       └── MASTER_ROADMAP.md
│
├── experiments/
│   └── README.md
│
├── evals/
│   └── README.md
│
└── testdata/
    └── README.md
```

Nếu một directory chưa có file thật:

> **Không tạo directory rỗng.**

---

# 39. Những thứ cố ý KHÔNG có trong initial skeleton

```text
PostgreSQL
Redis
DBOS
Kafka
Temporal
worker
lease
fencing
MCP
vector database
Kubernetes
Terraform
GraphRAG
manifest compiler
Ed25519 attestation
microservices
```

Không phải vì chúng xấu.

Mà vì:

> **Stage hiện tại chưa chứng minh chúng cần.**

ai-studio Reference Ledger sẽ giữ chúng như solutions cần nghiên cứu khi problem tương ứng xuất hiện.

---

# 40. Skeleton quality gates

Một thay đổi cấu trúc repository chỉ được chấp nhận khi trả lời được:

### Boundary

- File này thuộc domain nào?
- Ai sở hữu nó?
- Consumer là ai?

### Dependency

- Nó được phép import gì?
- Ai được phép import nó?

### Lifecycle

- Đây là source, generated artifact, test fixture hay runtime data?

### Architecture

- Việc thêm folder/service này có tạo architecture decision không?
- ADR đã có chưa?

### Learning

- Engineer giải thích được vì sao folder tồn tại không?

---

# 41. Anti-patterns

Không tạo:

```text
src/
└── utils/
    └── common.go
```

Không tạo:

```text
packages/shared/
```

như bãi chứa.

Không tạo:

```text
services/
```

cho mỗi domain noun chỉ vì microservice nghe “scalable”.

Không tạo:

```text
infra/k8s/
```

trước khi deployment model được quyết định.

Không để:

```text
contracts
```

bị fork giữa frontend/backend.

Không để:

```text
experiments
```

được import vào production code.

Không để:

```text
evals
```

trộn với unit test.

Không để:

```text
clinical safety
```

trở thành chỉ một prompt.

---

# 42. Mental model cuối cùng

Repository được chia thành 7 loại tài sản:

```text
1. KNOWLEDGE
   docs/

2. CONTRACT
   contracts/

3. EXPERIMENT
   experiments/

4. QUALITY
   evals/
   tests/
   testdata/

5. PRODUCT
   apps/

6. IMPLEMENTATION
   internal/
   packages/

7. OPERATIONS
   infra/
   tools/
   scripts/
```

Nếu một file mới không biết nên thuộc nhóm nào:

> Dừng lại và kiểm tra boundary trước khi tạo.

---

# 43. So sánh mental model với AI Studio

AI Studio có xu hướng thể hiện:

```text
Platform Kernel
→ infrastructure/runtime subsystems
→ product package
```

BioMarker mới ưu tiên:

```text
Clinical Product/Domain
        ↓
contracts + evals
        ↓
minimum runtime
        ↓
platform capabilities earned by evidence
        ↓
ai-studio integration
```

Không có bên nào “đúng tuyệt đối”.

Chúng đại diện cho hai maturity/problem contexts khác nhau.

Mục tiêu của BioMarker là:

> **đến cuối Stage 15, mọi complexity giống ai-studio mà BioMarker giữ lại đều phải có một lý do mà chính chúng ta đã khám phá và kiểm chứng.**

---

# 44. Baseline recommendation

Khóa proposal hiện tại:

```text
Repository style:
Polyglot monorepo

JavaScript package manager:
pnpm

JavaScript task graph:
Turborepo

Go:
single root Go module initially

Frontend:
React/Vite candidate, Stage 14 decision

Backend:
Go candidate, Stage 9 decision

Agent runtime:
Go + Eino candidate, Stage 9 evidence gate

Queue/Worker:
DEFER to Stage 12

Database:
DEFER to Stage 10

ai-studio integration:
DEFER architecture commitment to Stage 15

Canonical contracts:
top-level contracts/

AI/clinical evaluation:
top-level evals/

Architecture decisions:
docs/07-decisions/adr/

Clinical safety:
first-class docs/05-safety/

AI coding governance:
root AGENTS.md + minimal project-specific .agents/
```

---

# 45. Toolchain notes

## pnpm

pnpm phù hợp monorepo vì hỗ trợ workspace, internal workspace protocol và single workspace lockfile.

Project phải pin exact package-manager version khi materialize.

## Turborepo

Turbo dùng để xây task graph và cache deterministic tasks.

Không dùng Turbo để định nghĩa business/runtime architecture.

## Go workspace

Go hỗ trợ `go.work` cho multi-module workspace.

Project này **không dùng nó ở baseline** vì current recommendation là một root `go.mod`.

Nếu sau này tách nhiều Go modules, `go.work` là candidate chính thức thay vì local `replace` directives rải rác.

---

# 46. External references used for skeleton design

Các reference dưới đây chỉ hỗ trợ toolchain/workspace decisions; chúng không phải BioMarker business authority.

- pnpm Documentation — Workspaces / package manager behavior: `https://pnpm.io/`
- Turborepo Documentation: `https://turborepo.com/docs`
- Go Workspaces Tutorial: `https://go.dev/doc/tutorial/workspaces`
- Go Modules Reference: `https://go.dev/ref/mod`

---

# 47. Status summary

| Decision | Status |
|---|---|
| Polyglot monorepo | **PROPOSAL — RECOMMENDED** |
| pnpm | **USER-REQUESTED / RECOMMENDED** |
| Turborepo | **USER-REQUESTED / RECOMMENDED** |
| Root single Go module initially | **PROPOSAL — RECOMMENDED** |
| `go.work` immediately | **REJECT FOR NOW** |
| React/Vite | **CANDIDATE — Stage 14** |
| Go production backend | **CANDIDATE — Stage 9** |
| Go + Eino | **CANDIDATE — Stage 9** |
| PostgreSQL | **DEFER — Stage 10** |
| Worker / DBOS / durable queue | **DEFER — Stage 12** |
| Manifest / attestation | **DEFER — Stage 13** |
| ai-studio coupling | **DEFER — Stage 15** |
| `evals/` top-level | **RECOMMENDED CORE** |
| `experiments/` top-level | **RECOMMENDED CORE** |
| Security separate from clinical safety | **RECOMMENDED CORE** |

---

## Final principle

```text
A good repository skeleton does not predict every future component.

A good repository skeleton makes the correct next component obvious
when the requirement finally appears.
```

Với BioMarker:

> **Skeleton phải giúp chúng ta học được vì sao architecture tiến hóa, chứ không che giấu quá trình đó bằng một cây thư mục “enterprise” được sinh sẵn.**
