"""Try local HTTP; disclose asset-injection fallback if managed browser policy blocks navigation."""
from pathlib import Path
import json,subprocess,sys,time,urllib.request
R=Path(__file__).resolve().parents[2];Q=R/'research/bounded/quality'
Q.mkdir(exist_ok=True)
def main():
 from playwright.sync_api import sync_playwright
 checks=[];errors=[]
 def check(name,ok):
  checks.append({'name':name,'passed':bool(ok)})
  if not ok:raise AssertionError(name)
 server=subprocess.Popen([sys.executable,'-m','http.server','8768','--bind','127.0.0.1'],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:
  base='http://127.0.0.1:8768/research/bounded/web/'
  for _ in range(50):
   try:urllib.request.urlopen(base,timeout=1).read();break
   except Exception:time.sleep(.1)
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
   page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
   page.on('pageerror',lambda e:errors.append(str(e)))
   navigation_error=None
   try:
    response=page.goto(base,wait_until='networkidle')
    check('actual_http_navigation',response.status==200)
    navigation='actual local HTTP via headless Chromium'
   except Exception as exc:
    navigation_error=str(exc)
    if 'ERR_BLOCKED_BY_ADMINISTRATOR' not in navigation_error:raise
    page.close()
    page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    web=R/'research/bounded/web'
    html=(web/'index.html').read_text().replace('<link rel="stylesheet" href="style.css">','<style>'+(web/'style.css').read_text()+'</style>')
    for js in ['data.js','app.js']:
     html=html.replace('<script src="'+js+'"></script>','<script>'+(web/js).read_text()+'</script>')
    page.set_content(html,wait_until='load')
    navigation='deployment assets injected after managed browser blocked localhost navigation'
    check('injected_deployment_assets_loaded',page.locator('#results tbody tr').count()>0)
   check('initial_language_ko',page.locator('html').get_attribute('lang')=='ko')
   check('initial_G_3_rows',page.locator('#results tbody tr').count()==3)
   check('data_has_363_cells',page.evaluate('window.BOUNDED_DATA.summary.length')==363)
   check('data_has_105_traces',page.evaluate('window.BOUNDED_DATA.traces.length')==105)
   page.screenshot(path=str(Q/'viewer-desktop-ko.png'),full_page=True)
   # Every representative selector combination must render without NaN/undefined.
   selectors=page.evaluate('window.BOUNDED_DATA.traces.map(r=>({study:r.study,scenario:r.scenario,design:r.design,policy:r.policy,fraction:r.audit_fraction,repeats:r.repeats}))')
   for i,r in enumerate(selectors):
    page.locator(f'button[data-study="{r["study"]}"]').click()
    page.locator('#scenario').select_option(r['scenario'])
    page.locator('#design').select_option(r['design'] if r['study']=='G' else r['policy'] if r['study']=='H' else str(r['repeats']))
    if r['study']=='H':page.locator('#fraction').select_option(str(r['fraction']) if r['fraction'] else '0')
    text=page.locator('#results').inner_text();fig=page.locator('#figure').inner_html()
    check(f'valid_trace_{i}_{r["study"]}_{r["scenario"]}', bool(text) and 'NaN' not in fig and 'undefined' not in text and page.locator('#raw').get_attribute('href').endswith('.json'))
   for study in 'GHI':
    page.locator(f'button[data-study="{study}"]').click()
    for lang in ['en','ko']:
     page.locator('#language').click()
     check(f'language_{study}_{lang}',page.locator('html').get_attribute('lang')==lang)
     check(f'nonempty_title_{study}_{lang}',bool(page.locator('#title').inner_text()))
   page.locator('button[data-study="I"]').click();page.locator('#scenario').select_option('mean_missing')
   page.screenshot(path=str(Q/'viewer-I-ko.png'),full_page=True)
   page.locator('#language').click();page.screenshot(path=str(Q/'viewer-desktop-en.png'),full_page=True);page.locator('#language').click()
   page.set_viewport_size({'width':390,'height':844})
   page.locator('button[data-study="G"]').click()
   check('mobile_document_no_horizontal_overflow',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
   check('table_has_its_own_scroll_container',page.locator('.table-wrap').evaluate('(e)=>getComputedStyle(e).overflowX')=='auto')
   page.screenshot(path=str(Q/'viewer-mobile-ko.png'),full_page=True)
   # Directly retrieve the selected source via HTTP.
   raw=page.locator('#raw').get_attribute('href')
   import urllib.parse
   with urllib.request.urlopen(urllib.parse.urljoin(base,raw)) as res:
    data=json.loads(res.read());check('actual_http_raw_record',data['study']=='G' and 'record_digest' in data)
   check('no_javascript_page_errors',not errors)
   browser.close()
  result={'checks':len(checks),'all_passed':True,'navigation':navigation,'navigation_error':navigation_error,'checks_detail':checks,'page_errors':errors,'scope':'Rendering/selectors on actual deployment assets; separate HTTP transport. Full browser-to-localhost navigation may be blocked, as recorded above. No remote Pages, native Windows/macOS installation or completed browser download tested.'}
  (Q/'browser.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='checks_detail'},indent=2))
 finally:
  server.terminate();server.wait(timeout=10)
if __name__=='__main__':main()
