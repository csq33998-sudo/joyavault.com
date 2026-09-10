/* Locale belongs to the URL. This compatibility helper never rewrites page text. */
(() => {
  const getLanguage = () => document.documentElement.lang || 'en';
  const setLanguage = code => {
    const links = [...document.querySelectorAll('.locale-options a')];
    const target = links.find(link => link.lang === code);
    if (target) window.location.assign(target.href);
  };
  window.ML_I18N = { t: value => value, getLanguage, setLanguage, applyLanguage: () => {} };
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
  });
})();
