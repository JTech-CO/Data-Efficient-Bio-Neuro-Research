#!/usr/bin/env python3
"""Validate the additive research package without overwriting baseline QA artifacts.

Checks artifact preservation, all pilot records, recomputed summaries, schemas,
lineage/cost/split contracts, static-data identity and bilingual/local links.
Does not establish biological validity or remote deployment readiness.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from jsonschema import Draft202012Validator, FormatChecker
from research_lab.ledger import EvidenceLedger
from research_lab.contracts import Query
from research_lab.runner import summarize


def validate() -> dict:
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    def read(path):
        return json.loads((ROOT/path).read_text(encoding='utf-8'))
    def finite(value):
        if isinstance(value, float): return math.isfinite(value)
        if isinstance(value, dict): return all(finite(v) for v in value.values())
        if isinstance(value, list): return all(finite(v) for v in value)
        return True
    def equivalent(a, b):
        if isinstance(a, float) and isinstance(b, (float, int)):
            return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12)
        if isinstance(a, dict) and isinstance(b, dict):
            return a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
        if isinstance(a, list) and isinstance(b, list):
            return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
        return a==b
    baseline = read('research_lab/provenance/baseline_manifest.json')
    changed=[]
    for path, expected in baseline['sha256'].items():
        p=ROOT/path
        check(p.exists(),f'Baseline file missing: {path}')
        if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
            changed.append(path)
            check(path in baseline['allowed_modified'],f'Unexpected baseline change: {path}')
    for name in ['README.md','README.en.md']:
        before=(ROOT/'research_lab/provenance'/('baseline_'+name+'.txt')).read_bytes()
        check((ROOT/name).read_bytes().startswith(before),f'Non-additive README change: {name}')
    plan=read('research_lab/configs/pilot.json')
    summary=read('research_lab/results/pilot/summary.json')
    records=[json.loads(line) for line in (ROOT/'research_lab/results/pilot/runs.jsonl').read_text().splitlines()]
    demos=read('research_lab/results/pilot/demos.json')
    check(len(records)==640,'Expected 640 complete pilot records')
    check(len(demos)==25,'Expected 25 full seed-0 traces')
    groups=Counter((r['track'],r['scenario'],r['policy'],r['observer']) for r in records)
    check(len(groups)==32 and set(groups.values())=={20},'Pilot grid is not 32 cells by 20 seeds')
    check(Counter(r['track'] for r in records)=={'main':500,'ablation':140},'Main/ablation count mismatch')
    keys={(r['track'],r['scenario'],r['policy'],r['observer'],r['seed']) for r in records}
    check(len(keys)==len(records),'Duplicate run configurations')
    check(summary['plan_sha256']==hashlib.sha256((ROOT/'research_lab/configs/pilot.json').read_bytes()).hexdigest(),'Plan hash mismatch')
    expected_summary, expected_pairs=summarize(records)
    check(equivalent(expected_summary,summary['summary']),'Stored aggregate summary differs from raw records')
    check(equivalent(expected_pairs,summary['paired_comparisons']),'Stored paired bootstrap differs from raw records')
    for r in records:
        check(finite(r),'Non-finite pilot value')
        check(r['cost']<=r['budget']+1e-8,'Cost budget violated')
        check(r['information_budget']['biological_units']==0,'Biological unit incorrectly counted')
        check(all(c['cost']<=r['cost']+1e-8 for c in r['curves']),'Curve cost exceeds final cost')
        for domain in ('id','ood'):
            for coverage in ('observation_95_coverage','latent_95_coverage'):
                check(0<=r['final'][domain][coverage]<=1,'Coverage outside [0,1]')
    schema=Draft202012Validator(read('schemas/observation.schema.json'),format_checker=FormatChecker())
    n_observations=0
    for demo in demos:
        check(demo['evaluation']['access']=='post_run_only_not_visible_to_policy','Incorrect evaluation role')
        check(EvidenceLedger.verify(demo['evidence']),'Evidence hash chain failed')
        check(abs(sum(e['cost'] for e in demo['evidence'])-demo['total_cost'])<1e-8,'Ledger cost mismatch')
        check(len(demo['history'])==len(demo['evidence']),'History/evidence length mismatch')
        fitting=0; previous_cost=0.; training_keys=set()
        for h,e in zip(demo['history'],demo['evidence']):
            n_observations+=1
            check(schema.is_valid(e['observation']),'Observation incompatible with original schema')
            check(e['observation']['kind']=='simulated','Non-synthetic evidence in pilot')
            check(not e['observation']['counts_as_new_biological_unit'],'Synthetic evidence counted as biology')
            check(h['observation_id']==e['observation']['record_id'],'Observation ID mismatch')
            check(not h['approval']['real_world_authorized'],'Real-world authorization invented')
            check(h['cumulative_cost']>previous_cost,'Nonincreasing acquired cost')
            previous_cost=h['cumulative_cost']
            if h['phase']=='train':
                fitting+=1; key=Query(**e['query']).key
                check(key not in training_keys,'Duplicate training query');training_keys.add(key)
                check(e['role']=='train' and e['observation']['split']=='train','Training role mismatch')
            else:
                check(e['role']=='audit' and e['observation']['split']=='validation','Audit split mismatch')
            check(h['fit_n']==fitting,'Audit evidence entered fitting count')
            check(abs(sum(h['posterior']['weights'].values())-1)<1e-8,'Candidate weights not normalized')
        match=[r for r in records if r['track']=='main' and r['scenario']==demo['config']['scenario']
               and r['policy']==demo['config']['policy'] and r['seed']==demo['config']['seed']]
        check(len(match)==1 and match[0]['acquisition_sha256']==demo['acquisition_sha256'],'Demo/pilot acquisition mismatch')
    script=(ROOT/'research_lab/web/assets/demo-data.js').read_text(encoding='utf-8')
    embedded=json.loads(script.split('=',1)[1].strip().removesuffix(';'))
    check(embedded['demos']==demos and embedded['benchmark']==summary,'Browser data differ from pilot outputs')
    # Import, do not run __main__: original quality/validation_report.json is preserved.
    spec=importlib.util.spec_from_file_location('baseline_validator',ROOT/'scripts/validate_repository.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    internal=module.validate()
    errors.extend(internal['errors'])
    browser=read('research_lab/results/quality/browser_validation.json')
    check(browser['status']=='pass' and not browser['page_errors'],'Stored browser smoke failed')
    return {
        'status':'pass' if not errors else 'fail','errors':errors,
        'baseline_files':len(baseline['sha256']),'baseline_unchanged':len(baseline['sha256'])-len(changed),
        'allowed_baseline_changes':changed,'research_chapters_01_to_08_byte_preserved':not any(p.startswith('docs/') for p in changed),
        'pilot_runs':len(records),'pilot_cells':len(groups),'detailed_traces':len(demos),
        'detailed_observations_validated':n_observations,'summary_recomputed':True,
        'browser_data_match':embedded['demos']==demos and embedded['benchmark']==summary,
        'internal_repository_checks':internal,
        'scope':'Local structural and synthetic checks only; not biological validation, statistical superiority, URL navigation, or remote CI execution.'}

if __name__=='__main__':
    report=validate()
    target=ROOT/'research_lab/results/quality/package_validation.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0 if report['status']=='pass' else 1)
