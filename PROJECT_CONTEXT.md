# USV Meta GUI Project Context

## Purpose

This project is a desktop application for creating mouseTube-compatible USV metadata JSON files.

The intended workflow is:

1. Choose a template or start from an empty record.
2. Fill experiment, protocol, subject, user, and file metadata.
3. Preview the generated JSON.
4. Validate required fields and schema constraints.
5. Save one JSON file per recording.
6. Continue with the next recording while reusing context or subject information.

The app is designed for repeated metadata entry during recording sessions, with a strong focus on reducing manual re-entry.

## Current Scope

The current application is a PySide6 desktop GUI with:

- Template management
- User preset management
- Record editing
- JSON preview
- Save flow
- Required-field validation
- Schema-based validation using `schema.yaml`
- English UI as default
- Dictionary-based language switching infrastructure
- Windows executable packaging via PyInstaller

## Architecture Overview

The codebase is intentionally split into three layers.

### 1. Data / domain layer

Files:

- [app/models.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/models.py:1)
- [app/serializer.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/serializer.py:1)
- [app/validator.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/validator.py:1)
- [app/schema_validator.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/schema_validator.py:1)

Responsibilities:

- Represent form state as dataclasses
- Convert a `RecordingRecord` into mouseTube-shaped JSON
- Check basic required fields
- Check schema constraints from `schema.yaml`

Design intention:

- Keep JSON generation logic out of the GUI
- Make future Web app reuse easier
- Keep validation logic independent from widgets

### 2. Persistence layer

Files:

- [app/repositories.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/repositories.py:1)

Responsibilities:

- Load and save templates
- Load and save user presets
- Load and save local settings
- Save exported record JSON files
- Generate export filenames

Design intention:

- Use simple local JSON files instead of a database
- Keep storage replaceable later
- Make debugging easy by storing human-readable files

### 3. GUI layer

Files:

- [main.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/main.py:1)
- [app/main_window.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/main_window.py:1)
- `app/pages/*.py`

Responsibilities:

- Screen flow
- Data entry widgets
- Triggering serialization and validation
- Navigation between editor, preview, and save result pages

Design intention:

- Keep pages relatively independent
- Centralize flow logic in `MainWindow`
- Avoid complex state frameworks for a small desktop app

## Main Data Flow

The normal record creation flow is:

1. `HomePage`
2. `TemplateSelectPage`
3. `RecordEditorPage`
4. `JsonPreviewPage`
5. `SaveResultPage`

Details:

1. The editor collects GUI values into a `RecordingRecord`.
2. `MouseTubeSerializer.serialize()` turns it into a JSON payload.
3. `RecordValidator.validate()` checks basic required fields.
4. `MouseTubeSchemaValidator.validate_payload()` checks schema-level rules.
5. `RecordRepository.save()` writes the JSON file with an auto-generated filename.

## Key Design Decisions

### Local JSON storage instead of database

Reason:

- The app is small and single-user oriented.
- Users need files they can inspect and back up easily.
- Templates, presets, settings, and exported metadata are all simple structured records.

Tradeoff:

- Fine for this scale.
- If multi-user editing or search becomes important, a DB-backed design may become preferable.

### Dataclasses as the internal model

Reason:

- Clear structure
- Easy mapping between widgets and data
- Easy serialization through `asdict`
- Good fit for future API or Web migration

### Two-step validation

There are two kinds of validation:

- `RecordValidator`: practical required fields for data entry
- `MouseTubeSchemaValidator`: schema compatibility checks

Reason:

- Required-field errors should be simple and immediate
- Schema errors should reflect metadata format constraints

### Preview before save

Reason:

- The user should inspect the final JSON before export
- This reduces accidental malformed data

### Separate "interaction partner" helper fields

Current behavior:

- Interaction-partner-related form inputs are merged into `file.notes`

Reason:

- The target mouseTube payload does not currently have a separate top-level interaction partner object in export
- The GUI still needs a convenient way to capture that context

Tradeoff:

- Convenient for entry
- Less structurally explicit in the saved JSON

## Current File/Folder Roles

