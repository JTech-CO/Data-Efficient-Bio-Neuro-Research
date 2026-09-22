"""DOM/render checks with actual shipped assets; no HTTP navigation claim.

This environment's managed Chromium blocks file:// and localhost navigation.
The checks inject our own HTML/CSS/JS into an isolated page. Local HTTP/API
integration is separately exercised by test_closed_loop.ServerTests.
Optional dependency: playwright. Launch using PLAYWRIGHT_CHROMIUM or /usr/bin/chromium.
"""
from pathlib import Path
import json
import os
import re
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2]
QUALITY = ROOT / 'research/quality'

def main():
 checks=[]; errors=[]
 def check(name, condition):
  checks.append({'check':name,'passed':bool(condition)})
  if not condition: raise AssertionError(name)
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=os.getenv('PLAYWRIGHT_CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
  page.on('pageerror',lambda error:errors.append(str(error)))
  html=(ROOT/'index.html').read_text()
  html=re.sub(r'<link[^>]+stylesheet[^>]*>', '', html)
  html=re.sub(r'<script src=[^>]+></script>', '', html)
  page.set_content(html)
  page.add_style_tag(content=(ROOT/'lab/css/lab.css').read_text())
  for asset in ['lab/data/pilot-data.js','lab/js/i18n.js','lab/js/lab.js']:
   page.add_script_tag(content=(ROOT/asset).read_text())
  page.wait_for_function("document.querySelector('#run-title').textContent !== '-'")
  check('native-gzip-bundle-42-runs',page.evaluate('(async()=> (await window.CLOSED_LOOP_READY).runs.length)()')==42)
  check('static-mode-disables-new-calculation',page.locator('#run-new').is_disabled())
  check('desktop-no-horizontal-page-overflow',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
  check('initial-Korean',page.locator('html').get_attribute('lang')=='ko')
  page.screenshot(path=str(QUALITY/'desktop-ko.png'),full_page=True)
  page.locator('#first-step').click()
  check('pre-freeze-no-truth-access',page.locator('#show-truth').is_disabled())
  check('pre-freeze-diagnostic-label','진단' in page.locator('#metric-rmse-label').inner_text())
  page.locator('#last-step').click()
  check('post-freeze-truth-toggle',not page.locator('#show-truth').is_disabled())
  page.locator('#show-truth').check()
  check('truth-curve-after-freeze',page.locator('#response-chart .truth-line').count()==1)
  page.locator('#chart-readout').select_option('first/none')
  check('alternate-readout-chart',page.locator('#response-chart svg').count()==1)
  configs=page.evaluate('(async()=> (await window.CLOSED_LOOP_READY).runs.map(r=>r.config))()')
  for c in configs:
   page.locator('#scenario').select_option(c['scenario'])
   page.locator('#policy').select_option(c['policy'])
   if not page.locator('#observation-model').is_disabled(): page.locator('#observation-model').select_option(c['observation_model'])
   page.locator('#load-record').click()
   check('replay-'+c['scenario']+'-'+c['policy']+'-'+c['observation_model'],page.locator('#response-chart svg').count()==1)
  page.locator('[data-tab="comparison"]').click()
  for scenario in dict.fromkeys(c['scenario'] for c in configs):
   page.locator('#comparison-scenario').select_option(scenario)
   check('comparison-'+scenario,page.locator('#comparison-rows tr').count()>=4)
  page.locator('[data-tab="direction"]').click()
  check('six-hypotheses',page.locator('.agenda-card').count()==6)
  page.locator('#lang-toggle').click()
  check('English-switch',page.locator('html').get_attribute('lang')=='en')
  page.locator('[data-tab="experiment"]').click()
  page.locator('#scenario').select_option('mechanism_pair');page.locator('#policy').select_option('guarded');page.locator('#load-record').click()
  page.screenshot(path=str(QUALITY/'desktop-en.png'),full_page=True)
  with page.expect_download() as download_info:page.locator('#export-run').click()
  download=download_info.value
  check('JSON-download-event',download.suggested_filename.endswith('.json'))
  dest=QUALITY/'browser-export-check.json';download.save_as(dest)
  exported=json.loads(dest.read_text());check('exported-synthetic-run',exported['evidence_status']=='synthetic-pilot-only')
  page.locator('#import-json').set_input_files(str(dest))
  check('JSON-import-viewer','audit' in page.locator('#source-status').inner_text().lower())
  page.locator('#import-json').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"real_data_validation":true}'})
  check('invalid-import-rejected',page.locator('#status-message').is_visible())
  dest.unlink()
  page.set_viewport_size({'width':390,'height':844})
  for tab in ['experiment','comparison','direction']:
   page.locator('[data-tab="'+tab+'"]').click()
   check('mobile-'+tab+'-no-overflow',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
  page.locator('[data-tab="experiment"]').click()
  page.screenshot(path=str(QUALITY/'mobile-en.png'),full_page=True)
  page.locator('#lang-toggle').click();page.screenshot(path=str(QUALITY/'mobile-ko.png'),full_page=True)
  check('no-JavaScript-page-errors',not errors)
  version=browser.version;browser.close()
 report={'status':'pass','checks':checks,'count':len(checks),'page_errors':errors,'browser':version,
   'render_mode':'isolated set_content with actual shipped assets; native gzip decoded',
   'navigation_limit':'Managed Chromium returned ERR_BLOCKED_BY_ADMINISTRATOR for file:// and localhost. Real URL navigation and browser-to-server end-to-end execution were not verified.',
   'http_api':'Separately exercised through actual local HTTP in ServerTests, not mocked as browser E2E.'}
 (QUALITY/'browser_checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))

if __name__=='__main__':main()
