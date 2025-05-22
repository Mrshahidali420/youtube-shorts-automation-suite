# Project Directory Structure

This document outlines the organization of the YouTube Shorts Automation project.

## Overview

The project is organized into the following main directories:

```
Project GTA/
├── youtube_shorts/       # Main package with all source code
├── config/               # Configuration files
├── data/                 # Data files
├── docs/                 # Documentation
├── logs/                 # Log files
├── backups/              # Backup files
├── drivers/              # Executable drivers
├── output/               # Generated content
├── README.md             # Main project documentation
├── setup.py              # Package setup script
├── requirements.txt      # Dependencies
├── .gitignore            # Git ignore file
├── LICENSE               # License file
├── manual_workflow.bat   # Manual workflow batch file
└── run_manual_workflow.bat # Run manual workflow batch file
```

## Directory Contents

### youtube_shorts/

Contains all the Python source code for the project.

```
youtube_shorts/
├── utils/                # Utility modules
│   ├── api_utils.py      # API interaction utilities
│   ├── auth_utils.py     # Authentication utilities
│   ├── cache_utils.py    # Caching utilities
│   ├── channel_scoring.py # Channel scoring utilities
│   ├── config_utils.py   # Configuration utilities
│   ├── constants.py      # SOURCE OF TRUTH FOR ALL PATHS
│   ├── date_utils.py     # Date handling utilities
│   ├── keyword_manager.py # Keyword management utilities
│   ├── metadata_generator.py # Metadata generation utilities
│   ├── metrics_utils.py  # Metrics tracking utilities
│   ├── playlist_manager.py # Playlist management utilities
│   ├── test_utils.py     # Test utilities
│   ├── ytdlp_utils.py    # yt-dlp wrapper utilities
│   └── __init__.py       # Package initialization
├── page_objects/         # Page object models for Selenium
│   ├── base_page.py      # Base page object
│   ├── confirmation_page.py # Upload confirmation page
│   ├── details_page.py   # Video details page
│   ├── studio_home_page.py # YouTube Studio home page
│   ├── upload_page.py    # Upload page
│   ├── visibility_page.py # Video visibility page
│   └── __init__.py       # Package initialization
├── data/                 # Package data files
│   ├── config.txt.template # Configuration template
│   ├── channels.txt.template # Channels template
│   └── niche.txt.template # Niche template
├── __init__.py           # Package initialization
├── downloader_channel.py # Downloads videos from specific channels
├── downloader_keyword.py # Downloads videos based on keywords (with integrated metadata optimization)
├── excel_utils.py        # Excel file operations
├── performance_tracker.py # Tracks video performance
├── secure_config.py      # Secure configuration utilities
├── uploader.py           # Uploads videos to YouTube
├── uploader_pom.py       # Page Object Model for uploader
└── youtube_limits.py     # YouTube platform limits
```

### config/

Contains configuration files for the project.

```
config/
├── templates/            # Template files
│   ├── config.txt.template # Configuration template
│   ├── channels.txt.template # Channels template
│   └── niche.txt.template # Niche template
├── config.txt            # Main configuration file
├── config.example.txt    # Example configuration file
├── channels.txt          # Channel URLs for channel-based downloader
├── niche.txt             # Target niche for keyword-based downloader
└── seo_metadata_prompt.txt # SEO prompt template
```

### data/

Contains data files for the project.

```
data/
├── analytics_data/       # Analytics data
│   ├── api_cache/        # API response caches
│   └── analytics_reports/ # Generated HTML reports
├── shorts_data.xlsx      # Main Excel file
├── token.json            # OAuth token (gitignored)
├── client_secret.json    # API credentials (gitignored)
├── metadata_metrics.json # Metrics for metadata generation
├── metadata_metrics_channel.json # Metrics specific to channel downloader
├── metadata_metrics_keyword.json # Metrics specific to keyword downloader
├── performance_metrics.json # Performance tracking metrics
├── performance_metrics_channel.json # Performance metrics for channel videos
├── performance_metrics_keyword.json # Performance metrics for keyword videos
├── upload_correlation_cache.json # Cache for upload correlations
├── generated_keywords_cache.json # Cache for generated keywords
├── playlists_data_cache.json # Cache for playlist data
├── downloaded_video_ids.json # Cache for downloaded video IDs
├── api_quota_usage.json  # Tracks API quota usage
└── historical_performance.json # Historical performance data
```

### docs/

Contains documentation files for the project.

```
docs/
├── SECURITY.md           # Security policy
├── CONTRIBUTING.md       # Contribution guidelines
├── CHANGELOG.md          # Version history and changes
├── MANUAL_WORKFLOW.md    # Guide for manual workflow
├── FILE_STRUCTURE.md     # This file - documentation of project structure
├── COMPONENT_RELATIONSHIPS.md # Explains relationships between components
├── CODE_OF_CONDUCT.md    # Code of conduct for contributors
├── SECURITY_CONFIG.md    # Security configuration guidelines
├── README_METADATA_OPTIMIZER.md # Documentation for metadata optimizer
├── README_UPLOADER_POM.md # Documentation for uploader page object model
├── REPOSITORY_PROTECTION_SUMMARY.md # Summary of repository protection measures
├── UNAUTHORIZED_COPIES.md # Information about unauthorized copies
├── TODO.md               # Todo list for future development
└── excel_utils_README.md # Documentation for Excel utilities
```