- `main.py`: app startup, runtime file preparation, icon loading, initial window size
- `app/main_window.py`: central controller and screen transitions
- `app/pages/`: page widgets
- `app/i18n.py`: UI label dictionary and translation helper
- `data/templates.json`: reusable experiment templates
- `data/users.json`: reusable user presets
- `data/settings.json`: local settings including language and records directory
- `data/records/`: exported metadata JSON files
- `schema.yaml`: schema source currently used for validation
- `schema.json`: related schema artifact kept in the repo
- `USVMetaGUI.spec`: Windows packaging definition
- `assets/app.ico`: app icon

## Packaging Strategy

Windows packaging is handled by PyInstaller.

Relevant files:

- [USVMetaGUI.spec](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/USVMetaGUI.spec:1)
- [main.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/main.py:1)

Behavior:

- The executable bundles `data/`, `schema.yaml`, and `assets/`
- On first launch, runtime files are copied next to the executable if they do not exist
- This allows the packaged app to run without a separate installer

## Language / i18n Status

English is the current default UI language.

Implementation:

- `app/i18n.py` contains a dictionary-based translation table
- `AppSettings.language` stores the selected language
- `MainWindow.apply_language()` pushes the selected language into pages

Important note:

- The Japanese translation entries in `app/i18n.py` are currently mojibake/corrupted and need cleanup before Japanese switching can be considered production-ready.

## Known Issues and Cleanup Targets

### 1. Japanese translation strings are corrupted

Impact:

- English UI is usable
- Japanese UI cannot be trusted until strings are repaired

### 2. README tree display is corrupted

The tree block in `README.md` contains broken box-drawing characters.

Impact:

- Cosmetic/documentation issue only

### 3. Validation messages are still developer-facing

Examples:

- `experiment.name is required`
- schema path-style errors

Impact:

- Functional, but not ideal for end users

### 4. No automated test suite yet

Current confidence comes mainly from manual checks and compile/runtime smoke tests.

Impact:

- Future refactoring is riskier than necessary

## Suggested Next Technical Steps

Recommended order:

1. Repair Japanese translation strings in `app/i18n.py`
2. Clean up `README.md`
3. Add a small automated test set for serialization, filename generation, and schema validation
4. Improve user-facing validation wording
5. Rebuild the Windows executable after the above cleanup

## Web App Migration Plan

The desktop app was already structured in a way that supports future Web migration.

Recommended strategy:

### Reuse as-is

- `app/models.py`
- `app/serializer.py`
- `app/validator.py`
- `app/schema_validator.py`
- Parts of `app/repositories.py`

### Replace

- `app/main_window.py`
- `app/pages/*.py`
- Qt-specific widget code

### Best first Web stack

- FastAPI
- Jinja2 templates
- HTMX for partial updates if needed

Reason:

- Keeps most logic in Python
- Avoids a large frontend rewrite at first
- Makes migration incremental

### Proposed Web folder

```text
USVmetaGUI-web/
  app.py
  requirements.txt
  shared/
    models.py
    serializer.py
    validator.py
    schema_validator.py
    repositories.py
  web/
    routes.py
    templates/
    static/
```

### Web migration principle

Do not port the Qt widgets directly.

Instead:

- preserve the data model
- preserve validation and serialization rules
- redesign the UI around browser forms and request/response flow

## Resume Checklist

When restarting this project later, the most efficient sequence is:

1. Read this file
2. Read [README.md](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/README.md:1)
3. Read [app/main_window.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/main_window.py:1)
4. Check `git status`
5. Run the app from source
6. Decide whether the next task is desktop cleanup or Web app creation

Useful local commands:

```powershell
git status
python -m compileall main.py app
python main.py
python -m PyInstaller --noconfirm USVMetaGUI.spec
```

## Current Project State Summary

The desktop app is already functional and fairly complete.

What is done:

- Metadata entry flow
- Template reuse
- User preset reuse
- JSON preview
- Local JSON export
- Required-field validation
- Schema validation
- English UI default
- Language switch infrastructure
- Windows packaging

What remains most worth doing:

- fix Japanese strings
- polish validation UX
- add lightweight automated tests
- then begin a separate Web app project in a new folder
