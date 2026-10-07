/* Draws the Variables & budget page from data/register.json and data/budget.json. */
(function () {
  var mk = HS3.mk, clear = HS3.clear;
  var STATUS_LABEL = { TBD: "TBD", assumed: "Assumed", derived: "Derived", frozen: "Frozen" };
  var state = { quarter: "", status: "", owner: "", q: "" };
  var REG = null;

  function pill(status) {
    var s = mk("span", "pill");
    var dot = mk("i", "st-" + status);
    dot.setAttribute("aria-hidden", "true");
    s.appendChild(dot);
    s.appendChild(document.createTextNode(STATUS_LABEL[status] || status));
    return s;
  }

  function renderProgress(reg) {
    var box = document.getElementById("progress"); clear(box);
    reg.quarters.forEach(function (q) {
      var vars = reg.variables.filter(function (v) { return v.quarter === q; });
      var counts = {}; reg.statuses.forEach(function (s) { counts[s] = 0; });
      vars.forEach(function (v) { counts[v.status] = (counts[v.status] || 0) + 1; });
      var pinned = (counts.derived || 0) + (counts.frozen || 0);
      var card = mk("div", "pcard");
      card.appendChild(mk("h3", null, q));
      card.appendChild(mk("span", "sub", pinned + " of " + vars.length + " pinned down · " + (counts.TBD || 0) + " still TBD"));
      var bar = mk("div", "bar");
      bar.setAttribute("role", "img");
      bar.setAttribute("aria-label", q + ": " + reg.statuses.map(function (s) { return counts[s] + " " + s; }).join(", "));
      reg.statuses.forEach(function (s) {
        if (!counts[s]) return;
        var seg = mk("span", "st-" + s);
        seg.style.flex = String(counts[s]);
        seg.title = counts[s] + " " + s;
        bar.appendChild(seg);
      });
      card.appendChild(bar);
      var nums = mk("div", "legend");
      reg.statuses.forEach(function (s) { nums.appendChild(mk("span", null, counts[s] + " " + s)); });
      card.appendChild(nums);
      box.appendChild(card);
    });
    var legend = document.getElementById("legend"); clear(legend);
    var text = { TBD: "TBD: no value yet", assumed: "Assumed: placeholder, needs a source", derived: "Derived: backed by an analysis", frozen: "Frozen: agreed baseline" };
    reg.statuses.forEach(function (s) {
      var item = mk("span"); var dot = mk("i", "st-" + s); dot.setAttribute("aria-hidden", "true");
      item.appendChild(dot); item.appendChild(document.createTextNode(text[s])); legend.appendChild(item);
    });
  }

  function renderControls(reg) {
    var qf = document.getElementById("qfilter"); clear(qf);
    ["", "Q1", "Q2", "Q3"].forEach(function (q) {
      var b = mk("button", "fbtn", q || "All quarters"); b.type = "button";
      b.setAttribute("aria-pressed", String(q === state.quarter));
      b.addEventListener("click", function () {
        state.quarter = q;
        Array.prototype.forEach.call(qf.children, function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        renderTable();
      });
      qf.appendChild(b);
    });
    var sf = document.getElementById("status-filter");
    reg.statuses.forEach(function (s) { var o = mk("option", null, STATUS_LABEL[s]); o.value = s; sf.appendChild(o); });
    sf.addEventListener("change", function () { state.status = sf.value; renderTable(); });
    var of = document.getElementById("owner-filter");
    var owners = Array.from(new Set(reg.variables.map(function (v) { return v.owner || "unassigned"; }))).sort();
    owners.forEach(function (o) { var opt = mk("option", null, o); opt.value = o; of.appendChild(opt); });
    of.addEventListener("change", function () { state.owner = of.value; renderTable(); });
    var search = document.getElementById("search");
    search.addEventListener("input", function () { state.q = search.value.trim().toLowerCase(); renderTable(); });
  }

  function renderTable() {
    var body = document.getElementById("var-rows"); clear(body);
    var rows = REG.variables.filter(function (v) {
      if (state.quarter && v.quarter !== state.quarter) return false;
      if (state.status && v.status !== state.status) return false;
      if (state.owner && (v.owner || "unassigned") !== state.owner) return false;
      if (state.q) {
        var hay = [v.key, v.name, v.source, v.symbol, v.group, v.drives].join(" ").toLowerCase();
        if (hay.indexOf(state.q) < 0) return false;
      }
      return true;
    });
    document.getElementById("count").textContent = rows.length + " of " + REG.variables.length + " variables";
    var group = null;
    rows.forEach(function (v) {
      if (v.group !== group) {
        group = v.group;
        var gr = mk("tr", "group-row"); var gc = mk("td", null, group); gc.colSpan = 7; gr.appendChild(gc); body.appendChild(gr);
      }
      var tr = mk("tr");
      var name = mk("td");
      name.appendChild(mk("span", "var-name", v.name));
      name.appendChild(mk("span", "var-key", v.key + (v.symbol ? " · " + v.symbol : "")));
      tr.appendChild(name);
      tr.appendChild(mk("td", "mono", v.display));
      tr.appendChild(mk("td", "mono muted", v.range_display || ""));
      var st = mk("td"); st.appendChild(pill(v.status)); tr.appendChild(st);
      tr.appendChild(mk("td", "mono", v.quarter));
      tr.appendChild(mk("td", null, v.owner || ""));
      tr.appendChild(mk("td", "muted", v.source || ""));
      tr.title = v.drives ? "Drives: " + v.drives : "";
      body.appendChild(tr);
    });
    if (!rows.length) {
      var tr = mk("tr"); var td = mk("td", "muted", "No variables match these filters."); td.colSpan = 7; tr.appendChild(td); body.appendChild(tr);
    }
  }

  function renderBudget(b) {
    var sum = document.getElementById("budget-summary"); clear(sum);
    [["ok", "✓ " + b.summary.ok + " pass"], ["fail", "✗ " + b.summary.fail + " fail"], ["needs", "… " + b.summary.needs + " need inputs"]]
      .forEach(function (x) { sum.appendChild(mk("span", "tag check-" + x[0], x[1])); });
    var body = document.getElementById("budget-rows"); clear(body);
    b.groups.forEach(function (g) {
      var rows = b.rows.filter(function (r) { return r.group === g; });
      if (!rows.length) return;
      var gr = mk("tr", "group-row"); var gc = mk("td", null, g); gc.colSpan = 5; gr.appendChild(gc); body.appendChild(gr);
      rows.forEach(function (r) {
        var tr = mk("tr");
        tr.appendChild(mk("td", null, r.label));
        tr.appendChild(mk("td", "num", r.display));
        tr.appendChild(mk("td", "mono muted", r.unit));
        tr.appendChild(mk("td", "mono muted", r.eq));
        var icon = { ok: "✓ ", fail: "✗ ", needs: "… " }[r.check] || "";
        tr.appendChild(mk("td", r.check ? "check-" + r.check : "muted", (icon + (r.note || "")).trim()));
        body.appendChild(tr);
      });
    });
  }

  HS3.wireRepoLinks();
  Promise.all([HS3.loadJSON("data/register.json"), HS3.loadJSON("data/budget.json")]).then(function (res) {
    REG = res[0];
    renderProgress(REG);
    renderControls(REG);
    renderTable();
    renderBudget(res[1]);
  }).catch(function (err) {
    document.getElementById("var-rows").innerHTML = "";
    var tr = HS3.mk("tr"); var td = HS3.mk("td", "muted", "Could not load the data (" + err.message + "). Build the site with: python tools/build_site.py");
    td.colSpan = 7; tr.appendChild(td); document.getElementById("var-rows").appendChild(tr);
  });
})();
