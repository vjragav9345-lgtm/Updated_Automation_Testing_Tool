# AutoFlow QA — Folder Restructure Report

Date: 2026-11-03

The project was reorganized into `frontend/`, `backend/`, `data/`, `scripts/`, `docs/` and `_archive/`. Files were only moved. The only code edits are import lines and folder/path lines: 77 lines in 14 files, listed in section 5. No logic, routes, UI, CSS, JS behaviour, function names or dependencies changed. The start command is still `python app.py`.

Pre-flight: the first attempt found the Flask server running (PID 77907, port 5000), so it stopped without touching anything, as Rule 9 requires. On this run no `app.py`, replay, recording or Playwright process was running, and `localhost:5000` was free.

Backup: `../automate_testing_tool_new-main_BACKUP_BEFORE_RESTRUCTURE/` is a full copy made with `cp -Rp`, including `venv/`, data and `.git`. Both trees contain 14,760 entries.

---

## 1. Final folder tree

```
automate_testing_tool_new-main/
├── app.py                      (stays at root - start with: python app.py)
├── requirements.txt
├── README.md                   (path mentions updated)
├── .gitignore  .python-version  .claude/settings.local.json   (unchanged)
├── venv/                       (untouched)
├── config/
│   └── message_keywords.json
├── frontend/
│   ├── templates/   index.html, live_log.html, recording_editor.html,
│   │                report.html, run_stages.html, screenshots_viewer.html
│   └── static/
│       ├── css/style.css
│       └── js/script.js, run_control.js, remote_view.js
├── backend/
│   ├── __init__.py             (new, empty)
│   ├── utils.py
│   ├── remote_view.py
│   ├── recorder/    __init__.py, record_session.py, action_capture.js,
│   │                pick_element.py, page_snapshot.py
│   ├── generator/   __init__.py, script_generator.py
│   ├── executor/    __init__.py, run_execution.py
│   ├── validation/  __init__.py, compare.py, report_generator.py
│   └── storage/     __init__.py, repository.py, session_files.py, retention.py
├── data/
│   ├── recordings/             4 recordings + edited/ (1) + trimmed/ (empty)
│   ├── snapshots/              7 snapshot folders (132 files)
│   ├── executions/             (empty, legacy)
│   ├── searches/               (empty, legacy)
│   ├── generated_scripts/      98 generated scripts
│   │   ├── edited/             7 scripts
│   │   ├── fill_diagnostics/   7 png
│   │   └── screenshoots/       396 run folders (4,569 files)
│   ├── screenshots/            4 launch-screenshot folders
│   └── reports/                (empty)
│   (retention_archive/ did not exist; it is created on the first archive sweep)
├── scripts/
│   └── regenerate.py
├── tests/                      (unchanged - 392 .py files plus fixtures)
├── docs/                       (29 old reports and guides + this report)
└── _archive/
    ├── root_outputs/
    └── generated_scripts_handmade/
```

No empty `storage/`, `templates/`, `static/`, `generated_scripts/`, `screenshots/` or `reports/` folder was left at the root.

---

## 2. Old path → new path

| Old path | New path |
|---|---|
| `templates/*.html` (6 files) | `frontend/templates/` |
| `static/css/`, `static/js/` | `frontend/static/css/`, `frontend/static/js/` |
| `recorder/` (record_session.py, action_capture.js, pick_element.py, page_snapshot.py, `__init__.py`) | `backend/recorder/` |
| `generator/` (script_generator.py, `__init__.py`) | `backend/generator/` |
| `executor/` (run_execution.py, `__init__.py`) | `backend/executor/` |
| `validation/` (compare.py, report_generator.py, `__init__.py`) | `backend/validation/` |
| `storage/repository.py`, `session_files.py`, `retention.py`, `__init__.py` | `backend/storage/` |
| `utils.py` | `backend/utils.py` |
| `remote_view.py` | `backend/remote_view.py` |
| `regenerate.py` | `scripts/regenerate.py` |
| `storage/recordings/` (incl. `edited/`, `trimmed/`) | `data/recordings/` |
| `storage/snapshots/` | `data/snapshots/` |
| `storage/executions/` | `data/executions/` |
| `storage/searches/` | `data/searches/` |
| `generated_scripts/` (incl. `edited/`, `fill_diagnostics/`, `screenshoots/`) | `data/generated_scripts/` |
| `screenshots/` | `data/screenshots/` |
| `reports/` | `data/reports/` |
| `retention_archive/` | did not exist; the code now points to `data/retention_archive/` |
| `AUTOFLOW_CHANGES_REPORT.md`, `AutoFlow_Chatbot_Wait_Fix_Report.md`, `AutoFlow_FullAudit_Progress.md`, `AutoFlow_Full_Audit_Report.md`, `AutoFlow_MacFix_OTP_Warnings_Report.md`, `AutoFlow_OTP_Popup_FieldChange_Fix_Report.md`, `AutoFlow_Platform_Compatibility_Report.md`, `AutoFlow_Popup_Checkbox_Clear_Fix_Report.md`, `CROSS_PLATFORM_FIX_REPORT.md`, `FEATURE_PICK_ELEMENT_SNAPSHOT_REPORT.md`, `FIX_FALSE_MESSAGE_CARD_REPORT.md`, `FIX_OTP_GENERIC_REPORT.md`, `FIX_OTP_GROUP_REPORT.md`, `FIX_REDIRECT_DESTINATION_REPORT.md`, `FIX_SUBMIT_CAPTURE_REPORT.md`, `FIX_SUBMIT_ERROR_AND_STOP_REPORT.md`, `FIX_SUBMIT_MESSAGE_AND_REDIRECT_REPORT.md`, `FIX_TARGETED_RERUN_REPORT.md`, `PHASE_1_REPORT.md` … `PHASE_6_REPORT.md`, `ROLLBACK_REPORT.md`, `SCREENSHOT_LOGIC_REFERENCE.md`, `SEE_ALL_RESULTS_FIX_REPORT.md`, `PROJECT_GUIDE.md`, `sportzia_action_guide.md`, `Automation_Testing_Tool_Documentation_Updated_4.docx` | `docs/` (there was no guide PDF) |
| (new) | `backend/__init__.py` (empty) |

All moves used `mv`, so file timestamps were kept. This matters for the 30-day retention sweep.

---

## 3. Deleted files

Each one was checked first, and nothing in the app references any of them.

**Backup and rollback copies (23):**
`app.py.bak_20261103`, `app.py.rollback_saved`, `FEATURE_REPORT_rewind_reorder.md.rollback_removed`, `executor/run_execution.py.bak_20261103`, `executor/run_execution.py.rollback_saved`, `generator/script_generator.py.bak_20261103`, `generator/script_generator.py.bak_20261103_seeall`, `generator/script_generator.py.rollback_saved`, `recorder/action_capture.js.bak_20261103`, `recorder/pick_element.py.bak_20261103`, `recorder/record_session.py.bak_20261103`, `static/css/style.css.bak_20261103`, `static/css/style.css.rollback_saved`, `static/js/script.js.bak_20261103`, `static/js/script.js.rollback_saved`, `templates/index.html.bak_20261103`, `templates/live_log.html.bak_20261103`, `templates/live_log.html.rollback_saved`, `templates/recording_editor.html.bak_20261103`, `templates/recording_editor.html.rollback_saved`, `templates/report.html.rollback_saved`, `validation/report_generator.py.bak_20261103`, `validation/report_generator.py.rollback_saved`

