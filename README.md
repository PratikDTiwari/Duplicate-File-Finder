Duplicate File Finder
A simple yet powerful Python desktop application to find and manage duplicate files in any folder.
Features a user-friendly GUI, supports folder exclusions, and offers a dry-run mode to preview actions before making changes.

Features
🖥️ Easy-to-use GUI - No command-line needed!

🔍 Fast duplicate detection using file size and MD5 hash

📂 Exclude folders from the scan (e.g., system or backup directories)

📝 Dry-run mode - Preview what would be moved before actual changes

📄 Detailed log file saved after each scan

Screenshots
![Screenshot of Duplicate File Finder GUI](screenshot.png screenshot image here -->

Installation
Requirements
Python 3.7 or higher

The following Python packages (all standard in most Python installations):

tkinter

hashlib

shutil

os

logging

Steps
Clone this repository:

bash
git clone https://github.com/yourusername/duplicate-file-finder.git
cd duplicate-file-finder
Run the application:

bash
python duplicate_finder.py
Usage
Select the folder you want to scan.

(Optional) Enter folders to exclude, separated by commas.

(Optional) Enable Dry-run mode to preview actions.

Click Start Scanning.

View results in the window and check the log file (duplicates_log.txt) in your selected folder.

How It Works
The app scans all files in the chosen folder (and subfolders).

It ignores any folders you specify in the exclude list.

Duplicate files (by size and MD5 hash) are moved to a duplicates subfolder inside your chosen folder.

In dry-run mode, no files are moved-actions are only simulated and logged.

Example
text
Folder to Scan: /Users/yourname/Documents
Exclude Folders: /Users/yourname/Documents/Backups, /Users/yourname/Documents/System
[✓] Dry-run mode

Result:
Dry-run: Duplicate found - /Users/yourname/Documents/Photos/img1.jpg (would be moved to /Users/yourname/Documents/duplicates/img1.jpg)
...
Contributing
Pull requests and suggestions are welcome!
Please open an issue first to discuss any major changes.

License
MIT License

Disclaimer
Always review the log and use dry-run mode before moving files, especially on important directories.
The author is not responsible for any accidental data loss.

Author
Your Name

Happy cleaning! 🧹

Feel free to update the repository URL, author, and add screenshots as needed!
