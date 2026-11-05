# Flaky PAGE_MISMATCH, Failure Card, Export – Report

Backups: `_backup_flaky_export/` (8 files, same relative paths). Nothing was run except `py_compile`,
`node --check`, a template render into a scratch folder outside the project (deleted), and read-only dry checks
that call the destination / export helpers on files from `data/`.

Files changed: `backend/feature_flags.py`, `backend/generator/script_generator.py`,
`backend/recorder/record_session.py`, `backend/storage/repository.py`, `app.py`,
`frontend/templates/live_log.html`, `frontend/static/js/script.js`, `frontend/templates/index.html`.

---

## 1. Phase 1 root cause (plain English)

**Important evidence note:** the recording `session_20261104_105644`, its edited copy and their run folders are
**no longer in `data/`**. No `report.json` on disk contains the `/pricing` → `/notification` mismatch any more.
The `sportiza` folder now holds `session_20261104_182218`, `session_20261104_182701` and
`session_20261105_103040`. In all three, the Notification click is recorded correctly (`post_click.url_path_after`
= `/notification`, `navigated: true`). So the cause below is proven **from the code and from the exact failure
text** you quoted, not from the deleted run files.

**What makes "/pricing" the expectation.** The message "The recording reached '/pricing', but the browser went
to '/notification'" is built by `_page_mismatch_message` (`script_generator.py`, called from `_compare_post_click`).
The expectation itself comes from `_expected_post_click_destination` (`script_generator.py:7168`). When a click's
recorded `post_click.url_path_after` equals its `url_path_before`, and there is no `expected_url` and no link href,
it returns `("none", <url_path_before>)`. In plain words: "this click did not change the page, so the page must
stay `/pricing`" – which is the page the click **started** on.

**Why the recording said "no page change" (recorder).** The Notification click was the **last** step of that
recording. A route change that comes a moment after the click is credited to it by the page-side late-navigation
watch (`action_capture.js:4754-4808`) or by the navigation event (`record_session.py:1200-1262`). Both only work
while the recording is still running. When the recording is stopped with **Stop Recording / ENTER** right after
the last click, that credit never arrives, and the click is saved with `url_path_after` = the start page. The
existing "result unknown" safety rule only covered a **closed browser** (`stop_reason == "browser_closed"`), not
the other stop methods. The hover before the click is **not** the cause: hovers are skipped when linking a
navigation to its click (`record_session.py:1105-1137`) and don't end the late-navigation watch
(`action_capture.js:4945-4948`).

**Why it is flaky (replay).** For a `"none"` expectation, `_compare_post_click` calls `_settle_click_navigation`
(`script_generator.py:7134`). It waits only `CLICK_NAV_START_WAIT_S = 0.4` s (`:7084`) for a navigation to start:
- the site starts its route change **later** than 0.4 s → the URL still reads `/pricing` → "matches" → **PASS**;
- the site starts it **within** 0.4 s → the URL reads `/notification` → `nav_watch` is true → **PAGE_MISMATCH**.

So the same recording passes or fails depending on how fast the site is that time.

**Checked and not the cause:** (b) hover ordering – see above. (c) `migrate_expected_urls` only folds Navigate
steps that follow an action; it could in theory fold a Navigate back to the action's own page (now guarded).
(d) The editor saves the recording it received from `/api/recordings/view` as-is, so per-step `post_click` /
`result` / `expected_url` stay attached to their own step object. Nothing shifts between steps; an edited copy
just inherits the original's (wrong) last-click result. That one is now fixed in memory too (see 2.1).

---

## 2. Changes per phase

### 2.1 Phase 1

