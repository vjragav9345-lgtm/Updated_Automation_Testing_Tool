# AutoFlow QA – Changes Report (7 requirements)

Date: 2026-11-03

**Before testing:** restart the Flask server (`app.py`). The recorder reads `recorder/action_capture.js` only once, when the server starts. Every replay regenerates its script from the updated generator, so existing recordings pick up the replay fixes automatically.

## Backups

Every file was copied to `<file>.bak_20261103` before it was edited.

| File | Changed? | Backup |
|---|---|---|
| `generator/script_generator.py` | yes | `generator/script_generator.py.bak_20261103` |
| `app.py` | yes | `app.py.bak_20261103` |
| `recorder/action_capture.js` | yes | `recorder/action_capture.js.bak_20261103` |
| `templates/recording_editor.html` | yes | `templates/recording_editor.html.bak_20261103` |
| `templates/live_log.html` | yes | `templates/live_log.html.bak_20261103` |
| `templates/index.html` | yes | `templates/index.html.bak_20261103` |
| `static/js/script.js` | yes | `static/js/script.js.bak_20261103` |
| `static/css/style.css` | yes | `static/css/style.css.bak_20261103` |
| `validation/report_generator.py` | yes | `validation/report_generator.py.bak_20261103` |
| `recorder/record_session.py`, `recorder/pick_element.py`, `executor/run_execution.py` | **no** (backed up as a precaution only) | `*.bak_20261103` – can be deleted |

To undo any file, copy its `.bak_20261103` back over it.

---

## Phase 1 – OTP detection in every OTP situation

**Root cause.** The OTP mechanism (`_detect_otp_flow_roles`, plus the OTP-group handling built on it) only recognised split OTP boxes when each box had `maxlength="1"` or was at most 72 px wide. The Sign-in recording (`session_20261103_100714`, steps 7–10) records one digit per box, but its boxes are `maxlength="4"`, 105 px wide, with `inputmode="numeric"` and the label "Enter OTP". So:

- every recorded-data detector rejected the steps (1-digit value; `maxlength` ≠ 1; box too wide);
- group linking (`_otp_box_geom`) rejected the boxes as too wide;
- the replay-time box finder (`_OTP_ROW_JS`) had the same limits.

No step became an OTP step, so the old digits were typed back and the test PASSED.

**What changed** (all inside the existing mechanism – no second OTP system):

1. **New split-row recognition from recorded data** (`_otp_split_box`, `_otp_split_alike`, `_otp_split_run`). A group counts as a split OTP when *all* of these hold:
   - 3–12 different text-like inputs;
   - one character typed in each;
   - on one page, in one row, of similar size, under a shared recorded parent;
   - **and** an OTP sign: a label or nearby text naming a one-time code (otp, verification code, one time, passcode…), a field word (code, verification, verify, pin, otp), `autocomplete="one-time-code"`, a "Send OTP"-like click just before, or (4+ boxes only) numeric boxes holding only digits.

   A field whose own text names another kind of code (postal, promo, coupon, card, cvv…) never counts. A single "code" field needs more than one weak signal.
2. **Hooked into the existing detector.** `_detect_otp_flow_roles` now also accepts a split run. `_otp_in_same_group` also links such boxes. The existing roles therefore apply unchanged: `otp_fill` (ask once, fill all boxes) and `otp_fill_more` (the other boxes).
3. **Replay-time box finder extended.** `_OTP_ROW_JS` keeps its existing rule first. Only if that finds nothing, it accepts the nearest container that holds only a row of 3+ same-size text inputs (a container with any other field is never used).
4. **New replay-time safety net** (`_otp_live_field_check`). It runs only for a fill step the recording did not mark, whose recorded value is 1–8 digits. When the live field turns out to be an OTP field (one-time-code, OTP wording in name/id/placeholder/label, or a split row with OTP text or numeric boxes), the step joins the same OTP handling. The recorded 1-character fills that follow for the other boxes become "Part of OTP".
5. **Message changed.** The other boxes now log: `Step N: Part of OTP - filled from your input (step M)`.
6. **Timeout buffer.** `test_case_has_otp_step` (which adds extra time for the OTP wait) also recognises split runs.

