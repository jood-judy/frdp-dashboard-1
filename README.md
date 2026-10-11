# FrPD Dashboard

A responsive, single-page Fire Protection Department data dashboard. **No backend, account, database, or data upload service.** Assessment workbooks stay in your browser's memory; charts and computations are rendered locally. Built with HTML, CSS and Vanilla JavaScript.

## Start

1. Extract the ZIP without separating `index.html` from the other files.
2. Open **`index.html`** in a modern browser (Chrome, Edge, Safari or Firefox). No web server is needed.
3. Click **Upload data** (or drag a file onto the page) and choose your assessment `.xlsx`, `.xls` or `.csv` file.
4. The Unit → Station list is built into `index.html` (the `#stationMaster` block). Edit it there to add or rename stations; set a unit's `"division"` to `WNA`, `WSA` or `CS` if you want it fixed, otherwise it is read from the uploaded data.
5. Filter by division, year or Unit → Station, explore linked KPIs/analytics and export filtered assessment rows.

**Libraries:** Offline-ready `Plotly` for interactive charts and `JSZip` for `.xlsx` fallback are included in this folder. The official SheetJS parser is loaded from its CDN when internet is available, to support `.xls` and more Excel variants. `.csv` and ordinary `.xlsx` files work offline with the bundled parser. If legacy `.xls` fails offline, connect to the internet to load SheetJS or convert the workbook to `.xlsx` or `.csv`. Google Fonts are optional; the interface has system font fallbacks. No uploaded file contents are sent to these CDNs.

## Assessment dataset

The header matcher tolerates extra whitespace, case changes, `Unit` / `Units`, and `Station` / `Stations`. Original names and field values are kept for table display and CSV export. Multiple rows per station are supported. The expected headings are:

| Required | Additional optional columns |
| --- | --- |
| Function | No. |
| Type | Reference |
| Control Measure | Applicability |
| Compliance | Verification Method |
| Division | Recommendation |
| Units | Comments |
| Stations | Hidden Column |
| Date | Visit ID / Tour ID / Event ID |

Supported `Function`: **Compliance, Operational Excellence, Safety, Safety Tour**. `Type` categories are taken directly from the uploaded file, not hard-coded or invented. Compliance is normalized to `Yes`, `No`, `N/A` and blank. Date supports genuine Excel serial dates, Excel date objects, date strings and the years 2026/2027.

### Station master

Minimum headers in a separate `.csv` / `.xlsx` / `.xls` file:

```csv
Division,Units,Stations
```

Populate one row per distinct, real station using verified names and its actual unit/division. Do not create artificial placeholder station names. An optional `Station Status` or `Visit Status` (`No`, `Not Visited`, `Unvisited`) may explicitly mark an unvisited station; optional `Status Year` scopes that flag to a year. The original dataset's `Hidden Column` can also carry a delimited list of unvisited station names. Such names are matched exactly after whitespace/case normalization. Ambiguous or unknown names are reported rather than assigned to a unit.

Coverage totals and percentages require **27 unique mapped stations, 11 Division–Unit combinations, and no assessment station identity absent from the master**. Without verified mapping these KPIs show `N/A`. Tree filtering uses the master list including unvisited stations. Without it, only observed stations can appear (provisional).

## Metric definitions and important interpretation

- **Station coverage / Visit completion:** Unique qualifying assessed station identities ÷ authoritative scoped master station count × 100. A station identity is the normalized *Division + Unit + Station*; similarity alone never merges two stations. No physical visit is inferred from a row. The Quality Assurance widget is therefore explicitly marked as an **assessment-coverage proxy**. Choose `Any assessment` or `Compliance only` as its qualifying function; the provided `Function` vocabulary has no separate `Quality Assurance` value.
- **Safety tours / Operational excellence events:** Distinct events per normalized Visit ID / Tour ID / Event ID, scoped by year, division and function. If a relevant assessment row lacks an event ID, the actual event count is `N/A` and the assessment-item count is displayed as supporting context. If no rows match, the count is zero once a file has been loaded.
- **Compliance rate:** `Function = Compliance`, then `Yes ÷ (Yes + No) × 100`. **Non-compliance rate:** the same `Function = Compliance` scope, then `No ÷ (Yes + No) × 100`. The listed `Function` categories contain **no** `Non-Compliance` category, so a direct filter for it would always be empty. Both rates exclude `N/A`, blank and unknown status values.
- **Safety rate:** `Function = Safety` or `Safety Tour`, then `Yes ÷ (Yes + No) × 100`. N/A, blank and unknown status values are excluded; shows `N/A` when no Yes/No records exist in scope.
- **Competence indicators:** Yes versus No in assessment `Type = Interview` or `On Job Readiness`, excluding N/A/blank. This is an explicitly named proxy for competence since there is no dedicated `Competence` column.
- **Items by type:** Assessment **row** counts grouped by their actual Type values.
- **Top non-compliance item types:** Count rows with `Compliance = No`, group by Type and show available comments and affected stations/divisions.
- **Top repeated non-compliant control measures:** Count `Compliance = No` rows grouped by exact normalized Control Measure, with comments, station and division counts. The top five represent **frequency, never invented severity**.
- **Data table:** All original assessment fields, sortable headers, text search, status filter, pagination, expanded comments/recommendations, and scoped CSV export.

Invalid/unmapped records remain visible in the unfiltered assessment table, with data-health warnings. Year-specific filters include only the selected year; the default *All records* view includes uploaded rows even if their year is invalid, making errors inspectable. Blank Applicability and blank Compliance are independent fields.

## Files and maintenance

- `index.html`: app structure and accessible controls.
- `fire-1.jpg`: hero banner photo (shown semi-transparent behind the page title; replace the file to change it).
- `#stationMaster` in `index.html`: the unit → station list used for coverage and the filter tree.
- `styles.css`: FrPD-provided cream / charcoal / muted-red visual design, mobile breakpoints and reduced-motion support.
- `data.js`: parsers, normalization, validation, hierarchy, formulas and CSV export.
- `charts.js`: responsive Plotly charts.
- `app.js`: event handlers, connected filters, KPIs, tables and import flow.
- `dashboard.js`: classic-script bundle so `index.html` opens directly without a local server.
- `plotly.min.js` / `jszip.min.js`: browser-side dependencies.
- `build.py`: rebuilds `dashboard.js` after editing its three source files (`python build.py`). Python is only a build convenience; it is **not used when the dashboard runs**.

No fictional sample records or station names have been inserted into the dashboard.


## Publish on GitHub Pages

All files sit in one flat folder. Upload them to the root of a repository, then go to **Settings → Pages**, choose the `main` branch and `/ (root)`, and open the published link.
