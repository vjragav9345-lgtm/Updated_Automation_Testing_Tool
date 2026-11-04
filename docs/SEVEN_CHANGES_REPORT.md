# Seven Changes – Report

Backups of every edited file (original content, same relative paths): `_backup_seven_changes/`.
New file: `backend/feature_flags.py`. No files were moved, nothing was run except `py_compile`,
`node --check`, a template render into a scratch folder (deleted afterwards) and read-only calls of the new
storage helpers.

Files changed: `app.py`, `backend/storage/repository.py`, `backend/storage/session_files.py`,
`backend/storage/retention.py`, `backend/recorder/record_session.py`, `backend/generator/script_generator.py`,
`backend/executor/run_execution.py`, `frontend/static/js/script.js`, `frontend/templates/index.html`,
`frontend/templates/live_log.html`, `frontend/static/css/style.css`.

---

## Phase 0 – what was analysed (summary)

- Recordings are flat JSON files in `data/recordings/` (+ `edited/`, `trimmed/`). Run folders are
  `data/generated_scripts/screenshoots/<slug(name)>_<timestamp>/` and are tied to a recording only by its
  **name** (unique `session_<timestamp>`). Because of that, scripts, snapshots and run folders could stay
  where they are; only the recording JSON (and its draft / edited copy) needed to live inside a folder.
- `_resolve_recording_file` already accepted any path below `data/recordings/` (and rejects anything outside),
  so it needed **no change**. `load_recording` / `set_display_name` also accept nested paths unchanged.
- Places that only looked at the top level and needed folder support: `list_recordings`, crash-draft recovery,
  the recorder's draft path, `_finish_recording`, edited-copy save, editor "open the edited copy", the
  watcher's edited/original decision, `session_files` (Delete), retention.
- Replay = `SCRIPT_TEMPLATE` (string.Template) in `script_generator.py`, regenerated on every Replay.
- Validation types: `VALIDATION_ACTION_TYPES` in `script.js` (same set in `report_generator.py`) and the
  editor's `readOnly` flags in `ACTION_FIELD_DEFS`.

---

## 1. Changes per phase (file:line, old → new)

### Phase 1 – Folder popup + recordings stored in folders

| Where | Old → New |
|---|---|
| `backend/storage/repository.py:42-113` | **new** `RESERVED_FOLDER_NAMES` (`edited`, `trimmed`), `validate_folder_name()` (trim, empty, max 60 chars, `< > : " / \ \| ? *` + control chars, `..`, leading/trailing dot, Windows device names CON/PRN/AUX/NUL/COM1-9/LPT1-9, names ending `.json`/`.jsonl` or containing `.tmp` (so retention/list globs can never mistake a folder for a file), case-insensitive reuse of an existing folder), `folder_dir()`, `list_folders()`, `folder_of_path()`, `is_edited_recording_path()` |
| `repository.py:115` `save_recording` | always top level → optional `folder` param; writes `<recordings>/<folder>/<name>.json` and the JSON field `"folder"`. No folder = exactly as before |
| `repository.py:128` `save_edited_recording` | always `edited/` → optional `folder`: `<recordings>/<folder>/edited/<name>.json` |
| `repository.py:~420-450` `list_recordings` | top level + edited + trimmed → also every folder and its `edited/`. Existing fields unchanged; **added** `folder` (None = ungrouped) and `action_type_counts` |
| `repository.py:506` `recover_orphaned_drafts` | top-level drafts only → also drafts inside folders, recovered **into that folder** |
| `backend/recorder/record_session.py:1571,1615` `Recorder.start` | draft always top level → optional `draft_dir`; omitted = unchanged. Needed because `start()` itself already writes the first (navigate) action to the draft, so the draft must be in the folder from the start for crash recovery. Capture logic untouched. |
| `app.py:2905` `/api/browser/launch` | → optional `folder` field, validated; invalid = clear message, no launch. Missing = exactly as today |
| `app.py:~640/685/870/917` `_run_recording_session`, `_finish_recording` | → carry `folder`; `save_recording(test_case, folder=folder)`; recorder draft in the folder. All stop methods (browser close, Stop button, ENTER, crash save) go through `_finish_recording`, so all save into the folder |
| `app.py:290` watcher | edited copy = only `edited/` → also `<folder>/edited/` (script goes to the edited-scripts folder as before) |
| `app.py:1263` `/recording/edit` | "open the edited copy" only for top-level originals → also for originals in a folder (`<folder>/edited/<name>_edited.json`) |
| `app.py:2417` `/api/recordings/save` | edited copy always in `edited/` → in `<folder>/edited/` when the recording's `"folder"` field names an existing folder |
| `app.py:1063, 1070` | **new routes** `GET /api/recordings/folders`, `POST /api/recordings/folders/validate` |
| `backend/storage/session_files.py:76` | Delete looked only at top level/edited/trimmed → also each folder and its `edited/` |
| `backend/storage/retention.py:154` | → each folder and its `edited/` are extra targets (label `recordings-folder…`, same age rule, same "never while recording" guard) |
| `frontend/templates/index.html:329` | **new** folder popup (existing-folder dropdown + name box + error line + Cancel/Launch). CSS/JS cache versions bumped |
| `frontend/static/js/script.js:522-596` | Launch click → `openFolderModal()`; Confirm validates on the server, then calls `launchBrowserWithFolder(folder)` = the **unchanged** old launch body plus `folder` in the request. Cancel = nothing |
| `script.js:906-1000` | **new** `_folderGroups()`, `_renderFolderGroup()`; `renderRecordingsPage` renders one collapsible section per folder (name, count, **Play All**, **Stop All**) followed by the ungrouped list |
| `script.js:~1290` `createRecordingCard` | → optional `container` argument (folder body); every button/behaviour unchanged |
| "Name this test" popup | **not changed** – it still opens from the same `phase === "completed"` transition with the new path |

