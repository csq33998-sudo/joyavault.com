/* Category filtering; all example cards remain available without JavaScript. */
(() => {
  'use strict';
  const t = (text, params = {}) => window.ML_I18N ? window.ML_I18N.t(text, params) : text.replace(/\{(\w+)\}/g, (_, name) => params[name]);
  const cards = [...document.querySelectorAll('.accessory-card')];
  const buttons = [...document.querySelectorAll('button[data-category]')];
  const status = document.querySelector('#results-status');
  const empty = document.querySelector('#empty-state');

  function filter(category) {
    let count = 0;
    cards.forEach(card => {
      card.hidden = category !== 'All' && card.dataset.category !== category;
      if (!card.hidden) count++;
    });
    buttons.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.category === category));
    });
    status.textContent = t('{count} of {total} example finds', {count, total: cards.length}) + (category === 'All' ? '' : ' — ' + t(category));
    empty.hidden = count !== 0;
  }

  buttons.forEach(button => {
    button.disabled = false;
    button.addEventListener('click', () => filter(button.dataset.category));
  });
  document.querySelector('#reset-filters').addEventListener('click', () => {
    filter('All');
    buttons[0].focus();
  });
  document.querySelectorAll('.product-link[aria-disabled="true"]').forEach(link => {
    link.addEventListener('click', event => event.preventDefault());
  });

  const menu = document.querySelector('.mobile-menu');
  menu.addEventListener('click', event => {
    if (event.target.closest('a')) menu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
  document.addEventListener('click', event => {
    if (!menu.contains(event.target)) menu.open = false;
  });
  filter('All');
})();
