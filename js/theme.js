(function () {
  const STORAGE_KEY = "ml_theme";
  const root = document.documentElement;

  function getTheme() {
    return localStorage.getItem(STORAGE_KEY) || "light";
  }

  function applyTheme(theme) {
    const dark = theme === "dark";
    root.dataset.theme = dark ? "dark" : "light";
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.setAttribute("aria-pressed", String(dark));
    });
    document.querySelectorAll("[data-theme-label]").forEach((label) => {
      const key = dark ? "Day" : "Night";
      label.dataset.i18nKey = key;
      label.textContent = window.ML_I18N ? window.ML_I18N.t(key) : key;
    });
  }

  function setTheme(theme) {
    localStorage.setItem(STORAGE_KEY, theme);
    applyTheme(theme);
  }

  applyTheme(getTheme());

  document.addEventListener("click", (event) => {
    const toggle = event.target.closest("[data-theme-toggle]");
    if (!toggle) return;
    setTheme(getTheme() === "dark" ? "light" : "dark");
  });
})();