**Caches:** 6 `__pycache__/` folders, 17 `.pyc` files in total: root, `storage/`, `generator/`, `recorder/`, `executor/`, `validation/`. There were none in `tests/`.

**Old worktree:** `.claude/worktrees/agent-a8900f878cb86facb/` (203 files, 35 MB, an old full copy of the project).

**Superseded stop notice:** `RESTRUCTURE_REPORT.md` at the root. I wrote it during the first attempt, when the server was running. This report replaces it.

Everything deleted still exists in the backup folder.

---

## 4. Archived files and why

| Archived to | File | Why |
|---|---|---|
| `_archive/root_outputs/` | `out.json`, `test4_result.json`, `test5_result.json`, `video_run_recording.json`, `video_run_report1.json`, `video_run_report2.json` | Stray result files from old test runs. Nothing references them. |
| `_archive/root_outputs/` | `storage.zip` (130 MB, created 2026-11-03 15:13) | Looks like a manual zip of the old `storage/` folder. Nothing references it, but it was recent and not on the delete list, so I archived it instead of deleting it. |
| `_archive/generated_scripts_handmade/` | `item6_name_check_script_v2.py`, `_v3.py`, `_v4.py`, `item7_screenshot_name_check.py`, `item7_screenshot_name_check2.py`, `item_a_fallback_check.py`, `item_c_icon_check.py`, `item_c_icon_check2.py`, `sportzia_flaky_test.py`, `task1_095629_test.py` | Investigation scripts, not generated from any current recording. No code or test references them. Leaving them in `data/generated_scripts/` would also have made them targets of the retention sweep. |

All other `session_*_script.py` files, including the root-level `*_edited_script.py` copies, were generated from recordings. They stayed in `data/generated_scripts/`.

---

## 5. Every code line changed

There are 77 changed lines in 14 files. Before writing, the edit script checked that each old text matched the expected number of times. Each file kept its own line endings: CRLF in app.py, record_session.py, script_generator.py, run_execution.py, report_generator.py and repository.py. A diff against the backup shows no other line changed.

