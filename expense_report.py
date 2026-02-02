import requests
import pandas as pd
import numpy as np
import json
import datetime
import math
import os

year = 2026

if __name__ == "__main__":
    # Get credentials from environment variables
    username = os.getenv('NC_USERNAME')
    password = os.getenv('NC_PASSWORD')
    local_filename = f"expense_report_{year}.xlsx"

    # Fetch the list of values
    columns_res = requests.get("https://peacemountain.eu/nextcloud/index.php/apps/tables/api/1/tables/6/columns", auth=requests.auth.HTTPBasicAuth(username, password))
    if columns_res.status_code in (200, 201, 204):
        print(f"Columns fetched successfully")
    else:
        print(f"Failed to fetch columns. Status code: {columns_res.status_code}")
        print(columns_res.text)
        exit(1)
    columns = json.loads(columns_res.text)
    categories = {}
    sub_categories = {}
    for col in columns:
        if col["title"] == "Category":
            for cat in col["selectionOptions"]:
                categories[cat["id"]] = cat["label"]
        if col["title"] == "Sub-Category":
            for cat in col["selectionOptions"]:
                sub_categories[cat["id"]] = cat["label"]
    
    # Fetch the facts
    facts_res = requests.get("https://peacemountain.eu/nextcloud/index.php/apps/tables/api/1/tables/6/rows/simple", auth=requests.auth.HTTPBasicAuth(username, password))
    if facts_res.status_code in (200, 201, 204):
        print(f"Facts fetched successfully")
    else:
        print(f"Failed to fetch facts. Status code: {facts_res.status_code}")
        print(facts_res.text)
        exit(1)
    facts = json.loads(facts_res.text)


    # load into a dataframe
    df = pd.DataFrame(np.vstack(facts[1:]), columns=facts[0])

    # filter to current year
    df.where(df["Date"].str.startswith(f"{year}"), inplace=True)

    # remove NaN values
    df.dropna(inplace=True)
        
    # Sort by date
    df.sort_values("Date", inplace=True)
    
    # fill NaN with 0
    df['Category'] = df['Category'].fillna(0)
    df['Sub-Category'] = df['Sub-Category'].fillna(0)
        
    # Join list-of-values
    df['Category'] = df.apply(lambda x: categories[int(x['Category'])], axis=1)
    df['Sub-Category'] = df.apply(lambda x: sub_categories[int(x['Sub-Category']) if x['Sub-Category'] else 0], axis=1)
    df['Amount'] = df.apply(lambda x: float(x['Amount']), axis=1)

    # Fetch the debts table
    debts_res = requests.get("https://peacemountain.eu/nextcloud/index.php/apps/tables/api/1/tables/10/rows/simple", auth=requests.auth.HTTPBasicAuth(username, password))
    if debts_res.status_code in (200, 201, 204):
        print(f"Debts fetched successfully")
    else:
        print(f"Failed to fetch debts. Status code: {debts_res.status_code}")
        print(debts_res.text)
        exit(1)
    debts = json.loads(debts_res.text)
    debts_df = pd.DataFrame(np.vstack(debts[1:]), columns=debts[0]) 
    debts_df.dropna(inplace=True)  # remove NaN values
    debts_df['How much €'] = debts_df.apply(lambda x: float(x['How much €']), axis=1)

    with pd.ExcelWriter(local_filename, engine='xlsxwriter') as writer:
        sheet_name = 'All Expenses'
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        for i in range(len(df.columns)):
            writer.sheets[sheet_name].set_column(i, i, 10)
        writer.sheets['All Expenses'].set_column(2, 2, 15)
        writer.sheets['All Expenses'].set_column(4, 4, 50)

        # Add calculated month column
        df["Month"] = df.apply(lambda x: x['Date'][:7] if x['Date'] is not None and isinstance(x['Date'], str) else x, axis=1)

        # Group by month, category and sub-category
        sheet_name = 'Monthly'
        df1 = df.where(df["Category"] == "Actual")
        df1 = df1[["Month", "Sub-Category", "Amount"]].groupby(["Month", "Sub-Category"], as_index=False).sum()
        df1 = df1.pivot_table(values="Month", columns="Sub-Category", index="Month", aggfunc="sum", fill_value=0)
        #df1 = df1.sort_values("Month")
        df1['sum'] = df1[list(df1.columns)].sum(axis=1)
        df1.loc['Average'] = df1.mean()  # add a row for average
        df1.to_excel(writer, sheet_name=sheet_name)
        for i in range(len(df1.columns)):
            writer.sheets[sheet_name].set_column(i, i, 10)
 
        # Group by category / sub-category
        sheet_name = 'Category'
        df2 = df[["Category", "Sub-Category", "Amount"]].groupby(["Category", "Sub-Category"], as_index=False).sum()
        df2.to_excel(writer, sheet_name=sheet_name, index=False)
        for i in range(len(df2.columns)):
            writer.sheets[sheet_name].set_column(i, i, 15)

        # Cash flow
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        last_day = (datetime.datetime.today() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        df3 = df.where((df['Date'] >= today) & (df['Date'] <= last_day))
        df3 = df3[["Date","Description","Amount"]]
        df3.dropna(subset=['Date'], inplace=True)
        sheet_name = 'Cash Flow'
        df3a = df3.query(r'not(Description.str.contains("\\(01\\)") or Description.str.contains("\\(DKB\\)") or Description.str.contains("\\(Praxis\\)"))')
        df3a.to_excel(writer, sheet_name=sheet_name, index=False)
        for i in range(len(df3a.columns)):
            writer.sheets[sheet_name].set_column(i, i, 15)
        for i in range(len(df3a)):
            writer.sheets[sheet_name].write_formula("D" + str(i+2), "=D" + str(i+1) + "-C" + str(i+2))
        sheet_name = 'Cash Flow 01'
        df3a = df3[df3["Description"].str.contains("\\(01\\)")]
        df3a.to_excel(writer, sheet_name=sheet_name, index=False)
        for i in range(len(df3a.columns)):
            writer.sheets[sheet_name].set_column(i, i, 15)
        for i in range(len(df3a)):
            writer.sheets[sheet_name].write_formula("D" + str(i+2), "=D" + str(i+1) + "-C" + str(i+2))
        # Debts
        sheet_name = 'Debts'
        debts_df.to_excel(writer, sheet_name=sheet_name, index=False)
        for i in range(len(debts_df.columns)):
            writer.sheets[sheet_name].set_column(i, i, 15)
        # Total debts by Name
        sheet_name = 'Debts Summary'
        debts_df_total = debts_df[["Who","How much €"]]
        debts_df_total = debts_df_total.groupby("Who", as_index=False).sum()
        debts_df_total.to_excel(writer, sheet_name=sheet_name, index=False)
        for i in range(len(debts_df_total.columns)):
            writer.sheets[sheet_name].set_column(i, i, 15)  # set column width to 15

    # Upload the generated Excel file to Nextcloud using WebDAV
    # Base Nextcloud URL and WebDAV path can be overridden via environment variables if needed
    base_url = os.getenv("NC_BASE_URL", "https://peacemountain.eu/nextcloud")
    webdav_path = os.getenv("NC_WEBDAV_PATH", f"remote.php/dav/files/{username}")

    # Folder inside your Nextcloud account where the report will be stored
    # Make sure this folder already exists in Nextcloud
    upload_dir = os.getenv("NC_UPLOAD_DIR", "Documents")

    if upload_dir:
        remote_path = f"{upload_dir}/{local_filename}"
    else:
        remote_path = local_filename

    upload_url = f"{base_url.rstrip('/')}/{webdav_path.strip('/')}/{remote_path}"

    try:
        with open(local_filename, "rb") as f:
            upload_res = requests.put(upload_url, data=f, auth=requests.auth.HTTPBasicAuth(username, password))

        if upload_res.status_code in (200, 201, 204):
            print(f"Excel report uploaded successfully to Nextcloud at: {upload_url}")
        else:
            print(f"Failed to upload Excel report to Nextcloud. Status code: {upload_res.status_code}")
            print(upload_res.text)
    except Exception as e:
        print(f"Error uploading Excel report to Nextcloud: {e}")