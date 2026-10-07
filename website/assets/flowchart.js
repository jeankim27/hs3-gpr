/* Draws the flowchart page from data/flowchart.json (built from website/flowchart.yaml). */
(function () {
  var mk = HS3.mk, clear = HS3.clear, GLYPH = HS3.GLYPH;
  var ITEMS = {}, ORDER = [];

  var ARROW = '<svg viewBox="0 0 20 12"><path d="M1 6h16M12.5 1.5 17.5 6l-5 4.5"/></svg>';
  var DOWN = '<svg class="link-arrow" viewBox="0 0 12 28" aria-hidden="true"><path d="M6 1v24M1.5 20.5 6 25l4.5-4.5"/></svg>';
  var UP = '<svg class="link-arrow" viewBox="0 0 12 28" aria-hidden="true"><path d="M6 27V3M1.5 7.5 6 3l4.5 4.5"/></svg>';

  function kindEl(kind, label) {
    var k = mk("span", "kind");
    k.innerHTML = GLYPH[kind] || "";
    k.appendChild(mk("span", null, label || kind));
    return k;
  }

  function stepButton(step) {
    var b = mk("button", "node" + (step.kind === "physics" ? " phy" : ""));
    b.type = "button";
    b.id = "step-" + step.n;
    b.setAttribute("data-open", step.id);
    b.setAttribute("data-kind", step.kind);
    if (step.snr) b.setAttribute("data-snr", "");
    var top = mk("span", "node-top");
    top.appendChild(mk("span", "n", String(step.n)));
    var badges = mk("span", "badges");
    (step.badges || []).forEach(function (t) { badges.appendChild(mk("span", "badge", t)); });
    top.appendChild(badges);
    b.appendChild(top);
    b.appendChild(mk("span", "t", step.title));
    b.appendChild(mk("span", "d", step.summary));
    var meta = mk("span", "meta");
    meta.appendChild(kindEl(step.kind, step.label));
    if (step.uses && step.uses.length) meta.appendChild(mk("span", "uses", "uses " + step.uses.join(" · ")));
    b.appendChild(meta);
    return b;
  }

  function renderMasthead(d) {
    document.getElementById("eyebrow").textContent = d.eyebrow || "";
    document.getElementById("title").textContent = d.title || "";
    document.getElementById("lede").textContent = d.lede || "";
    var one = document.getElementById("oneline");
    clear(one);
    one.appendChild(mk("b", null, "In one line"));
    one.appendChild(document.createTextNode(d.one_line || ""));
    var chips = document.getElementById("chips");
    clear(chips);
    Object.keys(d.assumptions || {}).forEach(function (k) {
      var li = mk("li", null, k + " ");
      li.appendChild(mk("b", null, d.assumptions[k]));
      chips.appendChild(li);
    });
  }

  function renderSupport(d) {
    var box = document.getElementById("helpers");
    clear(box);
    d.support.forEach(function (s) {
      ITEMS[s.id] = { group: "Support subsystem", loc: "Spacecraft", title: s.title, kind: s.label, lead: s.lead || s.summary, details: s.details, feeds: s.feeds };
      var b = mk("button", "helper");
      b.type = "button";
      b.setAttribute("data-open", s.id);
      b.setAttribute("data-kind", s.kind);
      b.setAttribute("data-feeds", (s.feeds || []).join(" "));
      b.appendChild(mk("span", "t", s.title));
      b.appendChild(mk("span", "d", s.summary));
      var meta = mk("span", "meta");
      meta.appendChild(kindEl(s.kind, s.label));
      meta.appendChild(mk("span", "uses", s.feeds && s.feeds.length ? "feeds " + s.feeds.join(" · ") : "feeds —"));
      b.appendChild(meta);
      box.appendChild(b);
    });
  }

  function renderBands(d) {
    var root = document.getElementById("bands");
    clear(root);
    d.stages.forEach(function (stage, i) {
      var sec = mk("section", "band");
      sec.setAttribute("data-place", stage.place);
      var head = mk("header", "band-label");
      head.appendChild(mk("span", "loc", stage.place_label));
      var h = mk("h3", "stage", stage.name);
      head.appendChild(h);
      sec.appendChild(head);
      var body = mk("div", "band-body");
      var row = mk("div", "nodes" + (stage.steps.length === 1 ? " single" : ""));
      stage.steps.forEach(function (step, j) {
        ITEMS[step.id] = { num: step.n, loc: stage.place_label + " · " + stage.name, title: step.title, kind: step.label, lead: step.lead || step.summary, details: step.details };
        ORDER.push(step.id);
        if (j > 0) { var a = mk("span", "arr"); a.setAttribute("aria-hidden", "true"); a.innerHTML = ARROW; row.appendChild(a); }
        row.appendChild(stepButton(step));
      });
      body.appendChild(row);
      if (stage.side_path) {
        var sp = stage.side_path;
        ITEMS[sp.id] = { group: "Side path", loc: stage.place_label + " · " + stage.name, title: sp.title, kind: sp.label, lead: sp.lead || sp.summary, details: sp.details };
        var br = mk("button", "branch");
        br.type = "button";
        br.setAttribute("data-open", sp.id);
        br.setAttribute("data-kind", sp.kind);
        br.appendChild(mk("span", "branch-mark", "↳"));
        var txt = mk("span", "branch-text");
        txt.appendChild(mk("b", null, sp.title + ". "));
        txt.appendChild(document.createTextNode(sp.summary));
        br.appendChild(txt);
        br.appendChild(kindEl(sp.kind, sp.label));
        body.appendChild(br);
      }
      sec.appendChild(body);
      root.appendChild(sec);
      var last = i === d.stages.length - 1;
      var link = mk("div", "link" + (last ? " loop" : ""));
      link.innerHTML = last ? UP : DOWN;
      link.appendChild(mk("span", null, last ? (d.loop_label || "") : (stage.arrow || "")));
      root.appendChild(link);
    });
  }

  /* ---------- detail panel ---------- */
  var dlg, inner, opener = null, current = null;
  function render(id) {
    var d = ITEMS[id]; if (!d) return; current = id;
    document.getElementById("dt-step").textContent = d.num ? "Step " + d.num : d.group;
    document.getElementById("dt-loc").textContent = d.loc;
    document.getElementById("dt-title").textContent = d.title;
    document.getElementById("dt-kind").textContent = d.kind || "";
    document.getElementById("dt-lead").textContent = d.lead || "";
    var body = document.getElementById("dt-body"); clear(body);
    Object.keys(d.details || {}).forEach(function (label) {
      var sec = mk("section", "dt-sec"); sec.appendChild(mk("h3", null, label));
      var ul = mk("ul");
      (d.details[label] || []).forEach(function (t) { ul.appendChild(mk("li", null, t)); });
      sec.appendChild(ul); body.appendChild(sec);
    });
    if (d.feeds && d.feeds.length) {
      var sec = mk("section", "dt-sec"); sec.appendChild(mk("h3", null, "Feeds steps"));
      var rowEl = mk("div", "dt-feeds");
      d.feeds.forEach(function (n) {
        var b = mk("button", "btn btn-sm", n + " · " + ITEMS[String(n)].title); b.type = "button";
        b.addEventListener("click", function () { render(String(n)); });
        rowEl.appendChild(b);
      });
      sec.appendChild(rowEl); body.appendChild(sec);
    }
    var i = ORDER.indexOf(id);
    document.getElementById("dt-nav").hidden = i < 0;
    if (i >= 0) {
      document.getElementById("dt-prev").disabled = i === 0;
      document.getElementById("dt-next").disabled = i === ORDER.length - 1;
      document.getElementById("dt-pos").textContent = (i + 1) + " of " + ORDER.length;
    }
    inner.scrollTop = 0;
  }
  function open(id, from) {
    opener = from || null; render(id);
    if (!dlg.open) { if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", ""); }
  }
  function close() { if (typeof dlg.close === "function") dlg.close(); else { dlg.removeAttribute("open"); restore(); } }
  function restore() { if (opener && document.body.contains(opener)) opener.focus(); }
  function step(delta) { var i = ORDER.indexOf(current) + delta; if (i >= 0 && i < ORDER.length) render(ORDER[i]); }

  function wire() {
    dlg = document.getElementById("detail");
    inner = dlg.querySelector(".drawer-inner");
    dlg.addEventListener("close", restore);
    dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); });
    document.getElementById("dt-close").addEventListener("click", close);
    document.getElementById("dt-prev").addEventListener("click", function () { step(-1); });
    document.getElementById("dt-next").addEventListener("click", function () { step(1); });
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-open]");
      if (b) open(b.getAttribute("data-open"), b);
    });
    document.getElementById("walk").addEventListener("click", function (e) { open(ORDER[0], e.currentTarget); });

    var fbtns = Array.prototype.slice.call(document.querySelectorAll(".fbtn"));
    fbtns.forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-f");
        Array.prototype.forEach.call(document.querySelectorAll(".flow [data-kind]"), function (n) {
          var on = f === "all" || (f === "snr" ? n.hasAttribute("data-snr") : n.getAttribute("data-kind") === f);
          n.classList.toggle("dim", !on);
        });
        fbtns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      });
    });

    Array.prototype.forEach.call(document.querySelectorAll(".helper"), function (h) {
      var feeds = (h.getAttribute("data-feeds") || "").split(" ").filter(Boolean);
      function on() { feeds.forEach(function (n) { var el = document.getElementById("step-" + n); if (el) el.classList.add("fed"); }); }
      function off() { Array.prototype.forEach.call(document.querySelectorAll(".node.fed"), function (el) { el.classList.remove("fed"); }); }
      h.addEventListener("pointerenter", on); h.addEventListener("pointerleave", off);
      h.addEventListener("focus", on); h.addEventListener("blur", off);
    });
  }

  HS3.wireRepoLinks();
  HS3.loadJSON("data/flowchart.json").then(function (d) {
    renderMasthead(d);
    renderSupport(d);
    renderBands(d);
    document.getElementById("flow-loading").hidden = true;
    wire();
  }).catch(function (err) {
    document.getElementById("flow-loading").textContent =
      "Could not load the flowchart data (" + err.message + "). Build the site with: python tools/build_site.py";
  });
})();
