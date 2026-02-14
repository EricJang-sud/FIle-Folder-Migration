#!/usr/bin/env python3
"""
Pattern-Based File Organizer
=============================

A flexible Python utility for organizing files based on multiple criteria.
Perfect for automated file management, batch processing, and workflow automation.

Filter files by:
- Name patterns (e.g., files ending with "_1", "_draft")
- File types (e.g., .pdf, .jpg, .docx)
- File size (minimum and/or maximum in MB)
- Any combination of the above (SQL-like AND logic)

Author: Your Name
License: MIT
Repository: https://github.com/yourusername/pattern-file-organizer
"""

import os
import shutil
import argparse
import logging
from pathlib import Path
from typing import List, Tuple
from datetime import datetime


# ============================================
# CONFIGURATION - Easy Setup
# ============================================

# Default paths (can be overridden via command line)
DEFAULT_SOURCE = "/path/to/source/folder"
DEFAULT_DESTINATION = "/path/to/destination/folder"

# ============================================
# FILE MIGRATION SETTINGS
# ============================================
# Flexible pattern matching for FILES (SQL-like operators)
# You can filter by: filename pattern, file size, and/or file type
# 
# IMPORTANT: For name_pattern and file_type, you can use:
#   - A single value: "value" or ["value"]
#   - Multiple values: ["value1", "value2", "value3"]
#   - None: if you don't want to filter by this criteria
#
# NAME PATTERN MATCHING:
#   - "^pattern" = Starts with pattern (e.g., "^Report")
#   - "pattern$" = Ends with pattern (e.g., "_1$" or "_draft$")
#   - "*pattern*" = Contains pattern anywhere (e.g., "*2024*")
#   - "pattern" (no prefix/suffix) = Ends with pattern (default behavior)
#
# Set to None to disable file migration entirely
#
# Examples:
#   1. Files ending with _1:
#      {"name_pattern": "_1"} or {"name_pattern": "_1$"}
#
#   2. Files ending with _1 OR _2:
#      {"name_pattern": ["_1", "_2"]}
#
#   3. Files starting with Report OR Summary:
#      {"name_pattern": ["^Report", "^Summary"]}
#
#   4. Files containing "2024" anywhere in name:
#      {"name_pattern": "*2024*"}
#
#   5. All PDF files:
#      {"file_type": ".pdf"}
#
#   6. PDF OR JPG OR Word files:
#      {"file_type": [".pdf", ".jpg", ".docx"]}
#
#   7. Files >= 10 MB (any name, any type):
#      {"name_pattern": None, "file_type": None, "min_size_mb": 10}
#
#   8. Draft Word OR PowerPoint documents:
#      {"name_pattern": "_draft", "file_type": [".docx", ".pptx"]}
#
#   9. Large images (JPG OR PNG, >= 2 MB):
#      {"file_type": [".jpg", ".png"], "min_size_mb": 2}
#
#   10. Files with "invoice" anywhere, that are PDFs:
#       {"name_pattern": "*invoice*", "file_type": ".pdf"}
#
#   11. Disable file migration:
#       None
#
FILES_TO_MIGRATE = None  # Set to None to disable, or use dict with filters (like above)

# Example configurations (undocstring to use):
"""
FILES_TO_MIGRATE = {
    "name_pattern": "_1",               # Pattern(s) to match in filename
                                        # - Single: "_1" or ["_1"]
                                        # - Multiple: ["_1", "_2", "_draft"]
                                        # - Starts with: "^Report", "^Summary"
                                        # - Ends with: "_1$", "_draft$" (or just "_1", "_draft")
                                        # - Contains anywhere: "*2024*", "*invoice*"
                                        # - None: Don't filter by name
     
    "file_type": None,                  # File extension(s) to match
                                        # - Single: ".pdf" or [".pdf"]
                                        # - Multiple: [".pdf", ".jpg", ".xlsx"]
                                        # - None: Don't filter by type
     
    "min_size_mb": None,                # Minimum file size in MB (None = no minimum)
    "max_size_mb": None                 # Maximum file size in MB (None = no maximum)
}
"""

