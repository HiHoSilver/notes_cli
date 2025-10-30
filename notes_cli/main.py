import os
from datetime import datetime
import argparse
import subprocess

NOTES_DIR: str = "notes"

def create_dir() -> None:
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
        return
    
def create_note() -> None:
    title: str = input("Enter Note Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    
    filename: str = f"{title.replace(' ', '_')}.md"
    filepath = os.path.join(NOTES_DIR, filename)
    if os.path.exists(filepath):
        print("A note with this title already exists.")
        return
    
    print("Enter your note content (type 'END' on a new line to save):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        
        lines.append(line)
    
    content = "\n".join(lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content}\n\n---\n*Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    print(f"Note '{title}' saved successfully.")

def list_notes() -> list:
    notes: list[str] = os.listdir(NOTES_DIR)
    if not notes:
        print("No notes available.")
        return []
    
    print("\nAvaliable notes:")
    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note}")
    
    return notes

def view_note() -> None:
    notes = list_notes()
    if not notes:
        return
    
    choice: str = input("\nEnter note number to view: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Invalid choice.")
        return
    
    filename: list[str] = notes[int(choice) - 1]
    filepath: str = os.path.join(NOTES_DIR, filename)
    with open (filepath, "r", encoding="utf-8") as f:
        content: str = f.read()

    print(f"\n{'=' * 50}")
    print(content)
    print(f"{"=" * 50}")

def search_notes() -> None:
    keyword = input("Enter keyword to search: ").strip().lower()
    if not keyword:
        print("Keyword cannot be empty.")
        return
    
    found: bool = False
    for note in os.listdir(NOTES_DIR):
        filepath: str = os.path.join(NOTES_DIR, note)
        with open(filepath, "r", encoding="utf-8") as f:
            if keyword in f.read().lower():
                print(f" Found in: {note}")
                found: bool = True
    
    if not found:
        print("No matches found.")

import subprocess
import os

def edit_note() -> None:
    notes = list_notes()
    if not notes:
        return

    choice: str = input("\nEnter note number to edit: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Invalid choice.")
        return

    filename: str = notes[int(choice) - 1]
    filepath: str = os.path.join(NOTES_DIR, filename)

    print(f"Opening '{filename}' in Notepad...")
    subprocess.run(["notepad.exe", filepath])
    print(f"Finished editing '{filename}'.")

def delete_note() -> None:
    notes = list_notes()
    if not notes:
        return
    choice: str = input("\nEnter note number to delete: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Invalid choice.")
        return
    
    filename: str = notes[int(choice) - 1]
    filepath: str = os.path.join(NOTES_DIR, filename)
    os.remove(filepath)
    print(f"Deleted note '{filename}'.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Select mode")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--create", action="store_true", help="Create new note")
    group.add_argument("-v", "--view", action="store_true", help="View note")
    group.add_argument("-s", "--search", action="store_true", help="Search notes")
    group.add_argument("-e", "--edit", action="store_true", help="Edit note")
    group.add_argument("-d", "--delete", action="store_true", help="Delete note")
    args = parser.parse_args()
    
    create_dir()

    if args.create:
        create_note()
    elif args.view:
        view_note()
    elif args.search:
        search_notes()
    elif args.edit:
        edit_note()
    elif args.delete:
        delete_note()
    else:
        print("Invalid choice")

if __name__ == '__main__':
    main()
