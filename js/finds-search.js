(() => {
  'use strict';
  document.querySelectorAll('.discovery-page img').forEach((image) => {
    const fallback = () => {
      if (image.dataset.fallback) return;
      image.dataset.fallback = 'true';
      image.src = '/assets/icons/find-image-unavailable.webp';
      image.alt = `Image unavailable: ${image.alt}`;
    };
    image.addEventListener('error', fallback);
    if (image.complete && image.naturalWidth === 0) fallback();
  });
  const input = document.querySelector('#finds-search');
  if (!input) return;
  const grid = document.querySelector('#featured-grid');
  const form = document.querySelector('#finds-search-form');
  const externalSearch = form.hasAttribute('data-external-search');
  let updateExternalLink = () => {};
  if (externalSearch) {
    const link = form.querySelector('[data-external-search-link]');
    const updateLink = () => {
      const destination = new URL(form.action);
      destination.searchParams.set('q', input.value.trim());
      link.href = destination.href;
    };
    input.addEventListener('input', updateLink);
    updateExternalLink = updateLink;
    link.addEventListener('click', (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      form.requestSubmit();
    });
    updateLink();
  }
  const category = document.querySelector('#finds-category');
  const marketplace = document.querySelector('#finds-marketplace');
  const subcategory = document.querySelector('#finds-subcategory');
  const minPrice = document.querySelector('#finds-min-price');
  const maxPrice = document.querySelector('#finds-max-price');
  const brand = document.querySelector('#finds-brand');
  const cards = Array.from(grid.querySelectorAll('[data-find-id]'));
  const status = document.querySelector('#finds-status');
  const empty = document.querySelector('#finds-empty');
  const previous = document.querySelector('#finds-prev');
  const next = document.querySelector('#finds-next');
  const catalog = grid.dataset.mode === 'catalog';
  const pageSize = Number(grid.dataset.pageSize) || (catalog ? 24 : 8);
  const pageStatus = document.querySelector('#finds-page');

  function readUrl() {
    const params = new URLSearchParams(window.location.search);
    input.value = params.get('q') || '';
    updateExternalLink();
    [category, subcategory, marketplace, brand].filter(Boolean).forEach((select) => {
      const value = params.get(select.name) || '';
      select.value = Array.from(select.options).some((option) => option.value === value) ? value : '';
    });
    [minPrice, maxPrice].filter(Boolean).forEach((field) => { field.value = params.get(field.name) || ''; });
    return params.get('page');
  }

  function resultUrl(page = 1) {
    const params = new URLSearchParams();
    if (!externalSearch && input.value.trim()) params.set('q', input.value.trim());
    if (category && category.value) params.set('category', category.value);
    if (marketplace && marketplace.value) params.set('marketplace', marketplace.value);
    if (brand && brand.value) params.set('brand', brand.value);
    [subcategory, minPrice, maxPrice].filter(Boolean).forEach((field) => { if (field.value !== '') params.set(field.name, field.value); });
    if (page > 1) params.set('page', String(page));
    return `${window.location.pathname}${params.size ? `?${params}` : ''}#finds`;
  }

  function render(requestedPage = 1, saveUrl = false) {
    const filters = {query: externalSearch ? '' : input.value, category: category ? category.value : '', marketplace: marketplace ? marketplace.value : '', brand: brand ? brand.value : ''};
    Object.assign(filters, {subcategory: subcategory?.value || '', minPrice: minPrice?.value || '', maxPrice: maxPrice?.value || ''});
    const invalidPrice = (minPrice && !minPrice.validity.valid) || (maxPrice && !maxPrice.validity.valid) || (filters.minPrice !== '' && filters.maxPrice !== '' && Number(filters.minPrice) > Number(filters.maxPrice));
    const matches = cards.filter((card) => !invalidPrice && window.FindsFilter.matches(card.dataset, filters));
    const totalPages = Math.max(1, Math.ceil(matches.length / pageSize));
    const page = Math.min(totalPages, Math.max(1, Math.floor(Number(requestedPage) || 1)));
    const visible = new Set(matches.slice((page - 1) * pageSize, page * pageSize));
    cards.forEach((card) => { card.hidden = !visible.has(card); });
    empty.hidden = matches.length > 0;
    const filtered = Boolean(filters.query.trim() || filters.category || filters.marketplace || filters.brand || filters.subcategory || filters.minPrice !== '' || filters.maxPrice !== '');
    status.textContent = catalog
      ? (matches.length ? `Showing ${(page - 1) * pageSize + 1}–${Math.min(page * pageSize, matches.length)} of ${matches.length} ${filtered ? 'matching' : 'total'} finds.` : 'No finds match these filters.')
      : (filtered ? `Showing ${visible.size} of ${matches.length} matching finds.` : `Showing ${visible.size} featured finds from ${cards.length} records.`);
    if (invalidPrice) status.textContent = 'Enter a valid price range: use non-negative amounts with Min no greater than Max.';
    if (previous && next) {
      previous.hidden = page <= 1 || matches.length === 0;
      next.hidden = page >= totalPages || matches.length === 0;
      previous.href = resultUrl(page - 1);
      next.href = resultUrl(page + 1);
    }
    if (pageStatus) pageStatus.textContent = matches.length ? `Page ${page} of ${totalPages}` : '';
    if (saveUrl) history.replaceState(null, '', resultUrl(page));
  }

  if (!externalSearch) {
    input.addEventListener('input', () => render(1, true));
    input.addEventListener('search', () => render(1, true));
  }
  [category, subcategory, marketplace, brand].filter(Boolean).forEach((select) => select.addEventListener('change', () => render(1, true)));
  [minPrice, maxPrice].filter(Boolean).forEach((field) => field.addEventListener('input', () => render(1, true)));
  category?.addEventListener('change', () => {
    if (!subcategory) return;
    const available = new Set(cards.filter((card) => !category.value || card.dataset.category === category.value).map((card) => card.dataset.subcategory));
    for (const option of subcategory.options) option.disabled = Boolean(option.value && !available.has(option.value));
    if (subcategory.selectedOptions[0]?.disabled) subcategory.value = '';
    render(1, true);
  });
  form.addEventListener('submit', (event) => {
    if (externalSearch) {
      input.value = input.value.trim();
      return;
    }
    event.preventDefault();
    render(1, true);
    document.querySelector('#finds').scrollIntoView({behavior: 'auto', block: 'start'});
  });
  window.addEventListener('popstate', () => render(readUrl()));
  render(readUrl());
})();