| # | file:line | old text | new text |
|---|---|---|---|
| 1 | `app.py:51` | `from storage import repository` | `from backend.storage import repository` |
| 2 | `app.py:52` | `from storage import session_files` | `from backend.storage import session_files` |
| 3 | `app.py:53` | `from storage.repository import BASE_DIR` | `from backend.storage.repository import BASE_DIR` |
| 4 | `app.py:54` | `from storage.retention import run_cleanup, RETENTION_DAYS` | `from backend.storage.retention import run_cleanup, RETENTION_DAYS` |
| 5 | `app.py:55` | `from utils import normalize_url, attach_dialog_handler, server_safe_launch_kwargs` | `from backend.utils import normalize_url, attach_dialog_handler, server_safe_launch_kwargs` |
| 6 | `app.py:56` | `from recorder.record_session import Recorder` | `from backend.recorder.record_session import Recorder` |
| 7 | `app.py:57` | `import recorder.pick_element as pick_element` | `import backend.recorder.pick_element as pick_element` |
| 8 | `app.py:58` | `from recorder.pick_element import (` | `from backend.recorder.pick_element import (` |
| 9 | `app.py:62` | `from generator.script_generator import generate_script, EDITED_OUTPUT_DIR, OUTPUT_DIR, test_case_has_otp_step` | `from backend.generator.script_generator import generate_script, EDITED_OUTPUT_DIR, OUTPUT_DIR, test_case_has_otp_step` |
| 10 | `app.py:63` | `from executor.run_execution import execute_test,` | `from backend.executor.run_execution import execute_test,` |
| 11 | `app.py:64` | `from validation.report_generator import generate_report,` | `from backend.validation.report_generator import generate_report,` |
| 12 | `app.py:74` | `app = Flask(__name__)` | `app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static", static_url_path="/static")` |
| 13 | `app.py:78` | `import remote_view` | `import backend.remote_view as remote_view` |
| 14 | `app.py:592` | `BASE_DIR / "screenshots" /` | `BASE_DIR / "data" / "screenshots" /` |
| 15 | `app.py:685` | `from recorder.page_snapshot import RecordingSnapshotter` | `from backend.recorder.page_snapshot import RecordingSnapshotter` |
| 16 | `app.py:1062` | `from storage.retention import _active_run_dirs` | `from backend.storage.retention import _active_run_dirs` |
| 17 | `app.py:1491` | `from recorder import page_snapshot` | `from backend.recorder import page_snapshot` |
| 18 | `app.py:1514` | `(BASE_DIR / "recorder" / "action_capture.js")` | `(BASE_DIR / "backend" / "recorder" / "action_capture.js")` |
| 19 | `app.py:1668` | `from recorder import page_snapshot` | `from backend.recorder import page_snapshot` |
| 20 | `app.py:3299` | `run_dir = BASE_DIR / "generated_scripts" / "screenshoots" / run_id` | `run_dir = BASE_DIR / "data" / "generated_scripts" / "screenshoots" / run_id` |
| 21 | `app.py:3390` | `run_dir = BASE_DIR / "generated_scripts" / "screenshoots" / run_id` | `run_dir = BASE_DIR / "data" / "generated_scripts" / "screenshoots" / run_id` |
| 22 | `app.py:3524` | `run_dir = BASE_DIR / "generated_scripts" / "screenshoots" / run_id` | `run_dir = BASE_DIR / "data" / "generated_scripts" / "screenshoots" / run_id` |
| 23 | `app.py:4467` | `from generator.script_generator import _template_otp_helpers` | `from backend.generator.script_generator import _template_otp_helpers` |
| 24 | `backend/storage/repository.py:14` | `BASE_DIR = Path(__file__).resolve().parent.parent` | `BASE_DIR = Path(__file__).resolve().parent.parent.parent` |
| 25 | `backend/storage/repository.py:15` | `RECORDINGS_DIR = BASE_DIR / "storage" / "recordings"` | `RECORDINGS_DIR = BASE_DIR / "data" / "recordings"` |
| 26 | `backend/storage/repository.py:18` | `EXECUTIONS_DIR = BASE_DIR / "storage" / "executions"` | `EXECUTIONS_DIR = BASE_DIR / "data" / "executions"` |
| 27 | `backend/storage/repository.py:19` | `SEARCHES_DIR = BASE_DIR / "storage" / "searches"` | `SEARCHES_DIR = BASE_DIR / "data" / "searches"` |
| 28 | `backend/storage/repository.py:20` | `SNAPSHOTS_DIR = BASE_DIR / "storage" / "snapshots"` | `SNAPSHOTS_DIR = BASE_DIR / "data" / "snapshots"` |
| 29 | `backend/storage/repository.py:75` | `candidate = BASE_DIR / "storage" / p` | `candidate = BASE_DIR / "data" / p` |
| 30 | `backend/storage/repository.py:322` | `candidate = BASE_DIR / "storage" / p` | `candidate = BASE_DIR / "data" / p` |
| 31 | `backend/storage/repository.py:337` | `(RECORDINGS_DIR, "storage/recordings"),` | `(RECORDINGS_DIR, "data/recordings"),` |
| 32 | `backend/storage/repository.py:338` | `(EDITED_RECORDINGS_DIR, "storage/recordings/edited"),` | `(EDITED_RECORDINGS_DIR, "data/recordings/edited"),` |
| 33 | `backend/storage/repository.py:339` | `(TRIMMED_RECORDINGS_DIR, "storage/recordings/trimmed"),` | `(TRIMMED_RECORDINGS_DIR, "data/recordings/trimmed"),` |
| 34 | `backend/storage/retention.py:35` | `from storage.repository import BASE_DIR` | `from backend.storage.repository import BASE_DIR` |
| 35 | `backend/storage/retention.py:43` | `ARCHIVE_DIR = BASE_DIR / "retention_archive"` | `ARCHIVE_DIR = BASE_DIR / "data" / "retention_archive"` |
| 36 | `backend/storage/retention.py:52` | `BASE_DIR / "storage" / "recordings"` | `BASE_DIR / "data" / "recordings"` |
| 37 | `backend/storage/retention.py:53` | `BASE_DIR / "storage" / "recordings"` | `BASE_DIR / "data" / "recordings"` |
| 38 | `backend/storage/retention.py:54` | `BASE_DIR / "storage" / "recordings"` | `BASE_DIR / "data" / "recordings"` |
| 39 | `backend/storage/retention.py:55` | `BASE_DIR / "generated_scripts"` | `BASE_DIR / "data" / "generated_scripts"` |
| 40 | `backend/storage/retention.py:56` | `BASE_DIR / "generated_scripts"` | `BASE_DIR / "data" / "generated_scripts"` |
| 41 | `backend/storage/retention.py:57` | `BASE_DIR / "generated_scripts"` | `BASE_DIR / "data" / "generated_scripts"` |
| 42 | `backend/storage/retention.py:58` | `BASE_DIR / "generated_scripts"` | `BASE_DIR / "data" / "generated_scripts"` |
| 43 | `backend/storage/retention.py:59` | `("launch-screenshots", BASE_DIR / "screenshots", "*", False),` | `("launch-screenshots", BASE_DIR / "data" / "screenshots", "*", False),` |
| 44 | `backend/storage/retention.py:60` | `("reports", BASE_DIR / "reports", "*.html", False),` | `("reports", BASE_DIR / "data" / "reports", "*.html", False),` |
| 45 | `backend/storage/retention.py:80` | `from executor.run_execution import _active_replays, _active_replays_lock` | `from backend.executor.run_execution import _active_replays, _active_replays_lock` |
| 46 | `backend/storage/session_files.py:33` | `from storage.repository import (` | `from backend.storage.repository import (` |
| 47 | `backend/storage/session_files.py:40` | `SCRIPTS_DIR = BASE_DIR / "generated_scripts"` | `SCRIPTS_DIR = BASE_DIR / "data" / "generated_scripts"` |
| 48 | `backend/storage/session_files.py:49` | `from executor.run_execution import _slug` | `from backend.executor.run_execution import _slug` |
| 49 | `backend/storage/session_files.py:105` | `from recorder.page_snapshot import delete_snapshots` | `from backend.recorder.page_snapshot import delete_snapshots` |
| 50 | `backend/recorder/record_session.py:33` | `from storage.repository import RECORDINGS_DIR, SNAPSHOTS_DIR, _write_json, recover_orphaned_drafts` | `from backend.storage.repository import RECORDINGS_DIR, SNAPSHOTS_DIR, _write_json, recover_orphaned_drafts` |
| 51 | `backend/recorder/record_session.py:1810` | `from generator.script_generator import _template_otp_helpers` | `from backend.generator.script_generator import _template_otp_helpers` |
| 52 | `backend/recorder/pick_element.py:71` | `from generator.script_generator import generate_script` | `from backend.generator.script_generator import generate_script` |
| 53 | `backend/recorder/pick_element.py:72` | `from recorder.record_session import _CAPTURE_JS` | `from backend.recorder.record_session import _CAPTURE_JS` |
| 54 | `backend/recorder/pick_element.py:73` | `from utils import attach_dialog_handler, server_safe_launch_kwargs` | `from backend.utils import attach_dialog_handler, server_safe_launch_kwargs` |
| 55 | `backend/recorder/pick_element.py:74` | `import remote_view as _remote_view` | `import backend.remote_view as _remote_view` |
| 56 | `backend/recorder/pick_element.py:1129` | `from recorder import page_snapshot` | `from backend.recorder import page_snapshot` |
| 57 | `backend/recorder/pick_element.py:1225` | `from recorder import page_snapshot` | `from backend.recorder import page_snapshot` |
| 58 | `backend/recorder/page_snapshot.py:39` | `from storage.repository import SNAPSHOTS_DIR` | `from backend.storage.repository import SNAPSHOTS_DIR` |
| 59 | `backend/generator/script_generator.py:22` | `from storage.repository import BASE_DIR, strip_auto_created_validations, migrate_expected_urls, migrate_recording` | `from backend.storage.repository import BASE_DIR, strip_auto_created_validations, migrate_expected_urls, migrate_recording` |
| 60 | `backend/generator/script_generator.py:26` | `OUTPUT_DIR = BASE_DIR / "generated_scripts"` | `OUTPUT_DIR = BASE_DIR / "data" / "generated_scripts"` |
| 61 | `backend/generator/script_generator.py:5359` | `importlib.import_module("recorder.page_snapshot")` | `importlib.import_module("backend.recorder.page_snapshot")` |
| 62 | `backend/generator/script_generator.py:11212` | `Path(__file__).resolve().parent.parent / "config" / "message_keywords.json")` | `Path(__file__).resolve().parent.parent.parent / "config" / "message_keywords.json")` |
| 63 | `backend/executor/run_execution.py:28` | `from storage.repository import BASE_DIR` | `from backend.storage.repository import BASE_DIR` |
| 64 | `backend/executor/run_execution.py:29` | `from utils import normalize_url` | `from backend.utils import normalize_url` |
| 65 | `backend/executor/run_execution.py:30` | `from validation import compare` | `from backend.validation import compare` |
| 66 | `backend/executor/run_execution.py:204` | `run_dir = BASE_DIR / "generated_scripts" / "screenshoots" / run_id` | `run_dir = BASE_DIR / "data" / "generated_scripts" / "screenshoots" / run_id` |
| 67 | `backend/validation/compare.py:35` | `from storage.repository import BASE_DIR` | `from backend.storage.repository import BASE_DIR` |
| 68 | `backend/validation/report_generator.py:16` | `from storage.repository import BASE_DIR` | `from backend.storage.repository import BASE_DIR` |
| 69 | `backend/validation/report_generator.py:237` | `TEMPLATES_DIR = BASE_DIR / "templates"` | `TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"` |
| 70 | `backend/validation/report_generator.py:238` | `REPORTS_DIR = BASE_DIR / "reports"` | `REPORTS_DIR = BASE_DIR / "data" / "reports"` |
| 71 | `backend/remote_view.py:290` | `from executor import run_execution as _rex` | `from backend.executor import run_execution as _rex` |
| 72 | `scripts/regenerate.py:4` | `python regenerate.py storage/recordings/session_20260903_151100.json` | `python scripts/regenerate.py data/recordings/session_20260903_151100.json` |
| 73 | `scripts/regenerate.py:5` | `python regenerate.py  (regenerates all recordings in storage/recordings/)` | `python scripts/regenerate.py  (regenerates all recordings in data/recordings/)` |
| 74 | `scripts/regenerate.py:12` | `BASE_DIR = Path(__file__).resolve().parent` | `BASE_DIR = Path(__file__).resolve().parent.parent` |
| 75 | `scripts/regenerate.py:16` | `from generator.script_generator import generate_script` | `from backend.generator.script_generator import generate_script` |
| 76 | `scripts/regenerate.py:23` | `recordings_dir = BASE_DIR / "storage" / "recordings"` | `recordings_dir = BASE_DIR / "data" / "recordings"` |
| 77 | `frontend/templates/index.html:169` | `storage/recordings.` | `data/recordings.` |

