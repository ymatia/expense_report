"""Nextcloud External App for rendering expense report as HTML."""

from __future__ import annotations

import json
import os
from asyncio import to_thread
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated, Any

import numpy as np
import pandas as pd
import requests
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from nc_py_api import NextcloudApp
from nc_py_api.ex_app import AppAPIAuthMiddleware, LogLvl, nc_app, run_app, set_handlers
from fastapi.staticfiles import StaticFiles


def _request_json(url: str, payload: dict[str, Any] = None) -> list[Any]:
    nc_url = os.environ["NEXTCLOUD_URL"]
    print(f"nc_url={nc_url}")
    app_id = os.environ["APP_ID"]
    app_secret = os.environ["APP_SECRET"]

    if payload is None:
        r = requests.get(
            f"{nc_url}{url}"
            ,auth=(app_id, app_secret)
            ,headers={"OCS-APIRequest": "true"}
            ,timeout=60
        )
    else:
        r = requests.post(
            f"{nc_url}{url}"
            ,auth=(app_id, app_secret)
            ,headers={"OCS-APIRequest": "true"}
            ,json=payload
            ,timeout=60
        )

    if r.status_code not in (200, 201, 204):
        raise RuntimeError(f"Request failed ({r.status_code}) for {url}: {r.text}")
    return json.loads(r.text)


def _fetch_selection_values(table_id: int) -> tuple[dict[int, str], dict[int, str]]:
    columns_url = f"/index.php/apps/tables/api/1/tables/{table_id}/columns"
    columns = _request_json(columns_url)
    categories: dict[int, str] = {}
    sub_categories: dict[int, str] = {0: ""}
    for col in columns:
        if col["title"] == "Category":
            for cat in col["selectionOptions"]:
                categories[int(cat["id"])] = cat["label"]
        if col["title"] == "Sub-Category":
            for cat in col["selectionOptions"]:
                sub_categories[int(cat["id"])] = cat["label"]
    return categories, sub_categories


def _fetch_rows(table_id: int) -> pd.DataFrame:
    rows_url = f"/index.php/apps/tables/api/1/tables/{table_id}/rows/simple"
    rows = _request_json(rows_url)
    return pd.DataFrame(np.vstack(rows[1:]), columns=rows[0])


def _build_report_data(year: int, facts_table_id: int, debts_table_id: int) -> dict[str, pd.DataFrame]:
    categories, sub_categories = _fetch_selection_values(facts_table_id)
    df = _fetch_rows(facts_table_id)
    debts_df = _fetch_rows(debts_table_id)

    df.where(df["Date"].str.startswith(str(year)), inplace=True)
    df.dropna(inplace=True)
    df.sort_values("Date", inplace=True)
    df["Category"] = df["Category"].fillna(0)
    df["Sub-Category"] = df["Sub-Category"].fillna(0)

    df["Category"] = df.apply(lambda row: categories.get(int(row["Category"]), "Unknown"), axis=1)
    df["Sub-Category"] = df.apply(lambda row: sub_categories.get(int(row["Sub-Category"] or 0), ""), axis=1)
    df["Amount"] = df.apply(lambda row: float(row["Amount"]), axis=1)

    debts_df.dropna(inplace=True)
    debts_df["How much €"] = debts_df.apply(lambda row: float(row["How much €"]), axis=1)

    df["Month"] = df.apply(
        lambda row: row["Date"][:7] if row["Date"] is not None and isinstance(row["Date"], str) else row,
        axis=1,
    )

    monthly = df.where(df["Category"] == "Actual")
    monthly = monthly[["Month", "Sub-Category", "Amount"]].groupby(["Month", "Sub-Category"], as_index=False).sum()
    monthly = monthly.pivot_table(values="Month", columns="Sub-Category", index="Month", aggfunc="sum", fill_value=0)
    monthly["sum"] = monthly[list(monthly.columns)].sum(axis=1)
    monthly.loc["Average"] = monthly.mean()
    monthly = monthly.reset_index()

    by_category = df[["Category", "Sub-Category", "Amount"]].groupby(["Category", "Sub-Category"], as_index=False).sum()

    today = datetime.today().strftime("%Y-%m-%d")
    last_day = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    cash_flow = df.where((df["Date"] >= today) & (df["Date"] <= last_day))
    cash_flow = cash_flow[["Date", "Description", "Amount"]]
    cash_flow.dropna(subset=["Date"], inplace=True)

    cash_flow_default = cash_flow.query(
        r'not(Description.str.contains("\(01\)") or Description.str.contains("\(DKB\)") or Description.str.contains("\(Praxis\)"))'
    )
    cash_flow_01 = cash_flow[cash_flow["Description"].str.contains(r"\(01\)")]

    debts_summary = debts_df[["Who", "How much €"]].groupby("Who", as_index=False).sum()

    return {
        "all_expenses": df,
        "monthly": monthly,
        "category": by_category,
        "cash_flow": cash_flow_default,
        "cash_flow_01": cash_flow_01,
        "debts": debts_df,
        "debts_summary": debts_summary,
    }


