import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import lighthouse from '../audits/performance-tools/node_modules/lighthouse/core/index.js';
const require = createRequire(fs.realpathSync('audits/performance-tools/node_modules/lighthouse/package.json'));
const launcher = await import(pathToFileURL(require.resolve('chrome-launcher')).href);
fs.mkdirSync('audits/lighthouse-profile', {recursive:true});
const chrome = await launcher.launch({chromePath:process.env.CHROME_PATH,
  chromeFlags:['--headless','--no-sandbox'], userDataDir:path.resolve('audits/lighthouse-profile')});
try {
  const scores=[];
  for (const [name,route] of [['home','/en/'],['category','/en/best-joyagoo-finds/shoes/'],['article','/en/articles/joyagoo-spreadsheet-qc-checklist/']]) {
    const result=await lighthouse('http://127.0.0.1:5191'+route, {port:chrome.port,
      output:['html','json'], logLevel:'error', onlyCategories:['performance','accessibility','seo','best-practices']});
    fs.writeFileSync(`audits/mobile-${name}.report.html`,result.report[0]);
    fs.writeFileSync(`audits/mobile-${name}.report.json`,result.report[1]);
    const row={route,...Object.fromEntries(Object.entries(result.lhr.categories).map(([k,v])=>[k,Math.round(v.score*100)])),
      cls:result.lhr.audits['cumulative-layout-shift'].numericValue,
      lcp:result.lhr.audits['largest-contentful-paint'].displayValue};
    scores.push(row);console.log(row);
  }
  fs.writeFileSync('audits/lighthouse-scores.json',JSON.stringify(scores,null,2));
} finally { await chrome.kill(); }