# ============================================
# FOLDER MIGRATION SETTINGS
# ============================================
# Flexible pattern matching for FOLDERS (SQL-like operators)
# You can filter by: folder name pattern, file types in folder, and/or folder size
#
# IMPORTANT: For name_pattern and file_type, you can use:
#   - A single value: "value" or ["value"]
#   - Multiple values: ["value1", "value2", "value3"]
#   - None: if you don't want to filter by this criteria
#
# NAME PATTERN MATCHING (same as files):
#   - "^pattern" = Starts with pattern (e.g., "^Project")
#   - "pattern$" = Ends with pattern (e.g., "Archive$")
#   - "*pattern*" = Contains pattern anywhere (e.g., "*Backup*")
#   - "pattern" (no prefix/suffix) = Exact match or ends with
#
# Set to None to disable folder migration entirely
#
# Examples:
#   1. Folders named "Archive":
#      {"name_pattern": "Archive"}
#
#   2. Folders named "Archive" OR "Backup":
#      {"name_pattern": ["Archive", "Backup"]}
#
#   3. Folders starting with "Project":
#      {"name_pattern": "^Project"}
#
#   4. Folders containing "2024" in name:
#      {"name_pattern": "*2024*"}
#
#   5. Folders containing at least one PDF file:
#      {"file_type": ".pdf"}
#
#   6. Folders containing PDF OR Word files:
#      {"file_type": [".pdf", ".docx"]}
#
#   7. Folders >= 100 MB in size:
#      {"min_size_mb": 100}
#
#   8. Large folders (>= 50 MB) containing images:
#      {"file_type": [".jpg", ".png"], "min_size_mb": 50}
#
#   9. Folders with "OldData" OR "Archive" that are >= 100 MB:
#      {"name_pattern": ["OldData", "Archive"], "min_size_mb": 100}
#
#   10. Disable folder migration:
#       None
#
FOLDERS_TO_MIGRATE = None  # Set to None to disable, or use dict with filters (like above)

# Example configurations (undocstring to use):
"""
FOLDERS_TO_MIGRATE = {
    "name_pattern": "Archive",      # Pattern(s) to match in folder name
                                    # - Single: "Archive" or ["Archive"]
                                    # - Multiple: ["Archive", "Backup", "OldData"]
                                    # - Starts with: "^Project", "^2024"
                                    # - Ends with: "Backup$", "Archive$"
                                    # - Contains anywhere: "*Old*", "*2024*"
                                    # - None: Don't filter by name
     
     "file_type": None,             # File type(s) that folder must contain
                                    # - Single: ".pdf" or [".pdf"]
                                    # - Multiple: [".pdf", ".docx", ".jpg"]
                                    # - None: Don't filter by content
     
     "min_size_mb": None,           # Minimum folder size in MB (None = no minimum)
     "max_size_mb": None            # Maximum folder size in MB (None = no maximum)
}
"""

# ============================================
# COMBINATION MODE
# ============================================
# You can enable BOTH FILES_TO_MIGRATE and FOLDERS_TO_MIGRATE at the same time!
# The script will migrate both files and folders that match their respective criteria.
#
# Example: Migrate PDF files AND Archive folders together
# FILES_TO_MIGRATE = {"file_type": ".pdf"}
# FOLDERS_TO_MIGRATE = {"name_pattern": "Archive"}

# Operation modes
COPY_MODE = False  # False = Move files/folders, True = Copy files/folders
DRY_RUN = False    # True = Preview only, False = Execute changes

# ===== END OF USER INPUT ====================
# Do not modify code below unless you understand the implementation.
# ============================================
# LOGGING CONFIGURATION
# ============================================

def setup_logging(log_file: str = None, verbose: bool = False) -> None:
    """Configure logging for the application."""
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )


# ============================================
# CORE FUNCTIONALITY
# ============================================

