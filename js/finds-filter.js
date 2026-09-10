/* Shared, DOM-free search/filter rules; also usable in Node validation tests. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.FindsFilter = factory();
})(typeof window !== 'undefined' ? window : this, function () {
  const normalize = (value) => String(value || '').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').trim();
  function matches(record, filters) {
    const terms = normalize(filters.query).split(/\s+/).filter(Boolean);
    const hasMin = filters.minPrice !== undefined && filters.minPrice !== '';
    const hasMax = filters.maxPrice !== undefined && filters.maxPrice !== '';
    const price = Number(record.priceCny);
    const min = Number(filters.minPrice), max = Number(filters.maxPrice);
    if ((hasMin && (!Number.isFinite(min) || min < 0)) || (hasMax && (!Number.isFinite(max) || max < 0)) || (hasMin && hasMax && min > max)) return false;
    return (!filters.category || record.category === filters.category)
      && (!filters.subcategory || record.subcategory === filters.subcategory)
      && (!hasMin || (Number.isFinite(price) && price >= min))
      && (!hasMax || (Number.isFinite(price) && price <= max))
      && (!filters.marketplace || record.marketplace === filters.marketplace)
      && (!filters.brand || record.brand === filters.brand || String(record.styles || '').split('|').includes(filters.brand))
      && terms.every((term) => normalize(record.search).includes(term));
  }
  return { matches, normalize };
});
