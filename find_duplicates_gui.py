import os
import hashlib
import shutil
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from typing import List, Dict, Tuple, Optional

# --- Constants ---
DUPLICATES_DIRNAME = "duplicates"
LOG_FILENAME = "duplicates_log.txt"
CHUNK_SIZE = 8192

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Utility Functions ---

def get_file_hash(file_path: str, chunk_size: int = CHUNK_SIZE) -> Optional[str]:
    """Calculate the MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error hashing file {file_path}: {e}")
        return None

def is_in_excluded_folder(file_path: str, excluded_folders: List[str]) -> bool:
    """Check if a file is in any of the excluded folders."""
    return any(os.path.commonpath([os.path.abspath(file_path), ex]) == ex for ex in excluded_folders)

# --- Core Logic ---

def find_and_move_duplicates(
    root_folder: str, 
    exclude_folders: List[str], 
    dry_run: bool = False
) -> List[str]:
    """
    Find duplicate files in root_folder (excluding exclude_folders).
    Move duplicates to a 'duplicates' directory or simulate if dry_run.
    Returns log lines.
    """
    seen: Dict[Tuple[int, str], str] = {}
    duplicates_dir = os.path.join(root_folder, DUPLICATES_DIRNAME)
    os.makedirs(duplicates_dir, exist_ok=True)
    log_lines: List[str] = []

    for dirpath, _, filenames in os.walk(root_folder):
        if is_in_excluded_folder(dirpath, exclude_folders) or dirpath == duplicates_dir:
            continue

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if is_in_excluded_folder(file_path, exclude_folders):
                continue

            try:
                size = os.path.getsize(file_path)
                file_hash = get_file_hash(file_path)
                if not file_hash:
                    continue

                key = (size, file_hash)
                if key in seen:
                    base_name = os.path.basename(file_path)
                    target_path = os.path.join(duplicates_dir, base_name)
                    counter = 1
                    while os.path.exists(target_path):
                        target_path = os.path.join(duplicates_dir, f"{counter}_{base_name}")
                        counter += 1

                    if dry_run:
                        log_lines.append(f"Dry-run: Duplicate found - {file_path} (would be moved to {target_path})")
                    else:
                        shutil.move(file_path, target_path)
                        log_lines.append(
                            f"Moved duplicate:\n  {file_path}\n→ Original: {seen[key]}\n→ Moved to: {target_path}\n"
                        )
                else:
                    seen[key] = file_path
            except Exception as e:
                log_lines.append(f"Error processing {file_path}: {e}")

    log_file = os.path.join(root_folder, LOG_FILENAME)
    try:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))
    except Exception as e:
        logging.error(f"Failed to write log file: {e}")

    return log_lines

# --- GUI Functions ---

def browse_folder(entry: tk.Entry) -> None:
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path)

def run_duplicate_finder() -> None:
    root_folder = folder_entry.get().strip()
    exclude_folders = [os.path.abspath(f.strip()) for f in exclude_entry.get().split(",") if f.strip()]
    dry_run = dry_run_var.get()

    if not os.path.isdir(root_folder):
        messagebox.showerror("Invalid Folder", "Please provide a valid folder path.")
        return

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Scanning for duplicates...\n")
    result_text.update()

    log_lines = find_and_move_duplicates(root_folder, exclude_folders, dry_run)
    result_text.insert(tk.END, "\n".join(log_lines))
    result_text.insert(
        tk.END, f"\n\nLog saved to: {os.path.join(root_folder, LOG_FILENAME)}\n"
    )
    messagebox.showinfo("Process Complete", "Duplicate check complete. Log saved!")

# --- Main GUI Setup ---

def main():
    global folder_entry, exclude_entry, dry_run_var, result_text

    root = tk.Tk()
    root.title("Duplicate File Finder")

    # Folder selection
    tk.Label(root, text="Folder to Scan:").grid(row=0, column=0, padx=10, pady=10)
    folder_entry = tk.Entry(root, width=40)
    folder_entry.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse...", command=lambda: browse_folder(folder_entry)).grid(row=0, column=2, padx=10, pady=10)

    # Exclude folders entry
    tk.Label(root, text="Exclude Folders (comma-separated):").grid(row=1, column=0, padx=10, pady=10)
    exclude_entry = tk.Entry(root, width=40)
    exclude_entry.grid(row=1, column=1, padx=10, pady=10)

    # Dry-run option
    dry_run_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Dry-run mode (no files moved)", variable=dry_run_var).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # Run button
    tk.Button(root, text="Start Scanning", command=run_duplicate_finder).grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    # Result display area
    tk.Label(root, text="Scan Results:").grid(row=4, column=0, padx=10, pady=10)
    result_text = scrolledtext.ScrolledText(root, width=60, height=15)
    result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