class FileOrganizer:
    """
    A flexible file and folder organizer that sorts based on multiple criteria.
    
    Features:
    - Pattern-based file matching (filename, type, size)
    - Folder migration (single or multiple folders)
    - SQL-like filtering with AND conditions
    - Safe file/folder operations with error handling
    - Dry-run mode for previewing changes
    - Detailed logging and statistics
    - Support for copy or move operations
    """
    
    def __init__(self, source: str, destination: str, pattern: dict = None, 
                 folders_to_migrate: dict = None, copy_mode: bool = False, 
                 dry_run: bool = False):
        """
        Initialize the FileOrganizer.
        
        Args:
            source: Source directory path
            destination: Destination directory path
            pattern: Dictionary with filtering criteria (for files):
                - name_pattern (str/list): Pattern(s) in filename
                - file_type (str/list): File extension(s)
                - min_size_mb (float): Minimum file size in MB
                - max_size_mb (float): Maximum file size in MB
                Set to None to disable file migration
            folders_to_migrate: Dictionary with filtering criteria (for folders):
                - name_pattern (str/list): Pattern(s) in folder name
                - file_type (str/list): File type(s) that folder must contain
                - min_size_mb (float): Minimum folder size in MB
                - max_size_mb (float): Maximum folder size in MB
                Set to None to disable folder migration
            copy_mode: If True, copy files/folders instead of moving them
            dry_run: If True, only preview operations without executing
        """
        self.source = Path(source)
        self.destination = Path(destination)
        
        # Handle pattern - can be None, dict, or string (for backward compatibility)
        if pattern is None:
            self.pattern = None
        elif isinstance(pattern, dict):
            self.pattern = pattern
        elif isinstance(pattern, str):
            self.pattern = {"name_pattern": pattern}
        else:
            self.pattern = None
        
        self.copy_mode = copy_mode
        self.dry_run = dry_run
        
        # Handle folders_to_migrate - should be a dict or None
        if folders_to_migrate is None:
            self.folders_to_migrate = None
        elif isinstance(folders_to_migrate, dict):
            self.folders_to_migrate = folders_to_migrate
        else:
            # For backward compatibility, if it's a string or list, convert to dict
            if isinstance(folders_to_migrate, str):
                self.folders_to_migrate = {"name_pattern": folders_to_migrate}
            elif isinstance(folders_to_migrate, list):
                self.folders_to_migrate = {"name_pattern": folders_to_migrate}
            else:
                self.folders_to_migrate = None
        
        self.stats = {
            'matched': 0,
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'folders_matched': 0,
            'folders_migrated': 0
        }
    
    def validate_paths(self) -> bool:
        """
        Validate source and destination paths.
        
        Returns:
            True if paths are valid, False otherwise
        """
        if not self.source.exists():
            logging.error(f"Source directory does not exist: {self.source}")
            return False
        
        if not self.source.is_dir():
            logging.error(f"Source path is not a directory: {self.source}")
            return False
        
        return True
    
    def matches_pattern(self, file_path: Path) -> bool:
        """
        Check if a file matches the pattern criteria.
        
        Pattern matching supports:
        - ^pattern = Starts with
        - pattern$ = Ends with
        - *pattern* = Contains anywhere
        - pattern = Ends with (default)
        
        Multiple values within name_pattern or file_type use OR logic.
        Different criteria (name, type, size) use AND logic.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if file matches ALL specified criteria, False otherwise
        """
        name, ext = os.path.splitext(file_path.name)
        
        # Check name pattern (if specified)
        name_pattern = self.pattern.get("name_pattern")
        if name_pattern is not None:
            # Convert single pattern to list for uniform processing
            patterns = [name_pattern] if isinstance(name_pattern, str) else name_pattern
            
            # Check if ANY pattern matches (OR logic)
            pattern_matched = False
            for pattern in patterns:
                if pattern.startswith("^") and pattern.endswith("$"):
                    # Exact match: ^pattern$
                    if name == pattern[1:-1]:
                        pattern_matched = True
                        break
                elif pattern.startswith("^"):
                    # Pattern at start of filename
                    if name.startswith(pattern[1:]):
                        pattern_matched = True
                        break
                elif pattern.endswith("$"):
                    # Pattern at end of filename
                    if name.endswith(pattern[:-1]):
                        pattern_matched = True
                        break
                elif pattern.startswith("*") and pattern.endswith("*"):
                    # Pattern anywhere in filename
                    if pattern[1:-1] in name:
                        pattern_matched = True
                        break
                else:
                    # Default: Pattern at end of filename (before extension)
                    if name.endswith(pattern):
                        pattern_matched = True
                        break
            
            if not pattern_matched:
                return False
        
        # Check file type (if specified)
        file_type = self.pattern.get("file_type")
        if file_type is not None:
            # Convert single type to list for uniform processing
            types = [file_type] if isinstance(file_type, str) else file_type
            
            # Ensure all types start with a dot
            types = ["." + t if not t.startswith(".") else t for t in types]
            
            # Check if ANY type matches (OR logic)
            type_matched = False
            for ftype in types:
                if ext.lower() == ftype.lower():
                    type_matched = True
                    break
            
            if not type_matched:
                return False
        
        # Check file size constraints (if specified)
        try:
            file_size_mb = file_path.stat().st_size / (1024 * 1024)  # Convert to MB
            
            min_size = self.pattern.get("min_size_mb")
            if min_size is not None:
                if file_size_mb < min_size:
                    return False
            
            max_size = self.pattern.get("max_size_mb")
            if max_size is not None:
                if file_size_mb > max_size:
                    return False
        
        except OSError as e:
            logging.warning(f"Could not get size for {file_path.name}: {e}")
            return False
        
        # All criteria matched
        return True
    
    def matches_folder_pattern(self, folder_path: Path) -> bool:
        """
        Check if a folder matches the folder pattern criteria.
        
        Pattern matching supports:
        - ^pattern = Starts with
        - pattern$ = Ends with
        - *pattern* = Contains anywhere
        - pattern = Exact match or ends with (default)
        
        Multiple values within name_pattern or file_type use OR logic.
        Different criteria (name, type, size) use AND logic.
        
        Args:
            folder_path: Path to the folder to check
            
        Returns:
            True if folder matches ALL specified criteria, False otherwise
        """
        folder_name = folder_path.name
        
        # Check name pattern (if specified)
        name_pattern = self.folders_to_migrate.get("name_pattern")
        if name_pattern is not None:
            # Convert single pattern to list for uniform processing
            patterns = [name_pattern] if isinstance(name_pattern, str) else name_pattern
            
            # Check if ANY pattern matches (OR logic)
            pattern_matched = False
            for pattern in patterns:
                if pattern.startswith("^") and pattern.endswith("$"):
                    # Exact match: ^pattern$
                    if folder_name == pattern[1:-1]:
                        pattern_matched = True
                        break
                elif pattern.startswith("^"):
                    # Pattern at start of folder name
                    if folder_name.startswith(pattern[1:]):
                        pattern_matched = True
                        break
                elif pattern.endswith("$"):
                    # Pattern at end of folder name
                    if folder_name.endswith(pattern[:-1]):
                        pattern_matched = True
                        break
                elif pattern.startswith("*") and pattern.endswith("*"):
                    # Pattern anywhere in folder name
                    if pattern[1:-1] in folder_name:
                        pattern_matched = True
                        break
                else:
                    # Default: Exact match or ends with pattern
                    if folder_name == pattern or folder_name.endswith(pattern):
                        pattern_matched = True
                        break
            
            if not pattern_matched:
                return False
        
        # Check if folder contains specific file types (if specified)
        file_type = self.folders_to_migrate.get("file_type")
        if file_type is not None:
            # Convert single type to list for uniform processing
            types = [file_type] if isinstance(file_type, str) else file_type
            
            # Ensure all types start with a dot
            types = ["." + t if not t.startswith(".") else t for t in types]
            
            # Check if folder contains at least one file of the specified type(s)
            contains_type = False
            try:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_ext = os.path.splitext(file)[1].lower()
                        if any(file_ext == ftype.lower() for ftype in types):
                            contains_type = True
                            break
                    if contains_type:
                        break
            except (PermissionError, OSError) as e:
                logging.warning(f"Could not scan folder {folder_name}: {e}")
                return False
            
            if not contains_type:
                return False
        
        # Check folder size constraints (if specified)
        try:
            # Calculate total folder size
            folder_size_mb = 0
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    try:
                        file_path = Path(root) / file
                        folder_size_mb += file_path.stat().st_size / (1024 * 1024)
                    except (PermissionError, OSError):
                        continue
            
            min_size = self.folders_to_migrate.get("min_size_mb")
            if min_size is not None:
                if folder_size_mb < min_size:
                    return False
            
            max_size = self.folders_to_migrate.get("max_size_mb")
            if max_size is not None:
                if folder_size_mb > max_size:
                    return False
        
        except (PermissionError, OSError) as e:
            logging.warning(f"Could not calculate size for folder {folder_name}: {e}")
            return False
        
        # All criteria matched
        return True
    
    def get_matching_files(self) -> List[Tuple[Path, str]]:
        """
        Find all files matching the pattern criteria.
        
        Returns:
            List of tuples (source_path, filename)
        """
        matching_files = []
        
        try:
            for item in self.source.iterdir():
                if not item.is_file():
                    continue
                
                if self.matches_pattern(item):
                    matching_files.append((item, item.name))
                    self.stats['matched'] += 1
        
        except PermissionError as e:
            logging.error(f"Permission denied accessing source directory: {e}")
        
        return matching_files
    
    def process_file(self, source_path: Path, filename: str) -> bool:
        """
        Process a single file (copy or move).
        
        Args:
            source_path: Full path to source file
            filename: Name of the file
            
        Returns:
            True if successful, False otherwise
        """
        destination_path = self.destination / filename
        
        # Check if destination file already exists
        if destination_path.exists():
            logging.warning(f"File already exists at destination: {filename}")
            self.stats['skipped'] += 1
            return False
        
        try:
            if self.dry_run:
                action = "COPY" if self.copy_mode else "MOVE"
                logging.info(f"[DRY RUN] Would {action}: {filename}")
                self.stats['processed'] += 1
                return True
            
            # Create destination directory if it doesn't exist
            self.destination.mkdir(parents=True, exist_ok=True)
            
            # Perform copy or move operation
            if self.copy_mode:
                shutil.copy2(source_path, destination_path)
                logging.info(f"Copied: {filename}")
            else:
                shutil.move(str(source_path), str(destination_path))
                logging.info(f"Moved: {filename}")
            
            self.stats['processed'] += 1
            return True
        
        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")
            self.stats['errors'] += 1
            return False
    
    def get_folders_to_migrate(self) -> List[Tuple[Path, str]]:
        """
        Get list of folders to migrate based on folders_to_migrate filters.
        
        Returns:
            List of tuples (folder_path, folder_name)
        """
        folders = []
        
        if self.folders_to_migrate is None:
            return folders
        
        try:
            for item in self.source.iterdir():
                if not item.is_dir():
                    continue
                
                # Check if this folder matches the criteria
                if self.matches_folder_pattern(item):
                    folders.append((item, item.name))
                    self.stats['folders_matched'] += 1
        
        except PermissionError as e:
            logging.error(f"Permission denied accessing source directory: {e}")
        
        return folders
    
    def process_folder(self, source_folder: Path, folder_name: str) -> bool:
        """
        Process a single folder (copy or move entire directory tree).
        
        Args:
            source_folder: Full path to source folder
            folder_name: Name of the folder
            
        Returns:
            True if successful, False otherwise
        """
        destination_folder = self.destination / folder_name
        
        # Check if destination folder already exists
        if destination_folder.exists():
            logging.warning(f"Folder already exists at destination: {folder_name}")
            self.stats['skipped'] += 1
            return False
        
        try:
            if self.dry_run:
                action = "COPY" if self.copy_mode else "MOVE"
                logging.info(f"[DRY RUN] Would {action} folder: {folder_name}")
                self.stats['folders_migrated'] += 1
                return True
            
            # Create parent destination directory if it doesn't exist
            self.destination.mkdir(parents=True, exist_ok=True)
            
            # Perform copy or move operation
            if self.copy_mode:
                shutil.copytree(source_folder, destination_folder)
                logging.info(f"Copied folder: {folder_name}")
            else:
                shutil.move(str(source_folder), str(destination_folder))
                logging.info(f"Moved folder: {folder_name}")
            
            self.stats['folders_migrated'] += 1
            return True
        
        except Exception as e:
            logging.error(f"Error processing folder {folder_name}: {e}")
            self.stats['errors'] += 1
            return False
    
    def organize(self) -> dict:
        """
        Execute the file organization process.
        
        Returns:
            Dictionary containing operation statistics
        """
        logging.info("=" * 60)
        logging.info("Pattern-Based File & Folder Organizer")
        logging.info("=" * 60)
        logging.info(f"Source: {self.source}")
        logging.info(f"Destination: {self.destination}")
        
        # Check if we're migrating folders
        if self.folders_to_migrate:
            logging.info(f"Folder Migration Mode:")
            logging.info(f"Filter Criteria for Folders:")
            
            criteria_displayed = False
            
            # Display folder name patterns
            name_pattern = self.folders_to_migrate.get("name_pattern")
            if name_pattern is not None:
                if isinstance(name_pattern, str):
                    patterns = [name_pattern]
                else:
                    patterns = name_pattern
                
                pattern_desc = []
                for p in patterns:
                    if p.startswith("^"):
                        pattern_desc.append(f"starts with '{p[1:]}'")
                    else:
                        pattern_desc.append(f"'{p}'")
                
                logging.info(f"  - Folder Name: {' OR '.join(pattern_desc)}")
                criteria_displayed = True
            
            # Display folder file type requirements
            file_type = self.folders_to_migrate.get("file_type")
            if file_type is not None:
                if isinstance(file_type, str):
                    types = [file_type]
                else:
                    types = file_type
                
                logging.info(f"  - Contains File Type: {' OR '.join(types)}")
                criteria_displayed = True
            
            # Display folder size constraints
            if self.folders_to_migrate.get("min_size_mb") is not None:
                logging.info(f"  - Min Folder Size: {self.folders_to_migrate['min_size_mb']} MB")
                criteria_displayed = True
            if self.folders_to_migrate.get("max_size_mb") is not None:
                logging.info(f"  - Max Folder Size: {self.folders_to_migrate['max_size_mb']} MB")
                criteria_displayed = True
            
            if not criteria_displayed:
                logging.info(f"  - All folders (no filters)")
        else:
            logging.info(f"File Migration Mode:")
            logging.info(f"Filter Criteria for Files:")
            
            # Display active filters
            criteria_displayed = False
            
            # Display name patterns
            name_pattern = self.pattern.get("name_pattern")
            if name_pattern is not None:
                if isinstance(name_pattern, str):
                    patterns = [name_pattern]
                else:
                    patterns = name_pattern
                
                pattern_desc = []
                for p in patterns:
                    if p.startswith("^"):
                        pattern_desc.append(f"starts with '{p[1:]}'")
                    else:
                        pattern_desc.append(f"ends with '{p}'")
                
                logging.info(f"  - Name Pattern: {' OR '.join(pattern_desc)}")
                criteria_displayed = True
            
            # Display file types
            file_type = self.pattern.get("file_type")
            if file_type is not None:
                if isinstance(file_type, str):
                    types = [file_type]
                else:
                    types = file_type
                
                logging.info(f"  - File Type: {' OR '.join(types)}")
                criteria_displayed = True
            
            # Display size constraints
            if self.pattern.get("min_size_mb") is not None:
                logging.info(f"  - Min Size: {self.pattern['min_size_mb']} MB")
                criteria_displayed = True
            if self.pattern.get("max_size_mb") is not None:
                logging.info(f"  - Max Size: {self.pattern['max_size_mb']} MB")
                criteria_displayed = True
            
            if not criteria_displayed:
                logging.info(f"  - All files (no filters)")
        
        logging.info(f"Mode: {'COPY' if self.copy_mode else 'MOVE'}")
        logging.info(f"Dry Run: {'YES' if self.dry_run else 'NO'}")
        logging.info("=" * 60)
        
        # Validate paths
        if not self.validate_paths():
            return self.stats
        
        # Track if we're processing anything
        processed_something = False
        
        # Process folders if folder migration is enabled
        if self.folders_to_migrate:
            logging.info("Scanning for folders to migrate...")
            folders = self.get_folders_to_migrate()
            
            if folders:
                logging.info(f"Found {len(folders)} folder(s) matching criteria")
                logging.info("")
                
                # Process each folder
                for folder_path, folder_name in folders:
                    self.process_folder(folder_path, folder_name)
                processed_something = True
            else:
                logging.warning(f"No folders found matching the specified criteria")
        
        # Process files if file migration is enabled
        if self.pattern:
            logging.info("Scanning for matching files...")
            matching_files = self.get_matching_files()
            
            if matching_files:
                logging.info(f"Found {len(matching_files)} matching file(s)")
                logging.info("")
                
                # Process each file
                for source_path, filename in matching_files:
                    self.process_file(source_path, filename)
                processed_something = True
            else:
                logging.warning(f"No files found matching the specified criteria")
        
        # If neither files nor folders are configured for migration
        if not processed_something:
            if not self.folders_to_migrate and not self.pattern:
                logging.error("No migration configured. FILES_TO_MIGRATE and FOLDERS_TO_MIGRATE are both set to None.")
                logging.error("Please configure at least one in the script, or provide command line options.")
            return self.stats
        
        # Print summary
        self._print_summary()
        
        return self.stats
    
    def _print_summary(self) -> None:
        """Print operation summary."""
        logging.info("")
        logging.info("=" * 60)
        logging.info("OPERATION SUMMARY")
        logging.info("=" * 60)
        
        # Show file statistics if files were processed
        if self.pattern:
            logging.info(f"FILES:")
            logging.info(f"  Matched:   {self.stats['matched']}")
            logging.info(f"  Processed: {self.stats['processed']}")
        
        # Show folder statistics if folders were processed
        if self.folders_to_migrate:
            logging.info(f"FOLDERS:")
            logging.info(f"  Matched:  {self.stats['folders_matched']}")
            logging.info(f"  Migrated: {self.stats['folders_migrated']}")
        
        # Show common statistics
        if self.pattern or self.folders_to_migrate:
            logging.info(f"OVERALL:")
            logging.info(f"  Skipped: {self.stats['skipped']}")
            logging.info(f"  Errors:  {self.stats['errors']}")
        
        logging.info("=" * 60)


