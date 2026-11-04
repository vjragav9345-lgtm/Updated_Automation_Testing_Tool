# Fix: "See all results" failed in replay but passed on Retry

Date: 2026-11-03 · Only file changed by this fix: `generator/script_generator.py`

## Root cause (confirmed from the code and from your run)

Your run is `generated_scripts/screenshoots/session_20261103_111817_20261103_112406/report.json`. In it:

- Step 26 (the fill) ended at 11:25:08.767.
- Step 27 started 4 ms later and ran **5.97 s**.
- The step-27 diagnostic lists the whole tier list **twice**.

**The locators are fine** – Retry passes with them. The search dropdown appears only after the site answers a debounced search request. Two waits that already exist both ended before it appeared:

1. **The readiness wait before the step ended at once.** `_wait_page_ready` waits for requests that are *already pending* and for page activity. A debounced search box sends its request a few hundred ms *after* typing stops. 4 ms after the fill nothing was pending and the page was quiet, so the wait returned immediately.
2. **The settle-and-recheck inside the step stopped too early.** When the first search finds nothing, `_resolve_and_act_core` calls `_wait_for_next_step_ready(page, step)`, which is meant to poll for up to 9 s. It polls `_locator_findable`, and that accepts **any** element matching the recorded CSS path. Before the dropdown rendered, a different element sat at that path: a 49×49 `<div>` with no text. So "findable" was true immediately and the wait ended. The tier decision then correctly rejected that div ("text mismatch: recorded 'See all results' … own text ''"). The one recheck found nothing usable, so the step failed and paused about 0.5 s in. By then the search responses were still arriving ("server responses 5 (step-caused)"), so the dropdown was showing a few seconds later in the screenshot.
3. **Why Retry works.** By the time you click Retry, the dropdown is there. The earlier passing run (`…_112212`) passed only because the dropdown happened to be ready in time.

**Fill was not part of the cause.** `_do_fill` already types real keystrokes (`press_sequentially`: keydown / input / keyup per character, `fill()` only as a fallback). The passing run proves this fill opens the dropdown. **Fill behaviour was not changed.**

## What changed

`generator/script_generator.py` – backup: `generator/script_generator.py.bak_20261103_seeall`

1. **New bounded wait `_await_async_target`.** It runs only after the existing first search **and** the existing settle-and-recheck both found nothing usable. Each round:
   - (a) waits for the requests started since the previous step to finish. This reuses the readiness wait's existing request tracking (`_NET_PENDING` / `_NET_IGNORED`). A request that never ends holds a round back for at most the existing `READINESS_NET_HINT_S` (3 s).
   - (b) waits for the whole document to stop changing for 350 ms – the readiness wait's own quiet span, using its existing `_READY_JS` mutation watcher. This covers portals, overlays, dropdowns and listboxes. A page that keeps animating ends this after 2 s.
   - (c) runs **the same `_attempt_tiers()`** again: same tiers, same order, same decisions. Text-mismatch rejection and the position-fallback size rejection are unchanged.

   It repeats until the target is found or the window ends.
2. **The window.** It is the 9 s the existing settle-and-recheck already intended (`_wait_for_next_step_ready`'s own default), counted from when that recheck started, and never past the step's existing time budget `STEP_TIME_BUDGET_S` (`AUTOFLOW_STEP_BUDGET_S`, default 15 s). The remaining budget still allows the existing scroll-and-recheck for lazy lists.
3. **Previous step's start.** A one-line holder `_STEP_PREV_START` keeps the previous step's start time, so requests started by the fill count as step-caused. The existing `_PREV_STEP_START` is set exactly as before.
4. **Logging, only when the wait happened:**
   - On success, a normal (not warning) live-log note: `Waited 2.3s for the page to finish loading results, then found 'See all results'.` A Details line is added, and the wait appears under "Waits:" in the technical diagnostic.
   - On failure, a Details line saying it did not appear. Then the **existing** failure message, screenshot and Retry step / Stop run card follow exactly as before. The message's existing "after waiting N seconds" wording now reflects the real wait.
   - Only the latest round's method timings are kept, so Details stay readable.

**Not used (each keeps its own existing handling):**
- fill / select – they have their own retry loop;
- Pick Element / Validate fast-forward (turbo);
- a target that was found but is covered, hidden behind a menu, stayed disabled, or changed state.

## Why it is generic and doesn't slow passing steps

- **Generic.** Nothing names a site, URL, text, selector, size or timing for this case. It uses only "requests from the previous step finished" and "page stopped changing", then the existing locators. So it works for any element that appears after a request: suggestions, dropdowns, lazy lists, toasts, modals, menus.
- **No slowdown for steps that resolve today.** A step found on the first search, or on the existing recheck, returns before this code is reached.
- **Real failures still fail.** A genuinely missing element now fails after this bounded wait instead of about 0.5 s in – at most about 9 s more, and never beyond the step budget.

## Separate correction: line endings from my previous task

While making the backup I found that my previous task's edits had silently converted six files from Windows (CRLF) to Unix (LF) line endings:

- `generator/script_generator.py`
- `app.py`
- `templates/live_log.html`
- `templates/recording_editor.html`
- `recorder/action_capture.js`
- `validation/report_generator.py`

It didn't change how they run, but it was an unintended whole-file reformat. All six are back to CRLF; their content is identical apart from line endings.

## How to test

Restart the Flask server first.

1. **Events search:** replay the Events → click search box → fill "GAGNER" → click "See all results" recording (`session_20261103_111817`).
   - Expected: step 27 passes.
   - When the dropdown was late, the live log shows a note like "Waited 1.8s for the page to finish loading results, then found 'See all results'." It is a note, not a warning.
   - Replay it 3–4 times: it should pass every time.
2. **Real failures still fail:** in the editor, change step 27's text/XPath to something that doesn't exist, then replay.
   - Expected: it fails after a short wait (a few seconds, at most about 9 s), with the same "wasn't on the page…" message, screenshot and Retry step / Stop run card.
3. **Nothing else changed:** replay a normal recording that passed before, e.g. `session_20261103_100245`.
   - Expected: same result, same step timings (steps found immediately are not slower), no new notes.
   - OTP card, field-error card and "Already in the recorded state – click skipped" behave as before.