Notes on the less obvious lines:
- **`repository.py:14`**: `parent.parent` became `parent.parent.parent` because the file is now one folder deeper. `BASE_DIR` is still the project root.
- **`repository.py:337-339`**: these are the paths `list_recordings()` sends to the dashboard. `load_recording()` and `set_display_name()` resolve them as `BASE_DIR/data/<p>`, then `BASE_DIR/<p>`. With the old `storage/recordings/...` text, both lookups would miss the file and Replay would fail. A broad search for path strings found this after the first pass.
- **`repository.py:75, 322`**: the "short path" fallback (`recordings/foo.json`) now resolves under `data/` instead of `storage/`.
- **`script_generator.py:5359`** (inside `SCRIPT_TEMPLATE`): the replay subprocess imports the snapshot saver by module name, with the project root on `sys.path`. It is now `backend.recorder.page_snapshot`. There is no `$` in the change.
- **`script_generator.py:11212`** (inside `SCRIPT_TEMPLATE`): the fallback that finds `config/` from the script's own location. A script in `data/generated_scripts/` is one folder deeper, so it needs one more `.parent`. In normal use `run_execution` always sets `AUTOFLOW_MESSAGE_KEYWORDS_FILE`, so the fallback only applies when a script is run by hand.
- **`app.py:74`**: `Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static", static_url_path="/static")`. Flask resolves these relative to `app.py`'s folder, and every URL stays `/static/...`.
- **`app.py:78`, `pick_element.py:74`**: `import remote_view` became `import backend.remote_view as remote_view` (and `as _remote_view`). The local names are the same, and both refer to the same module object.
- **Not changed, because they still resolve correctly:**
  - `record_session.py:62` reads `action_capture.js` from its own folder, which moved with it.
  - `record_session.py:221` uses `SNAPSHOTS_DIR.parent.parent`, which is still the project root.
  - `run_execution.py`: the `venv` path, `config/message_keywords.json` and `AUTOFLOW_PROJECT_ROOT` are all relative to `BASE_DIR`, which is still the project root.
  - The template's `fill_diagnostics` and `screenshoots` fallbacks are relative to the script's own folder.
  - The replay subprocess has no `cwd=`, so it inherits the Flask working directory and receives absolute paths.
  - `app.py:38` (`BASE_DIR` and `sys.path` for the root).
- **Path safety checks** (`_resolve_recording_file`, `_resolve_run_dir`, `_resolve_screenshot_file` used by `/screenshots/raw` and `/run/report`, `_resolve_stage_dir`, retention `_is_within`): these compare against `repository.RECORDINGS_DIR`, `SCREENSHOTS_ROOT = OUTPUT_DIR / "screenshoots"` and the retention targets. Those constants now point to `data/...`, so none of the checks needed a separate edit. Section 6 confirms them.
- **Documentation edits (not code):**
  - **README.md**: the Project Structure block was rewritten for the new layout, including `scripts/regenerate.py` with its run command. 108 other lines had their path mentions updated (for example `storage/recordings/` → `data/recordings/`, `recorder/…` → `backend/recorder/…`). Lines describing what an older README said were left as they were.
  - **`frontend/templates/index.html:169`**: the dashboard description text "storage/recordings." became "data/recordings.". This is the only frontend change. It is a displayed folder name.
  - **`scripts/regenerate.py:4-5`**: the usage lines in the docstring were updated.

---

## 6. Static self-check results

The checks did not launch the app, a browser, a recording or a replay. They ran with `PYTHONDONTWRITEBYTECODE=1`, so no new `__pycache__` folders were created.

1. **Compile:** 125 `.py` files (app.py, backend, scripts, `data/generated_scripts`; not venv, _archive, tests or the backup) compiled with **0 errors**. The `SyntaxWarning: invalid escape sequence` messages come from unchanged code: `script_generator.py:1603` and the JavaScript regexes inside old generated scripts.
2. **Imports** (venv Python 3.12.16, from the project root): all of these imported OK.
   - `backend`, `backend.utils`, `backend.storage.repository`, `backend.storage.session_files`, `backend.storage.retention`
   - `backend.recorder.record_session`, `backend.recorder.page_snapshot`, `backend.recorder.pick_element`
   - `backend.generator.script_generator`, `backend.executor.run_execution`
   - `backend.validation.compare`, `backend.validation.report_generator`, `backend.remote_view`

   No old top-level name (`storage`, `recorder`, `utils`, …) was loaded. app.py itself was not imported, so no Flask app was created. Its `Flask(...)` arguments were read with `ast`.
3. **Path existence** (printed by a throwaway script kept outside the project; all exist):
```
EXISTS  project root (repository.BASE_DIR) -> /Users/kovaionconsulting/Downloads/automate_testing_tool_new-main
EXISTS  frontend/templates (app.py template_folder) -> .../frontend/templates
EXISTS  frontend/static (app.py static_folder) -> .../frontend/static      (static_url_path: /static)
EXISTS  data/recordings (RECORDINGS_DIR) -> .../data/recordings
EXISTS  data/recordings/edited (EDITED_RECORDINGS_DIR) -> .../data/recordings/edited
EXISTS  data/recordings/trimmed (TRIMMED_RECORDINGS_DIR) -> .../data/recordings/trimmed
EXISTS  data/snapshots (SNAPSHOTS_DIR) -> .../data/snapshots
EXISTS  data/executions (EXECUTIONS_DIR) -> .../data/executions
EXISTS  data/searches (SEARCHES_DIR) -> .../data/searches
EXISTS  data/generated_scripts (OUTPUT_DIR) -> .../data/generated_scripts
EXISTS  data/generated_scripts/edited (EDITED_OUTPUT_DIR) -> .../data/generated_scripts/edited
EXISTS  data/generated_scripts/screenshoots (app SCREENSHOTS_ROOT) -> .../data/generated_scripts/screenshoots
EXISTS  data/generated_scripts/screenshoots (session_files.RUNS_DIR) -> .../data/generated_scripts/screenshoots
EXISTS  data/generated_scripts/screenshoots (run_execution run folder parent) -> .../data/generated_scripts/screenshoots
EXISTS  data/screenshots (launch screenshots) -> .../data/screenshots
EXISTS  data/reports (REPORTS_DIR) -> .../data/reports
EXISTS  frontend/templates/report.html (report_generator) -> .../frontend/templates/report.html
EXISTS  config/message_keywords.json (AUTOFLOW_MESSAGE_KEYWORDS_FILE) -> .../config/message_keywords.json
EXISTS  backend/recorder/action_capture.js (record_session) -> .../backend/recorder/action_capture.js
EXISTS  backend/recorder/action_capture.js (app.py Validate) -> .../backend/recorder/action_capture.js
EXISTS  venv python (run_execution) -> venv/bin/python (symlink to Homebrew python3.12)
EXISTS  all 9 retention targets (data/recordings, /edited, /trimmed, data/generated_scripts, /edited,
        /fill_diagnostics, /screenshoots, data/screenshots, data/reports)
retention ARCHIVE_DIR -> .../data/retention_archive (created on first archive sweep; parent exists)
capture JS loaded at import: 437,635 chars;  SCRIPT_TEMPLATE now imports backend.recorder.page_snapshot
```
4. **Same project root:** `app.py BASE_DIR`, `repository.BASE_DIR` and `AUTOFLOW_PROJECT_ROOT` (`str(run_execution.BASE_DIR)`) all resolve to `/Users/kovaionconsulting/Downloads/automate_testing_tool_new-main`. **ALL SAME: True**.
   - Extra round-trip check: every path `list_recordings()` returns, such as `data/recordings/session_20261103_111917.json` and `data/recordings/edited/session_20261103_111817_edited.json`, resolves through a copy of `_resolve_recording_file`'s logic, through `load_recording(raw path)` (the Replay route), and through `set_display_name`'s lookup. `set_display_name` was not called, because it writes.
   - A run folder, a step screenshot and a `report.json`, made relative with `relative_to(BASE_DIR)` as the app does, all resolve back inside `SCREENSHOTS_ROOT`.
