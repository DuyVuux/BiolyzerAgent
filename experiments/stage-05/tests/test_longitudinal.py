import json, sys, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from snapshot import build_snapshot

ROOT=HERE.parents[1]
CASES=json.loads((ROOT/"testdata/synthetic/stage-05/longitudinal_cases.json").read_text())["cases"]
BY={c["id"]:c for c in CASES}

class LongitudinalTests(unittest.TestCase):
    def test_out_of_order_uses_clinical_time(self):
        s=build_snapshot(BY["chronology_out_of_order"]["observations"])
        self.assertEqual([p["selected_observation_id"] for p in s["series"][0]["points"]],["c-jan","c-feb","c-mar"])

    def test_duplicate_collapses(self):
        s=build_snapshot(BY["duplicate_import"]["observations"])
        self.assertEqual(sum(len(x["points"]) for x in s["series"]),1)
        self.assertIn("duplicate_collapsed",[g["resolution"] for g in s["lineage_groups"]])

    def test_revision_selects_latest_representation(self):
        s=build_snapshot(BY["corrected_revision"]["observations"])
        self.assertIn("r-new",[g.get("selected_observation_id") for g in s["lineage_groups"]])

    def test_same_value_time_is_not_duplicate(self):
        s=build_snapshot(BY["same_value_time_distinct_events"]["observations"])
        self.assertEqual(sum(len(x["points"]) for x in s["series"]),2)
        self.assertEqual(s["series"][0]["trend"]["status"],"indeterminate_same_time")

    def test_convertible_units_share_series(self):
        s=build_snapshot(BY["convertible_units"]["observations"])
        self.assertEqual(len(s["series"]),1)
        self.assertAlmostEqual(s["series"][0]["trend"]["absolute_delta"],10)

    def test_method_codes_split_series(self):
        s=build_snapshot(BY["different_methods_split"]["observations"])
        self.assertEqual(len(s["series"]),2)

    def test_candidate_mapping_excluded(self):
        s=build_snapshot(BY["candidate_mapping_excluded"]["observations"])
        self.assertEqual(len(s["series"]),0)
        self.assertEqual(s["excluded_observations"][0]["reason"],"mapping_not_validated")

    def test_cross_subject_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"CROSS_SUBJECT_INPUT"):
            build_snapshot(BY["cross_subject_rejected"]["observations"])

    def test_interval_no_midpoint_trend(self):
        s=build_snapshot(BY["interval_history_only"]["observations"])
        self.assertEqual(s["series"][0]["trend"]["status"],"history_only_interval")

    def test_censored_quantity_no_naive_delta(self):
        s=build_snapshot(BY["censored_quantity"]["observations"])
        self.assertEqual(s["series"][0]["trend"]["status"],"not_computed_censored_value")

    def test_snapshot_is_deterministic(self):
        obs=BY["chronology_out_of_order"]["observations"]
        a=build_snapshot(obs)
        b=build_snapshot(list(reversed(obs)))
        self.assertEqual(a["content_sha256"],b["content_sha256"])
        self.assertEqual(a["timeline_snapshot_id"],b["timeline_snapshot_id"])

    def test_identity_collision_idempotent_duplicate(self):
        s=build_snapshot(BY["identity_collision_idempotent_duplicate"]["observations"])
        self.assertEqual(sum(len(x["points"]) for x in s["series"]),1)
        self.assertIn("duplicate_collapsed",[g["resolution"] for g in s["lineage_groups"]])

    def test_identity_collision_hard_conflict(self):
        s=build_snapshot(BY["identity_collision_hard_conflict"]["observations"])
        self.assertEqual(len(s["series"]),0)
        self.assertIn("unresolved_conflict",[g["resolution"] for g in s["lineage_groups"]])
        self.assertIn("unresolved_lineage_conflict",[x["reason"] for x in s["excluded_observations"]])

    def test_ambiguous_representation_reconciliation_required(self):
        s=build_snapshot(BY["ambiguous_representation_reconciliation_required"]["observations"])
        self.assertEqual(len(s["series"]),0)
        self.assertIn("reconciliation_required",[g["resolution"] for g in s["lineage_groups"]])
        self.assertIn("reconciliation_required",[x["reason"] for x in s["excluded_observations"]])

if __name__=="__main__":
    unittest.main()
