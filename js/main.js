(function () {
  const products = window.ML_PRODUCTS || [];
  const brands = window.ML_BRANDS || [];

  const productGrid = document.querySelector("#productGrid");
  const brandGrid = document.querySelector("#brandGrid");
  const searchInput = document.querySelector("#searchInput");
  const emptyState = document.querySelector("#emptyState");
  const filterButtons = Array.from(document.querySelectorAll("[data-filter]"));

  let activeFilter = "all";
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

  function categoryUrl(category) {
    const query = String(category).trim();
    const params = new URLSearchParams({ q: query });
    return `https://streetstyle.maisonlooks.com/en/search?${params.toString()}`;
  }

  function productCard(product) {
    const haystack = `${product.name} ${product.brand} ${product.category} ${product.note}`;
    const viewUrl = product.url || categoryUrl(product.category);
    return `
      <a class="product-card" href="${escapeText(viewUrl)}" target="_blank" rel="noopener" data-search="${escapeText(haystack.toLowerCase())}" data-category="${escapeText(product.category)}">
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

  function renderProducts() {
    if (!productGrid) return;

    const query = (searchInput && searchInput.value ? searchInput.value : "").trim().toLowerCase();
    const filtered = products.filter((product) => {
      const matchesFilter = activeFilter === "all" || product.category === activeFilter;
      const searchable = `${product.name} ${product.brand} ${product.category} ${product.note}`.toLowerCase();
      return matchesFilter && (!query || searchable.includes(query));
    });

    productGrid.innerHTML = filtered.map(productCard).join("");
    if (emptyState) {
      emptyState.hidden = filtered.length > 0;
    }
  }

  function renderBrands() {
    if (!brandGrid) return;

    brandGrid.innerHTML = brands
      .map((brand) => {
        return `
          <button class="brand-card" type="button" data-brand-link="${escapeText(brand.name)}">
            <strong>${escapeText(brand.name)}</strong>
            <p>${escapeText(translate(brand.copy))}</p>
          </button>
        `;
      })
      .join("");
  }

  function setFilter(value) {
    activeFilter = value;
    filterButtons.forEach((button) => {
      button.classList.toggle("is-active", button.dataset.filter === value);
    });
    renderProducts();
  }

  renderBrands();
  renderProducts();

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => setFilter(button.dataset.filter));
  });

  if (searchInput) {
    searchInput.addEventListener("input", renderProducts);
  }

  window.addEventListener("ml:languagechange", () => {
    renderBrands();
    renderProducts();
  });

  document.addEventListener("click", (event) => {
    const brandLink = event.target.closest("[data-brand-link]");
    if (brandLink && searchInput) {
      searchInput.value = brandLink.dataset.brandLink;
      setFilter("all");
      productGrid.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
})();
