# USV Meta GUI

PySide6 desktop application for creating mouseTube-compatible USV metadata JSON files.

## Features

- Create one JSON file per recording
- Reuse experiment templates
- Reuse user presets
- Preview the generated JSON before saving
- Validate required fields and schema constraints before export
- Save metadata locally in a mouseTube-compatible structure

## Project Structure

```text
USVmetaGUI/
├─ main.py
├─ requirements.txt
├─ schema.yaml
├─ USVMetaGUI.spec
├─ assets/
│  └─ app.ico
├─ data/
│  ├─ templates.json
│  ├─ users.json
│  ├─ settings.json
│  └─ records/
└─ app/
   ├─ main_window.py
   ├─ models.py
   ├─ repositories.py
   ├─ schema_validator.py
   ├─ serializer.py
   ├─ validator.py
   └─ pages/
```

## Run From Source

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Build Windows Executable

Install PyInstaller if needed:

```bash
python -m pip install pyinstaller
```

Build the app:

```bash
python -m PyInstaller --noconfirm USVMetaGUI.spec
```

The generated executable will be placed here:

```text
dist/USVMetaGUI.exe
```

On first launch, the executable creates local `data/` and `schema.yaml` files next to itself if they are not already present.

## GitHub Release Flow

1. Commit and push the current branch.
2. Build `dist/USVMetaGUI.exe`.
3. Open the GitHub repository.
4. Create a new Release from the `Releases` page.
5. Upload `USVMetaGUI.exe` as a release asset.

## Data Files

- `data/templates.json`: reusable experiment templates
- `data/users.json`: reusable user presets
- `data/settings.json`: local app settings
- `data/records/`: exported metadata JSON files
