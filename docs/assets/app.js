const fmt = new Intl.NumberFormat("ja-JP");

function formatIncome(n) {
  const sign = n > 0 ? "+" : "";
  return `${sign}${fmt.format(n)}`;
}

function incomeClass(n) {
  if (n > 0) return "positive";
  if (n < 0) return "negative";
  return "zero";
}

function renderSummary(summary) {
  const el = document.getElementById("summary");
  const cards = [
    ["勝率", summary.win_rate != null ? `${summary.win_rate}%` : "—"],
    ["全体 PF", summary.pf != null ? summary.pf : "—"],
    ["損益合計", summary.total_income != null ? fmt.format(summary.total_income) : "—"],
    ["銘柄数", summary.symbol_count ?? "—"],
    ["勝ち", summary.wins ?? "—"],
    ["負け", summary.losses ?? "—"],
  ];
  el.innerHTML = cards
    .map(
      ([label, value]) =>
        `<div class="summary-card"><p class="label">${label}</p><p class="value">${value}</p></div>`,
    )
    .join("");
}

function renderList(symbols) {
  const list = document.getElementById("list");
  list.innerHTML = symbols
    .map((s) => {
      const ic = incomeClass(s.incomes);
      return `<li class="item">
        <span class="code">${s.code}<span class="badge">${s.winlose}</span></span>
        <span class="income ${ic}">${formatIncome(s.incomes)}</span>
        <span class="name">${escapeHtml(s.name)}</span>
        <span class="meta">PF ${s.pf} · 勝率 ${s.win_per}%</span>
      </li>`;
    })
    .join("");
}

function escapeHtml(text) {
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}

function sortSymbols(symbols, mode) {
  const copy = [...symbols];
  switch (mode) {
    case "incomes-asc":
      return copy.sort((a, b) => a.incomes - b.incomes);
    case "pf-desc":
      return copy.sort((a, b) => b.pf - a.pf);
    case "code-asc":
      return copy.sort((a, b) => a.code.localeCompare(b.code, "ja"));
    default:
      return copy.sort((a, b) => b.incomes - a.incomes);
  }
}

function filterSymbols(symbols, query) {
  const q = query.trim().toLowerCase();
  if (!q) return symbols;
  return symbols.filter(
    (s) =>
      s.code.toLowerCase().includes(q) ||
      (s.name && s.name.toLowerCase().includes(q)),
  );
}

async function init() {
  const err = document.getElementById("error");
  let data;
  try {
    const res = await fetch("data.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`data.json (${res.status})`);
    data = await res.json();
  } catch (e) {
    err.hidden = false;
    err.textContent =
      "データを読み込めませんでした。publish_results.py 実行後に GitHub Pages を更新してください。";
    document.getElementById("updated").textContent = "";
    return;
  }

  const updated = document.getElementById("updated");
  if (data.generated_at) {
    const dt = new Date(data.generated_at);
    updated.textContent = `更新: ${dt.toLocaleString("ja-JP")}`;
  }

  renderSummary(data.summary);

  let symbols = data.symbols || [];
  const search = document.getElementById("search");
  const sort = document.getElementById("sort");
  const count = document.getElementById("count");

  function refresh() {
    let rows = filterSymbols(symbols, search.value);
    rows = sortSymbols(rows, sort.value);
    renderList(rows);
    count.textContent = `${rows.length} / ${symbols.length} 銘柄`;
  }

  search.addEventListener("input", refresh);
  sort.addEventListener("change", refresh);
  refresh();
}

init();
