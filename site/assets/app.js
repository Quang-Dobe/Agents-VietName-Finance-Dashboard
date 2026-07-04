/* Giá Việt — helpers dùng chung (không framework). Cần Chart.js đã load trước. */

const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

const fmtVN = (n, digits = 0) =>
  n == null || n === "" || isNaN(n)
    ? "—"
    : new Intl.NumberFormat("vi-VN", { minimumFractionDigits: digits, maximumFractionDigits: digits }).format(n);

const num = (x) => {
  if (x == null || x === "") return null;
  const v = Number(x);
  return isNaN(v) ? null : v;
};

function deltaHTML(d, suffix = "") {
  if (d == null) return "";
  const cls = d >= 0 ? "up" : "down";
  const arrow = d >= 0 ? "▲ +" : "▼ −";
  return `<span class="${cls}">${arrow}${Math.abs(d).toFixed(1)}%</span>${suffix}`;
}

async function loadCSV(path) {
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) throw new Error(`${path} → ${res.status}`);
  const text = (await res.text()).trim();
  if (!text) return [];
  const [head, ...lines] = text.split("\n").map((l) => l.split(","));
  return lines.map((r) => Object.fromEntries(head.map((h, i) => [h.trim(), (r[i] ?? "").trim()])));
}

/* Lọc theo khung thời gian. months=0 => tất cả. dateKey mặc định 'date'. */
function sliceRange(rows, months, dateKey = "date") {
  if (!months) return rows;
  if (!rows.length) return rows;
  const last = new Date(rows[rows.length - 1][dateKey]);
  const from = new Date(last);
  from.setMonth(from.getMonth() - months);
  return rows.filter((r) => new Date(r[dateKey]) >= from);
}

/* ---- Chart.js: defaults dark + line chart 1 trục y ---- */
function applyChartDefaults() {
  if (!window.Chart) return;
  Chart.defaults.color = css("--ink-3");
  Chart.defaults.borderColor = css("--grid");
  Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
  Chart.defaults.font.size = 12;
  Chart.defaults.maintainAspectRatio = false;
}

function makeLineChart(canvas, labels, series, opts = {}) {
  applyChartDefaults();
  const datasets = series.map((s) => ({
    label: s.label,
    data: s.data,
    borderColor: s.color,
    backgroundColor: s.color,
    borderWidth: 2,
    borderDash: s.dim ? [5, 4] : [],
    pointRadius: 0,
    pointHoverRadius: 5,
    tension: 0.15,
    stepped: opts.stepped ? "before" : false,
    spanGaps: true,
  }));
  return new Chart(canvas, {
    type: "line",
    data: { labels, datasets },
    options: {
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: series.length > 1, labels: { boxWidth: 12, boxHeight: 2, color: css("--ink-2") } },
        tooltip: {
          backgroundColor: css("--surface-2"),
          borderColor: css("--border"),
          borderWidth: 1,
          titleColor: css("--ink"),
          bodyColor: css("--ink-2"),
          padding: 10,
          callbacks: {
            label: (c) => `${c.dataset.label}: ${fmtVN(c.parsed.y, opts.digits || 0)}${opts.unit || ""}`,
          },
        },
      },
      scales: {
        x: { grid: { display: false }, ticks: { maxTicksLimit: 8, maxRotation: 0 } },
        y: {
          grid: { color: css("--grid") },
          ticks: { callback: (v) => fmtVN(v, opts.digits || 0) },
          beginAtZero: false,
        },
      },
    },
  });
}

function sparkline(canvas, values, color) {
  applyChartDefaults();
  return new Chart(canvas, {
    type: "line",
    data: {
      labels: values.map((_, i) => i),
      datasets: [{ data: values, borderColor: color, borderWidth: 2, pointRadius: 0, tension: 0.3, fill: false }],
    },
    options: {
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      scales: { x: { display: false }, y: { display: false } },
      elements: { line: { capBezierPoints: true } },
    },
  });
}

