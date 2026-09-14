# AI Zip & Code Generation Rules

> **Purpose:** Guidelines for AI agents generating code, project archives (zips), PR bundles, or automated changes.

---

## 1. Core Directives

1. **No Hallucinated Directory Structures**:
   - Only create files within the active Stage boundaries.
   - Do not generate entire future directory trees (`apps/worker`, `infra/k8s`, `internal/platform/*`) preemptively.

2. **Clean File Outputs**:
   - Ensure line endings are normalized (`LF`).
   - Do not emit trailing whitespace or extraneous blank lines.
   - Every file must have a clear purpose and adhere to [BIOMARKER_PROJECT_SKELETON_V0.1.md](../../BIOMARKER_PROJECT_SKELETON_V0.1.md).

3. **No Phantom Dependencies**:
   - Dependencies added to `package.json` or `go.mod` must be pinned to exact versions.
   - Do not use `"latest"`.
   - Never add dependencies that are not directly used by active code.

4. **Preserve Existing Integrity**:
   - Never overwrite existing canonical schemas without an explicit migration and ADR.
   - Do not delete comments, rationale, or docstrings unless explicitly asked.

---

## 2. Archive & Export Cleanliness

When generating exports, zips, or distribution bundles:
- Exclude all build artifacts (`node_modules`, `.turbo`, `dist`, `.out`).
- Exclude local secrets, `.env` files, and local logs.
- Exclude `var/` runtime data.
- Ensure the bundle can be extracted and built deterministically with `pnpm install && pnpm check`.
