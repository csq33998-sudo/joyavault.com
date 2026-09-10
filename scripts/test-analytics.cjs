const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {config} = require('./build-analytics.cjs');
const source = fs.readFileSync(require('node:path').join(__dirname, '../js/analytics.js'), 'utf8');

// Minimal browser event harness: exercise the production script and navigation timing.
function setup({id = '', existing = true, callback = false, throws = false} = {}) {
  const events = [], navigation = [], scripts = [], timers = [], listeners = {};
  const document = {
    documentElement: {lang: 'en'},
    querySelector: () => null,
    createElement: () => ({}),
    head: {appendChild: script => scripts.push(script)},
    addEventListener: (type, fn) => (listeners[type] ||= []).push(fn),
  };
  const window = {
    JoyaAnalyticsConfig: {measurementId: id},
    location: {pathname: '/en/', href: 'https://joyavault.com/en/', origin: 'https://joyavault.com', assign: url => navigation.push(url)},
    setTimeout: fn => {timers.push(fn); return timers.length - 1;},
    clearTimeout: index => {timers[index] = null;},
  };
  if (existing) window.gtag = (...args) => {
    if (throws) throw new Error('Blocked analytics');
    events.push(args);
    if (callback && args[2]?.event_callback) args[2].event_callback();
  };
  const original = window.gtag;
  const context = vm.createContext({window, document, URL, Date});
  vm.runInContext(source, context);
  function dispatch(type, target, extra = {}) {
    const event = {type, target, button: 0, defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; }, ...extra};
    (listeners[type] || []).forEach(fn => fn(event));
    return event;
  }
  return {events, navigation, scripts, timers, window, original, context, dispatch,
    tick: () => timers.forEach(fn => fn && fn())};
}
function link(href, {card, product, language, header, target = '', dataset = {}} = {}) {
  const a = {
    href, target, dataset,
    getAttribute: name => name === 'lang' ? language : null,
    hasAttribute: () => false,
    closest: selector => ({
      'a[href]': a, '.find-card, .local-product': card,
      '[data-product-source]': product ? a : null,
      '.locale-switcher': language ? {} : null,
      'header': header ? {} : null,
    })[selector] || null,
  };
  return a;
}
const last = h => h.events.at(-1);
const params = h => JSON.parse(JSON.stringify(last(h)[2]));

