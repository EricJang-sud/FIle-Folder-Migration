# File & Folder Migration - Technical Documentation

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)

---

## Features

- 🎯 **Pattern Matching**: Filter by name (start, end, anywhere in name)
- 📁 **File & Folder Support**: Migrate files, folders, or both simultaneously
- 🔍 **Multiple Criteria**: Combine name patterns, file types, and size filters
- 🔄 **Flexible Operations**: Copy or move files/folders
- 👀 **Safe Preview**: Dry-run mode to preview changes before executing
- 📊 **Detailed Logging**: Track all operations with comprehensive logs
- 🚀 **No Dependencies**: Uses Python standard library only
- 💻 **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

**All Platforms:**
- Python 3.6 or higher ([Download Python](https://www.python.org/downloads/))

**Check Python Installation:**

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
python --version
```
If not installed, download from [python.org](https://www.python.org/downloads/windows/) and check "Add Python to PATH" during installation.
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
python3 --version
```
If not installed:
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
```
</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
python3 --version
```
If not installed:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3

# Fedora
sudo dnf install python3

# Arch Linux
sudo pacman -S python
```
</details>

### Installation

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
# Clone the repository
git clone https://github.com/yourusername/file-folder-migration.git
cd file-folder-migration

# Or download the ZIP file and extract it
```
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Clone the repository
git clone https://github.com/yourusername/file-folder-migration.git
cd file-folder-migration

# Make the script executable
chmod +x file_folder_migration.py
```
</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Clone the repository
git clone https://github.com/yourusername/file-folder-migration.git
cd file-folder-migration

# Make the script executable
chmod +x file_folder_migration.py
```
</details>

### Basic Usage

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
# Move all PDF files
python file_folder_migration.py "C:\Source" "C:\Destination" -t ".pdf"

# Move folders starting with "Project"
python file_folder_migration.py "C:\Source" "D:\Archive" --folder-pattern "^Project"

# Preview changes without executing
python file_folder_migration.py "C:\Users\YourName\Downloads" "D:\Sorted" -t ".pdf" --dry-run
```

**Note:** Use quotes around paths with spaces: `"C:\My Documents\Source"`
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Move all PDF files
python3 file_folder_migration.py /Users/yourname/Source /Users/yourname/Destination -t ".pdf"

# Move folders starting with "Project"
python3 file_folder_migration.py ~/Documents ~/Archive --folder-pattern "^Project"

# Preview changes without executing
python3 file_folder_migration.py ~/Downloads ~/Sorted -t ".pdf" --dry-run
```

**Note:** You can use `~` as shorthand for your home directory
</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Move all PDF files
python3 file_folder_migration.py /home/yourname/Source /home/yourname/Destination -t ".pdf"

# Move folders starting with "Project"
python3 file_folder_migration.py ~/Documents ~/Archive --folder-pattern "^Project"

# Preview changes without executing
python3 file_folder_migration.py ~/Downloads ~/Sorted -t ".pdf" --dry-run
```

**Note:** You can use `~` as shorthand for your home directory
</details>

## 🔤 Pattern Syntax

| Syntax | Meaning | Example | Matches |
|--------|---------|---------|---------|
| `^pattern` | Starts with | `^Report` | Report_2024.pdf |
| `pattern$` | Ends with | `_draft$` | document_draft.pdf |
| `*pattern*` | Contains | `*2024*` | file_2024_v1.pdf |
| `pattern` | Ends with (default) | `_1` | document_1.pdf |

## 🧪 Usage Examples

### Files Only

<details>
<summary><b>🪟 Windows Examples</b></summary>

```cmd
# Files ending with '_1'
python file_folder_migration.py "C:\Source" "C:\Destination" -p "_1"

# Files starting with 'Report'
python file_folder_migration.py "C:\Documents" "C:\Reports" -p "^Report"

# Files containing '2024' anywhere
python file_folder_migration.py "C:\Source" "C:\Archive" -p "*2024*"

# Multiple file types (PDF, DOCX, JPG)
python file_folder_migration.py "C:\Downloads" "C:\Sorted" -t ".pdf" ".docx" ".jpg"

# Large PDF files (>= 5 MB)
python file_folder_migration.py "C:\Documents" "D:\LargePDFs" -t ".pdf" --min-size 5

# Files with 'invoice' + PDF type
python file_folder_migration.py "C:\Business" "C:\Invoices" -p "*invoice*" -t ".pdf"
```
</details>

<details>
<summary><b>🍎 macOS Examples</b></summary>

```bash
# Files ending with '_1'
python3 file_folder_migration.py ~/Source ~/Destination -p "_1"

# Files starting with 'Report'
python3 file_folder_migration.py ~/Documents ~/Reports -p "^Report"

# Files containing '2024' anywhere
python3 file_folder_migration.py ~/Source ~/Archive -p "*2024*"

# Multiple file types (PDF, DOCX, JPG)
python3 file_folder_migration.py ~/Downloads ~/Sorted -t ".pdf" ".docx" ".jpg"

# Large PDF files (>= 5 MB)
python3 file_folder_migration.py ~/Documents ~/LargePDFs -t ".pdf" --min-size 5

# Files with 'invoice' + PDF type
python3 file_folder_migration.py ~/Business ~/Invoices -p "*invoice*" -t ".pdf"
```
</details>

<details>
<summary><b>🐧 Linux Examples</b></summary>

```bash
# Files ending with '_1'
python3 file_folder_migration.py /home/user/Source /home/user/Destination -p "_1"

# Files starting with 'Report'
python3 file_folder_migration.py ~/Documents ~/Reports -p "^Report"

# Files containing '2024' anywhere
python3 file_folder_migration.py ~/Source ~/Archive -p "*2024*"

# Multiple file types (PDF, DOCX, JPG)
python3 file_folder_migration.py ~/Downloads ~/Sorted -t ".pdf" ".docx" ".jpg"

# Large PDF files (>= 5 MB)
python3 file_folder_migration.py ~/Documents ~/LargePDFs -t ".pdf" --min-size 5

# Files with 'invoice' + PDF type
python3 file_folder_migration.py ~/Business ~/Invoices -p "*invoice*" -t ".pdf"
```
</details>

### Folders Only

<details>
<summary><b>🪟 Windows Examples</b></summary>

```cmd
# Folders named 'Archive' or 'Backup'
python file_folder_migration.py "C:\Data" "D:\Storage" --folder-pattern "Archive" "Backup"

# Folders starting with 'Project'
python file_folder_migration.py "C:\Projects" "D:\Archive" --folder-pattern "^Project"

# Folders containing PDF files
python file_folder_migration.py "C:\Documents" "D:\PDFArchive" --folder-contains ".pdf"

# Large folders (>= 100 MB)
python file_folder_migration.py "C:\Data" "D:\LargeFolders" --folder-min-size 100
```
</details>

<details>
<summary><b>🍎 macOS Examples</b></summary>

```bash
# Folders named 'Archive' or 'Backup'
python3 file_folder_migration.py ~/Data ~/Storage --folder-pattern "Archive" "Backup"

# Folders starting with 'Project'
python3 file_folder_migration.py ~/Projects ~/Archive --folder-pattern "^Project"

# Folders containing PDF files
python3 file_folder_migration.py ~/Documents ~/PDFArchive --folder-contains ".pdf"

# Large folders (>= 100 MB)
python3 file_folder_migration.py ~/Data ~/LargeFolders --folder-min-size 100
```
</details>

<details>
<summary><b>🐧 Linux Examples</b></summary>

```bash
# Folders named 'Archive' or 'Backup'
python3 file_folder_migration.py ~/Data ~/Storage --folder-pattern "Archive" "Backup"

# Folders starting with 'Project'
python3 file_folder_migration.py ~/Projects ~/Archive --folder-pattern "^Project"

# Folders containing PDF files
python3 file_folder_migration.py ~/Documents ~/PDFArchive --folder-contains ".pdf"

# Large folders (>= 100 MB)
python3 file_folder_migration.py ~/Data ~/LargeFolders --folder-min-size 100
```
</details>

### Files + Folders (Combination)

**Works the same on all platforms - just use your platform's path format:**

```bash
# Migrate PDF files AND Archive folders together
python file_folder_migration.py /source /dest -t ".pdf" --folder-pattern "Archive"

# Files ending with '_1' AND folders starting with 'Project'
python file_folder_migration.py /source /dest -p "_1" --folder-pattern "^Project"

# Files with '2024' + Folders with '2024'
python file_folder_migration.py /source /dest -p "*2024*" --folder-pattern "*2024*"
```

## ⚙️ Configuration File

Edit the script to set default behaviors (works the same on all platforms):

<details>
<summary><b>🪟 Windows Configuration</b></summary>

```python
# Default paths - Use Windows-style paths
DEFAULT_SOURCE = "C:\\Users\\YourName\\Documents\\Source"
DEFAULT_DESTINATION = "D:\\Archive"

# Migrate all PDF files
FILES_TO_MIGRATE = {
    "name_pattern": None,
    "file_type": ".pdf",
    "min_size_mb": None,
    "max_size_mb": None
}
```
</details>

<details>
<summary><b>🍎 macOS Configuration</b></summary>

```python
# Default paths - Use Unix-style paths
DEFAULT_SOURCE = "/Users/yourname/Documents/Source"
DEFAULT_DESTINATION = "/Users/yourname/Archive"

# Migrate all PDF files
FILES_TO_MIGRATE = {
    "name_pattern": None,
    "file_type": ".pdf",
    "min_size_mb": None,
    "max_size_mb": None
}
```
</details>

<details>
<summary><b>🐧 Linux Configuration</b></summary>

```python
# Default paths - Use Unix-style paths
DEFAULT_SOURCE = "/home/yourname/Documents/Source"
DEFAULT_DESTINATION = "/home/yourname/Archive"

# Migrate all PDF files
FILES_TO_MIGRATE = {
    "name_pattern": None,
    "file_type": ".pdf",
    "min_size_mb": None,
    "max_size_mb": None
}
```
</details>

Then run without arguments:

**Windows:** `python file_folder_migration.py`  
**macOS/Linux:** `python3 file_folder_migration.py`

## 🖥️ Command Line Options

### File Filters
| Option | Description |
|--------|-------------|
| `-p`, `--pattern` | Name pattern(s) to match |
| `-t`, `--type` | File extension(s) to match |
| `--min-size` | Minimum file size in MB |
| `--max-size` | Maximum file size in MB |

### Folder Filters
| Option | Description |
|--------|-------------|
| `--folder-pattern` | Folder name pattern(s) to match |
| `--folder-contains` | File type(s) folder must contain |
| `--folder-min-size` | Minimum folder size in MB |
| `--folder-max-size` | Maximum folder size in MB |

### Operations
| Option | Description |
|--------|-------------|
| `--copy` | Copy instead of move |
| `--dry-run` | Preview changes only |
| `-v`, `--verbose` | Enable verbose logging |
| `--log FILE` | Save log to file |

## 🌍 Real-World Use Cases

### 📸 Photo Organization

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
# Move large RAW files (>20 MB)
python file_folder_migration.py "C:\Photos" "D:\Photos\RAW" -t ".raw" ".cr2" --min-size 20

# Move edited finals
python file_folder_migration.py "C:\Photos" "C:\Photos\Finals" -p "_final" -t ".jpg"
```
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Move large RAW files (>20 MB)
python3 file_folder_migration.py ~/Pictures ~/Pictures/RAW -t ".raw" ".cr2" --min-size 20

# Move edited finals
python3 file_folder_migration.py ~/Pictures ~/Pictures/Finals -p "_final" -t ".jpg"
```
</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Move large RAW files (>20 MB)
python3 file_folder_migration.py ~/Pictures ~/Pictures/RAW -t ".raw" ".cr2" --min-size 20

# Move edited finals
python3 file_folder_migration.py ~/Pictures ~/Pictures/Finals -p "_final" -t ".jpg"
```
</details>

### 📄 Document Management

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
# Archive old reports
python file_folder_migration.py "C:\Documents" "D:\Archive" -p "*2023*" -t ".pdf" ".docx"

# Move draft documents
python file_folder_migration.py "C:\Documents" "C:\Drafts" -p "_draft"
```
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Archive old reports
python3 file_folder_migration.py ~/Documents ~/Archive -p "*2023*" -t ".pdf" ".docx"

# Move draft documents
python3 file_folder_migration.py ~/Documents ~/Drafts -p "_draft"
```
</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Archive old reports
python3 file_folder_migration.py ~/Documents ~/Archive -p "*2023*" -t ".pdf" ".docx"

# Move draft documents
python3 file_folder_migration.py ~/Documents ~/Drafts -p "_draft"
```
</details>

### 💻 Code Version Control

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
# Archive old versions
python file_folder_migration.py "C:\Projects" "D:\Archive" -p "_old" "_backup"

# Organize by project
python file_folder_migration.py "C:\Projects" "D:\Organized" --folder-pattern "^Project"
```
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Archive old versions
python3 file_folder_migration.py ~/Projects ~/Archive -p "_old" "_backup"

# Organize by project
python3 file_folder_migration.py ~/Projects ~/Organized --folder-pattern "^Project"
```
</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Archive old versions
python3 file_folder_migration.py ~/Projects ~/Archive -p "_old" "_backup"

# Organize by project
python3 file_folder_migration.py ~/Projects ~/Organized --folder-pattern "^Project"
```
</details>

### 🗂️ Cleanup & Backup

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
# Move large files for review
python file_folder_migration.py "C:\Downloads" "D:\Review" --min-size 50

# Backup important folders
python file_folder_migration.py "C:\Data" "D:\Backup" --folder-pattern "*Important*" --copy
```
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Move large files for review
python3 file_folder_migration.py ~/Downloads ~/Review --min-size 50

# Backup important folders
python3 file_folder_migration.py ~/Data ~/Backup --folder-pattern "*Important*" --copy
```
</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Move large files for review
python3 file_folder_migration.py ~/Downloads ~/Review --min-size 50

# Backup important folders
python3 file_folder_migration.py ~/Data ~/Backup --folder-pattern "*Important*" --copy
```
</details>

## 🖥️ Platform-Specific Notes

### 🪟 Windows
- Use backslashes `\` or forward slashes `/` in paths
- Use quotes around paths with spaces: `"C:\My Documents"`
- Run Command Prompt or PowerShell as Administrator if moving system files
- Python command is usually just `python` (not `python3`)

### 🍎 macOS
- Use forward slashes `/` in paths
- Use `~` for home directory shorthand
- Python 3 command is `python3` (not `python`)
- May need to grant disk access permissions in System Preferences > Security & Privacy

### 🐧 Linux
- Use forward slashes `/` in paths
- Use `~` for home directory shorthand
- Python 3 command is `python3` (not `python`)
- Use `sudo` if moving system files (not recommended for personal files)

## 🛡️ Safety Features

- ✅ **Dry-run mode**: Preview all operations before executing
- ✅ **Duplicate detection**: Skips files/folders that already exist
- ✅ **Error handling**: Continues processing even if individual items fail
- ✅ **Detailed logging**: Track every operation
- ✅ **Auto-create directories**: Creates destination if it doesn't exist

## 🛠️ Troubleshooting

<details>
<summary><b>Nothing happens when I run the script</b></summary>

- Make sure at least one filter is specified (file or folder patterns)
- Check that source directory exists and is accessible
- Try adding `--dry-run -v` to see what's happening
</details>

<details>
<summary><b>Python command not found</b></summary>

**Windows:** Try `python3` or reinstall Python with "Add to PATH" checked  
**macOS/Linux:** Try `python` instead of `python3`, or install Python
</details>

<details>
<summary><b>Files/folders are skipped</b></summary>

- They may already exist at destination
- Check the log for "already exists" warnings
- Use `--verbose` for detailed information
</details>

<details>
<summary><b>Permission errors</b></summary>

- Ensure you have read access to source and write access to destination
- **Windows:** Run Command Prompt as Administrator
- **macOS:** Grant disk access in System Preferences
- **Linux:** Check file permissions with `ls -la`
</details>

<details>
<summary><b>Path errors on Windows</b></summary>

- Use quotes around paths with spaces
- Use double backslashes `\\` or forward slashes `/`
- **Or use raw strings** (prefix with `r`): `r"C:\My Documents"`
- Examples:
  - `"C:\\My Documents\\Source"` (double backslash)
  - `"C:/My Documents/Source"` (forward slash)
  - `r"C:\My Documents\Source"` (raw string - easiest!)
</details>

---

## 👤 Author

- **Author:** Eric Jang
- **Email:** thericman05@gmail.com
- **LinkedIn:** [Connect with me](https://www.linkedin.com/in/eric-jang666/)

---

⭐ **If you find this useful, please consider starring the repository!**
