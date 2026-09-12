/* Munshi's inbox, shared by the hosted demo, the local inbox and the recorded replay.
   A page supplies an adapter: { start(), decide(card, choice), now(), note } and calls Munshi.mount(it). */
(function () {
  "use strict";
  var URGENT = { scam_shaped_payment: 1, unusual_payment: 1 };
  var TAB_NAMES = { cybercrime_report: "1930 and cybercrime.gov.in", bank_dispute: "Your bank", upi_help: "UPI Help" };
  var KINDS = { double_charge: "Charged twice", renewal_due: "Renews soon" };
  var timers = [], adapter = null, shown = 0;

  function el(tag, attrs, kids) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "cls") node.className = attrs[k];
      else if (k.slice(0, 2) === "on") node.addEventListener(k.slice(2), attrs[k]);
      else node.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (kid) { if (kid) node.appendChild(kid); });
    return node;
  }

  function byId(id) { return document.getElementById(id); }

  // Card times are the phone's local wall clock, and so is the browser's: the inbox belongs to the
  // family's own device. Served to a browser in another timezone, the clock would shift.
  function parseWhen(s) {
    var p = String(s).split(/[- :]/).map(Number);
    return new Date(p[0], p[1] - 1, p[2], p[3], p[4]);
  }

  function nowMs() { return adapter && adapter.now ? adapter.now() : Date.now(); }

  function clock(card) {
    var deadline = parseWhen(card.when).getTime() + 60 * 60 * 1000;
    var big = el("b"), words = el("span");
    function tick() {
      var left = Math.floor((deadline - nowMs()) / 1000);
      if (left > 0) {
        big.textContent = Math.floor(left / 60) + ":" + String(left % 60).padStart(2, "0");
        words.textContent = "left in the first hour, while the bank can still hold the money.";
      } else {
        big.textContent = "0:00";
        words.textContent = "The first hour has passed. Report anyway: 1930 and the bank still act on it.";
      }
    }
    tick();
    timers.push(setInterval(tick, 1000));
    return el("div", { cls: "clock", role: "timer" }, [big, words]);
  }

  function draftView(name, d) {
    var kids = [];
    if (name === "cybercrime_report") {
      kids.push(el("p", { text: d.text }));
      kids.push(el("dl", {}, [].concat.apply([], Object.keys(d.fields).filter(function (k) { return d.fields[k]; })
        .map(function (k) { return [el("dt", { text: k }), el("dd", { text: d.fields[k] })]; }))));
    } else if (name === "bank_dispute") {
      if (d.helpline) kids.push(el("p", { text: "Helpline from the bank's own message: " + d.helpline }));
      kids.push(el("p", { text: "Subject: " + d.subject }));
      kids.push(el("pre", { text: d.body }));
    } else {
      kids.push(el("p", { text: d.note }));
      kids.push(el("dl", {}, ["issue", "transaction_ref", "amount", "date", "recipient"].reduce(function (acc, k) {
        return d[k] ? acc.concat([el("dt", { text: k.replace("_", " ") }), el("dd", { text: String(d[k]) })]) : acc;
      }, [])));
    }
    var box = el("div", { cls: "draft", role: "tabpanel" }, kids);
    var copy = el("button", { cls: "copy", type: "button", text: "Copy" });
    copy.addEventListener("click", function () {
      var text = box.innerText.replace(/\nCopy$/, "");
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(
        function () { copy.textContent = "Copied"; }, function () { copy.textContent = "Select the text to copy"; });
    });
    box.appendChild(copy);
    return box;
  }

  function drafts(card) {
    var names = Object.keys(card.drafts || {});
    if (!names.length) return null;
    var panel = el("div");
    var tabs = el("div", { cls: "tabs", role: "tablist" });
    function show(i) {
      Array.prototype.forEach.call(tabs.children, function (b, j) { b.setAttribute("aria-selected", String(i === j)); });
      panel.replaceChildren(draftView(names[i], card.drafts[names[i]]));
    }
    names.forEach(function (n, i) {
      tabs.appendChild(el("button", { type: "button", role: "tab", text: TAB_NAMES[n] || n,
                                      onclick: function () { show(i); } }));
    });
    show(0);
    return el("details", URGENT[card.kind] ? { open: "" } : {},
              [el("summary", { text: "The paperwork, already filled in" }), tabs, panel]);
  }

  function pendingCard(card) {
    var urgent = !!URGENT[card.kind];
    var buttons = card.options.map(function (o, i) {
      return el("button", { type: "button", cls: i === 0 ? "primary" : "", text: o[1],
                            onclick: function (e) { decide(card, o[0], e.currentTarget); } });
    });
    return el("article", { cls: "card " + (urgent ? "urgent" : "quiet") }, [
      el("div", { cls: "kicker", text: urgent ? "Needs you now" : (KINDS[card.kind] || "Worth a look") }),
      el("h3", { cls: "headline", text: card.headline }),
      urgent ? clock(card) : null,
      el("ul", { cls: "facts" }, card.evidence.map(function (f) { return el("li", { text: f }); })),
      el("div", { cls: "choices" }, buttons),
      drafts(card)
    ]);
  }

  function reported(card) { return URGENT[card.kind] && card.decision === "report"; }

  function doneCard(card) {
    var chosen = card.options.filter(function (o) { return o[0] === card.decision; })[0];
    var act = reported(card);
    return el("article", { cls: "card " + (act ? "urgent" : "done") }, [
      el("div", { cls: "kicker", text: act ? "Your next steps" : "You chose: " + (chosen ? chosen[1] : card.decision) }),
      el("h3", { cls: "headline", text: card.headline }),
      act ? clock(card) : null,
      el("ol", { cls: "steps" }, card.outcome.split("\n").filter(Boolean).map(function (s) { return el("li", { text: s }); })),
      drafts(card)
    ]);
  }

  function plural(n, one) { return n + " " + one + (n === 1 ? "" : "s"); }

  function watching(s) {
    var payments = plural(s.watched.payments, "payment");
    if (s.household === "you") return "Your messages: " + payments + " read, nothing kept.";
    var name = s.household.charAt(0).toUpperCase() + s.household.slice(1);
    return name + "'s household. Watching " + payments +
      (s.watched.days >= 2 ? " over " + s.watched.days + " days" : "") + ", on the phone.";
  }

  function section(title, cards, make, empty) {
    var kids = [el("h2", { cls: "section", text: title })];
    if (!cards.length && empty) kids.push(el("p", { cls: "empty", text: empty }));
    cards.forEach(function (c) { kids.push(make(c)); });
    return cards.length || empty ? el("section", {}, kids) : null;
  }

  function render(s) {
    timers.forEach(clearInterval);
    timers = [];
    var who = byId("who");
    if (who) who.textContent = watching(s);
    var pending = s.cards.filter(function (c) { return c.status === "pending"; });
    var now = pending.filter(function (c) { return URGENT[c.kind]; });
    var later = pending.filter(function (c) { return !URGENT[c.kind]; });
    var done = s.cards.filter(function (c) { return c.status !== "pending"; }).reverse();
    var main = byId("main");
    main.replaceChildren.apply(main, [
      section("Now", now.concat(done.filter(reported)),
              function (c) { return c.status === "pending" ? pendingCard(c) : doneCard(c); },
              later.length || done.length ? null : "Nothing needs you. Munshi is watching quietly."),
      section("When you have a minute", later, pendingCard),
      section("Handled", done.filter(function (c) { return !reported(c); }), doneCard)
    ].filter(Boolean));
    renderLog(s.audit || []);
  }

  function renderLog(rows) {
    var log = byId("log");
    if (!log) return;
    if (rows.length < shown) { log.replaceChildren(); shown = 0; }
    rows.slice(shown).forEach(function (r) {
      var cls = r.refused ? "refused" : (r.status === "waiting for the household" ? "waiting" : "");
      log.insertBefore(el("li", { cls: cls }, [
        el("span", { cls: "t", text: (r.at || "").slice(11, 19) + " " }),
        el("span", { cls: "n", text: r.tool }),
        el("span", { text: r.status && r.status !== "success" ? " " + r.status : "" }),
        r.refused ? el("span", { cls: "r", text: r.refused }) : null
      ]), log.firstChild);
    });
    shown = rows.length;
  }

  function busy(on) {
    document.querySelectorAll("button").forEach(function (b) { b.disabled = on; });
  }

  function fail(e) {
    busy(false);
    var box = byId("error");
    if (box) box.textContent = (e && e.message) || String(e);
  }

  function decide(card, choice, button) {
    var box = byId("error");
    if (box) box.textContent = "";
    busy(true);
    button.textContent = "Munshi is on it…";
    Promise.resolve(adapter.decide(card, choice)).then(function (s) { busy(false); render(s); }, fail);
  }

  function post(url, body) {
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json", "X-Munshi": "1" },
                        body: JSON.stringify(body) })
      .then(function (r) { return r.json(); })
      .then(function (j) { if (!j.ok) throw new Error(j.error); return j.data; });
  }

  window.Munshi = {
    el: el, byId: byId, post: post, render: render, busy: busy, fail: fail, parseWhen: parseWhen,
    mount: function (a) {
      adapter = a;
      shown = 0;
      var log = byId("log");
      if (log) log.replaceChildren();
      return Promise.resolve(adapter.start()).then(render, fail);
    }
  };
})();