# ============================================
# COMMAND LINE INTERFACE
# ============================================

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Organize files and folders based on multiple criteria',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
FILE FILTERING EXAMPLES:
  # Files ending with '_1' or '_1$'
  python file_organizer.py /source /dest -p "_1"
  
  # Files starting with 'Report' (use ^)
  python file_organizer.py /source /dest -p "^Report"
  
  # Files containing '2024' anywhere (use *pattern*)
  python file_organizer.py /source /dest -p "*2024*"
  
  # Multiple patterns - files ending with '_1' OR '_2'
  python file_organizer.py /source /dest -p "_1" "_2"
  
  # Single file type - all PDF files
  python file_organizer.py /source /dest -t ".pdf"
  
  # Multiple file types - PDF, JPG, DOCX files
  python file_organizer.py /source /dest -t ".pdf" ".jpg" ".docx"
  
  # Files larger than 10 MB
  python file_organizer.py /source /dest --min-size 10
  
  # Combine: Files with 'invoice' anywhere that are PDFs
  python file_organizer.py /source /dest -p "*invoice*" -t ".pdf"

FOLDER FILTERING EXAMPLES:
  # Folders named 'Archive' OR 'Backup'
  python file_organizer.py /source /dest --folder-pattern "Archive" "Backup"
  
  # Folders starting with 'Project'
  python file_organizer.py /source /dest --folder-pattern "^Project"
  
  # Folders containing '2024' anywhere in name
  python file_organizer.py /source /dest --folder-pattern "*2024*"
  
  # Folders containing PDF files
  python file_organizer.py /source /dest --folder-contains ".pdf"
  
  # Folders containing images (JPG OR PNG)
  python file_organizer.py /source /dest --folder-contains ".jpg" ".png"
  
  # Large folders (>= 100 MB)
  python file_organizer.py /source /dest --folder-min-size 100
  
  # Combine: Large folders containing PDFs
  python file_organizer.py /source /dest --folder-contains ".pdf" --folder-min-size 50

