from __future__ import annotations
import argparse, json, csv, hashlib
from copy import deepcopy
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from source_registry import SourceRegistry, materialize_source
from claim_ledger import ClaimRegistry, build_claim
from bundle import build_bundle, DEFAULT_PROCESSING_PROFILE

def load_validator(repo_root):
    d = repo_root / "contracts/schemas/evidence"
    names = ["retrieval-attempt.schema.json", "evidence-source.schema.json", "evidence-claim.schema.json", "evidence-bundle.schema.json"]
    registry = Registry()
    schemas = {}
    for n in names:
        s = json.loads((d / n).read_text())
        Draft202012Validator.check_schema(s)
        schemas[n] = s
        registry = registry.with_resource(s["$id"], Resource.from_contents(s, default_specification=DRAFT202012))
    return (
        Draft202012Validator(schemas["evidence-bundle.schema.json"], registry=registry),
        Draft202012Validator(schemas["evidence-source.schema.json"], registry=registry),
        Draft202012Validator(schemas["evidence-claim.schema.json"], registry=registry),
    )

def main(repo_root: Path):
    data = json.loads((repo_root / "testdata/synthetic/stage-06/evidence_cases.json").read_text())
    out = repo_root / "experiments/stage-06/results"
    out.mkdir(parents=True, exist_ok=True)
    bv, sv, cv = load_validator(repo_root)

    source_by_ref = {s["logical_ref"]: s for s in data["sources"]}
    registry = SourceRegistry()

    # Register all results from successful attempts (excluding late attempt initially)
    initial_attempts = [a for a in data["attempts"] if a["attempt_id"] != "a4_late"]
    for attempt in initial_attempts:
        if attempt["status"] != "succeeded":
            continue
        for ref in attempt["result_source_refs"]:
            registry.register(source_by_ref[ref])

    sources = registry.all_verified()
    bundle, all_claims = build_bundle(
        data["question"], data["query_intents"], initial_attempts, sources, data["claims"]
    )

    assert not list(bv.iter_errors(bundle))
    assert all(not list(sv.iter_errors(s)) for s in bundle["selected_sources"])
    assert all(not list(cv.iter_errors(c)) for c in bundle["claims"])

    results = []

    def add(name, ok, detail=""):
        results.append({"scenario": name, "pass": bool(ok), "detail": detail})

    # SC-0601: Retry doesn't duplicate source.
    review_id = "doi:10.0000/synth.review.1"
    add("retry_does_not_duplicate_source", sum(1 for s in sources if s["source_id"] == review_id) == 1)

    # SC-0602: Same identity+digest idempotent.
    r = SourceRegistry()
    a = r.register(source_by_ref["src-review"])
    b = r.register(deepcopy(source_by_ref["src-review"]))
    add("same_identity_same_digest_idempotent", a["content_digest"] == b["content_digest"] and len(r.by_identity) == 1)

    # SC-0603: Same identity+version different digest conflicts (Fail Closed).
    mutated = deepcopy(source_by_ref["src-review"])
    mutated["content"] = "Changed synthetic content with same identity and version."
    c = r.register(mutated)
    add("same_identity_different_digest_conflict", c["integrity_state"] == "identity_conflict" and len(r.conflicts) == 1)

    # SC-0604: Explicit new version is distinct.
    r2 = SourceRegistry()
    v1 = r2.register(source_by_ref["src-review"])
    v2data = deepcopy(source_by_ref["src-review"])
    v2data["version"] = "2"
    v2data["content"] = "Synthetic updated version 2."
    v2 = r2.register(v2data)
    add("explicit_source_version_preserved", len(r2.by_identity) == 2 and v1["version"] != "2" and v2["version"] == "2")

    # SC-0605: Partial-only attempt yields incomplete bundle.
    partial_bundle, _ = build_bundle(
        data["question"], data["query_intents"], [data["attempts"][0]], [], data["claims"]
    )
    add("partial_attempt_not_verified", partial_bundle["status"] == "incomplete")

    # SC-0606: Retracted source cannot positive-support.
    claim_c1 = next(c for c in all_claims if c["claim_id"] == "c1")
    retracted_id = "doi:10.0000/synth.old.1"
    retracted_positive = any(x["source_id"] == retracted_id and x["relation"] == "supports" for x in claim_c1["links"])
    add("retracted_source_not_positive_support", not retracted_positive)

    # SC-0607: Supported claim linked & contradiction preserved.
    add("supported_claim_linked", claim_c1["status"] == "conflicted" and any(x["relation"] == "supports" for x in claim_c1["links"]))
    add("contradiction_preserved", any(x["relation"] == "contradicts" for x in claim_c1["links"]))

    # SC-0608: Unrelated citation not entailed.
    unrelated_id = "pmid:SYNTH1003"
    unrelated_links = [x for x in claim_c1["links"] if x["source_id"] == unrelated_id]
    add("unrelated_citation_not_entailed", bool(unrelated_links) and all(x["relation"] == "not_entailed" for x in unrelated_links))

    # SC-0609: Unsupported claim rejected from verified bundle.
    claim_c2 = next(c for c in all_claims if c["claim_id"] == "c2")
    add("unsupported_claim_rejected", claim_c2["status"] == "unsupported" and all(c["claim_id"] != "c2" for c in bundle["claims"]))

    # SC-0610: Input/source order does not change bundle identity (Determinism).
    rev_bundle, _ = build_bundle(
        data["question"], list(reversed(data["query_intents"])), list(reversed(initial_attempts)),
        list(reversed(sources)), list(reversed(data["claims"]))
    )
    add("retrieval_order_bundle_deterministic", bundle["bundle_id"] == rev_bundle["bundle_id"])

    # SC-0611: Policy change yields new bundle.
    p2, _ = build_bundle(data["question"], data["query_intents"], initial_attempts, sources, data["claims"], policy_version="evidence-retrieval-policy-v2")
    add("policy_change_new_bundle", bundle["bundle_id"] != p2["bundle_id"])

    # SC-0612: Timeline change yields new bundle.
    q2 = deepcopy(data["question"])
    q2["timeline_snapshot_id"] = "timeline-synthetic-002"
    t2, _ = build_bundle(q2, data["query_intents"], initial_attempts, sources, data["claims"])
    add("timeline_change_new_bundle", bundle["bundle_id"] != t2["bundle_id"])

    # --- NEW STAGE 06 v0.2 SCENARIOS ---

    # SC-0614: EVID-018 - Late retrieval cannot mutate frozen bundle.
    # Bundle frozen at T=10:10:00Z. Attempt a4_late completed at 10:20:00Z.
    frozen_timestamp = "2026-09-14T10:10:00Z"
    b_frozen, _ = build_bundle(
        data["question"], data["query_intents"], data["attempts"], sources, data["claims"],
        frozen_at=frozen_timestamp
    )
    add("late_retrieval_cannot_mutate_frozen_bundle", "a4_late" not in b_frozen["retrieval_attempt_ids"])

    # SC-0615: Claim identity collision - same key + same proposition is idempotent.
    cr = ClaimRegistry()
    cr.register(data["claims"][0], sources)
    c_repeat = cr.register(deepcopy(data["claims"][0]), sources)
    add("claim_identity_same_payload_idempotent", c_repeat["status"] in {"supported", "conflicted"} and len(cr.conflicts) == 0)

    # SC-0616: Claim identity collision - same key + different proposition fails closed.
    c_mutated = deepcopy(data["claims"][0])
    c_mutated["claim_text"] = "Mutated proposition text attempting silent replacement."
    c_conflict = cr.register(c_mutated, sources)
    add("claim_identity_different_payload_conflict", c_conflict["status"] == "claim_identity_conflict" and len(cr.conflicts) == 1)

    # SC-0617: EVID-017 - Closed dependency scope: processing profile change yields new bundle identity.
    prof_modified = deepcopy(DEFAULT_PROCESSING_PROFILE)
    prof_modified["entailment_policy"]["digest"] = hashlib.sha256(b"updated-entailment-policy-v2").hexdigest()
    b_prof2, _ = build_bundle(
        data["question"], data["query_intents"], initial_attempts, sources, data["claims"],
        processing_profile=prof_modified
    )
    add("processing_profile_change_yields_new_bundle", bundle["bundle_id"] != b_prof2["bundle_id"])

    # SC-0618: Raw source artifact hash is independent from metadata representation.
    raw_src = source_by_ref["src-review"]
    m1 = materialize_source(raw_src)
    raw_src_variant = deepcopy(raw_src)
    raw_src_variant["title"] = "Different metadata title"
    m2 = materialize_source(raw_src_variant)
    add(
        "raw_artifact_digest_independent_from_envelope",
        m1["raw_content_sha256"] == m2["raw_content_sha256"] and m1["content_digest"] == m2["content_digest"]
    )

    metrics = {
        "scenario_pass_rate": sum(r["pass"] for r in results) / len(results),
        "false_source_merge_rate": 0.0 if next(r for r in results if r["scenario"] == "same_identity_different_digest_conflict")["pass"] else 1.0,
        "unsupported_claim_acceptance_rate": 0.0 if next(r for r in results if r["scenario"] == "unsupported_claim_rejected")["pass"] else 1.0,
        "retracted_positive_support_rate": 0.0 if next(r for r in results if r["scenario"] == "retracted_source_not_positive_support")["pass"] else 1.0,
        "bundle_determinism": next(r for r in results if r["scenario"] == "retrieval_order_bundle_deterministic")["pass"],
        "source_collision_fail_closed": next(r for r in results if r["scenario"] == "same_identity_different_digest_conflict")["pass"],
        "claim_collision_fail_closed": next(r for r in results if r["scenario"] == "claim_identity_different_payload_conflict")["pass"],
        "conflict_preserved": next(r for r in results if r["scenario"] == "contradiction_preserved")["pass"],
        "late_retrieval_isolated": next(r for r in results if r["scenario"] == "late_retrieval_cannot_mutate_frozen_bundle")["pass"],
        "bundle_closure_enforced": next(r for r in results if r["scenario"] == "processing_profile_change_yields_new_bundle")["pass"],
    }

    (out / "evidence_bundle.json").write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    (out / "all_claim_candidates.json").write_text(json.dumps(all_claims, indent=2), encoding="utf-8")
    (out / "benchmark.json").write_text(json.dumps({"metrics": metrics, "scenarios": results}, indent=2), encoding="utf-8")
    with (out / "benchmark.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "pass", "detail"])
        for r in results:
            w.writerow([r["scenario"], r["pass"], r["detail"]])
    report = ["# Stage 06 Experiment Run Report (v0.2 Hardened)", "", "## Metrics", ""]
    report += [f"- `{k}`: `{v}`" for k,v in metrics.items()]
    report += ["", "## Scenarios", ""]
    report += [f"- `{r['scenario']}`: **{'PASS' if r['pass'] else 'FAIL'}**" for r in results]
    (out / "RUN_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    if metrics["scenario_pass_rate"] != 1.0:
        raise SystemExit(1)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    args = p.parse_args()
    main(args.repo_root.resolve())
