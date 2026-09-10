/* Real Chrome layout checks using the bundled Playwright library. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {chromium} = require(process.env.PLAYWRIGHT_PATH || 'playwright');
(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROME_PATH, headless: true});
  const results = [];
  try {
    for (const route of ['/en/', '/en/best-joyagoo-finds/', '/zh/best-joyagoo-finds/', '/ar/best-joyagoo-finds/']) {
      for (const [width, columns] of [[390,1],[768,2],[1440,4]]) {
        const page = await browser.newPage({viewport:{width,height:844}});
        await page.goto((process.env.PREVIEW_URL || 'http://127.0.0.1:5192')+route);
        const result = await page.evaluate(() => {
          const grid = document.querySelector('.home-product-grid, .local-products');
          const search = document.querySelector('input[type="search"]');
          return {columns:getComputedStyle(grid).gridTemplateColumns.split(' ').length,
            overflow:document.documentElement.scrollWidth > innerWidth,
            searchHeight:search?.getBoundingClientRect().height,
            hero:document.querySelector('.hero-board img')?.loading};
        });
        assert.equal(result.columns,columns,route+' at '+width);
        assert.equal(result.overflow,false,route+' horizontal overflow');
        assert(result.searchHeight >= 48,route+' search touch target');
        if (width === 390) {
          const summary=page.locator('.site-menu > summary');
          assert(await summary.isVisible());
          await summary.click();
          assert(await page.locator('.site-menu .nav-links a').first().isVisible());
          await summary.click();
          assert(!(await page.locator('.site-menu .nav-links a').first().isVisible()));
          await page.screenshot({path:'audits/mobile-'+route.split('/').filter(Boolean).join('-')+'.png'});
        } else if (width === 1440) {
          assert(await page.locator('.site-menu .nav-links a').first().isVisible(), 'desktop navigation visible');
        }
        results.push({route,width,...result});
        await page.close();
      }
    }
    fs.writeFileSync('audits/mobile-layout.json',JSON.stringify(results,null,2));
    console.log('PASS: 12 real Chrome layouts, 1/2/4 card columns, touch targets, no horizontal overflow, native mobile menu and visible desktop navigation.');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