5. **Search for old paths** (app.py, backend, frontend, scripts, config): there are no old `from storage/recorder/generator/executor/validation/utils/remote_view` imports. There is no `BASE_DIR / "storage"|"generated_scripts"|"screenshots"|"reports"|"templates"|"static"|"recorder"|"retention_archive"` left, and no old `import_module` target.
   - Some comments and docstrings still mention the old folder names, for example "Watches storage/recordings/" in app.py and the layout docstring in session_files.py. Rule 2 says not to touch comments, so they were left alone. They do not affect behaviour.
   - `app.py:4571` (`f"screenshots/{folder}/{inner}"`) is a folder name inside the export ZIP, not a disk path, so it was correctly left alone.
6. **No file lost:** all 9,986 original files outside `venv/` (counted from the backup, `.git` included) are accounted for:
   - 4,822 in `data/`, 18 in `backend/`, 10 in `frontend/`, 1 in `scripts/`, 1 in `config/`, 30 in `docs/`, 17 in `_archive/`, 4,805 in `tests/`
   - 5 at the root (app.py, README.md, requirements.txt, .gitignore, .python-version), 1 in `.claude/`, 32 in `.git/`
   - deleted: 23 backup copies, 17 cache files, 203 worktree files and 1 stop notice

   **Missing: 0.** The only new file is `backend/__init__.py`.
7. No check failed after the `repository.py:337-339` fix.

---

## 7. Stored paths in saved data, and what happens to old data

The saved data itself was not edited.

| Where | Stored path type | Example | After the move |
|---|---|---|---|
| Run `report.json` files in `data/generated_scripts/screenshoots/*/` | `screenshot` (593), `run_dir` (108), `console_log` (79), `final_screenshot` (51): root-relative paths | `generated_scripts/screenshoots/<run>/<stage>/stepN_….png` | These no longer point to a real file. See below. |
| Same files | Absolute paths from an older project location | `/Users/kovaionconsulting/Desktop/new/claude… 6/generated_scripts/...` (47) | These were already broken before the move, and nothing changes. |
| Same files | Absolute paths to this project | `/Users/kovaionconsulting/Downloads/automate_testing_tool_new-main/generated_scripts/...` (4) | These no longer point to a real file. |
| Recordings (`data/recordings/**.json`) | No folder paths stored (checked every field). `dom_snapshot_path` is null or not present. | – | No effect. |
| Snapshot metadata (`data/snapshots/*/*.json`) | Bare file names only (`"file": "final.mhtml"`). Snapshots are found by recording name under `SNAPSHOTS_DIR`. | – | No effect. Pick Element and Validate still find the snapshots. |
| Generated scripts already on disk (20 contain the old template text) | The old `import_module("recorder.page_snapshot")` and `parent.parent / "config"` fallback | – | The dashboard regenerates the script from the current template before every Replay (`app.py` → `generate_script` → `start_replay`), so dashboard replays use the new lines. Only running an old script by hand would print `[snapshot] WARNING: missing page snapshots will not be saved in this run`. That is non-fatal and the replay continues. |
| Browser `sessionStorage` (`SELECTED_RECORDINGS_KEY`) | The dashboard's checked recordings, stored as `storage/recordings/...` paths | – | They no longer match the new `data/recordings/...` paths, so any checkbox selection still open in a browser tab is dropped once. Select again; this is per tab and temporary. |

**What old runs (made before the move) still do:**
- The Screenshots viewer, the Stages viewer and View Last Log still list and open old runs, because they scan the folders on disk.
- Old `report.html` files still open in full, because their screenshots are embedded as base64.
- In View Last Log for an old run, the individual step-screenshot links (`/screenshots/raw?path=generated_scripts/...`) return "Screenshot not found." (404).
- The export ZIP still includes an old run's images, but the screenshot column in the CSV is empty for those steps.
- All runs made after the move store `data/generated_scripts/...` paths and work fully.

As instructed, no code was added to handle old data.

---

## 8. Test files that still use old paths (not edited)

370 test files under `tests/` (`.py`/`.sh`; there are 392 `.py` files in total) refer to old imports (`from storage…`, `from generator…`, `import recorder…` and so on; 116 files) or old folder paths (`storage/recordings`, `generated_scripts/`, `templates/`, `static/`, `action_capture.js`, `regenerate.py`). They will need path updates before they are run again. Many also insert the project root into `sys.path` and import the top-level packages, which now live under `backend.`.

<details><summary>Full list (370 files, relative to tests/)</summary>

