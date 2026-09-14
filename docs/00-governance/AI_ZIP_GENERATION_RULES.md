# AI Zip & Code Generation Rules

> **Purpose:** Guidelines for AI agents generating code, project archives (zips), PR bundles, or automated changes for any Stage of BioMarker Agent.
> **Enforcement:** Zero-Tolerance. Any generated zip violating these rules will be rejected and require regeneration.

---

## 1. Core Structural Principles

### 1.1. Root-Relative Path Principle (Tuyệt đối không bọc folder ngoài)
* **FORBIDDEN (CẤM):** Không được bọc các file bên trong một thư mục gốc ảo như `stage-01-product-discovery/docs/...`.
* **MANDATORY (BẮT BUỘC):** Mọi đường dẫn trong file zip phải bắt đầu tương đối trực tiếp từ **Monorepo Root**.
* **Kiểm tra Unzip:** Khi giải nén lệnh `unzip stage-XX.zip -d /workspace/projects/MialyzerAgent/`, các file phải rơi chính xác vào cây thư mục của dự án:
  - `docs/01-product/PRODUCT_CONTEXT.md` (ĐÚNG)
  - `stage-01/docs/01-product/PRODUCT_CONTEXT.md` (SAI)

---

## 2. Stage-Gated File Placement (Đúng Stage, Đúng Vị trí)

Mỗi Stage chỉ được phép tạo file trong phân vùng tương ứng đã quy định tại [BIOMARKER_PROJECT_SKELETON_V0.1.md](../../BIOMARKER_PROJECT_SKELETON_V0.1.md) và [MASTER_ROADMAP.md](./MASTER_ROADMAP.md):

| Stage | Thư mục được phép tạo / cập nhật | Điều cấm kỵ |
|---|---|---|
| **Stage 1** | `docs/01-product/`, `docs/00-governance/STAGE_02_HANDOFF.md` | CẤM tạo code Go, Python, React hay contracts. |
| **Stage 2** | `docs/02-domain/`, `contracts/schemas/clinical/` | CẤM tạo runtime backend/frontend. |
| **Stage 3** | `experiments/stage-03-ingestion/`, `testdata/synthetic/lab-reports/` | CẤM import `experiments/` vào `apps/` hay `internal/`. |
| **Stage 4** | `experiments/stage-04-normalization/`, `contracts/schemas/` | CẤM dùng thư viện normalization ngoài khi chưa đo đạc. |
| **Stage 5** | `docs/02-domain/LONGITUDINAL_TIMELINE_SPEC.md`, timeline contracts | CẤM tạo DB time-series chuyên biệt. |
| **Stage 6** | `experiments/stage-06-evidence/`, evidence contracts | CẤM lưu trữ bài báo có bản quyền trái phép. |
| **Stage 7** | `experiments/stage-07-reasoning-safety/`, `docs/05-safety/` | CẤM hạ thấp rào chắn an toàn lâm sàng. |
| **Stage 8** | `evals/datasets/`, `evals/scorers/`, `evals/harness/` | CẤM gộp `evals/` chung với unit `tests/`. |
| **Stage 9** | `go.mod`, `go.sum`, `apps/api/`, `internal/*` | Bắt đầu Go backend. CẤM tạo microservices hay `go.work`. |
| **Stage 10** | `internal/platform/persistence/`, `infra/local/` | Chỉ tạo DB adapter khi có schema migrations cụ thể. |
| **Stage 14** | `apps/web/`, `packages/api-client/`, `contracts/openapi/` | Bắt đầu React/Vite frontend. |

---

## 3. Phân tách Tài liệu Quản trị Cấp cao vs Ghi chép Nội bộ

Nhằm giữ repo luôn **sạch sẽ, chuyên nghiệp trước mắt lãnh đạo (Executive-Ready)**:

1. **Tài liệu chính thức (Sếp xem - Git track):**
   - Đặt trực tiếp vào thư mục nghiệp vụ: ví dụ `docs/01-product/PRODUCT_CONTEXT.md`.
   - Đặt tên chuẩn UPPER_SNAKE_CASE: `INTENDED_USE_AND_SAFETY_ENVELOPE.md`, `USERS_USE_CASES_AND_NON_GOALS.md`.
   - Biên bản bàn giao stage đặt tại: `docs/00-governance/STAGE_<XX>_HANDOFF.md`.

2. **Hồ sơ tự học, phân rã task vụn vặt (Nội bộ AI/Dev - Git ignore):**
   - Mọi file ghi chú học tập (`*_LEARNING_GUIDE.md`), phân rã task (`*_TASK_BREAKDOWN.md`), nhật ký nghiệm thu, hoặc manifest (`PACKAGE_MANIFEST.yaml`):
   - **BẮT BUỘC** phải gom vào thư mục con có hậu tố foundation: `docs/**/stage-<XX>-foundation/` (ví dụ: `docs/01-product/stage-01-foundation/`).
   - Thư mục này đã được `.gitignore` tự động bỏ qua, không hiển thị trên Git của công ty.

---

## 4. Bảo vệ Tính Toàn vẹn Repository (Integrity & Hygiene)

1. **Không ghi đè cấu hình Root:**
   - Không được tự ý ghi đè hoặc thay đổi `package.json`, `pnpm-workspace.yaml`, `turbo.json`, `.gitignore`, `.editorconfig` trừ khi có quyết định mở rộng công nghệ được chấp thuận.
2. **Không dùng `"latest"`:**
   - Mọi thư viện mới (nếu có) phải được ghim phiên bản tuyệt đối (exact version).
3. **Bảo tồn Comment & Lịch sử:**
   - Không xóa bớt comment, rationale y tế hay các quyết định kiến trúc cũ.
4. **Không rò rỉ PHI (Protected Health Information):**
   - Mọi dữ liệu kiểm thử trong `testdata/` bắt buộc phải là synthetic 100%. Tuyệt đối không commit hồ sơ bệnh nhân thật.

---

## 5. Verification Checklist trước khi đóng gói Zip

Trước khi xuất file zip, AI agent phải tự thẩm định:
- [ ] Khi giải nén không tạo ra folder bọc ngoài dư thừa.
- [ ] Không có folder rỗng.
- [ ] Mọi đường dẫn tương đối trỏ đúng vào cấu trúc hiện tại của monorepo.
- [ ] Các ghi chú học tập/manifest được đưa vào `stage-<XX>-foundation/`.
- [ ] Chạy `pnpm check` vẫn thành công (0 lỗi).
