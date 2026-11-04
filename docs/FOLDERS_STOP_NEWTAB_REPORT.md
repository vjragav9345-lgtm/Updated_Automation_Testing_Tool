# Folders, Stop, New-Tab – Report

Backups (original content, same relative paths): `_backup_folders_stop_newtab/`. No files were moved, nothing
was run except `py_compile`, `node --check`, a Jinja render of the two templates and a script render into a
scratch folder (deleted afterwards).

Files changed: `app.py`, `backend/executor/run_execution.py`, `backend/generator/script_generator.py`,
`backend/recorder/record_session.py`, `frontend/static/js/script.js`, `frontend/templates/index.html`,
`frontend/templates/live_log.html`, `frontend/static/css/style.css`.
(`run_control.js` and `repository.py` were backed up but needed no change.)

---

## 1. Changes per phase

### Phase 1 – Folder view on the dashboard

| Where | Old → New |
|---|---|
| `app.py:1026` `/api/recordings` | → new optional field `folders` (every folder on disk, empty ones included). Existing fields unchanged |
| `app.py:2949` `/api/browser/launch` | → the validated folder is created on disk as soon as the launch is accepted, so it shows with "0 tests" at once. Validation/saving of the name unchanged |
| `script.js:917-1130` | the folder sections (previous change) → **folder list**: one item per folder (📁 icon, name, "N tests") plus **"Ungrouped tests"** when old recordings exist. Click → **opened folder**: "← Back to folders" + breadcrumb "Recorded Tests / <folder> (N tests)", a toolbar (Select All, Play All, Stop All) and only that folder's cards, paginated (10 per page) |
| `script.js:927-985` | open folder kept in the page address `#folder=<name>` (try/catch, `history.replaceState`); restored on load (`:852`); a folder that no longer exists falls back to the list |
| `script.js:988` `_placeScopedControls` | the **existing** Select All checkbox and Play All button (same elements, same handlers) are moved into the opened folder's toolbar; with no folder open they are back in the header, hidden (`index.html:159`, `style.css:1751`) |
| `script.js:2388, 2400, 2421` | Select All / card selection / `_chosenRecordings` → scoped to the opened folder only |
| `script.js:2539` Play All | → runs the opened folder's selected tests (or all of them), in folder order, through the same `runPlayAll` + `/api/play_all/*` |
| `script.js:2696` Export | → inside a folder: its selected tests, or all of them; no folder open: export all (as before) |
| `script.js:339` | after a recording completes, the dashboard opens that recording's folder ("Name this test" popup unchanged) |
| cards | `createRecordingCard` unchanged (badges, TEST FAILED summary, validations, every button) |

### Phase 2 – Direct stop buttons in the live log

| Where | Old → New |
|---|---|
| `live_log.html:283-287` | "Stop run" → **Stop** (single replay); new **Stop this test** + **Stop all tests** (Play All) |
| `live_log.html:486` `showStopButtons` | decides which buttons to show from `/api/play_all/state` when the run starts |
| `live_log.html:499` `directStop` | one click: (Stop all → `POST /api/play_all/stop_all` first) then `POST /api/test/run/stop`. No dialog |
| `live_log.html:535` | the old click handler with the choice dialog is kept as `_legacyStopRunWithDialog` (not attached); `askQueueStop` and `#queueStopCard` are kept, unused |
| `live_log.html:1043` | a pause card's "Stop run" now stops this test directly too (no dialog) |
| `live_log.html:1178` | all stop buttons hide when the summary ("Stopped by the user. …") arrives |
| `live_log.html:804` | a step stopped while running shows **STOPPED BY USER** |
| dashboard Stop All | unchanged code, same path (`stop_all` + `run/stop`) |

### Phase 3 – Instant stop

