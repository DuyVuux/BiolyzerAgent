from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from snapshot import build_snapshot

def scenario_pass(case, snap=None, error=None):
    e = case["expect"]
    cid = case["id"]

    if "error" in e:
        return error == e["error"], {"error":error}

    if error:
        return False, {"error":error}

    series = snap["series"]
    groups = snap["lineage_groups"]
    excluded = snap["excluded_observations"]
    detail = {}

    if "series" in e:
        detail["series"] = len(series)
        if len(series) != e["series"]: return False, detail

    total_points = sum(len(s["points"]) for s in series)
    if "points" in e:
        detail["points"] = total_points
        if total_points != e["points"]: return False, detail

    if "lineage_resolution" in e:
        resolutions = [g["resolution"] for g in groups]
        detail["resolutions"] = resolutions
        if e["lineage_resolution"] not in resolutions: return False, detail

    if "selected" in e:
        selected = [g.get("selected_observation_id") for g in groups]
        detail["selected"] = selected
        if e["selected"] not in selected: return False, detail

    if "excluded_reason" in e:
        reasons = [x["reason"] for x in excluded]
        detail["excluded"] = reasons
        if e["excluded_reason"] not in reasons: return False, detail

    if "point_order" in e:
        ids = [p["selected_observation_id"] for p in series[0]["points"]]
        detail["point_order"] = ids
        if ids != e["point_order"]: return False, detail

    if series:
        trend = series[0]["trend"]
        if "trend_status" in e:
            detail["trend_status"] = trend["status"]
            if trend["status"] != e["trend_status"]: return False, detail
        if "direction" in e:
            detail["direction"] = trend.get("direction")
            if trend.get("direction") != e["direction"]: return False, detail
        if "delta" in e:
            detail["delta"] = trend.get("absolute_delta")
            if abs(trend.get("absolute_delta",999)-e["delta"]) > 1e-9: return False, detail
        if "rank_delta" in e:
            detail["rank_delta"] = trend.get("rank_delta")
            if trend.get("rank_delta") != e["rank_delta"]: return False, detail
        if "normalized_unit" in e:
            detail["normalized_unit"] = series[0].get("normalized_unit")
            if series[0].get("normalized_unit") != e["normalized_unit"]: return False, detail

    return True, detail

def main(repo_root: Path):
    case_file = repo_root / "testdata/synthetic/stage-05/longitudinal_cases.json"
    schema_file = repo_root / "contracts/schemas/clinical/longitudinal-timeline.schema.json"
    result_dir = repo_root / "experiments/stage-05/results"
    snap_dir = result_dir / "snapshots"
    result_dir.mkdir(parents=True, exist_ok=True)
    snap_dir.mkdir(parents=True, exist_ok=True)

    cases = json.loads(case_file.read_text())["cases"]
    schema = json.loads(schema_file.read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    rows = []
    passed = 0
    false_merges = 0
    deterministic = True

    for case in cases:
        snap = None
        error = None
        try:
            snap = build_snapshot(case["observations"])
            errs = list(validator.iter_errors(snap))
            if errs:
                raise AssertionError("SCHEMA_INVALID:"+errs[0].message)
            # Snapshot must not depend on input order.
            snap2 = build_snapshot(list(reversed(case["observations"])))
            deterministic = deterministic and (
                snap["content_sha256"] == snap2["content_sha256"]
                and snap["timeline_snapshot_id"] == snap2["timeline_snapshot_id"]
            )
            (snap_dir / f"{case['id']}.json").write_text(json.dumps(snap,indent=2),encoding="utf-8")
        except ValueError as ex:
            error = str(ex)

        ok, detail = scenario_pass(case, snap, error)
        passed += int(ok)
        if case["id"] == "same_value_time_distinct_events" and snap:
            if sum(len(s["points"]) for s in snap["series"]) != 2:
                false_merges += 1
        rows.append({
            "case":case["id"],
            "pass":ok,
            "error":error,
            "detail":detail,
        })

    metrics = {
        "scenario_pass_rate": passed / len(cases),
        "false_merge_rate": false_merges / 1,
        "snapshot_determinism": deterministic,
        "cross_subject_rejection": any(r["case"]=="cross_subject_rejected" and r["pass"] for r in rows),
        "duplicate_resolution": any(r["case"]=="duplicate_import" and r["pass"] for r in rows),
        "revision_selection": any(r["case"]=="corrected_revision" and r["pass"] for r in rows),
        "chronology_ordering": any(r["case"]=="chronology_out_of_order" and r["pass"] for r in rows),
        "comparability_split": any(r["case"]=="different_methods_split" and r["pass"] for r in rows),
        "candidate_mapping_exclusion": any(r["case"]=="candidate_mapping_excluded" and r["pass"] for r in rows),
        "identity_collision_idempotent_duplicate": any(r["case"]=="identity_collision_idempotent_duplicate" and r["pass"] for r in rows),
        "identity_collision_hard_conflict": any(r["case"]=="identity_collision_hard_conflict" and r["pass"] for r in rows),
        "reconciliation_required_exclusion": any(r["case"]=="ambiguous_representation_reconciliation_required" and r["pass"] for r in rows),
        "trend_boundary_cases": all(
            next(r for r in rows if r["case"]==name)["pass"]
            for name in ["ordinal_trend","categorical_change","interval_history_only","censored_quantity"]
        ),
    }
    (result_dir / "benchmark.json").write_text(json.dumps({"metrics":metrics,"cases":rows},indent=2),encoding="utf-8")
    with (result_dir / "benchmark.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["case","pass","error"])
        for r in rows: w.writerow([r["case"],r["pass"],r["error"] or ""])
    report = ["# Stage 05 Experiment Run Report","","## Metrics",""]
    for k,v in metrics.items(): report.append(f"- `{k}`: `{v}`")
    report += ["","## Cases",""]
    for r in rows: report.append(f"- `{r['case']}`: **{'PASS' if r['pass'] else 'FAIL'}**")
    (result_dir / "RUN_REPORT.md").write_text("\n".join(report)+"\n",encoding="utf-8")

    print(json.dumps(metrics, indent=2))
    if passed != len(cases):
        raise SystemExit(1)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=Path("."))
    args=p.parse_args()
    main(args.repo_root.resolve())
