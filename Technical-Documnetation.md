# File & Folder Migration Tool

A powerful yet simple Python script for organizing files and folders based on patterns, types, and sizes. Perfect for automating file management tasks.

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🎯 **Pattern Matching**: Filter by name (start, end, anywhere in name)
- 📁 **File & Folder Support**: Migrate files, folders, or both simultaneously
- 🔍 **Multiple Criteria**: Combine name patterns, file types, and size filters
- 🔄 **Flexible Operations**: Copy or move files/folders
- 👀 **Safe Preview**: Dry-run mode to preview changes before executing
- 📊 **Detailed Logging**: Track all operations with comprehensive logs
- 🚀 **No Dependencies**: Uses Python standard library only

## Quick Start

### Prerequisites

- Python 3.6 or higher
- No external dependencies required

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/file-folder-migration.git
cd file-folder-migration

# Make the script executable (Unix/Linux/macOS)
chmod +x file_folder_migration.py
```

### Basic Usage

```bash
# Move all PDF files
python file_folder_migration.py /source /destination -t ".pdf"

# Move folders starting with "Project"
python file_folder_migration.py /source /destination --folder-pattern "^Project"

# Preview changes without executing
python file_folder_migration.py /source /destination -t ".pdf" --dry-run
```

## Pattern Syntax

| Syntax | Meaning | Example | Matches |
|--------|---------|---------|---------|
| `^pattern` | Starts with | `^Report` | Report_2024.pdf |
| `pattern$` | Ends with | `_draft$` | document_draft.pdf |
| `*pattern*` | Contains | `*2024*` | file_2024_v1.pdf |
| `pattern` | Ends with (default) | `_1` | document_1.pdf |

## Usage Examples

### Files Only

```bash
# Files ending with '_1'
python file_folder_migration.py /source /dest -p "_1"

# Files starting with 'Report'
python file_folder_migration.py /source /dest -p "^Report"

# Files containing '2024' anywhere
python file_folder_migration.py /source /dest -p "*2024*"

# Multiple file types (PDF, DOCX, JPG)
python file_folder_migration.py /source /dest -t ".pdf" ".docx" ".jpg"

# Large PDF files (>= 5 MB)
python file_folder_migration.py /source /dest -t ".pdf" --min-size 5

# Files with 'invoice' + PDF type
python file_folder_migration.py /source /dest -p "*invoice*" -t ".pdf"
```

### Folders Only

```bash
# Folders named 'Archive' or 'Backup'
python file_folder_migration.py /source /dest --folder-pattern "Archive" "Backup"

# Folders starting with 'Project'
python file_folder_migration.py /source /dest --folder-pattern "^Project"

# Folders containing '2024' in name
python file_folder_migration.py /source /dest --folder-pattern "*2024*"

# Folders containing PDF files
python file_folder_migration.py /source /dest --folder-contains ".pdf"

# Large folders (>= 100 MB)
python file_folder_migration.py /source /dest --folder-min-size 100
```

### Files + Folders (Combination)

```bash
# Migrate PDF files AND Archive folders together
python file_folder_migration.py /source /dest -t ".pdf" --folder-pattern "Archive"

# Files ending with '_1' AND folders starting with 'Project'
python file_folder_migration.py /source /dest -p "_1" --folder-pattern "^Project"

# Files with '2024' + Folders with '2024'
python file_folder_migration.py /source /dest -p "*2024*" --folder-pattern "*2024*"
```

## Configuration File

Edit the script to set default behaviors:

```python
# Default paths
DEFAULT_SOURCE = "/path/to/source/folder"
DEFAULT_DESTINATION = "/path/to/destination/folder"

# Migrate all PDF files
FILES_TO_MIGRATE = {
    "name_pattern": None,
    "file_type": ".pdf",
    "min_size_mb": None,
    "max_size_mb": None
}

# Migrate folders starting with 'Project'
FOLDERS_TO_MIGRATE = {
    "name_pattern": "^Project",
    "file_type": None,
    "min_size_mb": None,
    "max_size_mb": None
}
```

Then run without arguments:
```bash
python file_folder_migration.py
```

## Command Line Options

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

## Real-World Use Cases

### 📸 Photo Organization
```bash
# Move large RAW files (>20 MB)
python file_folder_migration.py ~/Photos ~/Photos/RAW -t ".raw" ".cr2" --min-size 20

# Move edited finals
python file_folder_migration.py ~/Photos ~/Photos/Finals -p "_final" -t ".jpg"
```

### 📄 Document Management
```bash
# Archive old reports
python file_folder_migration.py ~/Documents ~/Archive -p "*2023*" -t ".pdf" ".docx"

# Move draft documents
python file_folder_migration.py ~/Documents ~/Drafts -p "_draft"
```

### 💻 Code Version Control
```bash
# Archive old versions
python file_folder_migration.py ~/Projects ~/Archive -p "_old" "_backup"

# Organize by project
python file_folder_migration.py ~/Projects ~/Organized --folder-pattern "^Project"
```

### 🗂️ Cleanup & Backup
```bash
# Move large files for review
python file_folder_migration.py ~/Downloads ~/Review --min-size 50

# Backup important folders
python file_folder_migration.py ~/Data ~/Backup --folder-pattern "*Important*" --copy
```

## Safety Features

- ✅ **Dry-run mode**: Preview all operations before executing
- ✅ **Duplicate detection**: Skips files/folders that already exist
- ✅ **Error handling**: Continues processing even if individual items fail
- ✅ **Detailed logging**: Track every operation
- ✅ **Auto-create directories**: Creates destination if it doesn't exist

## Troubleshooting

**Nothing happens when I run the script:**
- Make sure at least one filter is specified (file or folder patterns)
- Check that source directory exists and is accessible

**Files/folders are skipped:**
- They may already exist at destination
- Check the log for "already exists" warnings

**Permission errors:**
- Ensure you have read access to source and write access to destination
- Try running with appropriate permissions

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/file-folder-migration/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/file-folder-migration/discussions)

---

**⭐ Star this repository if you find it useful!**
