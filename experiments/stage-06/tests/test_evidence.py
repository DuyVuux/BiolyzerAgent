import json, sys, unittest, hashlib
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from source_registry import SourceRegistry, materialize_source
from claim_ledger import ClaimRegistry, build_claim
from bundle import build_bundle, DEFAULT_PROCESSING_PROFILE

ROOT = HERE.parents[1]
DATA = json.loads((ROOT / "testdata/synthetic/stage-06/evidence_cases.json").read_text())
BY = {s["logical_ref"]: s for s in DATA["sources"]}

class EvidenceTests(unittest.TestCase):
    def test_same_identity_same_digest_idempotent(self):
        r = SourceRegistry()
        r.register(BY["src-review"])
        r.register(deepcopy(BY["src-review"]))
        self.assertEqual(len(r.by_identity), 1)

    def test_same_identity_changed_content_conflicts(self):
        r = SourceRegistry()
        r.register(BY["src-review"])
        x = deepcopy(BY["src-review"])
        x["content"] = "different"
        out = r.register(x)
        self.assertEqual(out["integrity_state"], "identity_conflict")

    def test_explicit_version_is_distinct(self):
        r = SourceRegistry()
        r.register(BY["src-review"])
        x = deepcopy(BY["src-review"])
        x["version"] = "2"
        x["content"] = "updated"
        r.register(x)
        self.assertEqual(len(r.by_identity), 2)

    def test_retracted_source_cannot_support(self):
        src = materialize_source(BY["src-retracted"])
        claim = build_claim(DATA["claims"][0], [src])
        self.assertFalse(any(l["relation"] == "supports" for l in claim["links"]))

    def test_unrelated_source_not_entailed(self):
        src = materialize_source(BY["src-unrelated"])
        claim = build_claim(DATA["claims"][0], [src])
        self.assertTrue(all(l["relation"] == "not_entailed" for l in claim["links"]))

    def test_support_and_contradiction_conflicted(self):
        srcs = [materialize_source(BY["src-review"]), materialize_source(BY["src-observe"])]
        claim = build_claim(DATA["claims"][0], srcs)
        self.assertEqual(claim["status"], "conflicted")

    def test_unsupported_claim_not_selected(self):
        srcs = [materialize_source(BY["src-review"])]
        bundle, all_claims = build_bundle(DATA["question"], DATA["query_intents"], DATA["attempts"], srcs, DATA["claims"])
        self.assertTrue(all(c["claim_id"] != "c2" for c in bundle["claims"]))

    def test_bundle_deterministic_under_input_order(self):
        srcs = [materialize_source(BY["src-review"]), materialize_source(BY["src-observe"])]
        a, _ = build_bundle(DATA["question"], DATA["query_intents"], DATA["attempts"], srcs, DATA["claims"])
        b, _ = build_bundle(DATA["question"], list(reversed(DATA["query_intents"])), list(reversed(DATA["attempts"])), list(reversed(srcs)), list(reversed(DATA["claims"])))
        self.assertEqual(a["bundle_id"], b["bundle_id"])

    def test_policy_version_changes_bundle(self):
        srcs = [materialize_source(BY["src-review"])]
        a, _ = build_bundle(DATA["question"], DATA["query_intents"], DATA["attempts"], srcs, DATA["claims"], "p1")
        b, _ = build_bundle(DATA["question"], DATA["query_intents"], DATA["attempts"], srcs, DATA["claims"], "p2")
        self.assertNotEqual(a["bundle_id"], b["bundle_id"])

    # --- NEW STAGE 06 v0.2 TESTS ---

    def test_late_retrieval_cannot_mutate_frozen_bundle(self):
        """EVID-018: Attempts completing after frozen_at cannot enter the frozen bundle."""
        srcs = [materialize_source(BY["src-review"]), materialize_source(BY["src-observe"])]
        frozen_time = "2026-09-14T10:10:00Z"
        b_frozen, _ = build_bundle(
            DATA["question"], DATA["query_intents"], DATA["attempts"], srcs, DATA["claims"],
            frozen_at=frozen_time
        )
        self.assertNotIn("a4_late", b_frozen["retrieval_attempt_ids"])

        # When refreshed with late attempt allowed, a new distinct bundle is created
        b_refreshed, _ = build_bundle(
            DATA["question"], DATA["query_intents"], DATA["attempts"], srcs, DATA["claims"],
            frozen_at="2026-09-14T10:30:00Z"
        )
        self.assertIn("a4_late", b_refreshed["retrieval_attempt_ids"])
        self.assertNotEqual(b_frozen["bundle_id"], b_refreshed["bundle_id"])

    def test_claim_identity_same_payload_idempotent(self):
        """Re-extracting the exact same claim proposition is idempotent."""
        cr = ClaimRegistry()
        srcs = [materialize_source(BY["src-review"])]
        c1 = cr.register(DATA["claims"][0], srcs)
        c2 = cr.register(deepcopy(DATA["claims"][0]), srcs)
        self.assertEqual(len(cr.by_identity), 1)
        self.assertEqual(len(cr.conflicts), 0)
        self.assertEqual(c1["claim_id"], c2["claim_id"])

    def test_claim_identity_different_payload_conflicts(self):
        """Re-extracting a different proposition payload under the same claim_id fails closed."""
        cr = ClaimRegistry()
        srcs = [materialize_source(BY["src-review"])]
        cr.register(DATA["claims"][0], srcs)

        mutated = deepcopy(DATA["claims"][0])
        mutated["claim_text"] = "Mutated claim text representing conflicting extraction."
        conflict = cr.register(mutated, srcs)
        self.assertEqual(conflict["status"], "claim_identity_conflict")
        self.assertEqual(len(cr.conflicts), 1)

    def test_processing_profile_change_yields_new_bundle(self):
        """EVID-017: Changing any policy descriptor digest in the processing profile changes bundle identity."""
        srcs = [materialize_source(BY["src-review"])]
        b1, _ = build_bundle(DATA["question"], DATA["query_intents"], DATA["attempts"], srcs, DATA["claims"])

        prof2 = deepcopy(DEFAULT_PROCESSING_PROFILE)
        prof2["entailment_policy"]["digest"] = hashlib.sha256(b"changed-entailment-digest-v2").hexdigest()
        b2, _ = build_bundle(
            DATA["question"], DATA["query_intents"], DATA["attempts"], srcs, DATA["claims"],
            processing_profile=prof2
        )
        self.assertNotEqual(b1["bundle_id"], b2["bundle_id"])
        self.assertNotEqual(b1["experimental_content_sha256"], b2["experimental_content_sha256"])

    def test_raw_artifact_digest_independent_from_envelope(self):
        """Raw source bytes digest is distinct and independent from canonical structured metadata."""
        src = BY["src-review"]
        m1 = materialize_source(src)
        self.assertIn("raw_content_sha256", m1)
        self.assertIn("content_digest", m1)
        # Content digest is derived from body text, raw_content_sha256 is derived from raw_bytes
        self.assertNotEqual(m1["raw_content_sha256"], m1["content_digest"])

if __name__ == "__main__":
    unittest.main()
