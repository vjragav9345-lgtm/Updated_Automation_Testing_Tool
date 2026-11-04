# No Warnings on the Dashboard – Report

Backups: `_backup_no_warning_dashboard/frontend/static/js/script.js`,
`_backup_no_warning_dashboard/frontend/templates/index.html`.

## 1. Every place on the dashboard where a warning could appear

`frontend/static/js/script.js` is loaded **only** by the dashboard (`index.html`). Every warning the dashboard
shows is drawn there:

| # | Place | Where it was drawn |
|---|---|---|
| 1 | Yellow **"Warning"** result badge left of the test name | `_setCardBadge` (outcome `warning` from `_outcomeOfResult`, or `last_result.outcome` from `/api/recordings`) |
| 2 | **"· N warning(s)"** at the end of the card summary under TEST PASSED/FAILED | `renderResultSummary` (`warningCount`) |
| 3 | **"· N locator warning(s)"** in the same summary line | `renderResultSummary` (`locatorWarnings`) |
| 4 | **⚠ icon + amber colour** on a validation card (after Replay / View Last Log on the card) | `renderValidationPanel` (`validation-card-warning`) |
| 5 | **⚠️ icon + amber row** in "Show all steps" | `renderValidationPanel` (`validation-step-row-warning`) |
| 6 | **Warning note text** under a step in "Show all steps" | `renderValidationPanel` (`validation-step-warning`) |
| 7 | **"Warnings: N"** counter in the replay progress shown on the card while a run is going | `renderReplayProgress` |
| 8 | **⚠ icon + amber** step icon in that progress list | `renderReplayProgress` (`step-warning`) |
| 9 | **Warning note text** under a step in that progress list | `renderReplayProgress` |
| 10 | Warning fields in the **Raw Result** box (whatever an API answer contains) | `callApi` → `resultOutput` |

Checked and **no warning shown**: folder list items / opened-folder breadcrumb (name + test count only), Play
All panel messages (Passed / Failed / Stopped / Not run only), the recording status banner, `index.html`,
`run_control.js`, `remote_view.js`, the run message text (`result.message` never contains warning text). There
are no tooltips with warnings.

## 2. Every line changed (`frontend/static/js/script.js`, new line numbers)

| Line | Old → New |
|---|---|
| 239 | `JSON.stringify(data, null, 2)` → `JSON.stringify(data, _withoutWarningFields, 2)` (Raw Result hides keys containing "warn"; the data itself is untouched) |
| 1593-1599 | `_setCardBadge`: added – outcome `warning` → badge emptied and hidden (no other badge shown); every other outcome un-hides it and draws it exactly as before |
| 1638-1649 | added `_dashOutcome(step)` (a `warning` step is drawn as `pass`) and `_withoutWarningFields` |
| 1727-1728 | removed the two `statsParts.push(... warning ...)` blocks (with their "·" separator, since parts are joined by " · "); replaced by a comment. `warningCount` / `locatorWarnings` still computed |
| 1771 | validation card `_stepOutcome(step)` → `_dashOutcome(step)` |
| 1831 | "Show all steps" row `_stepOutcome(step)` → `_dashOutcome(step)` |
| 1872 | `if (step.warning)` → `if (step.warning && false)` (warning note not drawn) |
| 1955 (old 1939) | removed the `"Warnings: N"` span from the progress counts |
| 1977 | progress step icon `_stepOutcome(stepResult)` → `_dashOutcome(stepResult)` |
| 2001 | `if (stepResult && stepResult.warning)` → `... && false` (warning note not drawn) |

`frontend/templates/index.html:395`: `script.js?v=30` → `?v=31`, so the browser loads the new file.

The Passed / Failed / Stopped / Not run badges, TEST PASSED / TEST FAILED box, the other summary-line parts
(steps executed, actions passed, validations passed, failed, not run, manual-input), the progress counts
Passed / Failed / Not run / Manual-input / Elapsed (same numbers as before), cards, folders and every button are
unchanged. All of these drawing paths are the only ones used on first load, refresh, opening a folder, single
Replay, Play All and Stop, so a warning cannot come back.

## 3. Nothing outside the dashboard display changed

- No backend, API, API response, report.json, replay engine, `live_log.html`, `run_control.js`, other pages or
  result calculation changed.
- `style.css` (shared with the live log, editor, run stages, screenshots viewer) was **not** changed. The
  warning CSS classes are kept and simply no longer used by the dashboard.
- `_stepOutcome`, `_plainWarningText`, `_outcomeOfResult`, `CARD_OUTCOME_LABELS` are unchanged.
- Warnings still appear in the live log, the HTML report, report.json, run stages, screenshots viewer and
  Export CSVs.

## 4. Syntax check

`node --check frontend/static/js/script.js` → OK. No inline script in `index.html` was changed.

## 5. Test checklist

- [ ] A passed-with-warnings card: no "Warning" badge, no "· N warning" text; everything else the same
- [ ] No warning anywhere else on the dashboard: folder items, Play All messages, "Show all steps", replay progress, Raw Result
- [ ] The live log for the same run still shows the warning
- [ ] A failed test card looks exactly as before
- [ ] Still hidden after refresh, opening a folder, single Replay, Play All and Stop