COMBINATION MODE (FILES + FOLDERS):
  # Migrate PDF files AND Archive folders together
  python file_organizer.py /source /dest -t ".pdf" --folder-pattern "Archive"
  
  # Files with '_1' AND folders starting with 'Project'
  python file_organizer.py /source /dest -p "_1" --folder-pattern "^Project"
  
  # Multiple files + multiple folders
  python file_organizer.py /source /dest -p "_1" "_2" -t ".pdf" --folder-pattern "Archive" "Backup"
  
  # Files with '2024' + folders with '2024'
  python file_organizer.py /source /dest -p "*2024*" --folder-pattern "*2024*"

GENERAL OPTIONS:
  # Copy instead of move
  python file_organizer.py /source /dest -p "_1" --copy
  
  # Preview changes (dry run)
  python file_organizer.py /source /dest -t ".pdf" --dry-run
  
  # Verbose logging
  python file_organizer.py /source /dest -p "_old" -v --log operations.log

PATTERN SYNTAX:
  ^pattern  = Starts with pattern (e.g., "^Report")
  pattern$  = Ends with pattern (e.g., "_draft$")
  *pattern* = Contains pattern anywhere (e.g., "*2024*")
  pattern   = Ends with pattern (default) (e.g., "_1")
        """
    )
    
    parser.add_argument('source', nargs='?', default=DEFAULT_SOURCE,
                        help='Source directory path')
    parser.add_argument('destination', nargs='?', default=DEFAULT_DESTINATION,
                        help='Destination directory path')
    
    # Folder migration options
    folder_group = parser.add_argument_group('Folder Migration Options (overrides file filtering if any folder option is used)')
    folder_group.add_argument('--folder-pattern', nargs='+', dest='folder_name_pattern',
                        help='Folder name pattern(s) - use "^" for start (e.g., "Archive", "^Project")')
    folder_group.add_argument('--folder-contains', nargs='+', dest='folder_file_type',
                        help='File type(s) folder must contain (e.g., ".pdf", ".jpg")')
    folder_group.add_argument('--folder-min-size', type=float, dest='folder_min_size_mb',
                        help='Minimum folder size in MB')
    folder_group.add_argument('--folder-max-size', type=float, dest='folder_max_size_mb',
                        help='Maximum folder size in MB')
    
    # Pattern filtering options
    filter_group = parser.add_argument_group('File Filter Options (ignored if --folders is used)')
    filter_group.add_argument('-p', '--pattern', nargs='+', dest='name_pattern',
                        help='Name pattern(s) - use "^" for start, no prefix for end (e.g., "_1", "^A")')
    filter_group.add_argument('-t', '--type', nargs='+', dest='file_type',
                        help='File extension(s) (e.g., ".pdf", ".jpg", "txt")')
    filter_group.add_argument('--min-size', type=float, dest='min_size_mb',
                        help='Minimum file size in MB')
    filter_group.add_argument('--max-size', type=float, dest='max_size_mb',
                        help='Maximum file size in MB')
    
    # Operation options
    op_group = parser.add_argument_group('Operation Options')
    op_group.add_argument('--copy', action='store_true',
                        help='Copy files instead of moving them')
    op_group.add_argument('--dry-run', action='store_true',
                        help='Preview operations without executing them')
    
    # Logging options
    log_group = parser.add_argument_group('Logging Options')
    log_group.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    log_group.add_argument('--log', metavar='FILE',
                        help='Save log output to file')
    
    return parser.parse_args()


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    # Setup logging
    setup_logging(log_file=args.log, verbose=args.verbose)
    
    # Check if any folder migration options are specified
    has_folder_options = any([
        args.folder_name_pattern,
        args.folder_file_type,
        args.folder_min_size_mb is not None,
        args.folder_max_size_mb is not None
    ])
    
    # Check if any file migration options are specified
    has_file_options = any([
        args.name_pattern,
        args.file_type,
        args.min_size_mb is not None,
        args.max_size_mb is not None
    ])
    
    # Build folders_to_migrate dictionary from command line or use default
    folders_to_migrate = None
    
    if has_folder_options:
        # Build folder filter dictionary from command line arguments
        folders_to_migrate = {}
        
        # Handle folder name pattern
        if args.folder_name_pattern:
            if len(args.folder_name_pattern) == 1:
                folders_to_migrate['name_pattern'] = args.folder_name_pattern[0]
            else:
                folders_to_migrate['name_pattern'] = args.folder_name_pattern
        else:
            folders_to_migrate['name_pattern'] = None
        
        # Handle folder file type
        if args.folder_file_type:
            if len(args.folder_file_type) == 1:
                folders_to_migrate['file_type'] = args.folder_file_type[0]
            else:
                folders_to_migrate['file_type'] = args.folder_file_type
        else:
            folders_to_migrate['file_type'] = None
        
        # Handle folder size constraints
        folders_to_migrate['min_size_mb'] = args.folder_min_size_mb
        folders_to_migrate['max_size_mb'] = args.folder_max_size_mb
    else:
        # Use default from configuration
        folders_to_migrate = FOLDERS_TO_MIGRATE
    
    # Build file pattern dictionary from command line arguments or use default
    pattern = None
    
    if has_file_options:
        # Build file filter dictionary from command line arguments
        pattern = {}
        
        # Handle name_pattern (can be list or single value or None)
        if args.name_pattern:
            # If multiple patterns provided, keep as list; if single, keep as string
            if len(args.name_pattern) == 1:
                pattern['name_pattern'] = args.name_pattern[0]
            else:
                pattern['name_pattern'] = args.name_pattern
        else:
            pattern['name_pattern'] = None
        
        # Handle file_type (can be list or single value or None)
        if args.file_type:
            # If multiple types provided, keep as list; if single, keep as string
            if len(args.file_type) == 1:
                pattern['file_type'] = args.file_type[0]
            else:
                pattern['file_type'] = args.file_type
        else:
            pattern['file_type'] = None
        
        # Handle size constraints
        pattern['min_size_mb'] = args.min_size_mb
        pattern['max_size_mb'] = args.max_size_mb
    else:
        # Use default from configuration
        pattern = FILES_TO_MIGRATE
    
    # Check if at least one migration type is enabled
    if pattern is None and folders_to_migrate is None:
        logging.error("No migration enabled. Please enable either FILES_TO_MIGRATE or FOLDERS_TO_MIGRATE in the configuration,")
        logging.error("or provide command line options for file filtering (-p, -t, --min-size, --max-size)")
        logging.error("or folder filtering (--folder-pattern, --folder-contains, --folder-min-size, --folder-max-size)")
        return 1
    
    # Create organizer instance
    organizer = FileOrganizer(
        source=args.source,
        destination=args.destination,
        pattern=pattern,
        folders_to_migrate=folders_to_migrate,
        copy_mode=args.copy,
        dry_run=args.dry_run
    )
    
    # Execute organization
    stats = organizer.organize()
    
    # Exit with appropriate code
    exit_code = 1 if stats['errors'] > 0 else 0
    return exit_code


if __name__ == "__main__":
    exit(main())
