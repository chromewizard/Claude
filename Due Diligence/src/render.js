// Renders src/pages/*.html to a PDF at each page's declared output path.
// Usage: node src/render.js [name-fragment ...]      (from the "Due Diligence" directory)
//   No arguments: every page. With arguments: only pages whose filename contains one of them,
//   e.g. `node src/render.js 08_Applicant` — so a one-page fix does not re-stamp the other PDFs
//   (Chromium writes a creation date into each PDF, so a re-render never reproduces the old bytes).
// Each page declares <meta name="dd-output" content="relative/path/to/File.pdf">,
// <meta name="dd-version" content="DD-…"> and <meta name="dd-title" content="Short document title">.
// Portrait documents: Letter, 0.8in top / 0.7in sides / 0.8in bottom, a running header on every page
// (EnergyWave · document title · Confidential — Draft — For Discussion · version) and a footer
// (disclaimer · source pointer · page numbers).
// Slide decks declare <meta name="dd-format" content="slides">: 13.333in × 7.5in pages, no margins, no
// Chromium header or footer — each slide carries its own footer line in the HTML. Chromium via Playwright.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const FONT = "font-family:'Liberation Sans',Arial,sans-serif;";
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
    const title = (html.match(/<meta name="dd-title" content="([^"]+)">/) || [])[1] || path.basename(m[1], '.pdf');
    const slides = /<meta name="dd-format" content="slides">/.test(html);
    const page = await ctx.newPage();
    await page.goto('file://' + src, { waitUntil: 'load' });
    if (slides) {
      await page.pdf({ path: out, width: '13.333in', height: '7.5in', printBackground: true, preferCSSPageSize: true,
        margin: { top: '0', right: '0', bottom: '0', left: '0' }, displayHeaderFooter: false });
    } else {
      await page.pdf({
        path: out, format: 'Letter', printBackground: true, preferCSSPageSize: false,
        margin: { top: '0.8in', right: '0.7in', bottom: '0.8in', left: '0.7in' },
        displayHeaderFooter: true,
        headerTemplate: `<div style="width:100%;${FONT}font-size:6.6pt;color:#737B82;letter-spacing:0.14em;text-transform:uppercase;padding:0.28in 0.7in 0;display:flex;justify-content:space-between;">
          <span>EnergyWave · ${esc(title)}</span>
          <span style="white-space:nowrap;margin-left:12px;">Confidential — Draft — For Discussion · ${esc(version)}</span></div>`,
        footerTemplate: `<div style="width:100%;${FONT}font-size:7pt;color:#737B82;padding:0 0.7in 0.3in;display:flex;justify-content:space-between;align-items:flex-end;">
          <span>EnergyWave · ${esc(version)} · Early-stage research venture. Forward-looking statements are not proven capabilities or guarantees. For discussion only; not an offer to sell securities. Sources: cited at the end of this document; register in SOURCE_LEDGER.md.</span>
          <span style="white-space:nowrap;margin-left:12px;">page <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
      });
    }
    await page.close();
    console.log('rendered', m[1]);
  }
  await browser.close();
})();
