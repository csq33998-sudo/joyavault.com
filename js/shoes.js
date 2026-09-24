/* Framework-free footwear filters. The static HTML remains readable without JS. */
(() => {
  'use strict';
  const t = (text, params = {}) => window.ML_I18N ? window.ML_I18N.t(text, params) : text.replace(/\{(\w+)\}/g, (_, name) => params[name]);
  const cards = [...document.querySelectorAll('.shoe-card')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const namedBrands = new Set(buttons.filter(button => button.dataset.filter === 'brand')
    .map(button => button.dataset.value).filter(value => value !== 'All' && value !== 'Other'));
  const state = { brand: 'All', type: 'All' };
  const status = document.querySelector('#results-status');
  const empty = document.querySelector('#empty-state');

  function render() {
    let count = 0;
    cards.forEach(card => {
      const matchesBrand = state.brand === 'All'
        || (state.brand === 'Other' ? !namedBrands.has(card.dataset.brand) : card.dataset.brand === state.brand);
      const matchesType = state.type === 'All' || card.dataset.type === state.type;
      card.hidden = !(matchesBrand && matchesType);
      if (!card.hidden) count++;
    });
    buttons.forEach(button => {
      button.setAttribute('aria-pressed', String(state[button.dataset.filter] === button.dataset.value));
    });
    const selection = [state.brand, state.type].filter(value => value !== 'All');
    status.textContent = t('{count} of {total} finds', {count, total: cards.length}) + (selection.length ? ' — ' + selection.map(value => t(value)).join(' / ') : '');
    empty.hidden = count !== 0;
  }

  buttons.forEach(button => {
    button.disabled = false;
    button.addEventListener('click', () => {
      state[button.dataset.filter] = button.dataset.value;
      render();
    });
  });
  document.querySelector('#reset-filters').addEventListener('click', () => {
    state.brand = 'All';
    state.type = 'All';
    render();
    buttons[0].focus();
  });

  // Replace href, remove aria-disabled/tabindex, and remove the placeholder note
  // together when actual Joyagoo product links become available.
  document.querySelectorAll('.product-link[aria-disabled="true"]').forEach(link => {
    link.addEventListener('click', event => event.preventDefault());
  });

  const menu = document.querySelector('.mobile-menu');
  menu.addEventListener('click', event => { if (event.target.closest('a')) menu.open = false; });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
  document.addEventListener('click', event => { if (!menu.contains(event.target)) menu.open = false; });
  render();
})();
