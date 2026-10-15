// Renders src/pages/*.html to a PDF at each page's declared output path.
// Usage: node src/render.js [name-fragment ...]      (from the "Due Diligence" directory)
//   No arguments: every page. With arguments: only pages whose filename contains one of them,
//   e.g. `node src/render.js 08_Applicant` — so a one-page fix does not re-stamp the other PDFs
//   (Chromium writes a creation date into each PDF, so a re-render never reproduces the old bytes).
// Each page declares <meta name="dd-output" content="relative/path/to/File.pdf">.
// Letter, 0.6in/0.7in margins, footer with page numbers. Chromium via Playwright.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const filters = process.argv.slice(2);
  const pages = fs.readdirSync(path.join(__dirname, 'pages'))
    .filter(f => f.endsWith('.html'))
    .filter(f => filters.length === 0 || filters.some(x => f.includes(x)))
    .sort();
  if (pages.length === 0) { console.error('no page matches', filters); process.exit(1); }
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const ctx = await browser.newContext();
  for (const f of pages) {
    const src = path.join(__dirname, 'pages', f);
    const html = fs.readFileSync(src, 'utf8');
    const m = html.match(/<meta name="dd-output" content="([^"]+)">/);
    if (!m) { console.log('skip (no dd-output):', f); continue; }
    const out = path.join(root, m[1]);
    const version = (html.match(/<meta name="dd-version" content="([^"]+)">/) || [])[1] || '';
    const page = await ctx.newPage();
    await page.goto('file://' + src, { waitUntil: 'load' });
    await page.pdf({
      path: out, format: 'Letter', printBackground: true, preferCSSPageSize: false,
      margin: { top: '0.6in', right: '0.7in', bottom: '0.75in', left: '0.7in' },
      displayHeaderFooter: true, headerTemplate: '<span></span>',
      footerTemplate: `<div style="width:100%;font-family:'Liberation Sans',Arial,sans-serif;font-size:7pt;color:#737B82;padding:0 0.7in;display:flex;justify-content:space-between;">
        <span>EnergyWave · ${version} · Early-stage research venture. Forward-looking statements are not proven capabilities or guarantees. For discussion only; not an offer to sell securities.</span>
        <span style="white-space:nowrap;margin-left:12px;">page <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
    });
    await page.close();
    console.log('rendered', m[1]);
  }
  await browser.close();
})();