Run Until Selected Step uses the same engine and the same roles, so it is covered too. The OTP card, its masked input and the "already exists" field-error card are unchanged. The recorded OTP digits are never typed.

**Why it is generic:** it uses only structure (row, size, shared parent, input type), standard attributes and generic OTP wording. There is no site, URL, digit count, text or XPath hard-coded.

## Phase 2 – No "found by position" warnings on passing steps

**Root cause.** In `run()`, a step that passed using `position_fallback`, `bounding_box` or `state_target_proxy` got the warning "Couldn't find this element by its details, so it was found by its position on the page." That made it count as a warning. The dashboard and the HTML report also counted every step with `locator_report.weak` as a "locator warning", even when it passed. The summary sentence also called "used a fallback locator" a workaround.

**What changed:**

- `generator/script_generator.py`:
  - A passing fallback step now gets only a quiet Details line ("Found using a backup method (its position on the page)…").
  - The "element had moved but was checked to be the right one" note is also Details-only now (the element was verified, so it is not a problem).
  - "used a fallback locator" is no longer added to `workarounds`. Real workarounds such as Escape or coordinates still are.
- `static/js/script.js` and `validation/report_generator.py`: "locator warnings" count only steps that did **not** pass. The amber "weak" colour on the step's "found using …" line now appears only for steps that did not pass.

Unchanged: failures, ambiguous/wrong-element warnings, value-changed notes, the toggle-skip message, and the OTP / field-error messages.

## Phase 3 – Validate gives a proper 1-of-1 XPath

**Root cause** (for step 2, `(//*[@id='root']//div[contains(., 'Accept')])[7]`):

1. **Timing.** Validate counted the XPath straight after `domcontentloaded` on a React app, before the Accept banner had rendered, so it got 0.
2. **Weak XPath.** The XPath itself is weak: a document-wide index (`[7]`). The recorder fell back to it because `//div[normalize-space(.)='Accept']` matched two nested divs (the clickable div and its inner text div). The recording's own `match_count` shows `xpath: 0`.

**What changed:**

- `app.py` `validate_locator`:
  - **(a) Snapshot first.** It checks the page snapshot recorded for that step – the same page Pick Element opens, no replay. It falls back to the existing fast-forward replay only when there is no usable snapshot or the XPath is not found on it.
  - **(b) Waits.** It waits up to 1.5 s on the snapshot and 8 s on the live page for the element to appear, instead of counting immediately.
  - **(c) Repair.** If the step's *saved* XPath (when editing an existing step) matches 0 or several elements, it finds the element with the replay's own `_resolve_element` (recorded attributes, text, role, placeholder, CSS path…). It then builds a robust XPath, confirms it matches exactly 1, shows "✓ Found (1 match) – the saved XPath matched N elements, so a unique XPath for the same element was put in the box. Click Save to keep it." and puts the new XPath in the box. An XPath you typed yourself is checked as typed and never replaced.
- `recorder/action_capture.js`: new shared builder `afqaRobustXpath`, between the markers `AFQA-ROBUST-XPATH-BEGIN/END`. Validate loads exactly this text, so there is one rule, not two copies. It prefers, in order:
  - a stable attribute: data-testid / data-test / data-cy / an id that does not look generated / name / aria-label / placeholder / title / alt;
  - the exact visible text, using the outermost or innermost element when wrappers repeat the same text;
  - text plus role / tabindex / type;
  - the same inside the nearest uniquely identifiable ancestor.

  Every candidate must match exactly one element, and that element must be the target.
- **New recordings.** The recorder now uses this builder only when `xPath()` produced an index-based (`(...)[N]`) or absolute `/html…` path. Every other XPath is unchanged. Existing recordings are unchanged until you Validate + Save a step. Version marker bumped to `2026-11-03-a`.
- `templates/recording_editor.html`: sends the edited step's index and applies the suggested XPath.

## Phase 4 – Result badge in the top-right of each card

`static/js/script.js` / `static/css/style.css`:

- The badge and its summary lines are now drawn by `renderResultSummary` into a slot at the top-right of the card. The badge is TEST PASSED / TEST FAILED, in the same colours. The summary lines are "N steps executed · …" and the result message, e.g. "all steps resolved".
- The step list, the "Hide/Show all steps" button and the validation cards stay where they were.
- On narrow screens (≤ 700 px) the badge moves under the session details, aligned left.
- The badge is cleared when a new replay starts, and redrawn after Replay, View Last Log or Play All. It is also redrawn after Refresh or a page change for sessions already replayed during this page visit.
- Warning counts follow the Phase 2 rule.