### logs/

Contains log files generated by the project.

```
logs/
├── tuning_suggestions.log # Parameter tuning suggestions
├── run_summaries.log     # Run summaries
├── downloader_log.txt    # Downloader logs
├── downloader_channel_log.txt # Channel downloader logs
├── downloader_keyword_log.txt # Keyword downloader logs
├── uploader_log.txt      # Uploader logs
├── uploader_analysis_log.txt # AI-generated analysis of uploader errors
├── uploader_pom_log.txt  # Page Object Model uploader logs
├── performance_tracker_log.txt # Performance tracker logs
├── excel_utils.log       # Excel utilities logs
├── api_utils.log         # API utilities logs
├── auth_utils.log        # Authentication utilities logs
└── metadata_generator.log # Metadata generator logs
```

### backups/

Contains backup files organized by type.

```
backups/
├── excel/              # Excel file backups
│   └── shorts_data.xlsx.bak # Backup of main Excel file
├── json_data/          # JSON data backups
│   ├── upload_correlation_cache.json.bak # Backup of upload correlation cache
│   ├── generated_keywords_cache.json.bak # Backup of generated keywords cache
│   ├── downloaded_video_ids.json.bak # Backup of downloaded video IDs
│   ├── playlists_data_cache.json.bak # Backup of playlist data
│   └── performance_metrics.json.bak # Backup of performance metrics
├── prompts/            # Prompt backups
│   └── seo_metadata_prompt.txt.backup # Backup of SEO prompt
└── other/              # Other miscellaneous backups
```

### drivers/

Contains executable drivers.

```
drivers/
├── ffmpeg.exe            # FFmpeg executable
└── geckodriver.exe       # Geckodriver executable
```

### output/

Contains generated content during workflow.

```
output/
├── shorts_downloads/     # Downloaded videos (.mp4)
├── shorts_metadata/      # Video metadata (.json) - Initial generation AND optimization happens here
├── error_screenshots/    # Screenshots captured during errors
├── debug_recordings/     # Screen recordings for debugging upload issues
└── uploaded_videos/      # Optional directory for manually archiving uploaded videos
```

## Root Files

- `README.md`: Main project documentation
- `setup.py`: Package setup script
- `requirements.txt`: Dependencies
- `.gitignore`: Git ignore file
- `LICENSE`: License file
- `manual_workflow.bat`: Manual workflow batch file
- `run_manual_workflow.bat`: Run manual workflow batch file

## Batch Files

- `manual_workflow.bat`: Interactive batch file for manual workflow
- `run_manual_workflow.bat`: Simple batch file for running the manual workflow

## Usage

This project is designed to be used directly from the source code rather than as an installed package with command-line entry points. Users should run the Python scripts directly or use the provided batch files.

## Module Relationships

### Core Pipeline Flow

1. **Download & Optimize** (`downloader_keyword.py`, `downloader_channel.py`)
   - Downloads videos and generates initial metadata
   - Optimizes metadata immediately using `utils/metadata_generator.py`
   - Uses: `utils/auth_utils.py`, `utils/api_utils.py`, `utils/cache_utils.py`, `utils/metadata_generator.py`

2. **Select** (Manual Selection)
   - You manually select the best videos for upload
   - Mark them for upload (e.g., by renaming .json files, adding a flag inside .json, maintaining a list, or passing as CLI args to uploader)

3. **Schedule** (Manual Scheduling - Optional)
   - You manually schedule videos for upload
   - Edit the metadata JSON files to include scheduling information

4. **Upload** (`uploader.py`)
   - Uploads videos to YouTube
   - Uses: `utils/auth_utils.py`, `excel_utils.py`

5. **Track** (`performance_tracker.py`)
   - Tracks video performance
   - Uses: `utils/auth_utils.py`, `utils/api_utils.py`, `excel_utils.py`

6. **Analyze** (Manual Analysis)
   - You analyze the performance data collected by the performance tracker
   - Review data in `shorts_data.xlsx` and `performance_metrics.json`

### Utility Module Relationships

- **constants.py**: Central source of truth for all file paths and directory structures
  - Used by: ALL modules
  - Defines all directory paths, file paths, and other constants
  - Ensures consistent path usage across the application
  - Enables easy adaptation to different environments
  - Provides a single point of change for directory structure updates

- **auth_utils.py**: Handles authentication for all API interactions
  - Used by: `api_utils.py`, downloaders, uploader, performance_tracker

- **api_utils.py**: Provides functions for API interactions
  - Uses: `auth_utils.py`, `config_utils.py`, `cache_utils.py`
  - Used by: downloaders, performance_tracker