def _to_records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    if dataframe.empty:
        return []
    converted = dataframe.where(pd.notna(dataframe), None)
    return converted.to_dict(orient="records")


def get_report_payload(year: int) -> dict[str, Any]:
    facts_table_id = int(os.getenv("NC_FACTS_TABLE_ID", "6"))
    debts_table_id = int(os.getenv("NC_DEBTS_TABLE_ID", "10"))
    report = _build_report_data(year, facts_table_id, debts_table_id)
    return {
        "year": year,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tables": {
            "all_expenses": _to_records(report["all_expenses"]),
            "monthly": _to_records(report["monthly"]),
            "category": _to_records(report["category"]),
            "cash_flow": _to_records(report["cash_flow"]),
            "cash_flow_01": _to_records(report["cash_flow_01"]),
            "debts": _to_records(report["debts"]),
            "debts_summary": _to_records(report["debts_summary"]),
        },
    }


def build_app_html() -> str:
    print("in build_app_html")
    return """<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Expense Report</title>
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  <style>
    :root {
      color-scheme: light dark;
      --bg: #f6f7f9;
      --card: #ffffff;
      --text: #111827;
      --muted: #6b7280;
      --border: #d1d5db;
      --accent: #0082c9;
    }
    body {
      margin: 0;
      padding: 24px;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
    }
    h1 { margin: 0 0 8px; }
    .meta { color: var(--muted); margin-bottom: 16px; }
    .controls {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }
    input, select, button {
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 14px;
      background: #fff;
      color: #111827;
    }
    button { cursor: pointer; }
    .btn-primary {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }
    .tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 10px 0 14px;
    }
    .tab.active {
      border-color: var(--accent);
      color: var(--accent);
      font-weight: 600;
    }
    .table-wrap {
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: 8px;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      min-width: 700px;
    }
    th, td {
      border-bottom: 1px solid var(--border);
      text-align: left;
      padding: 8px;
      white-space: nowrap;
    }
    thead th {
      position: sticky;
      top: 0;
      background: #f3f4f6;
    }
  </style>
</head>
<body>
  <div id="app" class="container">
    <h1>Expense Report</h1>
    <p class="meta">
      Source: {{ meta.base_url || "-" }} | Generated at: {{ meta.generated_at || "-" }}
    </p>

    <div class="controls">
      <input type="number" v-model.number="year" placeholder="Year" min="2000" max="2100" />
      <input type="text" v-model.trim="textFilter" placeholder="Filter text (description/category/sub-category)" />
      <select v-model="categoryFilter">
        <option value="">All categories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
      <button class="btn-primary" @click="loadReport">Load Report</button>
    </div>

    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key">
        {{ tab.label }} ({{ displayedRows(tab.key).length }})
      </button>
    </div>

    <div class="table-wrap">
      <table v-if="activeRows.length > 0">
        <thead>
          <tr>
            <th v-for="col in activeColumns" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in activeRows" :key="idx">
            <td v-for="col in activeColumns" :key="col">{{ row[col] }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else style="padding: 16px; color: #6b7280;">No data for this selection.</div>
    </div>
  </div>

  <script>
    const { createApp } = Vue;
    createApp({
      data() {
        const now = new Date();
        return {
          year: now.getFullYear(),
          textFilter: "",
          categoryFilter: "",
          activeTab: "all_expenses",
          meta: {},
          tables: {
            all_expenses: [],
            monthly: [],
            category: [],
            cash_flow: [],
            cash_flow_01: [],
            debts: [],
            debts_summary: []
          },
          tabs: [
            { key: "all_expenses", label: "All Expenses" },
            { key: "monthly", label: "Monthly" },
            { key: "category", label: "Category" },
            { key: "cash_flow", label: "Cash Flow" },
            { key: "cash_flow_01", label: "Cash Flow 01" },
            { key: "debts", label: "Debts" },
            { key: "debts_summary", label: "Debts Summary" }
          ]
        };
      },
      computed: {
        categories() {
          const set = new Set();
          for (const row of this.tables.all_expenses || []) {
            if (row.Category) set.add(row.Category);
          }
          return Array.from(set).sort();
        },
        activeRows() {
          return this.displayedRows(this.activeTab);
        },
        activeColumns() {
          const rows = this.activeRows;
          return rows.length ? Object.keys(rows[0]) : [];
        }
      },
      methods: {
        displayedRows(tableKey) {
          const rows = this.tables[tableKey] || [];
          if (tableKey !== "all_expenses") return rows;
          return rows.filter((row) => {
            const catOk = !this.categoryFilter || row.Category === this.categoryFilter;
            const text = this.textFilter.toLowerCase();
            const hay = `${row.Description || ""} ${row.Category || ""} ${row["Sub-Category"] || ""}`.toLowerCase();
            const textOk = !text || hay.includes(text);
            return catOk && textOk;
          });
        },
        async loadReport() {
          const res = await fetch(`/data?year=${this.year}`);
          if (!res.ok) {
            const payload = await res.json().catch(() => ({}));
            throw new Error(payload.detail || "Failed loading report");
          }
          const payload = await res.json();
          this.meta = {
            base_url: payload.base_url,
            generated_at: payload.generated_at
          };
          this.tables = payload.tables;
        }
      },
      async mounted() {
        try {
          await this.loadReport();
        } catch (err) {
          console.error(err);
          alert(`Could not load report: ${err.message}`);
        }
      }
    }).mount("#app");
  </script>
</body>
</html>
"""


