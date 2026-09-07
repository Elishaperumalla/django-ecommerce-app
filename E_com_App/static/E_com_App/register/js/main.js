
(() => {
  const form = document.querySelector('.navbar-search');
  if (!form) return;

  const productsResults = document.querySelector('#products-results');
  // Only do dynamic updates on the Products page (where results exist).
  if (!productsResults) return;

  const categorySelect = form.querySelector('select[name="category"]');

  async function refreshProducts(pushUrl = true) {
    const endpoint = (window.location.pathname === HOME_URL) ? window.location.pathname : form.action;
    const url = new URL(endpoint, window.location.origin);
    const data = new FormData(form);
    for (const [key, value] of data.entries()) {
      if (value && String(value).trim() !== '') url.searchParams.set(key, value);
    }
    url.searchParams.set('partial', '1');

    const res = await fetch(url.toString(), { credentials: 'same-origin' });
    if (!res.ok) return;

    const html = await res.text();
    const currentResults = document.querySelector('#products-results');
    if (currentResults) currentResults.outerHTML = html;

    if (pushUrl) {
      url.searchParams.delete('partial');
      window.history.replaceState({}, '', url.toString());
    }
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    refreshProducts(true);
  });

  if (categorySelect) {
    categorySelect.addEventListener('change', () => refreshProducts(true));
  }
})();

(() => {
  const menu = document.querySelector('.user-menu');
  if (!menu) return;

  const trigger = menu.querySelector('.user-menu-trigger');
  const panel = menu.querySelector('.user-menu-panel');
  if (!trigger || !panel) return;

  function closeMenu() {
    panel.classList.remove('open');
    trigger.setAttribute('aria-expanded', 'false');
  }

  trigger.addEventListener('click', () => {
    const willOpen = !panel.classList.contains('open');
    if (willOpen) {
      panel.classList.add('open');
      trigger.setAttribute('aria-expanded', 'true');
    } else {
      closeMenu();
    }
  });

  document.addEventListener('click', (event) => {
    if (!menu.contains(event.target)) closeMenu();
  });
})();

