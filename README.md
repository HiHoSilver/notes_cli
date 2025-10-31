## Notes CLI Tool

A simple CLI tool for taking notes.

## Installation
* Navigate to root folder '.\notes_cli\' (ensure root folder is in PATH)
* Run 'pip install .' (or `pip install -e .` for editable mode).
* Make a file named `notes_dir.py` with `NOTES_DIR` as a variable set to the absolute path of where you want your `notes` directory to be saved.

Example:
* `""C:\\Users\\user\\sourcerepos\\notes_cli\\notes_cli\\notes"`

## Use
Run from anywhere: `notes` + 
* `-c` or `--create`: create new note
* `-v` or `--view`: view note
* `-s` or `--search`: search notes
* `-e` or `--edit`: edit note
* `-d` or `--delete`: delete note

Example:
* `notes --create`