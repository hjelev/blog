(function () {
  var root = document.documentElement;

  function effectiveTheme() {
    var attr = root.getAttribute('data-theme');
    if (attr === 'dark' || attr === 'light') return attr;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function sync() {
    var t = effectiveTheme();
    root.setAttribute('data-effective', t);
    var btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.setAttribute('aria-label', 'Switch to ' + (t === 'dark' ? 'light' : 'dark') + ' theme');
    }
  }

  sync();

  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = effectiveTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      sync();
    });
  }

  // Follow system changes when the user hasn't made an explicit choice.
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  (mq.addEventListener ? mq.addEventListener.bind(mq, 'change') : mq.addListener.bind(mq))(function () {
    var stored;
    try { stored = localStorage.getItem('theme'); } catch (e) {}
    if (stored !== 'dark' && stored !== 'light') sync();
  });

  // Mobile navigation drawer
  var navToggle = document.getElementById('nav-toggle');
  var sidebar = document.getElementById('sidebar');
  if (navToggle && sidebar) {
    navToggle.addEventListener('click', function () {
      var open = sidebar.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
    sidebar.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        sidebar.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
})();