### Phase 2 – Stop All

| Where | Old → New |
|---|---|
| `script.js:2376` `_updateFolderPlayAllButtons` | **new** – shows Stop All only in the folder whose Play All is running |
| `script.js:2392` `stopPlayAll` | **new** – reuses `POST /api/play_all/stop_all` then `POST /api/test/run/stop` (stop_request.txt) for the current run |
| `script.js:2476-2560` `runPlayAll` | → `folder` param and a run context; the loop checks the stop request before **each** next test (`ctxNow.stopRequested` + the server's `stop_all` as before), remaining tests are "Not run", queue always ends with `/api/play_all/end`; Stop All clicked while a test is still starting stops it as soon as its run id exists. Afterwards the button hides and `AFRunControl.refresh()` re-enables Replay |
| live log stop-queue choice | unchanged |

### Phase 3 – Result badges + validations

| Where | Old → New |
|---|---|
| `app.py:1007-1060` | `/api/recordings` → each recording gets optional `last_result` `{outcome, status, finished_at}` from its newest **full** replay; run folders matched exactly with `session_files.is_run_folder_of` (an original never takes its `_edited` copy's runs). Outcome: stopped (stopped_by_user / browser_closed) / passed / warning (PASS with a step warning) / failed |
| `script.js:148` | **new** `cardOutcomes` (results of this page visit) |
| `script.js:1315` | **new** `.af-result-badge` – always directly after the card's checkbox, before the title (same spot on every card) |
| `script.js:1476, 1486, ~1940` | `_outcomeOfResult`, `_setCardBadge`; a single Replay shows "Running..." then the real outcome (or restores the old badge if the replay could not start) |
| `runPlayAll` | each test's badge is updated; tests skipped by Stop All show "Not run" |
| `script.js:1454, 1458, 1348` | **new** "Validations: Validate Text x2, …" / "No validations" line under the buttons, labels from the existing `actionTypeLabel` |
| `style.css:1692+` | folder section, badge colours, validations line |

### Phase 4 – OTP card paused (flag `OTP_LIVE_ENTRY_ENABLED = False`)

| Where | Old → New |
|---|---|
| `script_generator.py:4187` | template constant `OTP_LIVE_ENTRY_ENABLED = $otp_live_entry_enabled_literal` (filled from `feature_flags.py` in `generate_script`, `:31178`) |
| `script_generator.py:24856` | `_otp_roles = _detect_otp_flow_roles(STEPS)` → `_otp_detected_roles` computed as before; `_otp_roles` = detected roles when the flag is on, `{}` when off. So no step is an OTP step: `_wait_for_live_otp` (otp_needed / pause kind "otp") never runs, the recorded value is typed by the normal fill, OTP steps follow the normal stop-on-failure rule |
| replay-time OTP field check (`_otp_live_field_check`) | → only when the flag is on |
| report entries (`:29842`, `:30494`) | **added** `otp_detected_role` (masking only) |
| `app.py:4614` `_export_otp_mask_indexes` | → also masks steps by `otp_detected_role`, so exports stay masked with the flag off |
| `run_execution.py:94` | +200 s OTP timeout buffer → only when the flag is on |
| `live_log.html:700, 1028` | `otp_needed` handler and pause kind "otp" ignored when off (second guard; the replay does not send them) |

**Recorded value check:** the recorder stores the OTP as typed (`data/recordings/session_20261103_100245.json`,
step 11: `fill`, `value '1234'`, `otp_field: true`) – **not masked**, so replay types the recorded value.
Masking in exports (`_export_otp_mask_indexes`) and page snapshots (`page_snapshot.py`) is unchanged.

### Phase 5 – Live-log Retry button paused (flag `LIVE_LOG_RETRY_ENABLED = False`)

Paused only the button and what it drives:
- `script_generator.py:30147-30177` failure ("fallback") card: `retry` is not offered; a card that would only
  have **Stop run** left is not shown at all (the normal failure handling runs straight away – the same outcome
  as answering Stop / not answering). A page-mismatch card still shows "Accept this page and continue" + Stop.
  A `retry` answer is ignored.
- `script_generator.py:30089` "form could not be corrected" card (only Retry/Stop) → not shown when off.
- `app.py:3410` `/api/test/run/pause/answer` rejects `action: "retry"` when off.
- `live_log.html:1061` the Retry button is never rendered when off.
- **Not touched:** the engine's own automatic internal retries (tier/strategy retries, bounding-box retry,
  chat resend …) – they don't depend on the button. The `step_retry` SSE event stays; it only fires after a
  retry answer, so it simply never fires while the flag is off.

### Phase 5B – "Already exists" pause paused (flag `ALREADY_EXISTS_PAUSE_ENABLED = False`)

- `script_generator.py:29378` the keyword check right after a submit step (`_keyword_message_for_step` →
  `_pre_msg_match`, which used to turn the step into "Failed: The website showed …") → not done when off.
- `script_generator.py:29917` the field-error card trigger (`_fe_msg`) → not computed when off, so the card,
  `_targeted_rerun_prepare`, the decision-trace line and `_save_field_values_to_recording` never run.
- `app.py:3410` pause/answer rejects `continue` / `retry_as_is` (used only by this card) when off.
- `live_log.html:1028` a `field_error` pause event is ignored when off.
- **Not touched:** `_pause_and_ask`, `pause_answer.json`, message capture itself (detection only),
  `config/message_keywords.json`, `renderFieldRows` / `collectFieldValues` / `answerPause` code.

### Phase 6 – Click performed but marked FAILED

| Where | Old → New |
|---|---|
| `script_generator.py:29889` browser-gone check after a step | marked the just-finished step FAILED even when it had **passed** → a passed step stays passed (note added to its Details); the run still stops and later steps are NOT RUN |
| `script_generator.py:30470` NOT RUN backfill | used `count_summary_rows`, `value_range_rows`, `page_mismatch_info` of the last executed step (stale), and **crashed with UnboundLocalError** when the run stopped before step 1 → `None` |
| `script_generator.py:25324` | those three are now set before each step's `try:`, so the crash handler can always build the entry |
| `script_generator.py:28441` + helper `:5251` `_click_done_and_page_moved` | an exception from the click handling became FAILED with only `str(e)` → if the click/press was already dispatched in this step **and** the page moved on (other URL or a new tab), the click counts as performed and the normal post-click check decides from the recorded effect; otherwise it stays FAILED |
| `script_generator.py:5273` `_step_failure_detail` + `_fail_check` set at each check (action, post_click_check, submit_check, message_check, stop_check, website_message, browser_closed, replay_loop) | **new** `failure_detail {check, exception_type, message}` on every failed step in report.json |
| `run_execution.py:272` | the "internal error" step of a crashed process gets `failure_detail` (exit code + end of stderr) |
| `run_execution.py:315` | a process that died (non-zero exit) before writing any step → every step listed as NOT RUN (was: empty list) |
| `app.py:3854, 3901` | live-log reason gets `exact` (one line) next to the existing plain-English text |
| `live_log.html:333, 620, 807` | shows "Exact reason: [check] Type: message" under a FAILED step; a line that becomes FAILED later via `step_update` now also shows its reason (it showed nothing before) |

Recorder check: for the click-then-navigate case (`data/recordings/session_20261103_111817.json`, step 24
"Events") the recorder has the right target (`text 'Events'`), `page_url …/feed`, `expected_url …/events`,
`post_click.navigated = true`, `url_path_after …/events`. **Recorder is correct – nothing changed in it.**

---

## 2. Phase 6 root cause (plain English, with evidence)

No run folder on disk shows the exact "Events" failure: in every saved run the Events click passed
(e.g. `session_20261103_111817_20261103_112406`, step 24 PASS). The recent run folders do show three generic
defects that produce exactly the three symptoms:

1. **A passed step was rewritten to FAILED after it finished, with no reason shown.**
   `session_20261103_111817_edited_20261103_163012/replay_console.txt`: step 2 prints `STATUS: SUCCESS`, then
   "The browser window was closed - the run stopped at step 2", and `report.json` has step 2 as
   `success: false, error "Stopped: The browser window was closed"`. The check that runs *after* a step
   overwrote the result of a step that had already succeeded. The live log had already printed that line as
   PASS; the later `step_update` flipped it to FAILED and printed **no reason** (that handler only printed
   warnings). Fixed: a passed step stays passed, and a line that turns FAILED later shows its reason.
2. **Remaining steps disappeared.** `session_20261103_111917_20261103_163019/replay_console.txt` ends with
   `UnboundLocalError: cannot access local variable 'count_summary_rows'` in the NOT RUN backfill. When the run
   stopped before step 1, the backfill crashed, so report.json had **0 steps** (runs 163019, 163022, 163025,
   163026, 170527, 170825, 170834, 170841 all have `steps: []`). The executor only completed missing steps when
   at least one step existed. Fixed in both places.
3. **An error after a successful click turned the click into a failure with only a raw message.** In the main
   loop, any exception from the click handling was caught as `strategy, found, ok, err = None, False, False,
   str(e)`. That includes errors raised by checks *after* the click when the page has already navigated
   (destroyed execution context, detached element). Fixed generically: the click counts as performed only when
   it was really dispatched in this step and the page really moved on; the existing post-click check then
   verifies the recorded effect. Real failures (no dispatch, page unchanged, wrong destination) still fail.

---

## 3. Feature flags

All three are in **`backend/feature_flags.py`** (one place), each default `False`:

| Flag | Turns off | To turn back on |
|---|---|---|
| `OTP_LIVE_ENTRY_ENABLED` | OTP card / OTP wait / OTP timeout buffer | set to `True` |
| `LIVE_LOG_RETRY_ENABLED` | live-log "Retry step" button and its handling | set to `True` |
| `ALREADY_EXISTS_PAUSE_ENABLED` | "already exists" keyword pause + field-error card | set to `True` |

Restart the Flask app after changing one. Each Replay regenerates its script, so the template constant follows
the flag automatically. With a flag `True`, every guarded condition reduces to the original expression
(e.g. `_otp_roles = _otp_detected_roles`, the original `_fc_actions` tuple, the original keyword call), so the
old code path runs exactly as before. Checked by rendering the template with all flags `False` and all `True`.

---

## 4. Choices made where the requirement was ambiguous

- **Pagination:** folders are always shown in full (collapsible sections); pagination (10 per page) applies to
  the **ungrouped** list, so old recordings look and page exactly as before.
- **Order inside a folder:** oldest first (recording order). That is also the folder's Play All order.
- **Top Play All, Select All, Export:** kept visible and working on all recordings. Folder cards have the same
  selection checkbox.
- **Folder Play All** uses the same confirmation panel (Start/Cancel) as the top Play All. The live-log
  window must be opened from a click, and the Start click does that.
- **Edited copies** still appear as their own cards (as today), in their folder. Their validations line comes
  from the edited file. After saving an edit, the dashboard shows the update on its next load/Refresh.
- **Validation types** = existing `VALIDATION_ACTION_TYPES` + any `validate_*` type (the editor marks all of
  them read-only; `validate_checked` was missing from the set). `count_elements` / capture types are data
  captures, not validations. Recorder-created auto validations are not counted, because replay skips them.
- **Badge after refresh** = newest full replay of that exact recording (partial runs ignored). A test skipped by
  Stop All shows "Not run" until the page is refreshed. After a refresh it shows its last real result.
  Browser closed during a run = "Stopped".
- **Badge position:** right after the checkbox, before the title. The existing TEST PASSED/FAILED summary in
  the top-right corner is unchanged.
- **Retry card with only "Stop run" left** is not shown (it would only pause the run until Stop or timeout).
- **"Not run" wording:** kept the existing `NOT RUN (stopped after step N failed): <reason>` (other code
  recognises the `NOT RUN` prefix). It already contains step N and the reason.
- **Folder names:** max 60 characters; an existing folder is reused case-insensitively (macOS/Windows file
  systems are case-insensitive).
- **Exact reason in the HTML report:** not added (the HTML report was listed as do-not-change). It is in
  report.json (`failure_detail`) and in the live log.
- Fill failure messages can still contain the typed value (existing behaviour, also for normal fills). Not
  changed.

---

## 5. Static check results

- `py_compile`: OK for all 8 changed/new Python files. The only warning (`script_generator.py:1604`, invalid
  escape `\d`) was already there.
- `node --check frontend/static/js/script.js`: OK.
- `live_log.html` inline script: rendered with Jinja (flags False and True), extracted, `node --check`: OK.
  `index.html` renders.
- SCRIPT_TEMPLATE: no `$` added except the three new placeholders. A script generated from
  `session_20261103_100245.json` into a scratch folder compiled with flags off and on (constants rendered as
  `False` / `True`). The scratch files were deleted. `test_case_has_otp_step` (which execs part of the
  template) still works.
- New template names (`_fail_check`, `_step_failure_detail`, `_click_done_and_page_moved`,
  `_otp_detected_roles`, …) are all defined in the generated script.
- Read-only helper check: `validate_folder_name` rejects empty, `a/b`, `..`, `edited`/`Edited`, `CON`,
  `x.json`, `.hidden`, 61 chars, `ok?`, and accepts/trims `"  Signup flow "`. `list_recordings` still returns
  all 7 existing (ungrouped) recordings with their old fields, plus `folder: null`.
- Old ungrouped recordings use the same code paths as before: listed (top level / edited), opened
  (`_resolve_recording_file` unchanged, editor swap branch unchanged), replayed (`recording_path` unchanged),
  edited (no `folder` field → `edited/` as before), deleted (`session_files` still scans the same dirs first).

---

## 6. Manual test checklist

- [ ] Launch Browser → folder popup appears; Cancel → nothing launches; an invalid name (e.g. `a/b`, `edited`) shows a message
- [ ] New folder name → record → close the browser → "Name this test" appears and works → card shows inside the folder (file at `data/recordings/<folder>/session_….json`)
- [ ] Launch again and pick the same folder from the dropdown → the second test joins it; also try Stop Recording and ENTER
- [ ] Folder Play All → Start → tests run oldest first; click **Stop All** mid-run → the current test stops, the rest show "Not run", the button hides, Replay buttons enable again
- [ ] Live log "Stop all of Play All" still works
- [ ] Badges after Play All, then Refresh the page → badges stay (from the last real run)
- [ ] Single Replay of one card → its badge shows Running..., then the result
- [ ] Validations line on cards; edit a recording, add a validation, save → its edited card shows it after Refresh
- [ ] Replay a test with an OTP step → recorded OTP is typed, no OTP card, no waiting
- [ ] A failing step → live log has no Retry button (page mismatch still offers "Accept this page")
- [ ] Signup with an already-used email/username → no field-error card, run continues with normal pass/fail
- [ ] Click-then-navigate case (e.g. "Events") → PASS; a real failure shows "Exact reason: …" on the step line, and every remaining step shows NOT RUN
- [ ] Close the replay browser right after a step passes → that step stays PASS, the rest are NOT RUN
- [ ] An old ungrouped recording: open, edit/save, replay, View Last Log, Screenshots, Rename, Delete
- [ ] Delete a test inside a folder → its JSON (and its edited copy) are removed
