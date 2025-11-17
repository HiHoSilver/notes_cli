import os
from datetime import datetime
import argparse
import subprocess
from .file_path import notes_dir

NOTES_DIR: str = notes_dir.NOTES_DIR

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
        f.write(f"# {title}\n\n*Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n---\n\n{content}")
    
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

def select_note(notes) -> str | None:
    choice: str = input("\nEnter note number to edit: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(notes):
        print("Invalid choice.")
        return

    filename: str = notes[int(choice) - 1]
    filepath: str = os.path.join(NOTES_DIR, filename)

    return filename, filepath

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

def edit_note() -> None:
    notes = list_notes()
    if not notes:
        return

    filename, filepath = select_note(notes)

    choice: str = input("\nEnter additional lines (1), edit specific lines (2), or open in editor (3)?: ").strip()
    if not choice.isdigit or int(choice) < 1:
        print("Invalid choice.")
        return

    match choice:           # TODO: Add undo to this
        case "1":
            print("\nEnter lines to append (type 'END' on a new line to finish):")
            lines: list[str] = []
            while True:
                line: str = input()
                if line.strip().upper() == "END":
                    break
                
                lines.append(line)

            if lines:
                with open(filepath, "a", encoding="utf-8") as f:
                    f.write("\n" + "\n".join(lines) + "\n")
                print(f"New lines appended to '{filename}'.")
            else:
                print("No lines were added.")
        
        case "2":
            with open(filepath, "r", encoding="utf-8") as f:
                lines: list[str]= f.read().splitlines()

            for i, line in enumerate(lines, start=1):
                print(f"{i}. {line}")

            history_stack: list[str] = []
            while True:
                choice: str = input("\nEnter line number to edit (or type 'undo'): ").strip()
                if choice == "undo":
                    if history_stack:
                        lines = history_stack.pop()
                        print("\nUndo successful. Current lines:")
                        for i, line in enumerate(lines, start=1):
                            print(f"{i}. {line}")
                    else:
                        print("Nothing to undo.")
                    continue

                if not choice.isdigit() or int(choice) < 1 or int(choice) > len(lines):
                    print("Invalid choice.")
                    continue
    
                line_selection: int = int(choice) - 1
                print("\nEnter updated line, or type 'DEL' to delete:")
                update: str = input()
                history_stack.append(lines.copy())
                if update.strip().upper() == "DEL":
                    del lines[line_selection]
                else:
                    lines[line_selection] = update
                choice2: str = input("\nDo you want to edit any more lines (y/n)?").strip().lower()
                
                if choice2 == "n":
                    break
                elif choice2 == "undo":
                    if history_stack:
                        lines = history_stack.pop()
                        print("\nUndo successful. Current lines:")
                        for i, line in enumerate(lines, start=1):
                            print(f"{i}. {line}")
                    else:
                        print("Nothing to undo.")
                elif choice2 != "y":
                    print("Invalid Choice. Please enter 'y', 'n', or 'undo'.")
                    continue

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")

            print(f"Note '{filename}' updated successfully.")

        case "3":
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

    with open(filepath, "r", encoding="utf-8") as file:
        backup_content: str = file.read()

    os.remove(filepath)
    print(f"Deleted note '{filename}'.")

    choice2: str = input("Would you like to undo (y/n)? ").strip().lower()
    if choice2 == "y":
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(backup_content)
        print(f"Undo successful. Note '{filename}' restored.")
    elif choice2 == "n":
        print(f"Note '{filename}' permanently deleted.")
    else:
        print("Invalid choice. Please enter 'y' or 'n'.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Select mode")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--create", action="store_true", help="Create new note")
    group.add_argument("-v", "--view", action="store_true", help="View note")
    group.add_argument("-s", "--search", action="store_true", help="Search notes")
    group.add_argument("-e", "--edit", action="store_true", help="Edit note")
    group.add_argument("-d", "--delete", action="store_true", help="Delete note")
    group.add_argument("-l", "--list", action="store_true", help="List notes")
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
    elif args.list:
        list_notes()
    else:
        print("Invalid choice")

if __name__ == '__main__':
    main()
