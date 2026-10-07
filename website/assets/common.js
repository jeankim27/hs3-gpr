/* Shared helpers for the team website. */
window.HS3 = (function () {
  function mk(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); }

  /* On GitHub Pages (owner.github.io/repo/) work out the repository URL, so edit links need no setup. */
  function repoUrl() {
    var host = location.hostname;
    if (!/\.github\.io$/.test(host)) return null;
    var owner = host.split(".")[0];
    var first = location.pathname.split("/").filter(Boolean)[0];
    var repo = first && !/\.html?$/.test(first) ? first : owner + ".github.io";
    return "https://github.com/" + owner + "/" + repo;
  }

  function wireRepoLinks() {
    var base = repoUrl();
    Array.prototype.forEach.call(document.querySelectorAll("[data-repo-path]"), function (a) {
      if (!base) { a.hidden = true; return; }
      a.href = base + a.getAttribute("data-repo-path");
      a.hidden = false;
    });
  }

  function loadJSON(path) {
    return fetch(path, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(path + " → " + r.status);
      return r.json();
    });
  }

  var GLYPH = {
    hardware: '<svg viewBox="0 0 10 10" aria-hidden="true"><rect x="1" y="1" width="8" height="8" rx="1.5"/></svg>',
    firmware: '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M5 .6 9.4 5 5 9.4.6 5Z"/></svg>',
    software: '<svg viewBox="0 0 10 10" aria-hidden="true"><circle cx="5" cy="5" r="4.2"/></svg>',
    physics: '<svg viewBox="0 0 10 10" aria-hidden="true"><path class="wave" d="M.6 5.4C1.9 2 3.1 2 4.4 5.4S6.9 8.6 8.2 5.2"/></svg>'
  };

  return { mk: mk, clear: clear, repoUrl: repoUrl, wireRepoLinks: wireRepoLinks, loadJSON: loadJSON, GLYPH: GLYPH };
})();