## Phase 5 – Play All

- **Button.** "Play All" sits next to Refresh. It runs the selected sessions, or all sessions when none are selected, strictly one after another.
- **Same path as Replay.** Each session runs through `runRecording()`, exactly like the card's Replay button: same engine, live log, OTP card, field-error card, screenshots and saved result. An OTP or field-error pause makes the queue wait.
- **Live log window.** It opens on the Start click (so the browser doesn't block it), and each session is shown in it in turn. The dashboard panel also has an "Open live log" link for the running session.
- **Progress and summary.** The panel shows progress ("Running 3 of 10: <name>") with each session's outcome. It ends with a summary: passed · failed · stopped · not run. A failed session is recorded and the queue continues.
- **Stop.** While a queue runs, the live log's "Stop run" button – and the Stop button on its cards – asks in the live-log window: "Stop this session only" / "Stop all of Play All" / Cancel.
- **Blocking other replays.** `app.py` keeps the queue state (`/api/play_all/begin|progress|stop_all|end|state`):
  - While a queue runs, any other replay start (Replay, editor Run Until, a second Play All) is refused with a clear message.
  - `/api/test/run/active` reports the queue as active, so the Replay/Run buttons on every page stay disabled for the whole queue, including the gap between sessions.
  - If the dashboard tab is closed, the queue is released 120 s after its last heartbeat – never while a session is still running.

## Phase 6 – Checkboxes and Select All

- A checkbox on every card, and **Select All** on the left of the header. Select All covers all sessions on all pages; it shows a partial state when only some are selected.
- Selections survive Refresh and page changes, and a page reload in the same tab (sessionStorage). The selection of a deleted session is dropped.
- When you click Play All, the dashboard panel (not a browser popup) shows either "N/M sessions selected – playing, one after another:" with the list, or "No sessions selected – all M will run…", with Start / Cancel.

## Phase 7 – Export

`POST /api/recordings/export` returns one ZIP (Export button in the header):

- `sessions.csv` – name, file, start URL, recorded at, saved at, actions, last result, last run at, message, final screenshot.
- `steps.csv` – step number, name, action, target text, XPath, CSS path, value, page URL, last result (Passed / Failed / Warning / Skipped / Not run), duration, start time, message, screenshot.
  - OTP values are masked as `******`. Detection uses the same OTP rules as replay, plus the last run's OTP steps. Password-field values are also masked.
- `live_logs.csv` – the live-log entries of the last full run.
- `screenshots/<session>/…` – the images of each session's last full replay. The CSVs reference them by their path inside the ZIP.

Format and safety:

- The CSVs are UTF-8 with BOM, and every field is quoted, so they open correctly in Excel.
- Data is read where it already lives: `storage/recordings/**.json` and each run folder's `report.json` and images. Storage is not changed. (There is no real database – `/api/database/connect` reports "not configured".)
- Sessions that were never replayed export as "Not run". A missing log or image is left blank.
- Export is disabled, and refused by the server, while Play All runs.

---

## Assumptions / safe decisions made on my own

- **"Stop all of Play All"** stops the current session, then marks the remaining sessions "Not run".
- **Card Stop buttons.** The pause cards' own "Stop run" button asks the same question as the header Stop button.
- **Badges on page load.** The dashboard does not load past results on page load (same as before). Badges appear after Replay, View Last Log or Play All.
- **Repair scope.** Validate repairs only the step's own saved XPath. A hand-typed XPath is reported as typed.
- **Recorder XPath.** The robust XPath replaces only index-based or absolute XPaths, to keep existing behaviour for everything else.
- **Masking.** Password values are masked in the export as well as OTPs.
- **Live OTP check timing.** The replay-time check waits at most 3 s for the field, only on unmarked 1–8-digit fills. That is the only possible timing change for ordinary steps.
- **Static checks only.** I ran syntax-only checks (Python parse of `app.py`, the generator and the generated-script template, and JavaScript parse of the edited JS). I did not run any replay, test or verification script.

## What to test

### Phase 1
1. **Sign-in OTP:** replay `session_20261103_100714` (Sign in → phone → Sign in → OTP).
   - Expected: the live log says "OTP group detected (4 boxes)" and the OTP card appears **once**.
   - Enter a fresh OTP. The 4 boxes fill one digit each, in order.
   - Steps 8–10 show "Part of OTP - filled from your input". Step 11 clicks Verify. No recorded digit is typed.
2. Repeat with **Run Until Selected Step** on step 11, and on step 8.
3. **Wrong length:** enter a wrong number of digits. The card asks again ("This page expects 4 digits; you entered N.").
4. **Single-field OTP:** replay `session_20261103_100245` (register → Verify OTP modal). The OTP card behaves as before.
5. Replay a recording **without OTP** (e.g. one with a coupon or postal code field). No OTP card should appear.

### Phase 2
6. Replay a session that used to show "found by its position" on passing steps.
   - The live log and dashboard show no warning for them, and no "locator warnings".
   - The step's Details or "found using …" line still says how it was found.
   - A real failure still shows as a failure.

### Phase 3
7. **Accept step:** View/Edit `session_20261103_100245` (or `_100714`) → edit step 2 "Click – Accept element" → Validate.
   - Expected: "✓ Found (1 match)…", with a new 1-of-1 XPath (most likely `//div[normalize-space(.)='Accept'][not(parent::*[normalize-space(.)='Accept'])]`) placed in the box.
   - Click Save, then replay. The step still passes.
8. Type a wrong XPath by hand → Validate → "✗ Not found". It must not be replaced.
9. Check that Pick Element still works the same: pink box, drag-select, click-to-lock, scrolling.
10. **New recording:** record something with nested wrappers (e.g. a cookie "Accept" button). In the editor, its XPath should be short and attribute/text-based, not `(...)[N]`.

### Phase 4
11. Replay or View Last Log on a few cards. The badge and summary appear at the top-right; the steps toggle stays below the buttons.
12. Narrow the window to below 700 px. The badge moves under the details.
13. Replay again. The old badge disappears while running, then the new one appears.

### Phase 5
14. Select 2–3 sessions → Play All → panel lists them → Start.
    - They run one by one in the same live log window, with progress shown.
    - Each card updates when its session finishes, and the summary appears at the end.
15. During Play All:
    - Card Replay buttons and the Play All button are disabled.
    - The editor's Run Until is refused with a message.
16. In the live log, click Stop run → choose "Stop this session only". The next session starts.
17. Run again, click Stop run → choose "Stop all of Play All". The queue ends, and the rest are "Not run".
18. Include an OTP session. The queue waits for the OTP card, then continues.

### Phase 6
19. Tick a few cards and use Select All on and off. The partial state shows when only some are ticked.
20. Click Refresh and change pages. The ticks are kept, and Play All / Export use them.
21. With nothing ticked, Play All says "No sessions selected – all N will run".

### Phase 7
22. Export with some sessions ticked, then with none ticked.
    - Open the ZIP: `sessions.csv`, `steps.csv` and `live_logs.csv` should open in Excel with correct characters and columns.
    - `screenshots/<session>/…` exist and match the CSV paths.
    - OTP values show as `******`.
    - Never-replayed sessions show "Not run".
23. Try Export during Play All. The button is disabled, and the server refuses.

## Noticed but deliberately not changed (out of scope)

- **Report Reason column.** The downloadable HTML report's "Reason" column still shows a passing step's raw technical note (e.g. "recorded target not found – used same position…"). It is not labelled or counted as a warning.
- **Edit-save drops locator details.** Saving an edited step in the editor replaces its whole locator with the XPath only. This is existing behaviour; a repaired 1-of-1 XPath fits it.
- **View Last Log matching.** `api/recordings/last_result` matches run folders by name prefix, so a session named `X` can pick up runs of `X_edited…`. Export uses the stricter `session_files` rule first.
- **Existing escape-sequence warnings.** Python prints `SyntaxWarning`s for existing escape sequences in the generator; they are not from my changes.
- **Recorder OTP marking.** The recorder's own `otp_field` marking at record time was left unchanged; replay now detects split OTPs regardless.
