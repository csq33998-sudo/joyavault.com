/* Static translated HTML is primary; this dictionary handles dynamic UI only. */
(() => {
  const translate = (value, params = {}) => {
    const template = window.ML_TRANSLATIONS?.[value] || value;
    return template.replace(/\{(\w+)\}/g, (match, name) => Object.hasOwn(params, name) ? String(params[name]) : match);
  };
  const getLanguage = () => document.documentElement.lang || 'en';
  const setLanguage = code => {
    const links = [...document.querySelectorAll('.locale-options a')];
    const target = links.find(link => link.lang === code);
    if (target) window.location.assign(target.href);
  };
  window.ML_I18N = { t: translate, getLanguage, setLanguage, applyLanguage: () => {} };
  // Retain search/filter state and anchor when following a corresponding page.
  const updateLinks = () => document.querySelectorAll('.locale-options a').forEach(link => {
    const url = new URL(link.href, window.location.href);
    url.search = window.location.search;
    url.hash = window.location.hash;
    link.href = url.href;
  });
  document.addEventListener('DOMContentLoaded', updateLinks);
  document.addEventListener('click', event => {
    if (event.target.closest('.locale-switcher')) updateLinks();
  }, true);
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('.locale-switcher[open]').forEach(menu => {
      menu.open = false;
      menu.querySelector('summary').focus();
    });
  });
  document.addEventListener('click', event => {
    document.querySelectorAll('.locale-switcher[open]').forEach(menu => {
      if (!menu.contains(event.target)) menu.open = false;
    });
  }, true);
})();
