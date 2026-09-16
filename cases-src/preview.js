// Скріншот зібраного сайту без доступу до tildacdn (наприклад, з claude.ai/code).
//   python3 -m http.server 8765 --directory .. &        # з папки cases-src
//   node preview.js http://localhost:8765/cases/ out 390 844          # вся сторінка → out-01.jpg, out-02.jpg …
//   node preview.js http://localhost:8765/cases/ out 390 844 480      # лише верхні 480px → out.png
//   SEL='#oks-pk' node preview.js http://localhost:8765/cases/ out 1440 900   # один блок → out.png
// Запити до *.tildacdn.com підміняються локальною копією з cases/tilda/ (її оновлює
// воркфлоу .github/workflows/fetch-tilda.yml; файли треба розпакувати з gzip, якщо CDN віддав стиснуті).
// Потрібні: node, playwright (глобально), Chromium за PLAYWRIGHT_BROWSERS_PATH, Pillow для нарізки.
const path = require('path'), fs = require('fs');
const pw = (() => { try { return require('playwright'); } catch (e) { return require('/opt/node22/lib/node_modules/playwright'); } })();
const ROOT = path.resolve(__dirname, '..', 'cases');
const TILDA = path.join(ROOT, 'tilda'), IMG = path.join(ROOT, 'img');
const CHROME = process.env.CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const MIME = { css: 'text/css', js: 'application/javascript', svg: 'image/svg+xml', woff: 'font/woff', woff2: 'font/woff2', png: 'image/png', jpg: 'image/jpeg' };
(async () => {
  const [url, out, w = 390, h = 844, clip = 0] = process.argv.slice(2);
  const browser = await pw.chromium.launch(CHROME ? { executablePath: CHROME } : {});
  const ctx = await browser.newContext({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1.5, isMobile: +w < 700, hasTouch: +w < 700 });
  const missing = new Set();
  await ctx.route(/tildacdn\.com/, route => {
    const u = new URL(route.request().url());
    if (/tilda-fallback/.test(u.pathname)) return route.fulfill({ body: '', contentType: 'application/javascript' });
    let f = path.join(TILDA, u.host, u.pathname);
    if (/\/ws\/project460786\/img\//.test(u.pathname)) f = path.join(IMG, path.basename(u.pathname));
    if (fs.existsSync(f)) return route.fulfill({ body: fs.readFileSync(f), contentType: MIME[f.split('.').pop()] || 'application/octet-stream' });
    missing.add(u.host + u.pathname); route.abort();
  });
  await ctx.route(/\.(google|googletagmanager|google-analytics|facebook)\.com/, r => r.abort());
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  await page.waitForTimeout(2500);
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0, 0); });
  await page.waitForTimeout(1500);
  const d = await page.evaluate(() => ({ h: document.body.scrollHeight, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
  console.log(`висота ${d.h}px | scrollWidth ${d.sw} / viewport ${d.cw} ${d.sw > d.cw ? '⚠️ ГОРИЗОНТАЛЬНИЙ СКРОЛ' : 'ok'}`);
  if (missing.size) console.log('немає локально:', [...missing].join(', '));
  if (errors.length) console.log('JS-помилки:', [...new Set(errors)].slice(0, 5).join(' | '));
  if (process.env.SEL) { const el = page.locator(process.env.SEL).first(); await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(600); await el.screenshot({ path: out + '.png' }); await browser.close(); return; }
  if (+clip) { await page.screenshot({ path: out + '.png', clip: { x: 0, y: 0, width: +w, height: +clip } }); await browser.close(); return; }
  const full = out + '-full.png';
  await page.screenshot({ path: full, fullPage: true });
  await browser.close();
  require('child_process').execSync(`python3 - "${full}" "${out}" <<'PY'
import sys; from PIL import Image
Image.MAX_IMAGE_PIXELS=None
im=Image.open(sys.argv[1]).convert('RGB'); W,H=im.size; step=2400; n=0
for y in range(0,H,step):
    n+=1; im.crop((0,y,W,min(y+step,H))).save(f"{sys.argv[2]}-{n:02d}.jpg", quality=80)
print(f"{n} шматків по {step}px (ширина {W})")
PY`, { stdio: 'inherit' });
})();
