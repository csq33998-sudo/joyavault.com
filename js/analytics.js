/* Delegated GA4 events; no DOM scan, dependencies, or blocking network requests. */
(() => {
  'use strict';
  if (window.JoyaAnalyticsLoaded) return;
  window.JoyaAnalyticsLoaded = true;
  const id = (window.JoyaAnalyticsConfig || {}).measurementId || '';
  if (typeof window.gtag !== 'function' && /^G-[A-Z0-9]+$/.test(id)) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', id);
    if (!document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
      const script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
      document.head.appendChild(script);
    }
  }

  const pagePath = () => window.location.pathname;
  const language = () => document.documentElement.lang || pagePath().split('/')[1] || 'en';
  function send(name, params, done) {
    if (typeof window.gtag !== 'function') return false;
    try {
      window.gtag('event', name, {...params, transport_type: 'beacon',
        ...(done ? {event_callback: done, event_timeout: 180} : {})});
      return true;
    } catch (_) { return false; }
  }
  function search(input) {
    if (input) send('search_submit', {query: input.value.trim(), page_path: pagePath()});
  }
  document.addEventListener('submit', (event) => {
    if (event.target.matches('#finds-search-form, form[role="search"]')) {
      search(event.target.querySelector('input[type="search"], input[name="q"]'));
    }
  }, true);
  // Localized live-filter inputs have no form. Enter explicitly submits a query.
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.isComposing && !event.repeat &&
        event.target.matches('#local-search') && !event.target.closest('form')) search(event.target);
  }, true);
  document.addEventListener('change', (event) => {
    if (event.target.matches('#finds-category, #local-category') && event.target.value) {
      send('category_click', {category: event.target.value.toLowerCase(), page_path: pagePath()});
    } else if (event.target.matches('#finds-marketplace') && event.target.value) {
      send('marketplace_click', {marketplace: event.target.value.toLowerCase(), page_path: pagePath()});
    }
  }, true);

  function click(event) {
    if ((event.type === 'click' && event.button !== 0) || (event.type === 'auxclick' && event.button !== 1)) return;
    const anchor = event.target.closest('a[href]');
    if (!anchor) return;
    let url;
    try { url = new URL(anchor.href, window.location.href); } catch (_) { return; }
    if (!/^https?:$/.test(url.protocol)) return;
    const internal = url.origin === window.location.origin;
    const events = [];
    const add = (name, params) => events.push([name, params]);
    if (anchor.closest('.locale-switcher')) {
      const to = anchor.getAttribute('lang') || url.pathname.split('/')[1];
      if (to && to !== language()) add('language_switch', {from_language: language(), to_language: to});
    } else if (internal) {
      const category = url.pathname.match(/^\/[a-z]{2}\/best-joyagoo-finds\/(.+?)\/$/);
      if (category) add('category_click', {category: category[1], page_path: pagePath()});
      const marketplace = url.pathname.match(/^\/[a-z]{2}\/marketplaces\/(taobao|weidian|1688)\/$/);
      const directory = /^\/[a-z]{2}\/best-joyagoo-finds\/$/.test(url.pathname);
      const marketFilter = directory ? url.searchParams.get('marketplace') : '';
      if (marketplace || marketFilter) add('marketplace_click', {marketplace: (marketplace ? marketplace[1] : marketFilter).toLowerCase(), page_path: pagePath()});
      const categoryFilter = directory ? url.searchParams.get('category') : '';
      if (categoryFilter) add('category_click', {category: categoryFilter.toLowerCase(), page_path: pagePath()});
      const guide = url.pathname.match(/^\/[a-z]{2}\/(joyagoo-spreadsheet|joyagoo-buying-guide|articles\/[^/]+)\/$/);
      if (guide) add('guide_click', {guide_name: guide[1].replace(/^articles\//, ''), page_path: pagePath()});
    }
    const card = anchor.closest('.find-card, .local-product');
    if (card && card.dataset.findId) {
      add('find_card_click', {find_id: card.dataset.findId, title: card.dataset.title,
        category: card.dataset.category, marketplace: card.dataset.marketplace});
    }
    const product = anchor.closest('[data-product-source]');
    if (!internal && product && product.dataset.productFindId) {
      add('external_product_click', {find_id: product.dataset.productFindId,
        source_domain: url.hostname, destination_url: url.href, page_path: pagePath()});
    }
    if (!internal && (url.hostname === 'joyagoo.com' || url.hostname.endsWith('.joyagoo.com'))) {
      const section = anchor.closest('section[id]');
      const location = anchor.dataset.ctaLocation || (anchor.closest('header') ? 'header' :
        anchor.closest('footer') ? 'footer' : card ? 'find_card' : section ? section.id : 'main');
      add('joyagoo_click', {page_path: pagePath(), cta_location: location});
    }
    if (!events.length) return;
    // Preserve new tabs, modifier keys, downloads and middle-click behavior.
    const wait = !internal && !event.defaultPrevented && event.type === 'click' &&
      !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey &&
      !anchor.hasAttribute('download') && (!anchor.target || anchor.target === '_self') &&
      typeof window.gtag === 'function';
    if (!wait) { events.forEach(([name, params]) => send(name, params)); return; }
    event.preventDefault();
    let finished = false;
    let remaining = events.length;
    const navigate = () => {
      if (finished) return;
      finished = true;
      window.location.assign(url.href);
    };
    const timer = window.setTimeout(navigate, 180);
    events.forEach(([name, params]) => {
      let called = false;
      const done = () => {
        if (called) return;
        called = true;
        if (--remaining === 0) { window.clearTimeout(timer); navigate(); }
      };
      if (!send(name, params, done)) done();
    });
  }
  document.addEventListener('click', click, true);
  document.addEventListener('auxclick', click, true);
})();