| Where | Old → New |
|---|---|
| `record_session.py:1819-1832` (`stop()`) | "result unknown" for the last click only when the **browser was closed** → for **every** stop (closed, Stop Recording, ENTER, error). Same 10 s (+2 s) window, same "no new tab / no navigation seen yet" condition |
| `repository.py:275-277` (`migrate_expected_urls`) | a following Navigate to the action's **own start page** could become its `expected_url` → never |
| `repository.py:393-448` | **new** `_unknown_result_timestamp` + `mark_unknown_last_click_result`: in memory, for **old recordings**. Uses `recorded_at` (stop time) and the last click's timestamp; same rule as the recorder. An edited copy (no `recorded_at`) takes the answer from its original recording, matched by the step timestamp. Nothing on disk is rewritten |
| `repository.py:451` | `migrate_recording` runs it first |
| `script_generator.py:7188-7190` | an `expected_url` equal to the click's start page is **ignored** (falls through to the next evidence) |
| `script_generator.py:7209-7216` | "none" (no page change) → if the **next recorded step** was made on another page, that page is the expectation (`"next_page"`), never the start page |
| `script_generator.py:7220-7240` | **new** `_next_page_evidence`: the next step's `page_url` (same tab), or the address of a Navigate this click caused. A typed address / Back / another tab / tab step gives no evidence |
| `script_generator.py:7500, 7521, 7685` | `"next_page"` joins the destination kinds: wait **by event** until the URL matches (bounded by `EFFECT_VERIFY_TIMEOUT_S`), accept a recorded redirect chain, ignore old-page focus after navigating |
| `script_generator.py:7565-7569` | `"next_page"` and still on the start page after the wait → not a failure of this click (the next step's own page check decides) |
| unchanged | a click whose expected page is X that lands on a different page Y (after the URL settled) is still **PAGE_MISMATCH** with its exact reason; the dynamic-URL rules; the existing unknown-result acceptance (`:7542`); locator matching |

**Determinism (C).** With the evidence fixed, the timing-sensitive `"none"` check is only used when the recording
really shows the user stayed on the same page. A click whose real result went to another page now has a
destination expectation (checked by waiting for the URL, so timing doesn't matter) or an unknown result (either
outcome accepted). Both give the same verdict on fast and slow runs.

### 2.2 Phase 2 – failure card paused

| Where | Old → New |
|---|---|
| `backend/feature_flags.py:37-42` | **new** `FAILURE_PAUSE_CARD_ENABLED = False` with how-to comment |
| `script_generator.py:4192` | template constant, filled at `:31365` |
| `script_generator.py:30334` | the failure ("fallback") card trigger → also needs `FAILURE_PAUSE_CARD_ENABLED` |
| `script_generator.py:30271` | the "form could not be corrected" `step_failed` card → also needs the flag |
| `app.py:4947` | `/logs` passes `failure_pause_card_enabled` |
| `live_log.html:335` | flag constant |
| `live_log.html:1099-1101` | a `step_failed` pause event is ignored (no card, no "Paused - waiting for you"); pause token/step cleared so nothing is remembered |
| unchanged | `_pause_and_ask`, `pause_answer.json`, `/api/test/run/pause/answer`, OTP / Retry / already-exists flags |

With the flag off, a failed step is FAILED with its plain + exact reason and screenshot link, then
stop-on-failure applies (remaining steps NOT RUN) – the same path as "no card answered" before.

### 2.3 Phase 3 – export

| Where | Old → New |
|---|---|
| `script.js:2711-2714` | Export sent the opened folder's / ticked tests → **always every session** (`paths: []` → server exports everything `repository.list_recordings()` lists: all folders, ungrouped, edited copies). Play All ticks unchanged |
| `index.html` | `script.js?v=31` → `?v=32` |
| `app.py:4651-4658` | **new** `_EXPORT_LIVE_LOG_COLUMNS`: Folder, Session, Session file name, Run folder, Time, Step, Level, Message (older columns kept), Row type, Step name, Action, Status, Started, Ended, Duration (s), Locator / how found, Plain reason, Exact reason, Screenshot file |
| `app.py:4660-4666` | **new** `_export_note_row` |
| `app.py:4668-4766` | **new** `_export_live_log_rows`: steps completed with `run_execution._complete_steps` (the same list the dashboard card shows), merged with the `live_log` lines by time exactly like `/api/test/run/stream`; one `step` row per step (status via `_step_display_status`, `STOPPED BY USER` like the live log, label via `_step_element_label`, reasons via `_step_failure_reason` / `_step_exact_reason`, "how found" from `locator_report`), `failed` / `warning` / `info` rows under it, `note` / `info` rows for log lines, one `summary` row. OTP / password values are masked in every text |
| `app.py:4819` | folder of each session (`Ungrouped` when none) |
| `app.py:4831-4914` | each session is exported inside its own `try`: an unreadable report or any error adds a `note` row and the export continues |
| `app.py:4846-4848` | screenshots → `screenshots/<folder or Ungrouped>/<session>/…` |
| `app.py:4879` | never-replayed session → "Not run yet" |
| sessions.csv / steps.csv | **Folder** column added first; every other column unchanged |
| live_logs.csv | `app.py:4926` writes the new columns |

---

## 3. The new flag

`backend/feature_flags.py:42` – `FAILURE_PAUSE_CARD_ENABLED = False`. Set it to `True` and restart the app. The
next replay's generated script then gets `FAILURE_PAUSE_CARD_ENABLED = True`. With `True`, every changed condition
reduces to the old one (`… and True`, `… or not True`), and the live-log guard is skipped.

All four pause flags are off: `OTP_LIVE_ENTRY_ENABLED`, `LIVE_LOG_RETRY_ENABLED`, `ALREADY_EXISTS_PAUSE_ENABLED`,
`FAILURE_PAUSE_CARD_ENABLED` (checked). A template render with all four `True` also compiles.

---

## 4. Dry-check results (Phase 4)

**Static:** `py_compile` OK for the 5 changed Python files (the old `\d` warning at `script_generator.py` ~1604
is pre-existing). `node --check script.js` OK. `live_log.html` rendered with all flags false and all true, inline
script `node --check` OK. No `$` added to the template except the new placeholder. A script generated from
`data/recordings/sportiza/session_20261105_103040.json` compiled, with the flags off and on. Scratch files deleted.

**Expected destination, old → new** (read from the JSON, no replay):

| Recording | Click step | Old | New |
|---|---|---|---|
| sportiza/session_20261104_182218 | 2 Events · 3 (event card) · 5 (event card) | recorded /events · recorded /events/anti-drug… · recorded /events/gagner… | same |
| sportiza/session_20261104_182701 | 2 Accept | none /feed | none /feed |
| | 3 Events · 4 card · 5 Pricing · 6 Notification · 8 Back | recorded /events · /events/larsen… · /pricing · /notification · /events/larsen… | same |
| | 7 (icon) · 11 Register For Free · 12 (icon) | none /notification · none /events/larsen… · none /events/larsen… | same |
| sportiza/session_20261105_103040 | 4 Events · 5 Pricing · 6 Notification | recorded /events · /pricing · /notification | same |
| synthetic copy of the reported case (Notification = last click, no page change recorded, ENTER 3 s later) | last click | **none /pricing** (flaky) | none, `result_unknown = true` → either outcome accepted |
| same click, followed by a step made on /notification | click | **none /pricing** | **next_page /notification** |

**Export** (helpers only, no server):

| Run folder | Steps in report.json | Step rows in live_logs.csv | Other rows |
|---|---|---|---|
| session_20261105_103040_20261105_103120 | 6 | 6 (all PASS) | 11 note, 3 info, 1 summary |
| session_20261104_182701_20261104_182748 | 13 | 13 (12 PASS, 1 WARNING) | 31 note, 8 info, 1 warning, 1 summary |
| session_20261103_111917_20261104_093650 (stopped) | 17 | 17 (3 PASS, 1 STOPPED BY USER, 13 NOT RUN) | summary "Stopped by the user. …" |

All 13 dashboard sessions are listed for export (folders: Ungrouped, myntra, sportiza, test).

---

## 5. Choices where the requirement was ambiguous

- The deleted session could not be read; the cause is proven from code and the error text.
- **"next_page" is softer than a recorded destination:** if the replay stays on the start page, this click is not
  failed – the next step's own page check decides. Landing on a third page still fails.
- `migrate_recording` does **not** write a new `expected_url` from the next step. The next-page rule lives in the
  replay, so the editor never saves a guessed destination into a file.
- "Result unknown" applies only to the **last** click-type step, stopped within 12 s.
- Edited copies without `recorded_at` take the stop time from their original recording file (matched by step
  timestamp); if the original no longer exists, nothing changes.
- The `step_failed` "form could not be corrected" card (only reachable with the paused field-error feature) is
  also covered by the new flag.
- `live_logs.csv` also includes the "↳ …" sub-lines (row type `note`). The live log window hides them, but the
  report's step Details show them – you asked for every line.
- steps.csv still uses the raw `report.json` steps (unchanged behaviour); live_logs.csv uses the completed list.
- Masking in live_logs.csv replaces masked values of 3+ characters, so short values like a single digit don't
  wipe unrelated text.

---

## 6. Test checklist

- [ ] Replay the Sportzia test 5 times: same result every time
- [ ] A click that goes to a different page passes when that is where the recording went next
- [ ] A real wrong page still fails with an exact reason
- [ ] No "Step failed (paused)" card, no "Accept this page and continue", no "Paused - waiting for you"
- [ ] Export with a folder open: the ZIP still has every folder and session (screenshots under `screenshots/<folder>/<session>/`)
- [ ] live_logs.csv has one row per step (same count as the card) plus notes, with status, times and reasons
- [ ] OTP and passwords are still masked in the CSVs
- [ ] Record a click as the last step, stop with ENTER right away, replay: it passes whether the page changes or not