`_apply_patch_mappers.py`, `_apply_patch_scaled.py`, `_probe_out/_dyn.py`, `_probe_out/acc/acc.py`, `_probe_out/altdbg/s.py`, `_probe_out/bakpaste/p.py`, `_probe_out/bug1_A_fixed/bug1_A_fixed.py`, `_probe_out/bug1_A_orig/bug1_A_orig.py`, `_probe_out/bug1_B_fixed/bug1_B_fixed.py`, `_probe_out/bug1_B_orig/bug1_B_orig.py`, `_probe_out/bug1_C_fixed/bug1_C_fixed.py`, `_probe_out/cdbg_a/s.py`, `_probe_out/cdbg_b/s.py`, `_probe_out/cdbg_c/s.py`, `_probe_out/cdbg_d/s.py`, `_probe_out/cdbg_e/s.py`, `_probe_out/cdbg_f/s.py`, `_probe_out/cdbg_g/s.py`, `_probe_out/cdbg_h/s.py`, `_probe_out/cdbg_i/s.py`, `_probe_out/cdbg_j/s.py`, `_probe_out/checkbox_v1_changed_site/checkbox_v1_changed_site_script.py`, `_probe_out/checkbox_v2_baseline_same_site/checkbox_v2_baseline_same_site_script.py`, `_probe_out/classifier/r1b_old_fill/r1b_old_fill_script.py`, `_probe_out/classifier/r1c_forever/r1c_forever_script.py`, `_probe_out/classifier/r1d_user/r1d_user_script.py`, `_probe_out/classifier/r2a_navmismatch/r2a_navmismatch_script.py`, `_probe_out/classifier/r2b_cover_esc/r2b_cover_esc_script.py`, `_probe_out/classifier/r2b_cover_perm/r2b_cover_perm_script.py`, `_probe_out/classifier/r3_hover/r3_hover_script.py`, `_probe_out/count_elements_click_delay6_check/count_elements_click_delay6_check_script.py`, `_probe_out/count_elements_click_delay6_recheck/count_elements_click_delay6_recheck_script.py`, `_probe_out/count_elements_click_delay_check/count_elements_click_delay_check_script.py`, `_probe_out/count_elements_delay_check/count_elements_delay_check_script.py`, `_probe_out/count_elements_zero_check/count_elements_zero_check_script.py`, `_probe_out/cover/copy/copy.py`, `_probe_out/cover/menu/menu.py`, `_probe_out/cover/stuck/stuck.py`, `_probe_out/cover/timer/timer.py`, `_probe_out/dc_bug1_fixed/dc_bug1_fixed_script.py`, `_probe_out/dc_bug1_original/dc_bug1_original_script.py`, `_probe_out/dc_debug2/dc_debug2_script.py`, `_probe_out/dc_final_check1_7of7/dc_final_check1_7of7_script.py`, `_probe_out/dc_final_check2_wrong_expectation/dc_final_check2_wrong_expectation_script.py`, `_probe_out/dc_final_check3_instant_pass/dc_final_check3_instant_pass_script.py`, `_probe_out/dc_full_repro/dc_full_repro_script.py`, `_probe_out/dc_item3_repro/dc_item3_repro_script.py`, `_probe_out/destination/dbg/dbg.py`, `_probe_out/destination/r6b_old_shape/r6b_old_shape.py`, `_probe_out/destination/r6c_wrong/r6c_wrong.py`, `_probe_out/destination/r6d_href/r6d_href.py`, `_probe_out/destination/r6d_href_noop/r6d_href_noop.py`, `_probe_out/destination/r6e_spa/r6e_spa.py`, `_probe_out/destination/r6f_tracking/r6f_tracking.py`, `_probe_out/destination/r6g_query/r6g_query.py`, `_probe_out/dollar_fix_check/dollar_fix_check_script.py`, `_probe_out/faultrun.py`, `_probe_out/fielddbg/s.py`, `_probe_out/first_action/fa.py`, `_probe_out/gap/gap.py`, `_probe_out/generic/a_dialog/a_dialog.py`, `_probe_out/generic/a_form/a_form.py`, `_probe_out/generic/a_icons/a_icons.py`, `_probe_out/generic/a_link_newtab/a_link_newtab.py`, `_probe_out/generic/a_link_same/a_link_same.py`, `_probe_out/generic/a_menu/a_menu.py`, `_probe_out/generic/a_noop/a_noop.py`, `_probe_out/generic/a_results_link/a_results_link.py`, `_probe_out/generic/a_search_reload/a_search_reload.py`, `_probe_out/generic/a_search_spa/a_search_spa.py`, `_probe_out/generic/a_tabs/a_tabs.py`, `_probe_out/generic/f_content/f_content.py`, `_probe_out/generic/f_content_gone/f_content_gone.py`, `_probe_out/generic/f_different_address/f_different_address.py`, `_probe_out/generic/f_enter_does_nothing/f_enter_does_nothing.py`, `_probe_out/generic/f_popup_never_opens/f_popup_never_opens.py`, `_probe_out/generic/f_target_missing/f_target_missing.py`, `_probe_out/generic/w_count/w_count.py`, `_probe_out/hover_baseline_same_site/hover_baseline_same_site_script.py`, `_probe_out/hover_changed_site_attempt1/hover_changed_site_attempt1_script.py`, `_probe_out/hover_changed_site_attempt2/hover_changed_site_attempt2_script.py`, `_probe_out/hover_changed_site_attempt3/hover_changed_site_attempt3_script.py`, `_probe_out/hover_modal/i2a_hidden_menu/i2a_hidden_menu.py`, `_probe_out/hover_modal/i2b_far_copy/i2b_far_copy.py`, `_probe_out/hover_modal/i3a_shadow/i3a_shadow.py`, `_probe_out/hover_modal/i3b_none/i3b_none.py`, `_probe_out/hover_modal/i3c_escape/i3c_escape.py`, `_probe_out/hover_modal/i3d_stuck/i3d_stuck.py`, `_probe_out/hover_only/direct/direct.py`, `_probe_out/hover_only/dwell/dwell.py`, `_probe_out/hover_only/off-screen-menu/off-screen-menu.py`, `_probe_out/hover_only/via-panel/via-panel.py`, `_probe_out/multipick_test_F_nav/multipick_test_F_nav_script.py`, `_probe_out/multipick_test_b/multipick_test_b_script.py`, `_probe_out/multipick_test_f/multipick_test_f_script.py`, `_probe_out/names/aria-label/n_aria-label.py`, `_probe_out/names/nothing/n_nothing.py`, `_probe_out/phase1_ambiguous/phase1_ambiguous_script.py`, `_probe_out/phase1_baseline_same_site/phase1_baseline_same_site_script.py`, `_probe_out/phase1_changed_site_attempt1/phase1_changed_site_attempt1_script.py`, `_probe_out/phase1_changed_site_attempt2/phase1_changed_site_attempt2_script.py`, `_probe_out/phase1_changed_site_attempt3/phase1_changed_site_attempt3_script.py`, `_probe_out/phase1c_strict/phase1c_strict_script.py`, `_probe_out/phase5_check/phase5_check_script.py`, `_probe_out/phase5_check2/phase5_check2_script.py`, `_probe_out/phase5_gen_check/phase5_gen_check_script.py`, `_probe_out/phase5_mismatch_check/phase5_mismatch_check_script.py`, `_probe_out/phaseB_test1_open_close/phaseB_test1_open_close_script.py`, `_probe_out/phaseB_test2_extra_close/phaseB_test2_extra_close_script.py`, `_probe_out/popup_close/a_open/a_open.py`, `_probe_out/popup_close/b_closed0/b_closed0.py`, `_probe_out/popup_close/b_closed1/b_closed1.py`, `_probe_out/popup_close/b_closed2/b_closed2.py`, `_probe_out/popup_close/b_closed3/b_closed3.py`, `_probe_out/popup_close/b_closed4/b_closed4.py`, `_probe_out/popup_close/c_stuck/c_stuck.py`, `_probe_out/popup_close/d_old/d_old.py`, `_probe_out/popup_flow/popup_flow.py`, `_probe_out/popup_idle/idle/idle.py`, `_probe_out/popup_idle/noclose/noclose.py`, `_probe_out/r8_regression/r8_regression_script.py`, `_probe_out/r8_regression_rerun/r8_regression_rerun_script.py`, `_probe_out/real/real_form/real_form.py`, `_probe_out/real/real_more/real_more.py`, `_probe_out/real/real_paste/real_paste.py`, `_probe_out/real/real_pyorg/real_pyorg.py`, `_probe_out/real/real_shop/real_shop.py`, `_probe_out/real/real_wiki/real_wiki.py`, `_probe_out/reveal/a_click_trigger/a_click_trigger.py`, `_probe_out/reveal/a_fast/a_fast.py`, `_probe_out/reveal/a_hover_empty/a_hover_empty.py`, `_probe_out/reveal/a_linger/a_linger.py`, `_probe_out/reveal/a_slow/a_slow.py`, `_probe_out/reveal/b_click_menu/b_click_menu.py`, `_probe_out/reveal/c_spa/c_spa.py`, `_probe_out/reveal/d_wrong/d_wrong.py`, `_probe_out/reveal/e_toggle/e_toggle.py`, `_probe_out/rn/phase2_trigger_click_1/phase2_trigger_click.py`, `_probe_out/rn/phase2_trigger_click_2/phase2_trigger_click.py`, `_probe_out/rn/phase2_trigger_click_3/phase2_trigger_click.py`, `_probe_out/rn/phase2_trigger_click_4/phase2_trigger_click.py`, `_probe_out/rn/phase2_trigger_click_5/phase2_trigger_click.py`, `_probe_out/rn/real_wiki_1/real_wiki.py`, `_probe_out/rn/session_20261001_230811_1/session_20261001_230811.py`, `_probe_out/rn/session_20261002_080847_1/session_20261002_080847.py`, `_probe_out/rn/session_20261002_080847_2/session_20261002_080847.py`, `_probe_out/rn/session_20261002_080847_3/session_20261002_080847.py`, `_probe_out/rn/session_20261002_080847_4/session_20261002_080847.py`, `_probe_out/rn/session_20261002_080847_5/session_20261002_080847.py`, `_probe_out/rn/session_20261002_081541_1/session_20261002_081541.py`, `_probe_out/rn/session_20261002_081541_2/session_20261002_081541.py`, `_probe_out/rn/session_20261002_081541_3/session_20261002_081541.py`, `_probe_out/rn/session_20261002_081541_4/session_20261002_081541.py`, `_probe_out/rn/session_20261002_081541_5/session_20261002_081541.py`, `_probe_out/rn/session_20261004_091722_1/session_20261004_091722.py`, `_probe_out/rn/session_20261004_154911_1/session_20261004_154911.py`, `_probe_out/rn/session_20261004_164227_1/session_20261004_164227.py`, `_probe_out/rn/session_20261004_213748_1/session_20261004_213748.py`, `_probe_out/rn_keep/session_20261002_080847_1/session_20261002_080847.py`, `_probe_out/rn_keep/session_20261002_080847_2/session_20261002_080847.py`, `_probe_out/rn_keep/session_20261002_080847_3/session_20261002_080847.py`, `_probe_out/rn_keep/session_20261002_080847_4/session_20261002_080847.py`, `_probe_out/rn_keep/session_20261002_080847_5/session_20261002_080847.py`, `_probe_out/rr/session_20261001_230456/session_20261001_230456.py`, `_probe_out/rr/session_20261001_230811/session_20261001_230811.py`, `_probe_out/rr/session_20261001_231104/session_20261001_231104.py`, `_probe_out/screenshot_settle/busy_manual/busy_manual.py`, `_probe_out/screenshot_settle/skeleton_manual/skeleton_manual.py`, `_probe_out/sidecheck/_dyn.py`, `_probe_out/sidecheck/a1/a1.py`, `_probe_out/sidecheck/a2/a2.py`, `_probe_out/sidecheck/a3/a3.py`, `_probe_out/sidecheck/a4/a4.py`, `_probe_out/sidecheck/a5/a5.py`, `_probe_out/sidecheck/b1/b1.py`, `_probe_out/sidecheck/b2/b2.py`, `_probe_out/sidecheck/b3/b3.py`, `_probe_out/sidecheck/b3b/b3b.py`, `_probe_out/sidecheck/b4/b4.py`, `_probe_out/sidecheck/b4ok/b4ok.py`, `_probe_out/sidecheck/b5/b5.py`, `_probe_out/sidecheck/b5f/b5f.py`, `_probe_out/sidecheck/c1/c1.py`, `_probe_out/sidecheck/c2/c2.py`, `_probe_out/sidecheck/c3/c3.py`, `_probe_out/sidecheck/c4/c4.py`, `_probe_out/sidecheck/c5/c5.py`, `_probe_out/sidecheck/c6/c6.py`, `_probe_out/sidecheck/c7/c7.py`, `_probe_out/sidecheck/c8/c8.py`, `_probe_out/sidecheck/c8ok/c8ok.py`, `_probe_out/sidecheck/c9a/c9a.py`, `_probe_out/sidecheck/c9b/c9b.py`, `_probe_out/sidecheck/chat5/chat5.py`, `_probe_out/sidecheck/dbg/dbg.py`, `_probe_out/strat_acc9/s.py`, `_probe_out/strat_after/s.py`, `_probe_out/strat_before/s.py`, `_probe_out/strat_demo6new/s.py`, `_probe_out/strat_demo6new2/s.py`, `_probe_out/strat_new/s.py`, `_probe_out/strat_r1/s.py`, `_probe_out/tabclose_guards_case1_last_tab/tabclose_guards_case1_last_tab_script.py`, `_probe_out/tabclose_guards_case2_already_closed/tabclose_guards_case2_already_closed_script.py`, `_probe_out/tabopen_investigate/tabopen_investigate_script.py`, `_probe_out/tabopen_investigate2_normal_control/tabopen_investigate2_normal_control_script.py`, `_probe_out/tabopen_investigate3/tabopen_investigate3_script.py`, `_probe_out/timing_105345/timing_105345_script.py`, `_probe_out/tl_after1/s.py`, `_probe_out/tl_after2/s.py`, `_probe_out/tl_after3/s.py`, `_probe_out/tl_after4/s.py`, `_probe_out/tl_before/s.py`, `_probe_out/twin/footer_by_href/footer_by_href.py`, `_probe_out/twin/footer_by_landmark/footer_by_landmark.py`, `_probe_out/twin/header_by_href/header_by_href.py`, `_probe_out/twin/header_by_landmark/header_by_landmark.py`, `_probe_out/url_classify/u.py`, `_probe_out/verify4_start_then_visible/verify4_start_then_visible_script.py`, `_probe_out/verify56_baseline_item5_myntra/verify56_baseline_item5_myntra_script.py`, `_probe_out/verify56_baseline_item6_blinkit/verify56_baseline_item6_blinkit_script.py`, `_probe_out/verify56_item5_myntra/verify56_item5_myntra_script.py`, `_probe_out/verify56_item6_blinkit/verify56_item6_blinkit_script.py`, `_probe_out/warning_status/a_prompt/a_prompt_script.py`, `_probe_out/warning_status/b_slot/b_slot_script.py`, `_probe_out/warning_status/c_nothing/c_nothing_script.py`, `acceptance_live.py`, `autoval_ui_check.py`, `bug1_2_deliberate_fail_check.py`, `bug1_wait_check.py`, `bug2_pick_check.py`, `bug2_pick_site2.py`, `checkbox_fix3_check.py`, `checkbox_hardening_check.py`, `checkbox_livesite_check.py`, `checkbox_state_helper_check.py`, `checkbox_ui_check.py`, `checkbox_value_changed_check.py`, `classifier_check.py`, `count_elements_validation_check.py`, `cover_check.py`, `dashboard_ui_check.py`, `dc_bug1_verify.py`, `dc_debug_check2.py`, `dc_final_repro.py`, `dc_full_repro.py`, `dc_item3_repro.py`, `dc_xpath_probe.py`, `dc_xpath_trace.py`, `destination_check.py`, `dragscroll_cascade_check.py`, `dragscroll_final_run.sh`, `dragscroll_final_run2.sh`, `dragscroll_final_run3.sh`, `dragscroll_final_run4.sh`, `dragscroll_probe.py`, `dragscroll_reached_check.py`, `dragscroll_scenario_record.py`, `dragscroll_scroll_check.py`, `dropdown_ui_check.py`, `dynurl_check.py`, `first_action_check.py`, `fixture_from_snapshot.py`, `fixtures/empirical_audit_fixture.py`, `fixtures/fill_replay_check.py`, `fixtures/highlight_test.py`, `fixtures/hover_probe.py`, `fixtures/regression_check/regcheck_myntra_men_tshirt_full_flow_edited.py`, `fixtures/stress_test_final.py`, `fixtures/validate_url_test.py`, `flowfix10_test1_crash_recovery.py`, `flowfix10_test2_locator_stability.py`, `flowfix10_test3_multithumb_drag.py`, `flowfix5_synthetic_test.py`, `flowfix9_test2_drag_capture.py`, `flowfix9_test3_drag_replay.py`, `flowfix9_test4_report_fix4.py`, `flowfix9_test5_snapshot_scale.py`, `flowfix9_test6_scale_benchmark.py`, `flowfix_validate.py`, `flowfixd_diagnostic.py`, `gap_check.py`, `generic_flow_check.py`, `hover_modal_check.py`, `hover_only_check.py`, `hover_volatile_number_check.py`, `livelog_display_check.py`, `livelog_replay.py`, `multipick_dragselect_check.py`, `multipick_nav_check.py`, `myntra_compare_old_new.py`, `names_check.py`, `navclass_check.py`, `navhost_check.py`, `navredirect_check.py`, `one_time_session_cleanup.py`, `otp_locator_probe.py`, `otp_natural_capture.py`, `otp_race_harness.py`, `otp_real_run_wrapper.py`, `otp_repeat_check.py`, `otp_resolver_unit_tests.py`, `overlay_recovery_recorded_modal_check.py`, `pairing_check.py`, `phase1_volatile_number_check.py`, `phase4_test_bug1_hover.py`, `phase4_test_bug2_card.py`, `phase4_test_helpers.py`, `phaseB_manual_tabopen_check.py`, `pick_prefix_failure_check.py`, `pick_prefix_probe.py`, `pick_prefix_ui_check.py`, `popup_close_check.py`, `popup_flow_check.py`, `popup_idle_check.py`, `prestart_check.py`, `proof_run_via_server.py`, `r8_regression_check.py`, `real_sites_check.py`, `record_live_flows.py`, `recorder_smoke_test.py`, `recorder_tabclose_check.py`, `regression_phase.py`, `replay_n.py`, `replay_recordings.py`, `reveal_check.py`, `run_empirical_audit.py`, `screenshot_settle_check.py`, `sidecheck_check.py`, `sidecheck_helpers.py`, `tabclose_guards_check.py`, `tabopen_investigate.py`, `tabopen_investigate2.py`, `tabopen_investigate3.py`, `task0_fill_probe.py`, `test_chat_enter_readiness.py`, `test_fill_target_identity.py`, `test_fix1_value_range.py`, `test_fix2_page_mismatch.py`, `test_overlay_position_target.py`, `test_relocated_click_identity.py`, `test_semantic_href_identity.py`, `test_step10_locator_identity.py`, `test_url_change_verification.py`, `test_warning_classification.py`, `timing_investigate_item0.py`, `timing_investigate_item0b.py`, `timing_probe_105345.py`, `townscript_record_live.py`, `twin_check.py`, `ui_verify_bug2_value_range.py`, `ui_verify_bug3_url_wildcard.py`, `ui_verify_bug4_popup.py`, `ui_verify_dragfix.py`, `ui_verify_dragfix_s6.py`, `ui_verify_fix1_value_range.py`, `ui_verify_fix2_page_mismatch.py`, `ui_verify_followup4.py`, `ui_verify_followup4_v10.py`, `ui_verify_v1_v2.py`, `ui_verify_v3_v4.py`, `ui_verify_v5_v6.py`, `ui_verify_v7.py`, `url_classify_check.py`, `validate_visible_dropdown_check.py`, `verify_item4.py`, `verify_items56.py`, `verify_items56_baseline_check.py`, `warning_live_run.py`, `warning_status_check.py`