assert.match(config({}), /"measurementId":""/);
assert.match(config({GA4_MEASUREMENT_ID: ' G-ABC123 '}), /G-ABC123/);
assert.throws(() => config({GA4_MEASUREMENT_ID: '<script>'}));
assert(!config({SECRET: 'never-expose'}).includes('never-expose'));
{
  const h = setup({existing: false});
  const event = h.dispatch('click', link('https://joyagoo.com/'));
  assert.equal(h.scripts.length, 0);
  assert.equal(h.window.gtag, undefined);
  assert.equal(event.defaultPrevented, false);
}
{
  const h = setup({existing: false, id: 'G-TEST123'});
  assert.equal(h.scripts.length, 1);
  assert.equal(h.scripts[0].async, true);
  assert.equal(h.window.dataLayer[1][0], 'config');
  h.dispatch('click', link('https://joyavault.com/en/joyagoo-buying-guide/'));
  assert.equal(h.window.dataLayer[2][1], 'guide_click');
}
{
  const h = setup({id: 'G-TEST123'});
  assert.equal(h.original, h.window.gtag);
  assert.equal(h.scripts.length, 0);
  vm.runInContext(source, h.context);
  h.dispatch('click', link('https://joyavault.com/en/best-joyagoo-finds/clothing/hoodies/'));
  assert.equal(h.events.length, 1);
  assert.equal(last(h)[1], 'category_click');
  assert.equal(params(h).category, 'clothing/hoodies');
  assert.equal(params(h).page_path, '/en/');
  h.dispatch('change', {matches: () => true, value: 'Shoes'});
  assert.equal(params(h).category, 'shoes');
}
{
  const h = setup();
  const input = {value: '  sneakers  ', matches: () => true, closest: () => null};
  h.dispatch('submit', {matches: () => true, querySelector: () => input});
  assert.equal(last(h)[1], 'search_submit');
  assert.equal(params(h).query, 'sneakers');
  h.dispatch('input', input);
  assert.equal(h.events.length, 1, 'typing must not count as submission');
  h.dispatch('keydown', input, {key: 'Enter'});
  assert.equal(h.events.length, 2);
  h.dispatch('keydown', input, {key: 'Enter', isComposing: true});
  h.dispatch('keydown', input, {key: 'Enter', repeat: true});
  assert.equal(h.events.length, 2);
}
{
  const h = setup();
  h.dispatch('click', link('https://joyavault.com/zh/', {language: 'zh'}));
  assert.equal(last(h)[1], 'language_switch');
  assert.equal(params(h).from_language, 'en');
  assert.equal(params(h).to_language, 'zh');
  h.dispatch('click', link('https://joyavault.com/en/', {language: 'en'}));
  assert.equal(h.events.length, 1);
  h.dispatch('click', link('https://joyavault.com/en/articles/joyagoo-spreadsheet-qc-checklist/'));
  assert.equal(last(h)[1], 'guide_click');
  assert.equal(params(h).guide_name, 'joyagoo-spreadsheet-qc-checklist');
}
{
  const h = setup();
  const card = {dataset: {findId: '123', title: 'Test Shoes', category: 'Shoes', marketplace: 'Weidian'}};
  h.dispatch('click', link('https://joyavault.com/en/finds/test/', {card}));
  assert.equal(last(h)[1], 'find_card_click');
  assert.equal(params(h).title, 'Test Shoes');
  assert.equal(params(h).marketplace, 'Weidian');
  assert.equal(params(h).category, 'Shoes');
  const event = h.dispatch('click', link('https://weidian.com/item.html?itemID=123',
    {card, product: true, target: '_blank', dataset: {productFindId: '123'}}));
  assert.equal(last(h)[1], 'external_product_click');
  assert.equal(params(h).find_id, '123');
  assert.equal(params(h).source_domain, 'weidian.com');
  assert.equal(params(h).page_path, '/en/');
  assert.equal(params(h).destination_url, 'https://weidian.com/item.html?itemID=123');
  assert.equal(event.defaultPrevented, false);
}
{
  const h = setup();
  const event = h.dispatch('click', link('https://mgt.joyagoo.com/register', {header: true}));
  assert.equal(last(h)[1], 'joyagoo_click');
  assert.equal(params(h).cta_location, 'header');
  assert(event.defaultPrevented);
  assert.equal(h.navigation.length, 0, 'event is emitted before navigation');
  last(h)[2].event_callback();
  h.tick();
  assert.equal(h.navigation.length, 1, 'callback and fallback navigate only once');
}
{
  const h = setup();
  h.dispatch('click', link('https://joyagoo.com/'));
  h.tick();
  assert.equal(h.navigation.length, 1, 'missing callbacks do not block navigation');
  const broken = setup({throws: true});
  broken.dispatch('click', link('https://joyagoo.com/'));
  assert.equal(broken.navigation.length, 1);
}
for (const extra of [{ctrlKey: true}, {metaKey: true}, {shiftKey: true}, {altKey: true}, {type: 'auxclick', button: 1}]) {
  const h = setup();
  const event = h.dispatch(extra.type || 'click', link('https://joyagoo.com/'), extra);
  assert.equal(h.events.length, 1);
  assert.equal(event.defaultPrevented, false);
}
{
  const h = setup({callback: true});
  h.dispatch('click', link('https://mgt.joyagoo.com/product', {product: true, dataset: {productFindId: '123'}}));
  assert.equal(h.events.length, 2);
  assert.equal(h.navigation.length, 1);
  h.dispatch('click', link('https://fakejoyagoo.com/'));
  assert.equal(h.events.length, 2, 'lookalike domains are excluded');
}
{
  const h = setup();
  h.dispatch('click', link('https://joyavault.com/en/marketplaces/taobao/'));
  assert.equal(last(h)[1], 'marketplace_click');
  assert.equal(params(h).marketplace, 'taobao');
  assert.equal(params(h).page_path, '/en/');
  h.dispatch('change', {matches: selector => selector === '#finds-marketplace', value: 'Weidian'});
  assert.equal(last(h)[1], 'marketplace_click');
  assert.equal(params(h).marketplace, 'weidian');
  h.dispatch('click', link('https://joyavault.com/en/best-joyagoo-finds/?category=Shoes&marketplace=1688'));
  assert.equal(h.events.at(-2)[1], 'marketplace_click');
  assert.equal(h.events.at(-2)[2].marketplace, '1688');
  assert.equal(last(h)[1], 'category_click');
  const count = h.events.length;
  h.dispatch('change', {matches: selector => selector === '#finds-marketplace', value: ''});
  assert.equal(h.events.length, count, 'reset is not a marketplace selection');
}
console.log('PASS: all 8 events, parameters, disabled mode, existing gtag reuse, async initialization, duplicate guard, modified clicks, callback ordering and failure fallback.');
