#!/usr/bin/env python3
"""Optional DOM/render smoke test. Requires playwright and a Chromium executable.

Loads the delivered HTML/CSS/JS through set_content, without URL navigation.
This validates DOM behavior, not file://, HTTP navigation, Pages deployment,
clipboard persistence, or the UI-to-server connection. HTTP APIs have separate tests.
"""
import argparse
import asyncio
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

async def main(executable: str) -> None:
    from playwright.async_api import async_playwright
    web = ROOT / 'research_lab/web'
    quality = ROOT / 'research_lab/results/quality'
    quality.mkdir(parents=True, exist_ok=True)
    html = (web / 'index.html').read_text(encoding='utf-8')
    import re
    html = re.sub(r'<link[^>]+href="assets/style.css"[^>]*>',
                  lambda _: '<style>' + (web/'assets/style.css').read_text() + '</style>', html)
    for asset in ['demo-data.js', 'app.js']:
        source = (web/'assets'/asset).read_text(encoding='utf-8').replace('</script', '<\\/script')
        html = html.replace(f'<script src="assets/{asset}"></script>', '<script>'+source+'</script>')
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=executable, headless=True,
                                          args=['--no-sandbox'])
        page = await browser.new_page(viewport={'width':1440, 'height':1050}, device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        await page.set_content(html, wait_until='load')
        assert await page.locator('#metrics .metric').count() == 4
        assert await page.locator('#run').is_disabled()
        await page.screenshot(path=str(quality/'desktop.png'), full_page=True)
        await page.locator('#language').click()
        assert await page.locator('html').get_attribute('lang') == 'en'
        await page.locator('#tab-prediction').click()
        assert await page.locator('#prediction-chart svg').count() == 1
        assert await page.locator('#learning-chart svg').count() == 1
        await page.locator('#tab-benchmark').click()
        assert await page.locator('#benchmark-body tr').count() == 5
        await page.locator('#ablations').check()
        assert await page.locator('#benchmark-body tr').count() == 8
        await page.locator('#tab-trace').click()
        await page.locator('#previous').click()
        before = await page.locator('#step-label').inner_text()
        await page.locator('#next').click()
        assert await page.locator('#step-label').inner_text() != before
        await page.locator('#scenario').select_option('hidden_mechanism')
        assert 'Truth outside' in await page.locator('#run-title').inner_text()
        await page.locator('#tab-scope').click()
        assert await page.locator('#scope-content .scope-block').count() == 5
        await page.locator('#tab-scope').press('Home')
        assert await page.locator('#tab-trace').get_attribute('aria-selected') == 'true'
        demo = json.loads((ROOT/'research_lab/results/pilot/demos.json').read_text())[0]
        await page.locator('#import').set_input_files({'name':'run.json','mimeType':'application/json','buffer':json.dumps(demo).encode()})
        await page.wait_for_function("document.getElementById('notification').textContent.includes('imported')")
        # Exercise serialization without claiming a browser download completed.
        await page.evaluate("window.__blobJSON=null; window.__makeBlobURL=URL.createObjectURL; URL.createObjectURL=(b)=>{b.text().then(t=>window.__blobJSON=t);return window.__makeBlobURL(b)};HTMLAnchorElement.prototype.click=function(){}")
        await page.locator('#export').click()
        await page.wait_for_function('window.__blobJSON !== null')
        exported = json.loads(await page.evaluate('window.__blobJSON'))
        assert exported['acquisition_sha256'] == demo['acquisition_sha256']
        # Text from imported records is escaped, never inserted as active markup.
        demo['config']['policy'] = '<img src=x onerror="window.injected=true">'
        await page.locator('#import').set_input_files({'name':'escape.json','mimeType':'application/json','buffer':json.dumps(demo).encode()})
        await page.wait_for_timeout(100)
        assert not await page.evaluate('Boolean(window.injected)')
        await page.locator('#policy').select_option('guarded_information')
        await page.locator('#scenario').select_option('noise_shift')
        await page.locator('#language').click()
        await page.locator('#tab-prediction').click()
        await page.screenshot(path=str(quality/'evaluation.png'), full_page=True)
        await page.set_viewport_size({'width':390,'height':844})
        await page.wait_for_timeout(150)
        assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        await page.screenshot(path=str(quality/'mobile.png'), full_page=True)
        assert not errors, errors
        report = {
            'status':'pass', 'browser':'Chromium '+browser.version,
            'harness':'set_content with exact delivered assets inlined; URL navigation not tested',
            'checks':['initial 4 metrics','static run disabled','KR/EN','all tabs and SVG plots',
                      '5 baseline and 8 expanded benchmark rows','timeline navigation',
                      'stored scenario switching','keyboard tab navigation','JSON import',
                      'exported Blob JSON identity (download suppressed)','import text escaping',
                      '390px layout without horizontal overflow'],
            'page_errors':errors, 'screenshots':['desktop.png','evaluation.png','mobile.png'],
            'not_tested':['HTTP and file URL navigation (environment browser policy blocks URLs)',
                          'browser-to-server end-to-end connection','completed file download',
                          'native clipboard and localStorage persistence','Windows or macOS native execution',
                          'remote GitHub Pages deployment','real biological data']}
        (quality/'browser_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        await browser.close()
        print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    asyncio.run(main(parser.parse_args().chromium))