def enabled_handler(enabled: bool, nc: NextcloudApp) -> str:
    print(f"enabled={enabled}")
    if enabled:
        # nc.ui.resources.set_initial_state(
        #     "top_menu",
        #     "report",
        #     "expense-report_state",
        #     {
        #         "initial_value": "test init value",
        #         "initial_sensitive_value": "test_sensitive_value",
        #     },
        # )
        nc.ui.resources.set_script("top_menu", "report", "../../../../../nextcloud/index.php/apps/app_api/proxy/expense-report/js/expense-report-main")
        nc.ui.top_menu.register("report", "Expense Report", "img/app.svg")
        nc.log(LogLvl.INFO, "Expense report app enabled")
        print("Expense report app enabled")
    else:
        nc.log(LogLvl.INFO, "Expense report app disabled")
        print("Expense report app disabled")
    return ""


@asynccontextmanager
async def lifespan(app: FastAPI):
    set_handlers(app, enabled_handler)
    yield


APP = FastAPI(lifespan=lifespan)
# Public probes: /heartbeat is registered by set_handlers() and always exempt.
# Also exempt /health so Docker or admins can curl it without AppAPI headers.
APP.add_middleware(AppAPIAuthMiddleware)

# Serve static files (JS, CSS, icons, etc.)
APP.mount("/img", StaticFiles(directory="../img"), name="img")
APP.mount("/js", StaticFiles(directory="../js"), name="js")


@APP.get("/", response_class=HTMLResponse)
async def root_page():
    print("In root_page")
    return HTMLResponse(content=build_app_html())

@APP.get("/report", response_class=HTMLResponse)
async def report_page():
    print("In report_page")
    return HTMLResponse(content=build_app_html())


@APP.get("/data")
async def report_data(
    nc: Annotated[NextcloudApp, Depends(nc_app)],
    year: int | None = None,
):
    print("in data")
    report_year = year or datetime.today().year
    try:
        payload = await to_thread(get_report_payload, report_year)
        nc.log(LogLvl.INFO, f"Loaded report data for {report_year}")
        print(f"Loaded report data for {report_year}")
        return JSONResponse(content=payload)
    except Exception as exc:
        nc.log(LogLvl.ERROR, f"Failed to load report data: {exc}")
        print(f"Failed to load report data: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    run_app("main:APP", log_level="info")
