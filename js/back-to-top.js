(() => {
  const control = document.querySelector('[data-back-to-top]');
  if (!control) return;
  let scheduled = false;
  const update = () => {
    control.hidden = window.scrollY < 100;
    scheduled = false;
  };
  window.addEventListener('scroll', () => {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(update);
    }
  }, { passive: true });
  window.addEventListener('pageshow', update);
  control.addEventListener('click', (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const heading = document.querySelector('h1');
    if (heading) {
      const previous = heading.getAttribute('tabindex');
      heading.setAttribute('tabindex', '-1');
      heading.focus({ preventScroll: true });
      heading.addEventListener('blur', () => {
        if (previous === null) heading.removeAttribute('tabindex');
        else heading.setAttribute('tabindex', previous);
      }, { once: true });
    }
    window.scrollTo({ top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  });
  update();
})();
