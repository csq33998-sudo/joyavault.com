/* JoyaVault shared interactions — vanilla JavaScript, safe with defer or late loading.
 * Product markup: .product-card[data-category][data-brand], inside .product-grid,
 * .products-grid, #productGrid, or [data-product-grid]. Wrap independent catalogs
 * in [data-product-catalog]. Controls: button[data-category], button[data-brand],
 * button[data-filter] (legacy category); search: [data-product-search] or #searchInput.
 * Optional [data-product-empty], [data-product-count]. Category + brand + search
 * combine with AND; empty / "all" resets one filter. Existing #featured-grid is
 * intentionally managed by finds-search.js, including its pagination.
 * FAQ: native details/summary, or .faq-question button + .faq-answer in .faq-item.
 */
(() => {
  'use strict';
  function init() {
    if (document.documentElement.dataset.joyaMainReady) return;
    document.documentElement.dataset.joyaMainReady = 'true';
    let id = 0;
    function ensureId(element, prefix) {
      if (!element.id) {
        do { element.id = prefix + '-' + (++id); } while (document.getElementById(element.id) !== element);
      }
      return element.id;
    }

    const header = document.querySelector('.site-header');
    if (header) {
      const nav = header.querySelector('.nav') || header;
      const links = header.querySelector('.nav-links');
      let toggle = header.querySelector('[data-menu-toggle], .menu-toggle, .hamburger');
      if (links && !toggle) {
        toggle = document.createElement('button');
        toggle.className = 'menu-toggle';
        toggle.type = 'button';
        toggle.setAttribute('aria-label', 'Toggle navigation');
        toggle.innerHTML = '<span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>';
        nav.insertBefore(toggle, links);
      }
      if (links && toggle) {
        const mobile = window.matchMedia('(max-width: 1024px)');
        const actions = header.querySelector('.nav-actions');
        const regions = [links, actions].filter(Boolean);
        toggle.setAttribute('aria-controls', regions.map(region => ensureId(region, 'site-navigation')).join(' '));
        const setMenu = (open, restoreFocus = false) => {
          header.classList.toggle('is-menu-open', open);
          toggle.setAttribute('aria-expanded', String(open));
          // inert also prevents keyboard focus when the shared CSS is not loaded.
          regions.forEach(region => { region.inert = mobile.matches && !open; });
          if (restoreFocus) toggle.focus();
        };
        header.classList.add('menu-ready');
        setMenu(false);
        toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
        header.addEventListener('keydown', event => {
          if (event.key === 'Escape' && header.classList.contains('is-menu-open')) setMenu(false, true);
        });
        header.addEventListener('click', event => {
          if (mobile.matches && event.target.closest('.nav-links a, .nav-actions a')) setMenu(false);
        });
        document.addEventListener('click', event => {
          if (mobile.matches && !header.contains(event.target) && header.classList.contains('is-menu-open')) {
            setMenu(false, header.contains(document.activeElement));
          }
        });
        mobile.addEventListener('change', () => {
          const focused = document.activeElement;
          setMenu(false, mobile.matches && regions.some(region => region.contains(focused)));
          if (!mobile.matches && focused === toggle) links.querySelector('a')?.focus();
        });
      }
      const updateScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 24);
      updateScroll();
      window.addEventListener('scroll', updateScroll, { passive: true });
      // Keep wrapped navigation from covering the page; don't offset by an open menu.
      const measureHeader = () => {
        if (!header.classList.contains('is-menu-open')) {
          document.documentElement.style.setProperty('--header-height', header.getBoundingClientRect().height + 'px');
        }
      };
      if ('ResizeObserver' in window) new ResizeObserver(measureHeader).observe(header);
      measureHeader();
    }

    // Keep the legacy ML_PRODUCTS / ML_BRANDS renderer and translation support.
    const products = window.ML_PRODUCTS || [];
    const brands = window.ML_BRANDS || [];
    const productGrid = document.querySelector('#productGrid');
    const brandGrid = document.querySelector('#brandGrid');
  function translate(key) {
    return window.ML_I18N ? window.ML_I18N.t(key) : key;
  }

  function escapeText(value) {
    return String(value).replace(/[&<>"']/g, (char) => {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
      }[char];
    });
  }

  function productCard(product) {
    if (!product.url || !/^https:\/\/maisonlooks\.com\/en\/p\/[^/?#]+$/.test(product.url)) return '';
    const haystack = `${product.name} ${product.brand} ${product.category} ${product.note}`;
    const viewUrl = product.url;
    return `
      <a class="product-card" href="${escapeText(viewUrl)}" target="_blank" rel="sponsored nofollow noopener noreferrer" data-search="${escapeText(haystack.toLowerCase())}" data-category="${escapeText(product.category)}" data-brand="${escapeText(product.brand)}">
        <div class="product-image">
          <img src="${escapeText(product.image)}" alt="${escapeText(product.name)}" loading="lazy" width="450" height="563" />
        </div>
        <div class="product-body">
          <div class="product-meta">
            <span>${escapeText(product.brand)}</span>
            <span class="badge">${escapeText(translate(product.category))}</span>
          </div>
          <h3>${escapeText(product.name)}</h3>
          <strong class="product-price">${escapeText(product.price)}</strong>
          <p>${escapeText(translate(product.note))}</p>
          <div class="product-actions">
            <span>${escapeText(translate("view"))}</span>
          </div>
        </div>
      </a>
    `;
  }

  function renderBrands() {
    if (!brandGrid) return;

    brandGrid.innerHTML = brands
      .map((brand) => {
        return `
          <a class="brand-card" href="#finds" data-brand-link="${escapeText(brand.name)}">
            <strong>${escapeText(brand.name)}</strong>
            <p>${escapeText(translate(brand.copy))}</p>
          </a>
        `;
      })
      .join("");
  }


    function renderLegacy() {
      // Never erase pre-rendered HTML when no legacy dataset was supplied.
      if (productGrid && Array.isArray(window.ML_PRODUCTS)) productGrid.innerHTML = products.map(productCard).join('');
      if (Array.isArray(window.ML_BRANDS)) renderBrands();
    }
    renderLegacy();

    const normalize = value => String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
    const controllers = [];
    const roots = new Set();
    document.querySelectorAll('[data-product-grid], #productGrid, .product-grid, .products-grid').forEach(grid => {
      if (grid.id !== 'featured-grid') roots.add(grid.closest('[data-product-catalog]') || document);
    });
    roots.forEach(root => {
      const owned = element => root === document ? !element.closest('[data-product-catalog]') : element.closest('[data-product-catalog]') === root;
      const select = selector => Array.from(root.querySelectorAll(selector)).filter(owned);
      const grids = select('[data-product-grid], #productGrid, .product-grid, .products-grid').filter(grid => grid.id !== 'featured-grid');
      const buttons = select('button[data-filter], button[data-category], button[data-brand]');
      const input = select('[data-product-search], #searchInput')[0];
      const empty = select('[data-product-empty], #emptyState')[0];
      const count = select('[data-product-count]')[0];
      const state = { category: '', brand: '' };
      const valueOf = (button, key) => normalize(button.dataset[key] ?? (key === 'category' ? button.dataset.filter : ''));
      const resetValue = value => value === 'all' ? '' : value;
      const keysOf = button => ['category', 'brand'].filter(key => button.hasAttribute('data-' + key) || (key === 'category' && button.hasAttribute('data-filter')));
      buttons.filter(button => button.matches('.is-active, .active, [aria-pressed="true"]')).forEach(button => {
        keysOf(button).forEach(key => { state[key] = resetValue(valueOf(button, key)); });
      });
      if (count) { count.setAttribute('role', 'status'); count.setAttribute('aria-live', 'polite'); count.setAttribute('aria-atomic', 'true'); }
      if (empty) { empty.setAttribute('role', 'status'); empty.setAttribute('aria-live', 'polite'); }
      const apply = () => {
        const terms = normalize(input?.value).split(/\s+/).filter(Boolean);
        let visible = 0;
        const cards = new Set(grids.flatMap(grid => Array.from(grid.querySelectorAll('.product-card, .find-card'))));
        cards.forEach(card => {
          const haystack = normalize([card.dataset.search, card.dataset.title, card.textContent, card.dataset.category, card.dataset.brand].join(' '));
          const matches = (!state.category || normalize(card.dataset.category) === state.category)
            && (!state.brand || normalize(card.dataset.brand) === state.brand)
            && terms.every(term => haystack.includes(term));
          card.hidden = !matches;
          if (matches) visible++;
        });
        buttons.forEach(button => {
          const active = keysOf(button).every(key => resetValue(valueOf(button, key)) === state[key]);
          button.classList.toggle('is-active', active);
          button.classList.toggle('active', active);
          button.setAttribute('aria-pressed', String(active));
        });
        if (empty) empty.hidden = visible > 0;
        if (count) count.textContent = String(visible);
      };
      buttons.forEach(button => button.addEventListener('click', event => {
        event.preventDefault();
        keysOf(button).forEach(key => { state[key] = resetValue(valueOf(button, key)); });
        apply();
      }));
      input?.addEventListener('input', apply);
      input?.addEventListener('search', apply);
      input?.closest('form')?.addEventListener('submit', event => { event.preventDefault(); apply(); });
      select('[data-brand-link]').forEach(link => link.addEventListener('click', () => {
        state.category = '';
        state.brand = normalize(link.dataset.brandLink);
        if (input) input.value = '';
        apply();
      }));
      controllers.push(apply);
      apply();
    });
    window.addEventListener('ml:languagechange', () => {
      // Brand links keep their event bindings while translated copy is refreshed.
      if (productGrid && Array.isArray(window.ML_PRODUCTS)) productGrid.innerHTML = products.map(productCard).join('');
      brandGrid?.querySelectorAll('[data-brand-link]').forEach(link => {
        const brand = brands.find(item => item.name === link.dataset.brandLink);
        if (brand && link.querySelector('p')) link.querySelector('p').textContent = translate(brand.copy);
      });
      controllers.forEach(apply => apply());
    });

    document.querySelectorAll('.faq-item:not(details)').forEach(item => {
      const button = item.querySelector('button.faq-question, button[data-faq-toggle]');
      const panel = item.querySelector('.faq-answer, [data-faq-panel]');
      if (!button || !panel) return;
      button.type = 'button';
      button.setAttribute('aria-controls', ensureId(panel, 'faq-answer'));
      panel.setAttribute('aria-labelledby', ensureId(button, 'faq-question'));
      const setOpen = open => {
        button.setAttribute('aria-expanded', String(open));
        panel.hidden = !open;
        item.classList.toggle('is-open', open);
      };
      setOpen(button.getAttribute('aria-expanded') === 'true' || item.classList.contains('is-open'));
      button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
    });
    // Native details already handles mouse/keyboard. Opt in to one-open-at-a-time
    // with data-faq-single on a wrapper; never cancel the summary's native action.
    document.querySelectorAll('[data-faq-single] details').forEach(details => {
      details.addEventListener('toggle', () => {
        if (!details.open) return;
        const group = details.closest('[data-faq-single]');
        group.querySelectorAll('details[open]').forEach(other => {
          if (other !== details && other.closest('[data-faq-single]') === group) other.open = false;
        });
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
