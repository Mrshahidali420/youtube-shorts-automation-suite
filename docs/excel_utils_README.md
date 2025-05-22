# Excel Utilities Module

This module provides robust Excel file handling with automatic process closing, retry mechanisms, and backup functionality to prevent permission errors.

## Features

- **Safe Excel Operations**: Handles Excel files with automatic process management to prevent permission errors
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Backup Functionality**: Automatically creates backups before operations
- **Archiving**: Moves old entries to archive sheets based on date
- **Robust Date Parsing**: Handles various date formats
- **Error Handling**: Comprehensive error handling with detailed messages
- **Logging**: Detailed logging for troubleshooting

## Dependencies

- **Required**:
  - `openpyxl`: For Excel file operations

- **Optional**:
  - `psutil`: For improved process management
  - `dateutil`: For enhanced date parsing

## Installation

```bash
pip install openpyxl psutil python-dateutil
```

## Usage Examples

### Basic Excel Operations

```python
import excel_utils

# Load or create an Excel file with specified sheets
sheets_config = {
    "Data": ["ID", "Name", "Value", "Date"],
    "Config": ["Setting", "Value", "Description"]
}
wb, sheets, save_needed = excel_utils.load_or_create_excel("data.xlsx", sheets_config)

# Add data to a sheet
rows = [
    ["ID1", "Test Name 1", 100, "2023-01-15"],
    ["ID2", "Test Name 2", 200, "2023-02-20"]
]
excel_utils.append_rows_to_sheet(sheets["Data"], rows)

# Save the workbook
excel_utils.save_workbook_with_fallback(wb, "data.xlsx", excel_utils.extract_workbook_data)
```

### Archiving Old Entries

```python
import excel_utils

# Load Excel file
wb, sheets, _ = excel_utils.load_or_create_excel("data.xlsx", {})

# Archive entries older than 30 days
excel_utils.archive_old_excel_entries(wb, "Data", "Date", 30)

# Save changes
excel_utils.save_workbook_with_fallback(wb, "data.xlsx", excel_utils.extract_workbook_data)
```

### Creating Backups

```python
import excel_utils

# Create a backup of an Excel file
backup_path = excel_utils.create_excel_backup("important_data.xlsx")
print(f"Backup created at: {backup_path}")

# Save data as JSON backup
data = {"key": "value", "numbers": [1, 2, 3]}
json_backup = excel_utils.save_data_as_json_backup(data, "original_file.xlsx")
print(f"JSON backup created at: {json_backup}")
```

### Process Management

```python
import excel_utils

# Find Excel processes
processes = excel_utils.find_excel_processes()
print(f"Found {len(processes)} Excel processes")

# Close Excel processes with a specific file open
excel_utils.close_excel_processes_with_file("data.xlsx")
```

## Function Reference

### Excel File Operations

- `load_or_create_excel(file_path, sheets_config)`: Loads or creates an Excel file with specified sheets
- `save_workbook_with_fallback(wb, file_path, data_extractor_func)`: Saves a workbook with fallback mechanisms
- `append_rows_to_sheet(sheet, rows)`: Appends rows to a sheet
- `find_column_index(sheet, column_name, case_sensitive=True)`: Finds the index of a column by name
- `extract_sheet_data(sheet)`: Extracts data from a sheet as a list of lists
- `extract_workbook_data(wb)`: Extracts data from all sheets in a workbook

### Process Management

- `find_excel_processes()`: Finds all running Excel processes
- `find_excel_processes_with_file(file_path)`: Finds Excel processes with a specific file open
- `close_excel_processes_with_file(file_path)`: Closes Excel processes with a specific file open
- `force_close_all_excel_processes()`: Forces all Excel processes to close

### Backup Functions

- `create_backup_folder()`: Creates a backup folder
- `create_excel_backup(file_path)`: Creates a backup of an Excel file
- `save_data_as_json_backup(data, original_file_path)`: Saves data as a JSON backup

### Archiving

- `archive_old_excel_entries(wb, sheet_name, date_col_name, days_to_keep)`: Archives entries older than a specified number of days

## Error Handling

The module includes comprehensive error handling with detailed error messages. Most functions return `None` or `False` on failure, along with appropriate error messages in the logs.

## Logging

The module uses Python's logging module for detailed logging. You can configure the logging level and handlers as needed.

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Testing

Run the module directly to execute the test function:

```bash
python excel_utils.py
```

This will run a comprehensive test of the module's functionality.
