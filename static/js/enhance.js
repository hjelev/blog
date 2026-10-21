(function () {
  var article = document.querySelector('.post.prose');

  /* ---- Copy buttons on code blocks ------------------------------------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy') ? resolve() : reject(); } catch (e) { reject(e); }
      document.body.removeChild(ta);
    });
  }

  document.querySelectorAll('.prose pre').forEach(function (pre) {
    // Rouge nests <pre> inside .highlight; only decorate the outermost wrapper once.
    if (pre.parentElement.closest('.codeblock')) return;

    var wrap = document.createElement('div');
    wrap.className = 'codeblock';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'codeblock__copy';
    btn.textContent = 'copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    wrap.appendChild(btn);

    btn.addEventListener('click', function () {
      var code = pre.querySelector('code') || pre;
      copyText(code.innerText.replace(/\n$/, '')).then(function () {
        btn.textContent = 'copied';
        btn.classList.add('is-done');
      }, function () {
        btn.textContent = 'error';
      }).then(function () {
        setTimeout(function () {
          btn.textContent = 'copy';
          btn.classList.remove('is-done');
        }, 1600);
      });
    });
  });

  /* ---- "On this page" table of contents (wide screens only) ------------ */
  if (!article) return;
  var headings = Array.prototype.slice.call(article.querySelectorAll('h2, h3'));
  if (headings.length < 3) return;

  var used = {};
  function slugify(text) {
    var base = text.toLowerCase().trim().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-') || 'section';
    var slug = base, n = 2;
    while (used[slug] || document.getElementById(slug)) slug = base + '-' + n++;
    used[slug] = true;
    return slug;
  }

  var toc = document.createElement('nav');
  toc.className = 'toc';
  toc.setAttribute('aria-label', 'On this page');
  var inner = document.createElement('div');
  inner.className = 'toc__inner';
  inner.innerHTML = '<div class="toc__title">on this page</div>';
  var list = document.createElement('ol');
  list.className = 'toc__list';

  var links = {};
  headings.forEach(function (h) {
    if (!h.id) h.id = slugify(h.textContent);
    var li = document.createElement('li');
    li.className = 'toc__item toc__item--' + h.tagName.toLowerCase();
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;
    li.appendChild(a);
    list.appendChild(li);
    links[h.id] = a;
  });

  inner.appendChild(list);
  toc.appendChild(inner);
  var content = document.getElementById('content');
  content.appendChild(toc);
  content.classList.add('has-toc');

  // Highlight the section currently being read.
  if ('IntersectionObserver' in window) {
    var current;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        if (current) current.classList.remove('is-active');
        current = links[entry.target.id];
        if (current) current.classList.add('is-active');
      });
    }, { rootMargin: '0px 0px -70% 0px' });
    headings.forEach(function (h) { observer.observe(h); });
  }
})();
