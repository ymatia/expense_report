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
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from nc_py_api import AsyncNextcloudApp  # , execute_fetchall
from nc_py_api.ex_app import AppAPIAuthMiddleware, LogLvl, nc_app, run_app, set_handlers
from fastapi.staticfiles import StaticFiles

# pd.options.future.infer_string = False  # resolve issue in Pandas 3.0 of exact type casting

def _request_json(url: str, payload: dict[str, Any] = None) -> list[Any]:
    global session
    nc_url = os.environ["NEXTCLOUD_URL"]
    headers = {
        "OCS-APIRequest": "true",
        'accept': 'application/json',
    }

    if payload is None:
        r = session.get(f"{nc_url}{url}", headers=headers, timeout=60)
    else:
        r = session.post(f"{nc_url}{url}", headers=headers, json=payload, timeout=60)

    if r.status_code not in (200, 201, 204):
        raise RuntimeError(f"Request failed ({r.status_code}) for {nc_url}{url}: {r.text}")
    return json.loads(r.text)


def _fetch_selection_values(table_id: int) -> tuple[dict[int, str], dict[int, str]]:
    columns_url = f"/apps/tables/api/1/tables/{table_id}/columns"
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
    rows_url = f"/apps/tables/api/1/tables/{table_id}/rows/simple"
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
    df["Amount"] = df["Amount"].astype(float)

    debts_df.dropna(inplace=True)
    debts_df["How much €"] = debts_df.apply(lambda row: float(row["How much €"]), axis=1)

    df["Month"] = df.apply(
        lambda row: row["Date"][:7] if row["Date"] is not None and isinstance(row["Date"], str) else row,
        axis=1,
    )

    monthly = df.where(df["Category"] == "Actual")  # Filter to include only Actual
    monthly = monthly[["Month", "Sub-Category", "Amount"]].groupby(["Month", "Sub-Category"], as_index=False).sum()  # Group by
    monthly = monthly.pivot_table(columns="Sub-Category", index="Month", aggfunc="sum", fill_value=0)
    print(monthly)  # Debug
    print(monthly.dtypes)  # Debug
    monthly["Sum"] = monthly[list(monthly.columns)].sum(axis=1)
    monthly.loc["Average"] = monthly.mean()
    monthly = monthly.reset_index()
    monthly.columns = [' '.join(header).replace("AMOUNT","").rstrip().title() for header in monthly.columns if header != ""]  # cleanup the headers
    monthly = monthly.round(0)  # Round the numbers

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
    report_dict = _to_records(report["monthly"])
    report_headers_dict = { 
        "headers": [ {"text": x, "value": x} for x in report["monthly"].columns ],
        "items": report_dict
    }
    json_obj = json.dumps(report_headers_dict, indent=4, sort_keys=True, default=str)
    return json_obj
    # return {
    #     "year": year,
    #     "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     "tables": {
    #         "all_expenses": _to_records(report["all_expenses"]),
    #         "monthly": _to_records(report["monthly"]),
    #         "category": _to_records(report["category"]),
    #         "cash_flow": _to_records(report["cash_flow"]),
    #         "cash_flow_01": _to_records(report["cash_flow_01"]),
    #         "debts": _to_records(report["debts"]),
    #         "debts_summary": _to_records(report["debts_summary"]),
    #     },
    # }


def enabled_handler(enabled: bool, nc: AsyncNextcloudApp) -> str:
    print(f"enabled={enabled}")
    if enabled:
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
APP.add_middleware(AppAPIAuthMiddleware)

# Serve static files (JS, CSS, icons, etc.)
APP.mount("/img", StaticFiles(directory="../img"), name="img")
APP.mount("/js", StaticFiles(directory="../js"), name="js")

@APP.get("/reelusage")
async def report_reelusage(request: Request, year: int | None = None):
    query = """select ct.value as REEL, sum(cn.value) as USAGE
        from oc_tables_tables t
        join oc_tables_columns cr on cr.table_id=t.id and cr.title='Reel'
        join oc_tables_columns cw on cw.table_id=t.id and cw.title='Weight'
        join oc_tables_row_cells_text ct on ct.column_id=cr.id
        join oc_tables_row_cells_number cn on cn.column_id=cw.id and cn.row_id=ct.row_id
        where t.title='3D Printing Log'
        group by 1 order by 1 desc"""
    # data = execute_fetchall(query)
    # headers = [{"text": "Reel", "value": "REEL"}, {"text": "Reel Usage (g)", "value": "USAGE"}]
    # response_dict = {"headers": headers, "data": data}
    # json_obj = json.dumps(response_dict, indent=4, sort_keys=True, default=str)
    # return json_obj


@APP.get("/data")
async def report_data(request: Request, year: int | None = None):
    global session
    # Store the current cookies for future REST API calls
    cookies_str = request.headers.get("Cookie")
    cookies_arr = cookies_str.split("; ")
    cookies = {x.split("=")[0]:x.split("=")[1] for x in cookies_arr}
    session = requests.Session()
    session.cookies.update(cookies)

    # default for report_year
    report_year = year or datetime.today().year
    
    # Fetch the data and reply back
    # try:
    payload = await to_thread(get_report_payload, report_year)
    # nc.log(LogLvl.INFO, f"Loaded report data for {report_year}")
    print(f"Loaded report data for {report_year}")
    print(payload)
    return payload
    # except Exception as exc:
    #     # nc.log(LogLvl.ERROR, f"Failed to load report data: {exc}")
    #     print(f"Failed to load report data: {exc}")
    #     raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    run_app("main:APP", log_level="info")