| Where | Old → New |
|---|---|
| `run_execution.py:616-686` | **new** `STOP_GRACE_S = 1.0`, `request_stop(run_id)`: waits up to 1 s for the replay to exit by itself, then ends it with `_kill_process_tree` |
| `run_execution.py:619, 640` | `_kill_process_tree`: Windows `taskkill /PID <pid> /T /F`; macOS/Linux: the whole tree read from `ps -A -o pid=,ppid=` **before** anything is ended, then `SIGKILL` to each. Needed because Playwright starts Chromium in its own process group, so killing only the Python process would leave Chromium windows behind |
| `run_execution.py:688` `_write_forced_stop_state` | after a forced stop: report.json gets `stopped_by_user: true`, the running step "Stopped by user - the run was stopped while this step was running." (not_run, so not a failure), every later step "NOT RUN (the run was stopped by the user)", a live-log line; pause/OTP cleared. Built from report.json, or the last readable copy kept by `poll_replay` (`:884`) |
| `run_execution.py:748` `_watch_replay` | → writes that state before the normal `_finalize_result` (report.html, summary, badges then work as for any finished run) |
| `run_execution.py:757` | the time-limit kill also ends the browser tree (was: only the Python process) |
| `run_execution.py:840` | the registry keeps the `proc` |
| `app.py:3528` `/api/test/run/stop`, `:3460` card Stop answer | → also call `request_stop` |
| `app.py:3620` `/api/play_all/stop_all` | → also stops the queue's current test on the server at once |
| `app.py:3323` `/api/test/run/start` | → refuses to start a test of a Play All queue that was told to stop |
| `script.js:2204` | Replay / Run controls refreshed as soon as a single run ends |
| normal runs | unchanged: `request_stop` only runs after a stop request |

### Phase 4 – "Expected no new tab, found a new tab"

**A) Recorder**

| Where | Old → New |
|---|---|
| `record_session.py:1544` `note_new_page_opening` (new), called from `app.py:708` | the click is marked `new_tab=True` the moment the browser **creates** the new page (before it loads) |
| `record_session.py:1580` | `record_new_tab` also stores the new tab's address on the click as `post_click.new_tab_url` |
| `record_session.py:1542, 1830, 1845` | the browser closed within 10 s after the **last** click (no new tab, no navigation seen) → `post_click.result_unknown = true`, `result.new_tab = null`, `result.unknown = true` (was `result.new_tab = false`, a guess) |
| other actions | unchanged |

**B) Replay** (`_compare_post_click`, the single place where clicks and Enter/submit are judged)

| Where | Old → New |
|---|---|
| `script_generator.py:7340-7385` | new `_TAB_OUTCOME`, `_SAME_TAB_PIDS`, `_post_click_result_unknown`, `_fresh_replay_tab`, `_tab_has_content` |
| `:7418` | recorded "no new tab" (or unknown), but a new tab opened and **loaded** (left about:blank) → passed; note "Opened in a new tab during replay (recorded: same tab / unknown); continuing on the new tab." |
| `:7513` | result unknown and the page changed in the same tab → accepted |
| `:7618` | recorded "new tab", but the page changed in the same tab → passed; note "Opened in the same tab during replay (recorded: new tab); continuing on this tab." A loaded new tab found late is accepted the same way |
| `:29545` main loop | the note goes to the live log; for a new tab, the step's own `page_id` now points at the new tab (its extra sequential id is released), so the next steps run there, as with a recorded new tab; for same tab, the recorded `tab_open` id points at the current page |
| `:26716` tab_open, `:26779` tab_close | a "tab" that opened in the same tab passes its `tab_open`; its `tab_close` goes back in history instead of closing the only page |
| `:25710` | the open tabs are also remembered before an Enter/submit with recorded post-click data, so the same rule applies there |
| still FAIL | no new tab and no page change (the existing "did not change the page" / "no new tab opened after N s" failures), a new tab stuck on about:blank, element not found / not clickable. Exact reasons unchanged. Locator matching untouched |

Old recordings: `data/recordings/myntra/session_20261104_090228.json` (step 3 has `post_click` without `new_tab`)
is handled by part B without editing the file.

---

## 2. Phase 3 root cause – why stop was slow

The stop button only wrote `stop_request.txt`. The replay reads that file **before each step** (and while a
card waits). So a stop waited for the running step to finish, which can be up to the 15 s step budget plus
navigation and new-tab waits. Then the replay still took the final screenshot, waited its 5 s close delay and
closed the browser. Nothing on the server ever ended the process, and the Play All loop waited for all of
that before it moved on. Now the server ends the process (and its browser) 1 s after the stop request if it
hasn't exited by itself, and writes the stopped state itself.

## 3. Phase 4 root cause

**Evidence:** recording `data/recordings/myntra/session_20261104_090228.json` (folder "myntra") and run
`data/generated_scripts/screenshoots/session_20261104_090228_20261104_090410/report.json`, step 3,
`failure_detail: [post_click_check] recorded new_tab=False, replay opened a tab=True`.
The recording has `stop_reason: browser_closed`, `page_count: 1`, no `tab_open` step, and step 3 is the last
action (recorded about 3 s before the save). Its `post_click` has no `new_tab` key at all.

