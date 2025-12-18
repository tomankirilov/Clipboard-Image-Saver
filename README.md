# Clipboard Image Saver

A small Windows desktop utility for saving images directly from the clipboard to disk.  
Designed for fast screenshot workflows and manual image collection without opening an image editor.

---

## Features

- Save clipboard images to disk (PNG / JPG)
- Configurable output directory  
  - Defaults to the user **Pictures** folder
- Optional custom filename  
  - Automatic timestamp fallback (`YYYY-MM-DD-HH-MM-SS`)
- PNG / JPG format selection
- Silent save mode (no success popup)
- Keyboard shortcut when focused (`Ctrl + S`)
- Persistent settings stored per user
- Custom window, taskbar, and EXE icon
- Portable one-file Windows EXE build

---

## Requirements

- Windows  
- Python 3.10+

---

## Development setup

### Create virtual environment

```powershell
py -m venv venv
```

### Activate environment

```powershell
venv\Scripts\activate
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Run the app (development)

```powershell
python src/clipboard_image_saver.py
```

---

## Build the EXE (one-file)

From the `src/` directory:

```powershell
python -m PyInstaller --onefile --windowed --icon app.ico clipboard_image_saver.py
```

### Output location

```
src/dist/clipboard_image_saver.exe
```

---

## Configuration storage

User settings are stored here:

```
%LOCALAPPDATA%\ClipboardImageSaver\config.json
```

This includes:
- Last used directory
- File extension
- Silent save preference

Settings persist across rebuilds and updates.

---

## Usage notes

- Clipboard must contain an image (screenshots, copied images, etc.)
- `Ctrl + S` only works while the app window is focused
- Silent save suppresses success dialogs but still shows errors
- Taskbar icon appears correctly only when running the built EXE  
  (`python.exe` will always show the Python icon)
