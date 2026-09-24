/* Refuse to package stale translations or pages with no language controls. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'src/translations/published.json'), 'utf8'));
function sourceHash(text) {
  text = text.replace(/\r\n/g, '\n')
    .replace(/<details class="locale-switcher">[\s\S]*?<\/details>/g, '{{language_switcher}}')
    .replace(/<link\b[^>]*hreflang=[^>]*>\s*/g, '')
    .replace(/<script\b[^>]*(?:src="\/js\/i18n.js"|id="site-translation-data")[^>]*>[\s\S]*?<\/script>\s*/g, '')
    .replace(/<link rel="stylesheet" href="\/locale.css" \/>\s*/g, '')
    .replaceAll('class="footer-brand" translate="no"', 'class="footer-brand"');
  return crypto.createHash('sha256').update(text).digest('hex');
}
function check() {
  const failures = [];
  for (const relative of fs.readdirSync(path.join(root, 'en'), {recursive: true})) {
    if (path.basename(relative) !== 'index.html') continue;
    const text = fs.readFileSync(path.join(root, 'en', relative), 'utf8');
    if (!text.includes('class="locale-switcher"') || !text.includes('/js/i18n.js')) failures.push(`Missing language controls: en/${relative}`);
  }
  for (const [route, record] of Object.entries(manifest)) {
    const source = path.join(root, 'en', route.split('/').slice(2).join('/'), 'index.html');
    const target = path.join(root, route, 'index.html');
    if (!fs.existsSync(source) || !fs.existsSync(target) || sourceHash(fs.readFileSync(source, 'utf8')) !== record.sourceHash) {
      failures.push(`Translation needs rebuilding: ${route}`);
    }
  }
  if (failures.length) throw new Error(failures.join('\n'));
  console.log(`Language controls and ${Object.keys(manifest).length} whole-site translations checked.`);
}
module.exports = {sourceHash, check};
if (require.main === module) check();
