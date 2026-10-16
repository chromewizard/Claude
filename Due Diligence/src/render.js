// Renders src/pages/*.html to PDF in two outputs from the one source:
//   internal — the canonical document at the page's dd-output path (markers, status tags, sources, version string);
//   final    — the presentation copy for the EnergyWave Final collection (projected language, no markers, no
//              internal apparatus), written to EnergyWave_Final/<folder>/<dd-final> for every folder in dd-final-folders.
// Usage: node src/render.js [--internal|--final|--both] [name-fragment ...]      (from the "Due Diligence" directory)
//   Default --both. With name fragments: only pages whose filename contains one of them, e.g. `node src/render.js 08_Applicant`
//   (Chromium writes a creation date into each PDF, so a re-render never reproduces the old bytes).
// Page metas: dd-output (internal path), dd-version, dd-title, optional dd-format=slides,
//   dd-final (presentation filename), dd-final-folders (comma list; "." = the Final root), optional dd-final-title.
// Presentation transform (fail-closed): elements with data-int are removed; elements with data-ext are revealed
//   (hidden in the internal output by CSS); every .need marker is replaced by its data-proj text (or the body's
//   data-proj-template with {field}; data-proj-empty for a bare marker) — a marker without one fails the render;
//   .tag and .sources elements are removed unless data-keep; .status text becomes its data-status (or the default);
//   .ver elements show the edition (or their data-final); the first span of each slide .foot becomes body data-final-foot;
//   then the visible text is scanned against src/build/final_banned.json and any hit fails the render.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const FONT = "font-family:'Liberation Sans',Arial,sans-serif;";
const FINAL_DIR = 'EnergyWave_Final';
const EDITION_LONG = '16 October 2026 · EnergyWave Final';
const EDITION_SHORT = 'Edition 16 Oct 2026';
const BANNED = JSON.parse(fs.readFileSync(path.join(__dirname, 'build', 'final_banned.json'), 'utf8'));

function transformFinal({ edition, finalFoot, banned }) {
  document.querySelectorAll('[data-int]').forEach(e => e.remove());
  document.querySelectorAll('.tag:not([data-keep])').forEach(e => e.remove());
  document.querySelectorAll('.status').forEach(e => { const s = e.getAttribute('data-status'); e.textContent = s !== null ? s : 'Confidential — Forecast — For Discussion'; });
  document.querySelectorAll('.ver').forEach(e => { const f = e.getAttribute('data-final'); e.textContent = f !== null ? f : edition; });
  if (finalFoot !== null) document.querySelectorAll('.foot > span:first-child').forEach(e => e.textContent = finalFoot);
  const tpl = document.body.getAttribute('data-proj-template');
  const emptyProj = document.body.getAttribute('data-proj-empty');
  const missing = [];
  document.querySelectorAll('.need').forEach(e => {
    if (!document.contains(e)) return;
    let p = e.getAttribute('data-proj');
    if (p === null && tpl !== null) {
      const t = e.textContent.replace(/\s+/g, ' ').trim();
      const m = t.match(/^\[TBD\](?:\s*—\s*(.*))?$/) || t.match(/^\[Pending:\s*(.*)\]$/);
      if (m) { const field = (m[1] || '').trim(); p = field ? tpl.replace('{field}', field) : emptyProj; }
    }
    if (p === null) { missing.push(e.textContent.replace(/\s+/g, ' ').trim().slice(0, 100)); return; }
    const s = document.createElement('span'); s.className = 'proj'; s.textContent = p; e.replaceWith(s);
  });
  if (missing.length) return { missing };
  document.querySelectorAll('[data-ext]').forEach(e => e.removeAttribute('data-ext'));
  document.querySelectorAll('.sources:not([data-keep])').forEach(e => e.remove());
  const text = document.body.textContent;  // not innerText: CSS text-transform would upper-case labels and defeat case-sensitive rules
  const hits = [];
  for (const [src, flags] of banned) {
    const re = new RegExp(src, flags || '');
    const m = text.match(re);
    if (m) { const i = text.indexOf(m[0]); hits.push(JSON.stringify(m[0]) + ' … ' + text.slice(Math.max(0, i - 70), i + 70).replace(/\s+/g, ' ')); }
  }
  return { hits };
}

