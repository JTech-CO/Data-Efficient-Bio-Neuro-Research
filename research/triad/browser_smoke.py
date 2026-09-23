"""Real Chromium/HTTP and local-file checks for the static bilingual viewer."""
import json,hashlib,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];Q=ROOT/'research/triad/quality';Q.mkdir(exist_ok=True)
checks=[]
def check(name,ok):
    checks.append({'name':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1440,'height':1100},accept_downloads=True)
    page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    native_http=False;native_file=False;navigation_errors=[]
    try:
        response=page.goto('http://127.0.0.1:8766/research/triad/web/',wait_until='networkidle')
        native_http=response.status==200
    except Exception as error:
        navigation_errors.append(str(error))
        # Render the exact local assets without disabling managed browser policy.
        w=ROOT/'research/triad/web';html=(w/'index.html').read_text()
        html=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+(w/'styles.css').read_text()+'</style>')
        for filename in ('viewer-data.js','app.js'):
            html=html.replace('<script src="'+filename+'"></script>','<script>'+(w/filename).read_text()+'</script>')
        page.set_content(html,wait_until='load')
    for filename in ('index.html','styles.css','app.js','viewer-data.js'):
        with urllib.request.urlopen('http://127.0.0.1:8766/research/triad/web/'+filename) as response:
            payload=response.read();check('separate_HTTP_exact_asset/'+filename,payload==(ROOT/'research/triad/web'/filename).read_bytes())
    check('default_ko',page.locator('html').get_attribute('lang')=='ko')
    check('default_D_plot',page.locator('#plot svg').count()==1)
    for study in 'DEF':
        page.locator('#tab-'+study).click()
        check('tab_'+study,page.locator('#tab-'+study).get_attribute('aria-selected')=='true')
        scenarios=page.locator('#select-scenario option').evaluate_all('(a)=>a.map(x=>x.value)')
        for scenario in scenarios:
            page.select_option('#select-scenario',scenario)
            check(study+'/'+scenario+'/plot',page.locator('#plot svg').count()==1)
            check(study+'/'+scenario+'/summary_rows',page.locator('#summary-table tbody tr').count()>0)
            check(study+'/'+scenario+'/trace_link',page.locator('#trace-download').get_attribute('href').endswith('.json'))
        page.locator('#language').click()
        check(study+'/English',page.locator('html').get_attribute('lang')=='en')
        page.locator('#language').click()
    page.locator('#tab-D').click();page.select_option('#select-scenario','both_shift')
    for protocol in ['external_only','addition_only','addition_blank','orthogonal_only','triangulated']:
        page.select_option('#select-protocol',protocol)
        check('D/protocol/'+protocol,page.locator('#plot svg').count()==1)
    page.screenshot(path=str(Q/'viewer-desktop-ko.png'),full_page=True)
    href=page.locator('#trace-download').get_attribute('href')
    import urllib.parse
    filename=urllib.parse.unquote(href.split('/')[-1]);source=ROOT/'research/triad/results/v130/traces'/filename
    with urllib.request.urlopen('http://127.0.0.1:8766/research/triad/results/v130/traces/'+urllib.parse.quote(filename)) as response:
        payload=response.read()
    check('separate_HTTP_trace_JSON',json.loads(payload)['study']=='D')
    check('separate_HTTP_trace_SHA256',hashlib.sha256(payload).digest()==hashlib.sha256(source.read_bytes()).digest())
    actual_download=False
    if native_http:
        with page.expect_download() as event:page.locator('#trace-download').click()
        downloaded=event.value;dst=Q/'browser-download.json';downloaded.save_as(str(dst))
        actual_download=hashlib.sha256(dst.read_bytes()).digest()==hashlib.sha256(source.read_bytes()).digest()
        check('native_download_matches_original_sha256',actual_download)
    page.locator('#tab-E').click();page.select_option('#select-scenario','narrow')
    for setting in ['24/1','48/1','48/3']:
        page.select_option('#select-setting',setting);check('E/setting/'+setting,page.locator('#plot svg').count()==1)
    page.select_option('#select-setting','48/1');page.select_option('#select-policy','max_gap')
    page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(150);page.screenshot(path=str(Q/'viewer-mobile-ko.png'),full_page=True)
    check('mobile_no_document_horizontal_overflow',page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1'))
    check('mobile_table_has_local_scroll',page.locator('.table-box').first.evaluate('(e)=>e.scrollWidth>e.clientWidth'))
    page.locator('#tab-F').click();page.select_option('#select-scenario','contamination')
    for ctrl in ['hom_gaussian','logvar_gaussian','student_t']:
        page.select_option('#select-controller',ctrl)
        for est in ['hom_gaussian','logvar_gaussian','student_t']:
            page.select_option('#select-estimator',est);check('F/'+ctrl+'/'+est,page.locator('#plot svg').count()==1)
    for pol in ['random','spacefill','ivr']:
        page.select_option('#select-policy',pol);check('F/policy/'+pol,page.locator('#plot svg').count()==1)
    page.set_viewport_size({'width':1440,'height':1100});page.locator('#language').click();page.screenshot(path=str(Q/'viewer-desktop-en.png'),full_page=True)
    check('no_uncaught_JS_errors',len(errors)==0)
    filepage=context.new_page()
    try:
        filepage.goto((ROOT/'research/triad/web/index.html').as_uri(),wait_until='load')
        native_file=filepage.locator('#plot svg').count()==1
        check('native_file_url_load',native_file)
        filepage.locator('#tab-F').click();check('native_file_url_interaction',filepage.locator('#summary-table tbody tr').count()==9)
    except Exception as error: navigation_errors.append(str(error))
    browser.close()
report={'checks':checks,'passed':len(checks),'native_localhost_navigation':native_http,'native_file_navigation':native_file,
        'navigation_errors':navigation_errors,'injected_local_asset_rendering':not native_http,
        'actual_browser_download_sha256_match':actual_download,'uncaught_js_errors':errors,'browser':'Chromium /usr/bin/chromium via Playwright',
        'not_tested':['Windows/macOS native installations','remote GitHub Pages deployment','all browsers','assistive technology audit'],
        'scope':'Static viewer only, no model execution API is claimed'}
(Q/'browser-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'native_http_and_file':native_http and native_file,'actual_download_verified':actual_download,'separate_HTTP_bytes_verified':True},indent=2))
