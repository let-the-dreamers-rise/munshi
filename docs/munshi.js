/* Munshi's inbox, shared by the hosted demo, the local inbox and the recorded replay.
   A page supplies an adapter: { start(), decide(card, choice), now(), note } and calls Munshi.mount(it). */
(function () {
  "use strict";
  var URGENT = { scam_shaped_payment: 1, unusual_payment: 1 };
  var WORDS = {
    en: {
      now: "Now", later: "When you have a minute", handled: "Handled", needs: "Needs you now",
      worth: "Worth a look", double_charge: "Charged twice", renewal_due: "Renews soon",
      quiet: "Nothing needs you. Munshi is watching quietly.",
      quietYours: "Munshi read your messages and found nothing worth raising. It speaks up when money goes to a "
        + "payee you have never paid within half an hour of a threatening message, when the same charge repeats "
        + "with no refund, or when a subscription is about to renew. Paste the threatening message too, and a few "
        + "weeks of ordinary bank SMS, so it has something to compare with.",
      paperwork: "The paperwork, already filled in", steps: "Your next steps", chose: "You chose: ",
      copy: "Copy", copied: "Copied", copyAll: "Copy everything", share: "Send to family on WhatsApp",
      copiedAll: "Copied — paste it into cybercrime.gov.in", selectText: "Select the text to copy",
      call1930: "Call 1930", callBank: function (b) { return "Call " + b; },
      onIt: "Munshi is on it…", other: "हिन्दी",
      left: "left in the first hour, while the bank can still hold the money.",
      spoken: function (m) { return "About " + m + " minute" + (m === 1 ? "" : "s") + " left in the first hour."; },
      over: "The first hour has passed. Report anyway: 1930 and the bank still act on it.",
      yours: function (n) { return "Your messages: " + n + " read, nothing kept."; },
      watching: function (who, n, days) {
        return who + "'s household. Watching " + n + (days >= 2 ? " over " + days + " days" : "") + ", on the phone.";
      },
      payments: function (n) { return n + " payment" + (n === 1 ? "" : "s"); }
    },
    hi: {
      now: "अभी", later: "जब समय मिले",
      handled: "हो गया",
      needs: "अभी आपकी ज़रूरत है",
      worth: "देखने लायक",
      double_charge: "दो बार कटे",
      renewal_due: "जल्द रिन्यू होगा",
      quiet: "अभी कुछ ज़रूरी नहीं है। "
             + "मुंशी चुपचाप देख रहा है।",
      quietYours: "मुंशी ने आपके मैसेज पढ़े और बताने लायक कुछ नहीं मिला। "
        + "मुंशी तब बोलता है जब किसी धमकी भरे मैसेज के आधे घंटे के अंदर किसी नए पेयी को पैसे जाएं, "
        + "एक ही चार्ज दो बार लगे और रिफंड न आए, या कोई सब्सक्रिप्शन रिन्यू होने वाला हो। "
        + "धमकी वाला मैसेज और कुछ हफ़्तों के आम बैंक मैसेज भी पेस्ट करें, ताकि तुलना करने को कुछ हो।",
      paperwork: "कागज़ी कार्रवाई, पहले "
                 + "से भरी हुई",
      steps: "आगे क्या करना है",
      chose: "आपने चुना: ",
      copy: "कॉपी करें", copied: "कॉपी हो गया",
      copyAll: "सब कुछ कॉपी करें", share: "घर वालों को WhatsApp पर भेजें",
      copiedAll: "कॉपी हो गया — cybercrime.gov.in पर "
                 + "पेस्ट करें",
      selectText: "कॉपी करने के लिए टेक्स्ट "
                  + "चुनें",
      call1930: "1930 पर कॉल करें",
      callBank: function (b) { return b + " को कॉल करें"; },
      onIt: "मुंशी कर रहा है…", other: "English",
      left: "पहले घंटे में इतना समय "
            + "बचा है, जब तक बैंक पैसे "
            + "रोक सकता है।",
      spoken: function (m) {
        return "पहले घंटे में लगभग " + m +
          " मिनट बचे हैं।";
      },
      over: "पहला घंटा बीत चुका है। "
            + "फिर भी रिपोर्ट करें: 1930 "
            + "और बैंक अब भी कार्रवाई "
            + "करते हैं।",
      yours: function (n) {
        return "आपके मैसेज: " + n +
          " पढ़े गए, कुछ सहेजा नहीं।";
      },
      watching: function (who, n, days) {
        return who + " का घर। " + n +
          (days >= 2 ? ", " + days + " दिन के" : "") +
          " फोन पर देखे जा रहे हैं।";
      },
      payments: function (n) { return n + " भुगतान"; }
    }
  };
  var lang = "en", latest = null;

  function t() { return WORDS[lang]; }

  // The Hindi card is written from the same facts by munshi/hindi.py, not translated here.
  function say(card, key, fallback) {
    var hi = card.hi || {};
    return lang === "hi" && hi[key] ? hi[key] : fallback;
  }
  var TAB_NAMES = { cybercrime_report: "1930 and cybercrime.gov.in", bank_dispute: "Your bank", upi_help: "UPI Help" };
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
    var big = el("b", { "aria-hidden": "true" }), words = el("span", { "aria-hidden": "true" });
    // The digits change every second; a screen reader is told only when the minute does.
    var spoken = el("span", { cls: "sr" }), said = null;
    function tick() {
      var left = Math.floor((deadline - nowMs()) / 1000);
      var mins = Math.max(0, Math.ceil(left / 60));
      if (left > 0) {
        big.textContent = Math.floor(left / 60) + ":" + String(left % 60).padStart(2, "0");
        words.textContent = t().left;
        if (mins !== said) spoken.textContent = t().spoken(mins);
      } else {
        big.textContent = "0:00";
        words.textContent = t().over;
        if (said !== 0) spoken.textContent = t().over;
      }
      said = left > 0 ? mins : 0;
    }
    tick();
    timers.push(setInterval(tick, 1000));
    return el("div", { cls: "clock", role: "timer", "aria-live": "polite" }, [big, words, spoken]);
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
    var box = el("div", { cls: "draft" }, kids);
    var copy = el("button", { cls: "copy", type: "button", text: t().copy });
    copy.addEventListener("click", function () {
      var text = box.innerText.replace(new RegExp("\\n" + t().copy + "$"), "");
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(
        function () { copy.textContent = t().copied; }, function () { copy.textContent = t().selectText; });
    });
    box.appendChild(copy);
    return box;
  }

  function drafts(card) {
    var names = Object.keys(card.drafts || {});
    if (!names.length) return null;
    var panel = el("div");
    var tabs = el("div", { cls: "tabs" });
    function show(i) {
      Array.prototype.forEach.call(tabs.children, function (b, j) { b.setAttribute("aria-pressed", String(i === j)); });
      panel.replaceChildren(draftView(names[i], card.drafts[names[i]]));
    }
    names.forEach(function (n, i) {  // plain buttons: aria-pressed, not tabs we do not key-handle
      tabs.appendChild(el("button", { type: "button", text: TAB_NAMES[n] || n,
                                      onclick: function () { show(i); } }));
    });
    show(0);
    return el("details", URGENT[card.kind] ? { open: "" } : {},
              [el("summary", { text: t().paperwork }), tabs, panel]);
  }

  function pendingCard(card) {
    var urgent = !!URGENT[card.kind];
    var options = say(card, "options", card.options);
    var buttons = options.map(function (o, i) {
      return el("button", { type: "button", cls: i === 0 ? "primary" : "", text: o[1],
                            onclick: function (e) { decide(card, o[0], e.currentTarget); } });
    });
    return el("article", { cls: "card " + (urgent ? "urgent" : "quiet") }, [
      el("div", { cls: "kicker", text: urgent ? t().needs : (t()[card.kind] || t().worth) }),
      el("h3", { cls: "headline", text: say(card, "headline", card.headline) }),
      urgent ? clock(card) : null,
      el("ul", { cls: "facts" }, say(card, "evidence", card.evidence).map(function (f) { return el("li", { text: f }); })),
      el("div", { cls: "choices" }, buttons),
      drafts(card)
    ]);
  }

  function reported(card) { return URGENT[card.kind] && card.decision === "report"; }

  function everything(card) {
    var lines = [card.headline, ""];
    var report = (card.drafts || {}).cybercrime_report;
    var bank = (card.drafts || {}).bank_dispute;
    if (report) {
      Object.keys(report.fields).forEach(function (k) {
        if (report.fields[k]) lines.push(k + ": " + report.fields[k]);
      });
    }
    if (bank) lines.push("", bank.subject, "", bank.body);
    return lines.join("\n");
  }

  function dial(label, number, primary) {
    return el("a", { cls: "btn" + (primary ? " primary" : ""), href: "tel:" + number, text: label });
  }

  // Nobody deals with this alone: one tap opens WhatsApp with the whole pack, recipient still to choose.
  function share(card) {
    return el("a", { cls: "btn", target: "_blank", rel: "noopener",
                     href: "https://wa.me/?text=" + encodeURIComponent(everything(card)), text: t().share });
  }

  // In the first hour, the useful thing is a phone call, not more reading.
  function actions(card) {
    var bank = (card.drafts || {}).bank_dispute || {};
    var copy = el("button", { type: "button", text: t().copyAll });
    copy.addEventListener("click", function () {
      (navigator.clipboard ? navigator.clipboard.writeText(everything(card)) : Promise.reject()).then(
        function () { copy.textContent = t().copiedAll; },
        function () { copy.textContent = t().selectText; });
    });
    return el("div", { cls: "choices" }, [
      dial(t().call1930, "1930", true),
      bank.helpline ? dial(t().callBank(bank.bank || "bank"), bank.helpline) : null,
      copy,
      share(card)
    ]);
  }

  function doneCard(card) {
    var chosen = say(card, "options", card.options).filter(function (o) { return o[0] === card.decision; })[0];
    var act = reported(card);
    return el("article", { cls: "card " + (act ? "urgent" : "done") }, [
      el("div", { cls: "kicker", text: act ? t().steps : t().chose + (chosen ? chosen[1] : card.decision) }),
      el("h3", { cls: "headline", text: say(card, "headline", card.headline) }),
      act ? clock(card) : null,
      act ? actions(card) : null,
      el("ol", { cls: "steps" }, say(card, "outcome", card.outcome).split("\n").filter(Boolean)
        .map(function (s) { return el("li", { text: s }); })),
      drafts(card)
    ]);
  }

  function watching(s) {
    var payments = t().payments(s.watched.payments);
    if (s.household === "you") return t().yours(payments);
    return t().watching(s.household.charAt(0).toUpperCase() + s.household.slice(1), payments, s.watched.days);
  }

  function section(title, cards, make, empty) {
    var kids = [el("h2", { cls: "section", text: title })];
    if (!cards.length && empty) kids.push(el("p", { cls: "empty", text: empty }));
    cards.forEach(function (c) { kids.push(make(c)); });
    return cards.length || empty ? el("section", {}, kids) : null;
  }

  function render(s) {
    latest = s;
    timers.forEach(function (id) { clearInterval(id); clearTimeout(id); });
    timers = [];
    var who = byId("who");
    if (who) who.textContent = watching(s);
    var pending = s.cards.filter(function (c) { return c.status === "pending"; });
    var now = pending.filter(function (c) { return URGENT[c.kind]; });
    var later = pending.filter(function (c) { return !URGENT[c.kind]; });
    var done = s.cards.filter(function (c) { return c.status !== "pending"; }).reverse();
    var main = byId("main");
    main.replaceChildren.apply(main, [
      section(t().now, now.concat(done.filter(reported)),
              function (c) { return c.status === "pending" ? pendingCard(c) : doneCard(c); },
              later.length || done.length ? null : (s.household === "you" ? t().quietYours : t().quiet)),
      section(t().later, later, pendingCard),
      section(t().handled, done.filter(function (c) { return !reported(c); }), doneCard)
    ].filter(Boolean));
    renderLog(s.audit || []);
  }

  function logRow(r) {
    var cls = r.refused ? "refused" : (r.status === "waiting for the household" ? "waiting" : "");
    return el("li", { cls: cls }, [
      el("span", { cls: "t", text: (r.at || "").slice(11, 19) + " " }),
      el("span", { cls: "n", text: r.tool }),
      el("span", { text: r.status && r.status !== "success" ? " " + r.status : "" }),
      r.refused ? el("span", { cls: "r", text: r.refused }) : null
    ]);
  }

  // The agent's own log, revealed in the order it happened rather than all at once, so a
  // person can see what it did. Nothing here is invented: these rows are the audit file.
  function renderLog(rows) {
    var log = byId("log");
    if (!log) return;
    if (rows.length < shown) { log.replaceChildren(); shown = 0; }
    var fresh = rows.slice(shown);
    shown = rows.length;
    var quick = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var step = quick || fresh.length < 2 ? 0 : Math.min(180, 1400 / fresh.length);
    fresh.forEach(function (r, i) {
      if (!step) { log.insertBefore(logRow(r), log.firstChild); return; }
      timers.push(setTimeout(function () { log.insertBefore(logRow(r), log.firstChild); }, i * step));
    });
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
    button.textContent = t().onIt;
    Promise.resolve(adapter.decide(card, choice)).then(function (s) { busy(false); render(s); }, fail);
  }

  function post(url, body) {
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json", "X-Munshi": "1" },
                        body: JSON.stringify(body) })
      .then(function (r) { return r.json(); })
      .then(function (j) { if (!j.ok) throw new Error(j.error); return j.data; });
  }

  function stored(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }

  function setLang(next) {
    lang = WORDS[next] ? next : "en";
    try { window.localStorage.setItem("munshi-lang", lang); } catch (e) { /* private window */ }
    document.documentElement.lang = lang;
    var button = byId("lang");
    if (button) button.textContent = t().other;
    if (latest) { shown = 0; var log = byId("log"); if (log) log.replaceChildren(); render(latest); }
  }

  function startLang() {
    var saved = stored("munshi-lang");
    setLang(saved || (/^hi\b/i.test(navigator.language || "") ? "hi" : "en"));
    var button = byId("lang");
    if (button) button.addEventListener("click", function () { setLang(lang === "hi" ? "en" : "hi"); });
  }

  window.Munshi = {
    el: el, byId: byId, post: post, render: render, busy: busy, fail: fail, parseWhen: parseWhen,
    setLang: setLang, lang: function () { return lang; },
    // Rejects if the run fails, so the caller decides where the reason belongs.
    mount: function (a) {
      adapter = a;
      shown = 0;
      var log = byId("log");
      if (log) log.replaceChildren();
      return Promise.resolve(adapter.start()).then(render);
    },
    ready: startLang
  };
})();
