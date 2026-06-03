# expense_report

Nextcloud External App that renders an interactive annual expense report UI from
Nextcloud Tables data.

## Endpoints

- `GET /` - simple status payload.
- `GET /health` - container healthcheck endpoint.
- `GET /report` - Vue-based report UI (tabs, filters, year picker).
- `GET /report/data?year=2026` - report data API consumed by the UI.

## Required environment variables

None

## Optional environment variables

- `NC_FACTS_TABLE_ID` (default: `6`)
- `NC_DEBTS_TABLE_ID` (default: `10`)

## Local run

```bash
python -m pip install -r requirements.txt
cd ex_app/lib
python main.py
```

## Guides
Nextcloud Developer Guide: https://docs.nextcloud.com/server/latest/developer_manual/exapp_development/development_overview/ExAppOverview.html
Nextcloud and Vue: https://nextcloud-vue-components.netlify.app/
Material Design Icons: https://pictogrammers.com/library/mdi/