**Recorder:** the new tab was only linked to its click by `record_new_tab`. The dashboard's new-page handler
called that only **after the new tab had loaded** (it waits up to 10 s for DOMContentLoaded first). The browser
was closed before that, so the tab was never registered and the click never got `new_tab=True`. On save,
`stop()` then wrote `result.new_tab = bool(None)` = `False`: a guess stored as a fact.

**Replay:** `_compare_post_click` failed every click whose tab kind differed from the recording
(`rec_tab != opened`), even when the click clearly worked (a product page loaded in the new tab). It judged
*which* tab, not *whether* the click worked.

---

## 4. Choices made where the requirement was ambiguous

- Order inside a folder: oldest first (recording order) = Play All order. "Ungrouped tests": newest first, as
  the dashboard always listed them.
- Pagination: inside an opened folder only (10 cards per page); the folder list itself is not paginated.
- Folder Play All with some cards ticked runs only the ticked ones (same rule as the old Play All); with none
  ticked, the whole folder.
- Export inside a folder with nothing ticked exports the whole folder; with no folder open it exports all.
- A recording saved without a folder opens "Ungrouped tests" after it completes.
- The pause card's "Stop run" also stops directly (this test only), so the old dialog is fully unused.
- The step that was running when stopped is marked `not_run` (with the text "Stopped by user …"), so it is not
  counted as a failure. The run status is FAIL with "The run was stopped by the user", as for a stop between
  steps today.
- Grace period 1.0 s. A stop between steps still ends normally (the replay exits by itself in time). One that
  is not done after 1 s (e.g. in its 5 s close delay) is ended. Its own complete report is kept.
- Unknown post-click result is only set for the **last** click before the browser was closed, within 10 s
  (the same 10 s the recorder gives a new tab to load).
- A new tab counts as a real response only after it leaves about:blank (waited up to the existing new-tab
  wait time).
- When the recorded new tab opened in the same tab, a later recorded "Close Tab" for it goes back in history.
- No new Python dependency was added (psutil is not installed). The process tree is found with `ps` /
  `taskkill`.

---

## 5. Static check results

- `py_compile`: OK – `app.py`, `run_execution.py`, `script_generator.py`, `record_session.py` (the old
  `\d` warning in `script_generator.py:1604` is pre-existing).
- `node --check frontend/static/js/script.js`: OK. `live_log.html` rendered with Jinja, inline scripts
  extracted, `node --check`: OK. `index.html` renders.
- SCRIPT_TEMPLATE: no `$` in the added text. Scripts generated from
  `data/recordings/myntra/session_20261104_090228.json` and `data/recordings/session_20261103_100245.json` into
  a scratch folder rendered and compiled, and contain the new helpers. Scratch files deleted.
- Paused flags still off: `OTP_LIVE_ENTRY_ENABLED = False`, `LIVE_LOG_RETRY_ENABLED = False`,
  `ALREADY_EXISTS_PAUSE_ENABLED = False` (`backend/feature_flags.py` unchanged).
- Same code paths: Launch popup (`openFolderModal` / `_confirmFolder` / `launchBrowserWithFolder`) unchanged.
  "Name this test" (`openNameTestModal`) unchanged. Ungrouped and folder recordings use the same
  `createRecordingCard`, `runRecording`, `/api/recordings/view`, `/api/test/run/start`, editor and Delete.

---

## 6. Manual test checklist

- [ ] Dashboard shows the folder list (icon, name, test count) + "Ungrouped tests"; click a folder → only its tests; "Back to folders" works
- [ ] Refresh / replay inside a folder → still in that folder
- [ ] Launch Browser with a new folder name → the folder shows at once with "0 tests"
- [ ] Inside a folder: Select All and card checkboxes affect only that folder; Export uses that folder
- [ ] Folder Play All runs only that folder's tests, in order; dashboard Stop All works
- [ ] Live log: "Stop" during a single replay; "Stop this test" + "Stop all tests" during Play All; one click, no dialog
- [ ] Stop takes effect within 1-2 s; no leftover browser windows/processes; running step shows STOPPED BY USER, the rest NOT RUN; the HTML report opens
- [ ] "Stop all tests" → no next test starts; Replay buttons enabled again right after
- [ ] Record a click that opens a new tab (and close the browser right after it), then replay → step passes, next steps run on the new tab
- [ ] Replay `myntra / check` (session_20261104_090228) → step 3 now passes with the "Opened in a new tab during replay" note
- [ ] An ungrouped old recording still opens, replays, edits and deletes as before