(async () => {
  const root = path.resolve(__dirname, '..');
  const args = process.argv.slice(2);
  let mode = 'both';
  const filters = [];
  for (const a of args) { if (a === '--internal' || a === '--final' || a === '--both') mode = a.slice(2); else filters.push(a); }
  const pages = fs.readdirSync(path.join(__dirname, 'pages'))
    .filter(f => f.endsWith('.html'))
    .filter(f => filters.length === 0 || filters.some(x => f.includes(x)))
    .sort();
  if (pages.length === 0) { console.error('no page matches', filters); process.exit(1); }
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const ctx = await browser.newContext();
  let failed = 0;
  const meta = (html, name) => (html.match(new RegExp('<meta name="' + name + '" content="([^"]*)">')) || [])[1];
  for (const f of pages) {
    const src = path.join(__dirname, 'pages', f);
    const html = fs.readFileSync(src, 'utf8');
    const out = meta(html, 'dd-output');
    if (!out) { console.log('skip (no dd-output):', f); continue; }
    const version = meta(html, 'dd-version') || '';
    const title = meta(html, 'dd-title') || path.basename(out, '.pdf');
    const slides = /<meta name="dd-format" content="slides">/.test(html);
    const finalName = meta(html, 'dd-final');
    const finalFolders = (meta(html, 'dd-final-folders') || '').split(',').map(s => s.trim()).filter(Boolean);
    const finalTitle = meta(html, 'dd-final-title') || title.replace(/\s*\(draft\)\s*$/i, '');
    const finalFoot = (html.match(/<body[^>]*\sdata-final-foot="([^"]*)"/) || [null, null])[1];

    const render = async (page, isFinal) => {
      if (slides) {
        return page.pdf({ width: '13.333in', height: '7.5in', printBackground: true, preferCSSPageSize: true,
          margin: { top: '0', right: '0', bottom: '0', left: '0' }, displayHeaderFooter: false });
      }
      const headRight = isFinal ? `Confidential — Forecast — For Discussion · ${EDITION_SHORT}` : `Confidential — Draft — For Discussion · ${esc(version)}`;
      const footLeft = isFinal
        ? `EnergyWave, Inc. (a Delaware corporation, in formation) · ${EDITION_LONG} · Early-stage research venture. Projections are forecasts on stated assumptions, not commitments; forward-looking statements are not proven capabilities or guarantees. For discussion only; not an offer to sell, or a solicitation of an offer to buy, securities.`
        : `EnergyWave · ${esc(version)} · Early-stage research venture. Forward-looking statements are not proven capabilities or guarantees. For discussion only; not an offer to sell securities. Sources: cited at the end of this document; register in SOURCE_LEDGER.md.`;
      return page.pdf({
        format: 'Letter', printBackground: true, preferCSSPageSize: false,
        margin: { top: '0.8in', right: '0.7in', bottom: '0.8in', left: '0.7in' },
        displayHeaderFooter: true,
        headerTemplate: `<div style="width:100%;${FONT}font-size:6.6pt;color:#737B82;letter-spacing:0.14em;text-transform:uppercase;padding:0.28in 0.7in 0;display:flex;justify-content:space-between;">
          <span>EnergyWave · ${esc(isFinal ? finalTitle : title)}</span>
          <span style="white-space:nowrap;margin-left:12px;">${headRight}</span></div>`,
        footerTemplate: `<div style="width:100%;${FONT}font-size:7pt;color:#737B82;padding:0 0.7in 0.3in;display:flex;justify-content:space-between;align-items:flex-end;">
          <span>${footLeft}</span>
          <span style="white-space:nowrap;margin-left:12px;">page <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
      });
    };

    if (mode !== 'final') {
      const page = await ctx.newPage();
      await page.goto('file://' + src, { waitUntil: 'load' });
      const buf = await render(page, false);
      fs.mkdirSync(path.dirname(path.join(root, out)), { recursive: true });
      fs.writeFileSync(path.join(root, out), buf);
      await page.close();
      console.log('rendered', out);
    }
    if (mode !== 'internal' && finalName) {
      if (finalFolders.length === 0) { console.error('FINAL REFUSED', f, '— dd-final without dd-final-folders'); failed++; continue; }
      const page = await ctx.newPage();
      await page.goto('file://' + src, { waitUntil: 'load' });
      const r = await page.evaluate(transformFinal, { edition: EDITION_LONG, finalFoot, banned: BANNED });
      if (r.missing) { console.error('FINAL REFUSED', f, '— markers without a projected text:\n  ' + r.missing.join('\n  ')); failed++; await page.close(); continue; }
      if (r.hits.length) { console.error('FINAL REFUSED', f, '— internal language in the presentation text:\n  ' + r.hits.join('\n  ')); failed++; await page.close(); continue; }
      const buf = await render(page, true);
      for (const folder of finalFolders) {
        const dir = folder === '.' ? path.join(root, FINAL_DIR) : path.join(root, FINAL_DIR, folder);
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(path.join(dir, finalName), buf);
      }
      await page.close();
      console.log('final   ', finalName, '→', finalFolders.join(', '));
    }
  }
  await browser.close();
  if (failed) { console.error(`${failed} presentation render(s) refused`); process.exit(2); }
})();