</details>

---

## 9. Uncertain items and things deliberately left alone

1. **`.gitignore`** was not edited (rule: keep hidden config files as they are), but its patterns no longer match the new layout:
   - `storage/` has no leading slash, so it matches any folder named `storage` and **now ignores `backend/storage/`**, which is source code.
   - `generated_scripts/screenshoots/` and `generated_scripts/fill_diagnostics/` contain a slash, so they only match at the root. Run output under `data/generated_scripts/` is no longer ignored.
   - Before the next commit, these lines are suggested in place of the old ones: `/data/recordings/`, `/data/snapshots/`, `/data/executions/`, `/data/searches/`, `/data/screenshots/`, `/data/generated_scripts/screenshoots/`, `/data/generated_scripts/fill_diagnostics/`, and drop the bare `storage/` line. `screenshots/` still works as it is.
2. **`.claude/settings.local.json`** still allows `python -m py_compile generator/script_generator.py app.py`. That is a Claude permission rule, not app code, and was left unchanged. The new equivalent path is `backend/generator/script_generator.py`.
3. **`storage.zip`** was archived rather than deleted (see section 4). Delete it from `_archive/` if it is not needed.
4. **Comments and docstrings** in the code that mention `storage/recordings/`, `generated_scripts/` and so on were not changed (Rule 2). Only `regenerate.py`'s usage docstring was updated, because it tells you how to run the tool.
5. **`docs/*.md` history reports** describe the old layout and were moved without changes.
6. **Logger names** now include the package, for example `backend.storage.repository` instead of `storage.repository`, because modules use `getLogger(__name__)`. Nothing in the project filters loggers by name, so this only changes the label in log lines.
7. **README** still mentions `templates/recording_trim.html`, which did not exist before this change either. Only its path prefix was updated.
8. `data/executions/`, `data/searches/` and `data/reports/` are empty legacy folders. They were moved anyway because the code creates or uses them.

---

## 10. How to start the app

Unchanged, from the project root:

```
python app.py
```

(or `venv/bin/python app.py`). The dashboard is still at `http://localhost:5000`. The script-regeneration tool is now `python scripts/regenerate.py [data/recordings/<file>.json ...]`.

Nothing was launched for this change. Please start the app and check the usual flows: dashboard, record, edit, replay, screenshots and export. If anything is wrong, the full original is in `../automate_testing_tool_new-main_BACKUP_BEFORE_RESTRUCTURE/`.
