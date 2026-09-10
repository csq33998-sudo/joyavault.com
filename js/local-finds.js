/* All cards remain visible without JavaScript. Labels come from the page locale. */
(() => {
  const input = document.querySelector('#local-search');
  if (!input) return;
  const category = document.querySelector('#local-category');
  const status = document.querySelector('#local-results');
  const cards = [...document.querySelectorAll('#local-products .local-product')];
  const normalize = text => text.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const apply = () => {
    const terms = normalize(input.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      card.hidden = !((!category.value || category.value === card.dataset.category) && terms.every(term => normalize(card.dataset.search).includes(term)));
      if (!card.hidden) count++;
    }
    status.textContent = count ? status.dataset.label + ': ' + count : status.dataset.empty;
  };
  input.addEventListener('input', apply);
  category.addEventListener('change', apply);
})();
