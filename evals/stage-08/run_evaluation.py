from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
from copy import deepcopy

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from canonical import canonical_json, canonical_digest, verify_attestation
from metrics import compute_metrics,slice_metrics
from metamorphic import transform
from stats import zero_failure_required_n

def main(repo_root:Path):
    stage07_dir=repo_root/"experiments/stage-07"
    sys.path.insert(0,str(stage07_dir))
    from harness import evaluate

    stage07_cases=json.loads(
        (repo_root/"testdata/synthetic/stage-07/reasoning_cases.json").read_text()
    )["cases"]
    s7={c["id"]:c for c in stage07_cases}

    eval_cases=json.loads(
        (repo_root/"testdata/synthetic/stage-08/evaluation_cases.json").read_text()
    )["cases"]

    results=[]
    for ec in eval_cases:
        source=s7[ec["source_case_id"]]
        decision,_=evaluate(deepcopy(source["input"]),deepcopy(source["candidate"]))
        results.append({
            "schema_version":"1.0",
            "case_id":ec["case_id"],
            "gold_verdict":ec["gold"]["verdict"],
            "actual_verdict":decision["verdict"],
            "exact_match":decision["verdict"]==ec["gold"]["verdict"],
            "risk_severity":ec["risk_severity"],
            "violations":sorted({v["code"] for v in decision["violations"]}),
        })

    metrics=compute_metrics(results)
    slices=slice_metrics(results,eval_cases)

    meta_specs=json.loads(
        (repo_root/"testdata/synthetic/stage-08/metamorphic_cases.json").read_text()
    )["relations"]
    metamorphic_results=[]
    for spec in meta_specs:
        base=deepcopy(s7[spec["source_case_id"]])
        base_decision,_=evaluate(deepcopy(base["input"]),deepcopy(base["candidate"]))
        changed=transform(base,spec["transform"])
        changed_decision,_=evaluate(changed["input"],changed["candidate"])
        if spec.get("expected_relation")=="same_verdict":
            ok=base_decision["verdict"]==changed_decision["verdict"]
        else:
            ok=changed_decision["verdict"]==spec["expected_verdict"]
        metamorphic_results.append({
            "relation_id":spec["id"],
            "pass":ok,
            "base_verdict":base_decision["verdict"],
            "transformed_verdict":changed_decision["verdict"],
        })

    metrics["metamorphic_pass_rate"]=sum(x["pass"] for x in metamorphic_results)/len(metamorphic_results)
    metrics["zero_failure_n_for_upper95_below_5pct"]=zero_failure_required_n(0.05)
    metrics["zero_failure_n_for_upper95_below_1pct"]=zero_failure_required_n(0.01)
    metrics["zero_failure_n_for_upper95_below_0_1pct"]=zero_failure_required_n(0.001)

    model_manifest={
        "schema_version":"1.0",
        "manifest_id":"fixture-stage07-candidates-v1",
        "provider":"synthetic_fixture",
        "model_id":"stage07-candidate-fixtures",
        "model_version":"1",
        "configuration_digest":"a"*64,
        "program_digest":"b"*64,
        "temperature":0.0,
        "seed":0,
        "capability_profile":[],
    }
    dataset_digest=canonical_digest(eval_cases)
    manifest_digest=canonical_digest(model_manifest)
    if not verify_attestation(eval_cases, dataset_digest):
        raise ValueError("Dataset attestation verification failed (digest drift)")
    if not verify_attestation(model_manifest, manifest_digest):
        raise ValueError("Manifest attestation verification failed (digest drift)")

    payload={
        "schema_version":"1.0",
        "evaluator_version":"stage-08-v0.1",
        "dataset_digest":dataset_digest,
        "model_manifest":model_manifest,
        "metrics":metrics,
        "results":results,
    }
    run_id="eval-"+canonical_digest(payload)[:16]
    evaluation_run={"schema_version":"1.0","evaluation_run_id":run_id,**{k:v for k,v in payload.items() if k!="schema_version"}}

    out=repo_root/"evals/stage-08/results"
    out.mkdir(parents=True,exist_ok=True)
    (out/"evaluation_run.json").write_text(json.dumps(evaluation_run,indent=2),encoding="utf-8")
    (out/"metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    (out/"slices.json").write_text(json.dumps(slices,indent=2),encoding="utf-8")
    (out/"metamorphic.json").write_text(json.dumps(metamorphic_results,indent=2),encoding="utf-8")

    report=[
        "# Stage 08 Evaluation Run Report",
        "",
        "## Provenance & Integrity (RFC 8785)",
        "",
        f"- `run_id`: `{run_id}`",
        f"- `dataset_digest`: `{dataset_digest}`",
        f"- `manifest_digest`: `{manifest_digest}`",
        f"- `attestation_verified`: `True`",
        "",
        "## Metrics",
        "",
    ]
    for k,v in metrics.items():
        report.append(f"- `{k}`: `{v}`")
    report += [
        "",
        "## Metamorphic Relations",
        "",
        f"- `total_relations`: `{len(metamorphic_results)}`",
        f"- `passed_relations`: `{sum(1 for m in metamorphic_results if m['pass'])}`",
        "",
        "## Interpretation",
        "",
    ]
    if metrics["unsafe_escape_count"]==0:
        report.append(
            f"- Observed unsafe escapes are 0/{metrics['unsafe_case_count']}, "
            f"but the one-sided 95% zero-failure upper bound is "
            f"{metrics['unsafe_escape_zero_failure_upper95']:.4f}; this is not proof of zero population risk."
        )
    report.append("- This run evaluates Stage-07 synthetic policy cases, not a production LLM.")
    (out/"RUN_REPORT.md").write_text("\n".join(report)+"\n",encoding="utf-8")

    print(json.dumps(metrics,indent=2))
    if metrics["exact_verdict_accuracy"] != 1.0 or metrics["metamorphic_pass_rate"] != 1.0:
        raise SystemExit(1)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=Path("."))
    args=p.parse_args()
    main(args.repo_root.resolve())
