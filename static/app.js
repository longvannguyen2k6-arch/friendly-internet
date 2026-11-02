// Progressive enhancement: every page still works without JavaScript.
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  // ── Header gets a shadow once the page is scrolled ──
  var header = $(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 4); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // ── Fade elements in as they scroll into view ──
  var reveals = $$("[data-reveal]");
  if (reveals.length) {
    if ("IntersectionObserver" in window && !reduceMotion) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
        });
      }, { threshold: 0.15 });
      reveals.forEach(function (el, i) {
        el.style.transitionDelay = Math.min(i, 5) * 80 + "ms";
        io.observe(el);
      });
    } else {
      reveals.forEach(function (el) { el.classList.add("in"); });
    }
  }

  // ── Count up the prices in the hero ──
  $$("[data-count-to]").forEach(function (el) {
    var target = parseFloat(el.dataset.countTo);
    if (isNaN(target) || reduceMotion) return;
    var whole = target % 1 === 0, start = null, duration = 700;
    function fmt(v) { return "£" + (whole ? Math.round(v) : v.toFixed(2)); }
    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      el.textContent = fmt(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step); else el.textContent = fmt(target);
    }
    requestAnimationFrame(step);
  });

  // ── Show / hide password ──
  $$("[data-toggle-password]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var input = $(btn.dataset.togglePassword);
      if (!input) return;
      var show = input.type === "password";
      input.type = show ? "text" : "password";
      btn.textContent = show ? "Hide" : "Show";
    });
  });

  // ── Password strength checklist + "passwords match" message ──
  $$("[data-strength-for]").forEach(function (box) {
    var input = $(box.dataset.strengthFor);
    if (!input) return;
    box.hidden = false;
    var bar = $(".strength-bar span", box);
    function update() {
      var v = input.value;
      var rules = { length: v.length >= 8, upper: /[A-Z]/.test(v), digit: /\d/.test(v) };
      var score = 0;
      Object.keys(rules).forEach(function (k) {
        var li = $('[data-rule="' + k + '"]', box);
        if (li) li.classList.toggle("ok", rules[k]);
        if (rules[k]) score++;
      });
      box.dataset.level = score;
      bar.style.width = (v ? Math.max(score, 1) / 3 * 100 : 0) + "%";
    }
    input.addEventListener("input", update);
    update();
  });

  $$("[data-match-for]").forEach(function (msg) {
    var a = $(msg.dataset.matchFor), b = $(msg.dataset.matchWith);
    if (!a || !b) return;
    function check() {
      if (!b.value) { msg.hidden = true; return; }
      var ok = a.value === b.value;
      msg.hidden = false;
      msg.textContent = ok ? "Passwords match" : "Passwords do not match yet";
      msg.className = "hint " + (ok ? "good" : "bad");
    }
    a.addEventListener("input", check);
    b.addEventListener("input", check);
  });

  // ── Reset code: digits only ──
  $$(".code-input").forEach(function (input) {
    input.addEventListener("input", function () {
      input.value = input.value.replace(/\D/g, "").slice(0, 6);
    });
    if (!input.value) input.focus();
  });

  // ── Plans page: provider filter, sort, max price, SIM only ──
  var grid = $(".plans-grid");
  var cards = $$(".plan[data-provider]");
  if (grid && cards.length && $(".filter-btn[data-filter]")) {
    var toolbar = $("[data-toolbar]");
    var sortSel = $("#sort-plans"), range = $("#max-price"), out = $("#price-out");
    var simOnly = $("#sim-only"), count = $("#plan-count");
    var buttons = $$(".filter-btn[data-filter]");
    var provider = "all";
    var maxPrice = Math.ceil(Math.max.apply(null, cards.map(function (c) { return parseFloat(c.dataset.price) || 0; })));

    var empty = document.createElement("p");
    empty.className = "no-results";
    empty.textContent = "No plans match these filters.";
    grid.parentNode.insertBefore(empty, grid.nextSibling);

    function apply() {
      var limit = range ? parseFloat(range.value) : maxPrice;
      var shown = 0;
      cards.forEach(function (c) {
        var ok = (provider === "all" || c.dataset.provider === provider) &&
                 parseFloat(c.dataset.price) <= limit &&
                 (!simOnly || !simOnly.checked || c.dataset.sim === "1");
        c.hidden = !ok;
        if (ok) shown++;
      });
      if (count) count.textContent = "Showing " + shown + " of " + cards.length + " plans";
      empty.style.display = shown ? "none" : "block";
      buttons.forEach(function (b) { b.classList.toggle("active", b.dataset.filter === provider); });
    }

    function sortCards() {
      var mode = sortSel ? sortSel.value : "default";
      var sorted = cards.slice().sort(function (a, b) {
        if (mode === "price-asc") return a.dataset.price - b.dataset.price;
        if (mode === "price-desc") return b.dataset.price - a.dataset.price;
        return a.dataset.order - b.dataset.order;
      });
      sorted.forEach(function (c) { grid.appendChild(c); });
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () { provider = b.dataset.filter; apply(); });
    });

    if (toolbar) {
      toolbar.hidden = false;
      range.max = maxPrice;
      range.value = maxPrice;
      out.textContent = "£" + maxPrice;
      range.addEventListener("input", function () { out.textContent = "£" + range.value; apply(); });
      sortSel.addEventListener("change", sortCards);
      simOnly.addEventListener("change", apply);
    }

    var wanted = new URLSearchParams(location.search).get("provider");
    if (wanted) provider = wanted.toLowerCase();
    apply();
  }

  // ── Quiz: only enable phone models when "include a phone" is chosen ──
  var models = $("#phone-models");
  var phoneRadios = $$('input[name="phone_required"]');
  if (models && phoneRadios.length) {
    var syncModels = function () {
      var yes = phoneRadios.some(function (r) { return r.checked && r.value === "yes"; });
      models.classList.toggle("is-off", !yes);
      $$("input", models).forEach(function (i) { i.disabled = !yes; if (!yes) i.checked = false; });
    };
    phoneRadios.forEach(function (r) { r.addEventListener("change", syncModels); });
    syncModels();
  }

  // ── Payment method toggle (Card vs Apple Pay) + card input formatting ──
  var payRadios = $$('input[name="payment_method"]');
  var cardBox = $("#card-fields");
  var appleNote = $("#apple-pay-note");
  var payBtn = $("#pay-submit-btn");
  if (payRadios.length && cardBox) {
    var cardInputs = $$("[data-card-input]", cardBox);
    var syncPayment = function () {
      var method = "card";
      payRadios.forEach(function (r) { if (r.checked) method = r.value; });
      var isCard = method === "card";
      cardBox.hidden = !isCard;
      if (appleNote) appleNote.hidden = isCard;
      cardInputs.forEach(function (inp) {
        inp.required = isCard;
        inp.disabled = !isCard;
      });
      if (payBtn) {
        payBtn.textContent = isCard ? payBtn.dataset.cardLabel : payBtn.dataset.appleLabel;
        payBtn.classList.toggle("btn-apple", !isCard);
      }
    };
    payRadios.forEach(function (r) { r.addEventListener("change", syncPayment); });
    syncPayment();
  }

  $$("[data-format-card]").forEach(function (inp) {
    inp.addEventListener("input", function () {
      var digits = inp.value.replace(/\D/g, "").slice(0, 16);
      inp.value = digits.replace(/(\d{4})(?=\d)/g, "$1 ");
    });
  });

  $$("[data-format-expiry]").forEach(function (inp) {
    inp.addEventListener("input", function () {
      var digits = inp.value.replace(/\D/g, "").slice(0, 4);
      inp.value = digits.length > 2 ? digits.slice(0, 2) + "/" + digits.slice(2) : digits;
    });
  });

  $$("[data-format-cvc]").forEach(function (inp) {
    inp.addEventListener("input", function () {
      inp.value = inp.value.replace(/\D/g, "").slice(0, 4);
    });
  });

  // ── Copy membership ID ──
  $$("[data-copy]").forEach(function (btn) {
    var target = $(btn.dataset.copy);
    if (!target || !navigator.clipboard) return;
    btn.hidden = false;
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(target.textContent.trim()).then(function () {
        var old = btn.textContent;
        btn.textContent = "Copied";
        btn.classList.add("copied");
        setTimeout(function () { btn.textContent = old; btn.classList.remove("copied"); }, 1500);
      });
    });
  });

  // ── Stop double submits (e.g. paying twice) ──
  $$("form").forEach(function (form) {
    form.addEventListener("submit", function () {
      var btn = $('button[type="submit"]', form);
      if (!btn || btn.dataset.locked) return;
      btn.dataset.locked = "1";
      btn.dataset.label = btn.textContent;
      setTimeout(function () {
        btn.disabled = true;
        btn.classList.add("is-loading");
        btn.textContent = "Please wait…";
      }, 0);
    });
  });
  // Restore buttons when the user comes back with the browser's back button
  window.addEventListener("pageshow", function (e) {
    if (!e.persisted) return;
    $$('button[type="submit"][data-locked]').forEach(function (btn) {
      btn.disabled = false;
      btn.classList.remove("is-loading");
      btn.textContent = btn.dataset.label;
      delete btn.dataset.locked;
    });
  });
})();
