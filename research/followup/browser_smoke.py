from pathlib import Path
import json,hashlib,threading,functools,http.server,re,urllib.request
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2]; W=R/'research/followup/web';Q=R/'research/followup/quality';Q.mkdir(exist_ok=True)
checks=[]; errors=[]; navigation={}; download_ok=False
def ck(c,s):
 if not c:raise AssertionError(s)
 checks.append(s)
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(R)));th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 context=browser.new_context(viewport={'width':1440,'height':1100},accept_downloads=True)
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 try:
  page.goto((W/'index.html').as_uri(),wait_until='load');navigation['file']='passed'
 except Exception as exc:
  navigation['file']=str(exc).split('Call log:')[0].strip()
 html=(W/'index.html').read_text().replace('<link rel="stylesheet" href="style.css">','<style>'+(W/'style.css').read_text()+'</style>')
 html=html.replace('<script defer src="bundle.js"></script>','').replace('<script defer src="app.js"></script>','')
 html=html.replace('</body>','<script>'+(W/'bundle.js').read_text().replace('</script','<\\/script')+'</script><script>'+(W/'app.js').read_text().replace('</script','<\\/script')+'</script></body>')
 page.set_content(html,wait_until='load');page.wait_for_selector('#a-rows tr')
 ck(page.locator('#a-rows tr').count()==3,'actual assets in inline harness render three detectors');ck('38.5%' in page.locator('#a-kpis').inner_text(),'actual normal false warning shown')
 ck(page.locator('html').get_attribute('lang')=='ko','Korean default')
 page.screenshot(path=str(Q/'viewer-desktop-ko.png'),full_page=True)
 page.locator('#language').click();ck('Detecting a fault' in page.locator('h1').inner_text(),'English translation')
 page.locator('#scenario').select_option('reference_mismatch');ck('observational' in page.locator('#scenario-warning').inner_text().lower(),'non-identifiability caution')
 page.locator('[data-tab="acquisition"]').click();ck(page.locator('#b-rows tr').count()==6,'six real policy summaries');ck('Not monitored' in page.locator('#b-rows').inner_text(),'no audit is not zero alarms')
 page.locator('[data-tab="trace"]').click();page.locator('#scenario').select_option('combined');ck(page.locator('#curve path').count()==3,'actual interval and two paths')
 path0=page.locator('#curve path').last.get_attribute('d');page.locator('#u').select_option('1');ck(path0!=page.locator('#curve path').last.get_attribute('d'),'intervention changes plot')
 page.locator('#policy').select_option('no_reference');ck('3 / 5' in page.locator('#trace-kpis').inner_text(),'rank ablation visible')
 page.locator('#policy').select_option('block_targeted');page.locator('#language').click();page.screenshot(path=str(Q/'viewer-trace-ko.png'),full_page=True)
 # Exercise every bundle scenario/policy without executing new computations.
 for sc in page.locator('#scenario option').evaluate_all('(xs)=>xs.map(x=>x.value)'):
  page.locator('#scenario').select_option(sc)
  for pol in page.locator('#policy option').evaluate_all('(xs)=>xs.map(x=>x.value)'):
   page.locator('#policy').select_option(pol);ck(page.locator('#step-rows tr').count()>0,f'trace {sc}/{pol}')
 # Actual HTTP navigation and native downloaded bytes, not an injected harness.
 base=f'http://127.0.0.1:{srv.server_port}'
 try:
  page.goto(base+'/research/followup/web/index.html',wait_until='load');navigation['http']='passed'
 except Exception as exc:
  navigation['http']=str(exc).split('Call log:')[0].strip()
 page.set_content(html,wait_until='load')
 for asset in ['index.html','style.css','app.js','bundle.js']:
  with urllib.request.urlopen(base+'/research/followup/web/'+asset) as resp: raw=resp.read()
  ck(raw==(W/asset).read_bytes(),'actual HTTP bytes '+asset)
 # Browser download cannot be inferred from HTTP transport tests.
  # Smartphone size, without full-page horizontal overflow.
 page.set_viewport_size({'width':390,'height':844});page.locator('[data-tab="detector"]').click();page.locator('#scenario').select_option('normal');
 ck(page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),'mobile document fits horizontally')
 page.screenshot(path=str(Q/'viewer-mobile-ko.png'),full_page=True)
 ck(page.locator('#language').bounding_box()['width']>=44,'language touch target')
 ck(page.locator('body').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=16,'16px body font')
 page.locator('[data-tab="trace"]').click()
 ck(page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),'mobile trace document fits horizontally')
 ck(page.locator('#curve').bounding_box()['width']>=1000,'mobile plot scrolls rather than shrinking labels')
 ck(not errors,'zero JavaScript runtime errors')
 browser.close();srv.shutdown()
(Q/'browser-validation.json').write_text(json.dumps({'status':'passed','checks':checks,'n_checks':len(checks),'runtime_errors':errors,'navigation_attempts':navigation,'validation_mode':'actual assets injected into browser; separate native HTTP transport','native_file_navigation':navigation.get('file')=='passed','native_local_http_navigation':navigation.get('http')=='passed','native_http_download':download_ok,'not_tested':['remote GitHub Pages deploy','Windows/macOS native Python','real biology','Python compute API in new static viewer','browser download completion']},ensure_ascii=False,indent=2))
print('Browser checks:',len(checks))