/* ---- Dashboard: render các card từ summary.json ---- */
function renderCards(s) {
  setText("updated", s.generated_at ? "Cập nhật: " + fmtDateTime(s.generated_at) : "");

  // flags banner
  if (s.flags && s.flags.length) {
    const el = document.getElementById("flags");
    el.hidden = false;
    el.innerHTML = `<div class="box">⚠ ${s.flags.map((f) => `${f.module}: ${f.msg}`).join(" · ")}</div>`;
  }

  if (s.gold) card("gold", fmtVN(s.gold.latest.sjc_sell / 1000, 1) + " tr", "₫/lượng (SJC bán)",
    [["hôm qua", s.gold.delta_1d], ["7 ngày", s.gold.delta_7d]], s.gold.spark_30d, css("--c-gold"));

  if (s.fx) card("fx", fmtVN(s.fx.latest.vcb_sell), "₫/USD (VCB bán)",
    [["hôm qua", s.fx.delta_1d], ["7 ngày", s.fx.delta_7d]], s.fx.spark_30d, css("--c-fx"));

  if (s.fuel) card("fuel", fmtVN(s.fuel.latest.ron95), "₫/lít (RON95)",
    [["kỳ trước", s.fuel.delta_period]], s.fuel.spark_30d, css("--c-fuel"));

  if (s.rates && s.rates.top12m)
    card("rates", s.rates.top12m.rate.toFixed(2) + "%", `cao nhất 12T · ${s.rates.top12m.bank}`,
      [], null, css("--c-rates"), s.rates.median_12m != null ? `Trung vị 12T: ${s.rates.median_12m}%` : "");
  else cardEmpty("rates", "Lãi suất", "Cập nhật thứ Hai");

  if (s.utilities) {
    const u = s.utilities;
    const gasVal = u.gas_price != null ? u.gas_price : u.gas_mien_nam; // tương thích ngược
    const sub = [u.tier1_price ? `Điện bậc 1: ${fmtVN(u.tier1_price)}₫` : "", gasVal ? `Gas 12kg: ${fmtVN(gasVal)}₫` : ""].filter(Boolean).join(" · ");
    card("utilities", gasVal ? fmtVN(gasVal) + " ₫" : "—", `Gas 12kg (${u.gas_region || "Hà Nội"})`,
      u.gas_delta != null ? [["tháng trước", u.gas_delta]] : [], null, css("--c-utilities"), sub);
  }
}

function card(key, big, unit, deltas, spark, color, extra = "") {
  const el = document.getElementById("card-" + key);
  if (!el) return;
  el.querySelector(".big").innerHTML = `${big} <span class="unit-sm">${unit}</span>`;
  const dEl = el.querySelector(".deltas");
  const parts = deltas.filter(([, d]) => d != null).map(([lbl, d]) => deltaHTML(d, " " + lbl));
  if (extra) parts.push(`<span>${extra}</span>`);
  dEl.innerHTML = parts.join(" ");
  const sc = el.querySelector(".spark");
  if (spark && spark.length > 1 && sc) {
    sparkline(sc, spark, color);
    sc.setAttribute("aria-label", `${unit}: ${spark.length} điểm, từ ${fmtVN(spark[0])} đến ${fmtVN(spark[spark.length - 1])}`);
  } else if (sc) sc.remove();
}

function cardEmpty(key, title, msg) {
  const el = document.getElementById("card-" + key);
  if (!el) return;
  el.querySelector(".big").innerHTML = `<span class="unit-sm">${msg}</span>`;
  const sc = el.querySelector(".spark");
  if (sc) sc.remove();
}

/* ---- Detail page khung chung ---- */
function initDetailPage(rows, cfg) {
  const dateKey = cfg.dateKey || "date";
  const wrap = document.getElementById("chart-host");
  let chart = null;
  const scale = cfg.scale || 1;

  function draw(months) {
    const view = sliceRange(rows, months, dateKey);
    if (chart) chart.destroy();
    if (!view.length) {
      wrap.innerHTML = '<p class="empty">Chưa có dữ liệu cho khung thời gian này.</p>';
      return;
    }
    wrap.innerHTML = '<canvas id="chart"></canvas>';
    const labels = view.map((r) => r[dateKey]);
    const series = cfg.series.map((s) => ({
      label: s.label, color: s.color, dim: s.dim,
      data: view.map((r) => { const v = num(r[s.key]); return v == null ? null : v / scale; }),
    }));
    chart = makeLineChart(document.getElementById("chart"), labels, series,
      { stepped: cfg.stepped, digits: cfg.digits || 0, unit: cfg.unit || "" });
  }

  // nút khung thời gian
  document.querySelectorAll(".ranges button").forEach((b) => {
    b.addEventListener("click", () => {
      document.querySelectorAll(".ranges button").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      draw(Number(b.dataset.m));
    });
  });
  const initial = document.querySelector(".ranges button.active");
  draw(initial ? Number(initial.dataset.m) : 12);

  // bảng
  const tbtn = document.getElementById("toggle-table");
  if (tbtn) tbtn.addEventListener("click", () => {
    const t = document.getElementById("table");
    t.hidden = !t.hidden;
    if (!t.hidden) renderTable(t, rows.slice(-30).reverse(), cfg, dateKey);
  });
}

function renderTable(t, rows, cfg, dateKey) {
  const cols = [{ key: dateKey, label: "Ngày" }, ...cfg.series.map((s) => ({ key: s.key, label: s.label }))];
  t.innerHTML =
    "<thead><tr>" + cols.map((c) => `<th>${c.label}</th>`).join("") + "</tr></thead>" +
    "<tbody>" + rows.map((r) =>
      "<tr>" + cols.map((c, i) => `<td>${i === 0 ? r[c.key] : fmtVN(num(r[c.key]), cfg.digits || 0)}</td>`).join("") + "</tr>"
    ).join("") + "</tbody>";
}

/* ---- utils ---- */
function setText(id, txt) { const el = document.getElementById(id); if (el) el.textContent = txt; }
function fmtDateTime(iso) {
  const d = new Date(iso);
  const p = (n) => String(n).padStart(2, "0");
  return `${p(d.getHours())}:${p(d.getMinutes())} · ${p(d.getDate())}/${p(d.getMonth() + 1)}/${d.getFullYear()}`;
}
