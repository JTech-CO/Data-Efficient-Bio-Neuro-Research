"""Regenerate the static bundle from complete saved summary and trace files.

This does not compute new experiments or accept arbitrary biological datasets.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
def build():
 source=ROOT/'research/followup/results/v120';target=ROOT/'research/followup/web/bundle.js'
 summary=json.loads((source/'summary.json').read_text(encoding='utf-8'));traces={}
 keys=['world','policy','public_design','threshold','final_model','diagnosis','audit_history','steps','evaluation','costs']
 for p in sorted((source/'traces').glob('*.json')):
  r=json.loads(p.read_text(encoding='utf-8'));traces[p.stem]={k:r[k] for k in keys}
 expected={f'{s}--{p}' for s in summary['config']['scenarios'] for p in summary['config']['policies']}
 if set(traces)!=expected:raise ValueError('Missing or unexpected trace cells')
 text='window.RESEARCH_DATA='+json.dumps({'summary':summary,'traces':traces},ensure_ascii=False,allow_nan=False,separators=(',',':'))+';\n'
 target.write_text(text,encoding='utf-8');print(f'Bundled {len(traces)} saved traces; no new computation.')
if __name__=='__main__':build()
