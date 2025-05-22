#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constants Module

This module defines constants used throughout the application.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0
"""

import os

# --- Base Directory Definitions based on FILE_STRUCTURE.md ---
# Assumes constants.py is in youtube_shorts/utils/
# SCRIPT_DIR will be .../Project GTA/youtube_shorts/utils
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# UTILS_DIR is CURRENT_FILE_DIR
# SCRIPT_DIR (for youtube_shorts package) is one level up from utils
PACKAGE_ROOT = os.path.dirname(CURRENT_FILE_DIR) # This is .../Project GTA/youtube_shorts/
# PROJECT_ROOT is one level up from the package
PROJECT_ROOT = os.path.dirname(PACKAGE_ROOT)    # This is .../Project GTA/

# --- New Directory Structure Paths ---
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs") # Not typically used in constants, but good to be aware
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
BACKUPS_DIR = os.path.join(PROJECT_ROOT, "backups")
DRIVERS_DIR = os.path.join(PROJECT_ROOT, "drivers")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# --- Configuration files (now in config/ directory) ---
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, "config.txt")
CHANNELS_FILE_PATH = os.path.join(CONFIG_DIR, "channels.txt")
KEYWORDS_FILE_PATH = os.path.join(CONFIG_DIR, "keywords.txt") # Assuming this exists, if not, it will be created there
SEO_METADATA_PROMPT_FILE = os.path.join(CONFIG_DIR, "seo_metadata_prompt.txt")

# --- Authentication files (now in data/ directory) ---
CLIENT_SECRETS_FILE = os.path.join(DATA_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(DATA_DIR, "token.json") # Main token for YouTube Data/Analytics
ANALYTICS_TOKEN_FILE = os.path.join(DATA_DIR, "youtube_analytics_token.pickle") # Specific token for analytics in analytics.py

# --- Output sub-directories (now under output/) ---
SHORTS_DOWNLOADS_DIR = os.path.join(OUTPUT_DIR, "shorts_downloads")
SHORTS_METADATA_DIR = os.path.join(OUTPUT_DIR, "shorts_metadata")
# Removed SELECTED_VIDEOS_DIR and OPTIMIZED_VIDEOS_DIR as part of A/B testing removal
# Metadata optimization now happens directly in downloaders
SCHEDULED_VIDEOS_DIR = os.path.join(OUTPUT_DIR, "scheduled_videos")
UPLOADED_VIDEOS_DIR = os.path.join(OUTPUT_DIR, "uploaded_videos") # For after upload, if used

# --- Data files (now in data/ directory) ---
EXCEL_FILE_PATH = os.path.join(DATA_DIR, "shorts_data.xlsx")
METADATA_METRICS_FILE = os.path.join(DATA_DIR, "metadata_metrics.json")
PERFORMANCE_METRICS_FILE = os.path.join(DATA_DIR, "performance_metrics.json")
API_QUOTA_FILE = os.path.join(DATA_DIR, "api_quota_usage.json") # Used by api_utils.py & analytics.py
CHANNEL_PROCESSED_IDS_CACHE = os.path.join(DATA_DIR, "channel_processed_ids_cache.json")
CHANNEL_LISTING_CACHE = os.path.join(DATA_DIR, "channel_listing_cache.json")
UPLOAD_CORRELATION_CACHE = os.path.join(DATA_DIR, "upload_correlation_cache.json")
# Removed AB_TEST_DATA_FILE as part of A/B testing removal
GENERATED_KEYWORDS_CACHE_FILE = os.path.join(DATA_DIR, "generated_keywords_cache.json")
PLAYLIST_DATA_CACHE_FILE = os.path.join(DATA_DIR, "playlists_data_cache.json")
TRENDING_TOPICS_CACHE_FILE = os.path.join(DATA_DIR, "trending_topics_cache.json") # Used by video_selector.py
VIDEO_SCORES_CACHE_FILE = os.path.join(DATA_DIR, "video_scores_cache.json") # Used by video_selector.py
HISTORICAL_PERFORMANCE_FILE = os.path.join(DATA_DIR, "historical_performance.json") # Used by video_selector.py and analytics.py
CONTENT_CALENDAR_DATA_FILE = os.path.join(DATA_DIR, "content_calendar_data.json") # Used by content_calendar.py

# --- Analytics data sub-directory (under data/) ---
ANALYTICS_DATA_DIR = os.path.join(DATA_DIR, "analytics_data") # For audience_insights, performance_history from analytics.py
ANALYTICS_API_CACHE_DIR = os.path.join(ANALYTICS_DATA_DIR, "api_cache") # For analytics.py API caching
ANALYTICS_REPORTS_DIR = os.path.join(ANALYTICS_DATA_DIR, "analytics_reports") # For HTML reports from analytics.py

# --- Driver files (now in drivers/ directory) ---
FFMPEG_PATH = os.path.join(DRIVERS_DIR, "ffmpeg.exe")
GECKODRIVER_PATH = os.path.join(DRIVERS_DIR, "geckodriver.exe") # Note: webdriver-manager usually handles this

# --- Log files (now in logs/ directory) ---
# General logs
ERROR_LOG_FILE = os.path.join(LOGS_DIR, "error_log.txt") # A general error log
EXCEL_UTILS_LOG_FILE = os.path.join(LOGS_DIR, "excel_utils.log")
UPLOADER_POM_LOG_FILE = os.path.join(LOGS_DIR, "uploader_pom.log")
CONTENT_CALENDAR_LOG_FILE = os.path.join(LOGS_DIR, "content_calendar.log")
ANALYTICS_LOG_FILE = os.path.join(LOGS_DIR, "analytics.log")
# Specific downloader/uploader logs
DOWNLOADER_KEYWORD_LOG_FILE = os.path.join(LOGS_DIR, "downloader_keyword_log.txt")
DOWNLOADER_CHANNEL_LOG_FILE = os.path.join(LOGS_DIR, "downloader_channel_log.txt")
UPLOADER_LOG_FILE = os.path.join(LOGS_DIR, "uploader_log.txt")
PERFORMANCE_TRACKER_LOG_FILE = os.path.join(LOGS_DIR, "performance_tracker_log.txt")
# Self-improvement/suggestion logs
TUNING_SUGGESTIONS_LOG_FILE = os.path.join(LOGS_DIR, "tuning_suggestions.log")
RUN_SUMMARIES_LOG_FILE = os.path.join(LOGS_DIR, "run_summaries.log")
SUGGESTED_CHANNELS_LOG_FILE = os.path.join(LOGS_DIR, "suggested_channels.log") # Changed from .txt
# Removed METADATA_OPTIMIZER_LOG_FILE as metadata optimization is now integrated into downloaders
VIDEO_SELECTOR_LOG_FILE = os.path.join(LOGS_DIR, "video_selector_log.txt") # For video_selector.py
# Removed AB_TESTING_LOG_FILE as part of A/B testing removal # For ab_testing.py

# --- Backup sub-directories (under backups/) ---
EXCEL_BACKUPS_DIR = os.path.join(BACKUPS_DIR, "excel")
JSON_BACKUPS_DIR = os.path.join(BACKUPS_DIR, "json_data")
PROMPT_BACKUPS_DIR = os.path.join(BACKUPS_DIR, "prompts")

# --- Other Output Folders (for debugging, etc.) ---
ERROR_SCREENSHOTS_DIR = os.path.join(OUTPUT_DIR, "error_screenshots") # From base_page.py
DEBUG_RECORDINGS_DIR = os.path.join(OUTPUT_DIR, "debug_recordings") # From uploader.py

# --- OAuth scopes (Unchanged) ---
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube" # For uploads and playlist management
]

# --- Excel sheet names (Unchanged) ---
DOWNLOADED_SHEET_NAME = "Downloaded"
UPLOADED_SHEET_NAME = "Uploaded"
DOWNLOADED_ARCHIVE_SHEET_NAME = "Downloaded_Archive"
UPLOADED_ARCHIVE_SHEET_NAME = "Uploaded_Archive"

# --- Excel column names (Unchanged) ---
COLUMN_VIDEO_INDEX = "Video Index"
COLUMN_OPTIMIZED_TITLE = "Optimized Title"
COLUMN_ORIGINAL_TITLE = "Original Title"
COLUMN_DOWNLOADED_DATE = "Downloaded Date"
COLUMN_VIEWS = "Views"
COLUMN_UPLOADER = "Uploader"
COLUMN_VIDEO_ID = "YouTube Video ID"
COLUMN_UPLOAD_TIMESTAMP = "Upload Timestamp"
COLUMN_SCHEDULED_TIME = "Scheduled Time"
COLUMN_PUBLISH_STATUS = "Publish Status"
COLUMN_VIEWS_YT = "Views (YT)"
COLUMN_LIKES_YT = "Likes (YT)"
COLUMN_COMMENTS_YT = "Comments (YT)"
COLUMN_LAST_UPDATED = "Last Updated"
# Removed COLUMN_TEST_GROUP and COLUMN_TEST_VARIANT as part of A/B testing removal

# --- YouTube limits (Unchanged, but good to have them here) ---
YOUTUBE_TITLE_LIMIT = 100 # Added based on youtube_limits.py
YOUTUBE_DESCRIPTION_LIMIT = 4950
YOUTUBE_TAG_LIMIT = 100
YOUTUBE_TOTAL_TAGS_LIMIT = 460 # From config and youtube_limits.py
YOUTUBE_MAX_TAGS_COUNT = 40

# --- yt-dlp settings (Unchanged) ---
YT_PLAYLIST_FETCH_LIMIT = 50
MAX_SHORT_DURATION = 61
# YT_SEARCH_RESULTS_PER_KEYWORD from config, not a global constant here typically

# --- Metadata settings (Unchanged) ---
MAX_ERROR_SAMPLES = 20 # Max error samples in metadata_metrics.json
# METADATA_ERROR_THRESHOLD from config
MAX_TAG_WORD_OCCURRENCES = 7
# MAX_TITLE_LENGTH from config or YOUTUBE_TITLE_LIMIT
# MAX_DESCRIPTION_LENGTH from config or YOUTUBE_DESCRIPTION_LIMIT
# MAX_TAGS_LENGTH from config or YOUTUBE_TOTAL_TAGS_LIMIT
# MAX_TAGS_COUNT from config or YOUTUBE_MAX_TAGS_COUNT

# --- Performance settings (Unchanged) ---
MIN_VIEWS_THRESHOLD = 1000
MIN_LIKES_THRESHOLD = 100
MIN_COMMENTS_THRESHOLD = 10

# --- Cache settings (Unchanged) ---
CACHE_EXPIRY_DAYS = 7
ANALYTICS_CACHE_EXPIRY_HOURS = 24 # Used by uploader.py for peak times

# --- Download settings (from config, not global constants here) ---
# MAX_DOWNLOADS_PER_CHANNEL
# MAX_DOWNLOADS_PER_RUN
MAX_DOWNLOAD_ATTEMPTS = 3

# --- Scoring settings (Unchanged) ---
VIEW_COUNT_WEIGHT = 0.5
LIKE_COUNT_WEIGHT = 0.3
COMMENT_COUNT_WEIGHT = 0.2
RECENCY_WEIGHT = 0.4
DIVERSITY_FACTOR = 0.2

# --- API settings (Unchanged) ---
API_RETRY_COUNT = 3
API_RETRY_DELAY = 1 # seconds
API_TIMEOUT = 60 # seconds
API_QUOTA_DAILY_LIMIT = 10000

# --- Retry configuration (Unchanged) ---
MAX_RETRIES = 3
RETRY_DELAY_BASE = 5 # seconds
RETRY_DELAY_MAX = 30 # seconds

# --- Logging settings (Unchanged) ---
# LOG_LEVEL typically configured in individual scripts or logging setup

# --- Template File Paths (relative to PACKAGE_ROOT/data as per FILE_STRUCTURE.md) ---
PACKAGE_DATA_DIR = os.path.join(PACKAGE_ROOT, "data")
CONFIG_TEMPLATE_FILE = os.path.join(PACKAGE_DATA_DIR, "config.txt.template")
CHANNELS_TEMPLATE_FILE = os.path.join(PACKAGE_DATA_DIR, "channels.txt.template")
NICHE_TEMPLATE_FILE = os.path.join(PACKAGE_DATA_DIR, "niche.txt.template")

# --- Original SCRIPT_DIR and UTILS_DIR (for potential use within utils if needed) ---
# This assumes constants.py remains in youtube_shorts/utils/
ORIGINAL_UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_SCRIPT_DIR = os.path.dirname(ORIGINAL_UTILS_DIR) # This would be .../Project GTA/youtube_shorts
