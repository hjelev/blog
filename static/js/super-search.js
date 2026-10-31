/*  Super Search
    Author: Kushagra Gour (http://kushagragour.in)
    MIT Licensed
    Reworked to read a JSON index (/search.json) instead of an RSS sitemap.
*/

(function () {
    var searchInputEl = document.querySelector('#js-search__input'),
        searchResultsEl = document.querySelector('#js-search__results'),
        lastSearchResultHash = '',
        posts = [],
        indexRequested = false;

    if (!searchInputEl || !searchResultsEl) return;

    // Fetch the index lazily, the first time the search box is used
    function loadIndex() {
        if (indexRequested) return;
        indexRequested = true;
        fetch('/search.json')
            .then(function (res) {
                if (!res.ok) throw new Error(res.status);
                return res.json();
            })
            .then(function (data) {
                posts = data;
                if (searchInputEl.value) runSearch();
            })
            .catch(function () { indexRequested = false; });
    }

    function escapeHtml(s) {
        return (s + '').replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    function hideResults() {
        lastSearchResultHash = '';
        searchResultsEl.classList.add('is-hidden');
    }

    function runSearch() {
        var query = (searchInputEl.value + '').trim().toLowerCase();
        if (query.length < 3) return hideResults();

        // Title matches first, then category, then body text
        var scored = posts.map(function (post) {
            var score = 0;
            if (post.title.toLowerCase().indexOf(query) !== -1) score = 3;
            else if (post.categories.toLowerCase().indexOf(query) !== -1) score = 2;
            else if (post.content.toLowerCase().indexOf(query) !== -1) score = 1;
            return { post: post, score: score };
        }).filter(function (r) { return r.score > 0; });
        scored.sort(function (a, b) { return b.score - a.score; });

        if (!scored.length) return hideResults();

        var currentResultHash = scored.map(function (r) { return r.post.url; }).join('|');
        if (currentResultHash !== lastSearchResultHash) {
            searchResultsEl.innerHTML = scored.slice(0, 10).map(function (r) {
                return '<li><a href="' + escapeHtml(r.post.url) + '">' + escapeHtml(r.post.title) +
                    '<span class="search__result-date">' + escapeHtml(r.post.date) + '</span></a></li>';
            }).join('');
        }
        searchResultsEl.classList.remove('is-hidden');
        lastSearchResultHash = currentResultHash;
    }

    searchInputEl.addEventListener('input', function () {
        loadIndex();
        runSearch();
    });

    // Esc clears the box; "/" focuses it from anywhere on the page
    window.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && document.activeElement === searchInputEl) {
            searchInputEl.value = '';
            hideResults();
            searchInputEl.blur();
        } else if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName) &&
                   !document.activeElement.isContentEditable) {
            e.preventDefault();
            searchInputEl.focus();
        }
    });

    // Close results when clicking elsewhere
    document.addEventListener('click', function (e) {
        if (!e.target.closest('#js-search')) searchResultsEl.classList.add('is-hidden');
    });
    searchInputEl.addEventListener('focus', function () {
        loadIndex();
        if (searchResultsEl.innerHTML && searchInputEl.value.trim().length >= 3) runSearch();
    });
})();
