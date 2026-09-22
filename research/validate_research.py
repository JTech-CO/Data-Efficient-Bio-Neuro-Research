"""Validate the additive research release without overwriting historical QA.

All reported checks concern saved synthetic artifacts and structural contracts.
They do not certify scientific, biological, clinical, or production validity.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.closed_loop.runner import audit_run, load_run, runtime_fingerprint
from research.closed_loop.contracts import digest


def validate():
 errors=[]
 baseline=json.loads((ROOT/'research/baseline/manifest.json').read_text())
 unchanged=[];archived=[]
 for item in baseline['entries']:
  target=ROOT/(item['archived_original'] or item['path'])
  if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=item['sha256']:
   errors.append('Original not preserved: '+item['path'])
  elif item['archived_original']:archived.append(item['path'])
  else:unchanged.append(item['path'])
 spec=importlib.util.spec_from_file_location('historical_validator',ROOT/'scripts/validate_repository.py')
 legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
 historical=legacy.validate()
 errors.extend(historical['errors'])
 ko={p.name for p in (ROOT/'research/docs/ko').glob('*.md')}
 en={p.name for p in (ROOT/'research/docs/en').glob('*.md')}
 if ko!=en:errors.append('New chapter parity mismatch')
 schema=json.loads((ROOT/'research/schemas/run.schema.json').read_text())
 Draft202012Validator.check_schema(schema);validator=Draft202012Validator(schema)
 pilot=ROOT/'research/results/pilot'
 summary=json.loads((pilot/'summary.json').read_text())
 protocol=json.loads((pilot/'protocol.lock.json').read_text())
 if digest(protocol['matrix'])!=protocol['execution_matrix_sha256']:errors.append('Execution matrix hash mismatch')
 if digest(protocol['protocol'])!=protocol['config_sha256']:errors.append('Protocol hash mismatch')
 if summary['protocol_hash']!=protocol['config_sha256']:errors.append('Summary/config mismatch')
 if len(summary['runs'])!=len(protocol['matrix']) or summary['n_runs']!=len(summary['runs']):errors.append('Run count mismatch')
 ids=[];fingerprints=set();schemas_checked=0;audits_checked=0;json_gz=0;strict_tests=0
 configs=[]
 for row in summary['runs']:
  path=pilot/row['relative_path'];result=load_run(path)
  ids.append(result['run_id']);configs.append(result['config'])
  fingerprints.add(result['execution']['source_sha256'])
  schema_errors=list(validator.iter_errors(result))
  if schema_errors:errors.append('Schema '+result['run_id']+': '+schema_errors[0].message)
  schemas_checked+=1
  report=audit_run(result)
  if report['status']!='pass':errors.append('Audit '+result['run_id']+': '+str(report['errors']))
  audits_checked+=1
  for metric in ['rmse_latent','rmse_observed','observation_95_coverage','observation_95_mean_width']:
   if row[metric]!=result['final'][metric]:errors.append('Summary metric mismatch '+result['run_id']+'/'+metric)
  if row['deterministic_payload_sha256']!=result['deterministic_payload_sha256']:errors.append('Summary payload mismatch')
  if result['final']['cost_to_target'] is not None:errors.append('Unsupported first-passage estimate')
  if result['budget']['n_independent_biological_groups']!=0:errors.append('Biological evidence promotion')
  if path.suffix=='.gz':json_gz+=1
  strict_tests+=sum(e['type']=='final_test_evaluated' for e in result['events'])
 if len(set(ids))!=len(ids):errors.append('Duplicate run IDs')
 if digest(configs)!=protocol['execution_matrix_sha256']:errors.append('Actual execution/config matrix mismatch')
 if fingerprints!={protocol['runtime']['source_sha256']}:errors.append('Mixed runtime source fingerprints')
 # Historical runs may be read on a different OS/library version, but code must match this release.
 if fingerprints!={runtime_fingerprint()['source_sha256']}:errors.append('Saved runs do not match current numerical source')
 if len(summary['groups'])!=42 or len(ids)!=504:errors.append('Release pilot expected 42 cells / 504 runs')
 grouped_total=sum(g['n_seeds'] for g in summary['groups'])
 if grouped_total!=len(ids):errors.append('Group counts mismatch')
 browser_file=ROOT/'research/quality/browser_checks.json'
 browser=json.loads(browser_file.read_text()) if browser_file.is_file() else None
 if browser and browser['status']!='pass':errors.append('Recorded browser checks failed')
 result={'status':'pass' if not errors else 'fail','errors':errors,
   'baseline_original_files':baseline['original_file_count'],'original_paths_byte_identical':len(unchanged),
   'original_versions_archived_exactly':archived,'original_paired_chapters':historical['paired_research_chapters'],
   'new_paired_chapters':len(ko),'local_markdown_links_checked':historical['local_links_checked'],
   'json_syntax_files_checked':historical['json_files_checked'],'run_schemas_checked':schemas_checked,
   'run_semantic_audits_checked':audits_checked,'run_ids_unique':len(set(ids)),
   'gzip_runs_checked':json_gz,'single_final_evaluations_checked':strict_tests,
   'one_frozen_source_fingerprint':len(fingerprints)==1,'source_sha256':next(iter(fingerprints)),
   'browser_recorded_checks':browser['count'] if browser else None,
   'scope':'Original-file preservation, synthetic artifact integrity and contracts; not biological, clinical, causal or production validation.'}
 return result

if __name__=='__main__':
 result=validate();output=ROOT/'research/quality/validation_report.json'
 output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['status']!='pass')