- **config_utils.py**: Manages configuration
  - Uses: `constants.py` for file paths
  - Used by: most modules

- **cache_utils.py**: Handles caching of data
  - Uses: `constants.py` for cache file paths
  - Used by: downloaders, performance_tracker

- **date_utils.py**: Provides date parsing and formatting
  - Used by: uploader, performance_tracker

- **metrics_utils.py**: Tracks metrics for metadata and performance
  - Uses: `constants.py` for metrics file paths
  - Used by: metadata_optimizer, performance_tracker

- **metadata_generator.py**: Generates and validates metadata
  - Uses: `constants.py` for metadata file paths
  - Used by: downloaders, metadata_optimizer

## Excel File Structure

The main Excel file (`shorts_data.xlsx`) contains the following sheets:

1. **Downloaded**: Tracks downloaded videos
   - Video Index, Original Title, Downloaded Date, Views, Uploader, etc.

2. **Uploaded**: Tracks uploaded videos
   - Video ID, Title, Description, Tags, Upload Date, Views, Likes, Comments, etc.

3. **Downloaded_Archive**: Archive of downloaded videos
   - Same structure as Downloaded sheet

4. **Uploaded_Archive**: Archive of uploaded videos
   - Same structure as Uploaded sheet

## Configuration Files

### config.txt

Contains global configuration parameters:

```
API_KEY=your_api_key
GEMINI_API_KEY=your_gemini_api_key
MAX_DOWNLOADS=24
MAX_UPLOADS=24
SCHEDULING_MODE=analytics_priority
SCHEDULE_INTERVAL_MINUTES=120
...
```

## Documentation Files

The project includes comprehensive documentation:

- `README.md`: Main project documentation
- `MANUAL_WORKFLOW.md`: Guide for manual workflow
- `FILE_STRUCTURE.md`: This file - documentation of project structure
- `COMPONENT_RELATIONSHIPS.md`: Explains relationships between components
- `CHANGELOG.md`: Version history and changes
- `CODE_OF_CONDUCT.md`: Code of conduct for contributors
- `CONTRIBUTING.md`: Guidelines for contributing to the project
- `LICENSE`: MIT license file
- `SECURITY.md`: Security policy
- `SECURITY_CONFIG.md`: Security configuration guidelines
- `README_METADATA_OPTIMIZER.md`: Documentation for metadata optimizer
- `README_UPLOADER_POM.md`: Documentation for uploader page object model
- `REPOSITORY_PROTECTION_SUMMARY.md`: Summary of repository protection measures
- `UNAUTHORIZED_COPIES.md`: Information about unauthorized copies
- `TODO.md`: Todo list for future development
- `excel_utils_README.md`: Documentation for Excel utilities

## Data Flow in Manual Workflow

1. Videos are downloaded to `output/shorts_downloads/` and optimized metadata is stored in `output/shorts_metadata/` by running `downloader_keyword.py` or `downloader_channel.py`
2. You manually select which videos to upload (e.g., by reviewing the metadata files)
3. (Optional) You manually edit schedule times in the selected .json files in `output/shorts_metadata/` if not relying on uploader's dynamic scheduling
4. Videos are uploaded by running `uploader.py` which uses the metadata from `output/shorts_metadata/`
5. After successful upload, you can manually archive/move the processed .mp4 and .json files
6. Performance is tracked by running `performance_tracker.py`
7. All video data is tracked in `data/shorts_data.xlsx`
8. Performance data is stored in `data/performance_metrics.json`
9. Analytics data is cached in `data/analytics_data/`

## File Path Management

All file paths in the project are centralized in `youtube_shorts/utils/constants.py`. This approach provides several benefits:

1. **Consistency**: All modules use the same paths, eliminating discrepancies
2. **Maintainability**: Changing a path requires editing only one file
3. **Robustness**: Directory creation is handled before file operations
4. **Adaptability**: Easy to adapt to different environments or directory structures
5. **Clarity**: Clear documentation of the project's file organization

Each module imports constants.py with fallback mechanisms to ensure the application can run even if the import path is not correctly set up. Before file operations, directories are checked and created if they don't exist, preventing common file operation errors.

Example of robust import in modules:
```python
try:
    from .utils import constants  # If module is part of package
except ImportError:
    try:
        from utils import constants  # If run from youtube_shorts folder
    except ImportError:
        # Fallback with minimal constants if needed
        print("WARNING: Could not import constants.py")
```

Example of directory creation before file operations:
```python
# Ensure directory exists before writing
os.makedirs(os.path.dirname(constants.LOG_FILE_PATH), exist_ok=True)
with open(constants.LOG_FILE_PATH, "a", encoding="utf-8") as f:
    f.write(log_message)
```

## Dependencies

The project has the following main dependencies:

- **Google API Client**: For YouTube API access
- **Selenium**: For browser automation
- **OpenPyXL**: For Excel file operations
- **Google Generative AI**: For metadata generation
- **dateutil**: For robust date parsing
- **psutil**: For process management
