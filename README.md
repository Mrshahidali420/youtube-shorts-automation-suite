# YouTube Shorts Automation Suite with Self-Improvement

[![GitHub Release](https://img.shields.io/badge/release-v1.4.0-blue)](https://github.com/Mrshahidali420/youtube-shorts-automation-suite/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This suite of scripts automates the entire YouTube Shorts workflow - from finding videos to tracking performance. It includes advanced self-improvement features that use AI to analyze performance, optimize metadata, and suggest improvements.

## Components

The suite consists of three main scripts:

1. **Performance Tracker** (`performance_tracker.py`): Collects performance metrics from uploaded videos
2. **Keyword-Based Downloader** (`downloader_keyword.py`): Finds and downloads new videos using keywords with integrated SEO optimization and self-improvement
3. **Channel-Based Downloader** (`downloader_channel.py`): Downloads videos from specific YouTube channels listed in channels.txt with integrated metadata optimization
4. **Uploader** (`uploader.py`): Uploads the videos to YouTube with optimized metadata

These components work together to create a complete automation pipeline for YouTube Shorts.

## Features

### Keyword-Based Downloader Features
- **SEO-Focused Metadata Generation**: Creates highly optimized titles, descriptions, and tags
- **Dynamic Category Suggestion**: Uses AI to suggest the most appropriate YouTube category based on video content
- **Performance-Based Keyword Selection**: Learns which keywords lead to better-performing videos
- **Dynamic Keyword Management**: Adds new keywords and removes underperforming ones
- **Metadata Prompt Refinement**: Automatically improves the prompt used for metadata generation
- **Parameter Tuning Suggestions**: Analyzes performance metrics to suggest configuration changes

### Channel-Based Downloader Features
- **Channel-Specific Video Discovery**: Downloads videos from specific YouTube channels listed in channels.txt
- **Permanent Channel Caching**: Stores channel video lists to avoid repeatedly fetching the same content
- **Per-Channel Processed ID Tracking**: Keeps track of which videos have been processed for each channel
- **View Count Prioritization**: Downloads videos with higher view counts first
- **SEO-Focused Metadata Generation**: Creates optimized titles, descriptions, and tags with proper credit to original uploaders
- **Compatible with Uploader**: Works seamlessly with the uploader script and performance tracking system

### Uploader Features
- **Automated Uploads**: Batch upload videos to YouTube as Shorts
- **Metadata Management**: Apply optimized titles, descriptions, and tags
- **Smart Category Selection**: Uses AI-suggested categories with fallback to default configuration
- **Dynamic Scheduling**: Schedule videos based on YouTube Analytics data for optimal viewer engagement
- **Flexible Scheduling Modes**: Choose between immediate publishing, fixed intervals, custom times, or analytics-based scheduling
- **Error Handling**: Robust error detection and recovery
- **Performance Tracking**: Track upload success rates and error patterns
- **AI-Assisted Analysis**: Use Google's Gemini AI to analyze errors and suggest improvements
- **Debug Recording**: Optional screen recording during uploads for troubleshooting
- **Excel Auto-Closing**: Automatically detects and closes Excel processes to prevent permission errors when saving
- **Excel Archiving**: Automatically moves old entries to archive sheets to keep main sheets manageable
- **Metadata Cross-Validation**: Validates generated metadata for consistency and quality

## Self-Improvement Features

The suite includes AI-powered self-improvement capabilities in both the downloader and uploader:

### Downloader Self-Improvement

- **Performance Feedback Loop**: Tracks how videos perform and adjusts keyword scores
- **Metadata Quality Analysis**: Monitors metadata generation success rates and improves the prompt
- **Parameter Tuning**: Analyzes overall performance and suggests configuration changes
- **Keyword Pool Management**: Dynamically adds new keywords and removes underperforming ones

### Uploader Self-Improvement

- **Performance Metrics Tracking**: Tracks upload attempts and successes
- **Error Categorization**: Categorizes and counts different types of errors
- **Error Sample Analysis**: Stores detailed error samples for analysis
- **AI-Assisted Error Analysis**: Uses Google's Gemini AI to analyze error patterns
- **Selector Optimization**: Recommends XPath selector updates, timeout adjustments, and other optimizations

### How to Use Self-Improvement Features

1. Add your Gemini API key to the `config.txt` file:
   ```
   API_KEY=your_gemini_api_key_here
   ```
   Get your API key from: https://aistudio.google.com/app/apikey

2. For uploader analysis, run with the `--analyze` or `-a` flag:
   ```
   python uploader.py --analyze
   ```

3. For downloader, the self-improvement happens automatically during normal operation

4. Review the analysis in the console output and in the log files

5. Apply any suggested improvements to the configuration

## Configuration

Edit the `config.txt` file to customize the suite's behavior. Here's a detailed explanation of all available options:

```
# API Keys (Required for both downloader and uploader)
API_KEY=your_gemini_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # Same as API_KEY, used for AI features

# Download and Upload Limits
MAX_DOWNLOADS=6        # Maximum number of videos to download per run
MAX_UPLOADS=12         # Maximum number of videos to upload per run
MAX_KEYWORDS=200       # Maximum number of keywords to store

# Upload Settings
UPLOAD_CATEGORY=Gaming  # Default YouTube category for uploads (used as fallback if AI suggestion fails)

# --- Scheduling Settings ---

# Mode for scheduling uploads. Options:
#   analytics_priority = Automatically schedule videos during peak viewer hours based on YouTube Analytics data.
#   default_interval   = Publish first video now, schedule subsequent videos at fixed interval.
#   custom_tomorrow    = Try custom schedule times from config (for tomorrow onwards), then use fixed interval fallback.
SCHEDULING_MODE=analytics_priority

# Fallback interval (in minutes) used when:
# - analytics_priority mode can't find a suitable peak hour
# - default_interval mode for all videos after the first
# - custom_tomorrow mode when custom slots are exhausted/invalid
SCHEDULE_INTERVAL_MINUTES=120

# List of preferred schedule times (HH:MM AM/PM format, comma-separated) for 'custom_tomorrow' mode.
# The script will try to use these times sequentially for videos in a run, always targeting TOMORROW's date or later.
CUSTOM_SCHEDULE_TIMES=6:00 AM, 9:00 AM, 11:30 AM, 3:00 PM, 6:00 PM, 10:00 PM

# Minimum number of minutes ahead of the current time a video can be scheduled.
# Prevents scheduling too close to the current time, which YouTube might reject.
MIN_SCHEDULE_AHEAD_MINUTES=20

# --- Analytics-Based Scheduling Settings ---
# These settings apply to the analytics_priority mode

# Number of days of analytics data to analyze for determining peak hours
ANALYTICS_DAYS_TO_ANALYZE=7

# Number of peak hours to identify from analytics data (1-24)
# Higher values include more hours but may dilute the focus on truly peak times
ANALYTICS_PEAK_HOURS_COUNT=5

# How long to cache analytics data before refreshing (in hours)
# Lower values provide more up-to-date data but increase API calls
ANALYTICS_CACHE_EXPIRY_HOURS=24

# Browser Profile
PROFILE_PATH=C:\Users\YourUsername\AppData\Roaming\Mozilla\Firefox\Profiles\yourprofile.default

# YouTube Limits (Character/Count Limits for Uploads)
YOUTUBE_DESCRIPTION_LIMIT=4950
YOUTUBE_TAG_LIMIT=100
YOUTUBE_TOTAL_TAGS_LIMIT=450
YOUTUBE_MAX_TAGS_COUNT=40

# Debug Recording Settings
# Enable screen recording for debugging (True/False). Requires FFmpeg installed.
ENABLE_DEBUG_RECORDING=False
# Optional: Specify full path to ffmpeg executable if not found automatically in system PATH
FFMPEG_PATH=C:\path\to\ffmpeg.exe

# Excel Archiving Settings
# Number of days to keep entries in the main Excel sheets before moving to archive sheets
# Older entries will be moved to "Downloaded_Archive" and "Uploaded_Archive" sheets
EXCEL_ARCHIVE_DAYS=180
```

### Important Configuration Options

#### Scheduling Modes

- **analytics_priority** (Recommended): Automatically schedules videos during peak viewer hours based on YouTube Analytics data. The script will:
  1. Query the YouTube Analytics API to identify your channel's peak viewer hours
  2. Automatically schedule videos during those peak hours
  3. Use the fallback interval only when no suitable peak hour can be found
  4. Cache the analytics data to minimize API calls

- **default_interval**: Publishes the first video immediately and schedules subsequent videos at fixed intervals defined by `SCHEDULE_INTERVAL_MINUTES`.

- **custom_tomorrow**: Uses the times specified in `CUSTOM_SCHEDULE_TIMES` starting from tomorrow, then falls back to fixed intervals if needed. No videos are published immediately.

#### Analytics-Based Scheduling

The analytics_priority mode provides fully automatic, data-driven scheduling:

1. **Automatic Peak Hour Detection**: Identifies when your audience is most active
2. **Smart Scheduling**: Prioritizes uploads during those peak hours
3. **Fallback Mechanism**: Uses standard interval when no suitable peak hour is available
4. **Configurable Parameters**:
   - `ANALYTICS_DAYS_TO_ANALYZE`: How many days of historical data to analyze
   - `ANALYTICS_PEAK_HOURS_COUNT`: How many peak hours to identify
   - `ANALYTICS_CACHE_EXPIRY_HOURS`: How long to cache analytics data

This feature requires:
- YouTube Analytics API access (automatically enabled when you authenticate)
- The `token.json` file to be deleted the first time you use this feature (to request the additional API scope)
- A channel with sufficient historical data for meaningful analysis

#### Firefox Profile

Using a dedicated Firefox profile is recommended for the uploader. This allows you to:
- Stay logged into YouTube
- Avoid login captchas
- Maintain session cookies

To create a new Firefox profile:
1. Open Firefox and type `about:profiles` in the address bar
2. Click "Create a New Profile" and follow the instructions
3. Copy the profile path from the "Root Directory" field
4. Paste it into the `PROFILE_PATH` setting in `config.txt`

## Excel File Structure

The system uses an Excel file (`shorts_data.xlsx`) with four sheets:

### Downloaded Sheet
- Video Index
- Optimized Title
- Downloaded Date
- Views
- Uploader
- Original Title

### Uploaded Sheet
- Video Index
- Optimized Title
- YouTube Video ID
- Upload Timestamp
- Scheduled Time
- Publish Status
- Views (YT)
- Likes (YT)
- Comments (YT)
- Last Updated

### Downloaded_Archive Sheet
- Contains the same columns as the Downloaded sheet
- Stores older entries that have been archived from the main Downloaded sheet
- Created automatically when archiving is performed

### Uploaded_Archive Sheet
- Contains the same columns as the Uploaded sheet
- Stores older entries that have been archived from the main Uploaded sheet
- Created automatically when archiving is performed

## Requirements

- Python 3.8+
- Required packages: `yt_dlp`, `google-generativeai`, `openpyxl`, `colorama`, `selenium`, `psutil`
- Firefox browser (for uploader)
- Google Gemini API key (for all AI features)
- FFmpeg (for video processing and optional debug recording)

## Installation

### Option 1: Standard Installation

1. Download the [latest release](https://github.com/Mrshahidali420/youtube-shorts-automation-suite/releases/latest) or clone this repository
2. Install required packages: `pip install -r requirements.txt`
3. Create configuration files from templates:
   - Copy `templates/config.txt.template` to `config.txt` and update with your settings
   - Copy `templates/niche.txt.template` to `niche.txt` and add your target niche (e.g., "GTA 6")
   - Copy `templates/channels.txt.template` to `channels.txt` and add your target channels (if using channel-based downloader)
4. Run each component as needed (see 'Running Individual Components' section below)

### Option 2: Package Installation

1. Clone this repository
2. Install the package in development mode: `pip install -e .`
3. Set up your workspace: `yt-setup` or `python -m youtube_shorts.setup_workspace`
4. Create configuration files from templates:
   - Copy `templates/config.txt.template` to `config.txt` and update with your settings
   - Copy `templates/niche.txt.template` to `niche.txt` and add your target niche (e.g., "GTA 6")
   - Copy `templates/channels.txt.template` to `channels.txt` and add your target channels (if using channel-based downloader)
5. Use the command-line tools:
   ```
   yt-track    # Run performance tracker
   yt-download # Run keyword-based downloader
   yt-channel  # Run channel-based downloader
   yt-upload   # Run uploader
   ```

## Running Individual Components

### Using Python Directly

```
python performance_tracker.py
python downloader_keyword.py   # Run keyword-based downloader
python downloader_channel.py   # Run channel-based downloader
python uploader.py
```

### Using Package Commands (if installed as a package)

```
yt-track    # Run performance tracker
yt-download # Run keyword-based downloader
yt-channel  # Run channel-based downloader
yt-upload   # Run uploader
```

### Setting Up Channel-Based Downloads

1. Create a `channels.txt` file in the root directory (copy from `templates/channels.txt.template`)
2. Add one YouTube channel URL per line (e.g., `https://www.youtube.com/@ChannelName`)
3. Run the channel-based downloader: `python downloader_channel.py`

The channel-based downloader will:
- Download videos from the specified channels
- Store metadata in the same format as the keyword-based downloader
- Add entries to the same Excel file for processing by the uploader

## Error Types Tracked

### Uploader Error Types
- XPath Selector Errors
- Timeout Errors
- Network Errors
- WebDriver Errors
- Session Errors
- YouTube UI Change Errors
- Input Field Errors
- Click Interaction Errors
- Validation Errors
- File Operation Errors

### Downloader Error Types
- Metadata Generation Errors
- API Timeout Errors
- Download Failures
- Parsing Errors
- File Operation Errors

## Files

### Main Scripts
- `performance_tracker.py`: Tracks video performance metrics
- `downloader_keyword.py`: Downloads videos with integrated SEO optimization and self-improvement using keywords
- `downloader_channel.py`: Downloads videos from specific YouTube channels with integrated metadata optimization
- `uploader.py`: Uploads videos to YouTube
- `excel_utils.py`: Utilities for robust Excel file handling
- `youtube_limits.py`: Constants for YouTube platform limits

### Package Structure
- `youtube_shorts/`: Package directory
  - `__init__.py`: Package initialization
  - `performance_tracker.py`: Performance tracking module
  - `downloader.py`: Video downloading module (keyword-based)
  - `uploader.py`: Video uploading module
  - `excel_utils.py`: Excel utilities module
  - `setup_workspace.py`: Workspace setup utility

### Configuration and Data Files
- `setup.py`: Package setup script
- `requirements.txt`: Required dependencies
- `templates/`: Directory containing template files
  - `templates/config.txt.template`: Template for configuration settings
  - `templates/niche.txt.template`: Template for target niche
  - `templates/channels.txt.template`: Template for channel URLs
- `config.txt`: Configuration settings (created from template or by setup script)
- `niche.txt`: Target niche for content for keyword-based downloader (created from template or by setup script)
- `channels.txt`: List of YouTube channel URLs for channel-based downloader (created from template)
- `shorts_data.xlsx`: Excel file tracking downloaded and uploaded videos (created by setup script)
- `seo_metadata_prompt.txt`: Cache for the potentially improved SEO prompt (created during runtime)
- `metadata_metrics.json`: Tracks metadata generation metrics (created during runtime)
- `performance_metrics.json`: Tracks overall performance metrics (created during runtime)
- `channel_processed_ids_cache.json`: Tracks which videos have been processed from each channel (created during runtime)
- `channel_listing_cache.json`: Stores channel video lists to avoid repeatedly fetching the same content (created during runtime)
- `upload_correlation_cache.json`: Stores links between video indices, discovery keywords, and YouTube Video IDs (created during runtime)

### Directories
- `shorts_downloads/`: Where downloaded videos are stored (created by setup script)
- `shorts_metadata/`: Where optimized metadata files are stored (created by setup script)
- `templates/`: Contains template files for user configuration
- `youtube_shorts/data/`: Contains template files for package configuration

## Releases

### Latest Release: [v1.4.0](https://github.com/Mrshahidali420/youtube-shorts-automation-suite/releases/tag/v1.4.0)

The latest stable release of the YouTube Shorts Automation Suite is v1.4.0. You can:

- **Download**: Get the [ZIP file](https://github.com/Mrshahidali420/youtube-shorts-automation-suite/archive/refs/tags/v1.4.0.zip) directly
- **Clone**: Use Git to clone a specific version: `git clone -b v1.4.0 https://github.com/Mrshahidali420/youtube-shorts-automation-suite.git`
- **Install**: Install with pip: `pip install git+https://github.com/Mrshahidali420/youtube-shorts-automation-suite.git@v1.4.0`

### Release Notes

#### v1.4.0 - Latest Release

**New Features:**
- **Analytics Priority Mode**: New scheduling mode that automatically prioritizes peak viewer hours
- **Fully Automatic Scheduling**: Simplified configuration with intelligent, data-driven scheduling
- **Peak Hour Detection**: Automatically identifies peak viewer hours for your channel
- **Smart Time Slot Selection**: Finds the next available peak hour for each video
- **Analytics Caching**: Caches analytics data to minimize API calls and improve performance

**Improvements:**
- Enhanced scheduling logic to optimize video visibility
- Simplified configuration with sensible defaults
- Improved documentation for analytics-based scheduling
- Added graceful fallback when analytics data is unavailable
- Made analytics-based scheduling the default mode

#### v1.3.0

**New Features:**
- **Excel Archiving**: Added automatic archiving of old entries to archive sheets to keep main sheets manageable
- **Metadata Cross-Validation**: Added validation checks for generated metadata to ensure consistency and quality
- **Configuration for Archiving**: Added EXCEL_ARCHIVE_DAYS setting to control when entries are archived

**Improvements:**
- Enhanced error handling for Excel archiving operations
- Improved metadata quality through validation checks
- Added detailed logging for archiving operations

#### v1.2.0

**New Features:**
- **Excel Auto-Closing Functionality**: Added robust Excel handling to prevent permission errors when saving Excel files
- **Excel Utilities Module**: Created a dedicated module for Excel operations with process management
- **Automatic Backup Creation**: Added automatic backup of Excel files before saving
- **Retry Mechanics**: Implemented retry logic for Excel operations with exponential backoff
- **Fallback Save Methods**: Added multiple fallback methods for saving Excel data when primary methods fail

**Improvements:**
- Enhanced error handling for Excel operations
- Added graceful degradation when Excel utilities are not available
- Improved logging for Excel-related operations

#### v1.1.0

**New Features:**
- **Dynamic Category Suggestion**: Added AI-powered YouTube category suggestion based on video content
- **Smart Category Selection**: Uploader now uses AI-suggested categories with fallback to default configuration
- **Channel-Based Downloader**: Added new script to download videos from specific YouTube channels
- **Integrated Downloaders**: Both keyword-based and channel-based downloaders work together seamlessly

**Bug Fixes:**
- Fixed issue where info.json file was deleted before tag extraction, causing "Info file not found" warnings
- Various code improvements and optimizations

See the [releases page](https://github.com/Mrshahidali420/youtube-shorts-automation-suite/releases) for detailed release notes, which include:

- New features and improvements
- Bug fixes
- Breaking changes (if any)
- Installation instructions

## Open Source

This project is open source and welcomes contributions from the community. We believe in the power of collaboration and are excited to see how others might extend and improve this tool.

### How to Contribute

We welcome contributions of all kinds - from bug reports to feature requests to code contributions. Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed guidelines on how to contribute.

### Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating in our community.

## Repository History

This project was previously hosted at [https://github.com/Mrshahidali420/youtube-shorts-automation](https://github.com/Mrshahidali420/youtube-shorts-automation) and has been migrated to this new repository for better organization and continued development.

## API Keys and Authentication

This project requires several API keys and authentication files to function properly:

1. **Google Gemini API Key**: Required for AI-powered features like metadata generation and error analysis
   - Get your API key from: https://aistudio.google.com/app/apikey
   - Add it to `config/config.txt` as both `API_KEY` and `GEMINI_API_KEY`

2. **YouTube API Authentication**: Required for YouTube API access (analytics, playlist management)
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the YouTube Data API v3
   - Create OAuth 2.0 credentials (Desktop application type)
   - Download the credentials as `client_secret.json` and place it in the `data/` directory
   - The first time you run scripts that use the YouTube API, you'll be prompted to authenticate

These sensitive files are excluded from the repository by the `.gitignore` file for security reasons. You must set them up locally after cloning the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. The MIT License is a permissive license that allows you to use, modify, and distribute this software for both private and commercial purposes.
