#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Utilities

This module provides functions for interacting with various APIs.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union, Callable

# --- NEW: Import constants from the new location ---
try:
    from . import constants
    CONSTANTS_IMPORTED = True
except ImportError:
    # Fallback if run as script or constants is higher up
    try:
        from .. import constants # If utils is a sub-package of youtube_shorts and constants is in youtube_shorts.utils
        CONSTANTS_IMPORTED = True
    except ImportError:
        try: # If constants is directly accessible in PYTHONPATH (less likely for direct project run)
            import constants
            CONSTANTS_IMPORTED = True
        except ImportError:
            CONSTANTS_IMPORTED = False
            print("CRITICAL: api_utils.py could not import constants.py. Path issues.")
            class MinimalConstants: # Fallback
                API_QUOTA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "api_quota_usage.json")
            constants = MinimalConstants()
            print("WARNING: api_utils.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__) # Use __name__ for module-specific logger
if not logger.handlers: # Avoid adding handlers multiple times if imported
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Try to import Google API libraries
try:
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    logger.warning("Google API libraries not found.")
    GOOGLE_API_AVAILABLE = False

# Import local modules
try:
    from .auth_utils import get_authenticated_service
    # from .cache_utils import load_cache, save_cache # Not used in this version but good to keep if planned
    from .config_utils import load_config, get_config_value # config_utils will handle path to config.txt
    AUTH_UTILS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Auth utils or Config utils module not available in api_utils: {e}")
    AUTH_UTILS_AVAILABLE = False # Set to False if any crucial import fails

# Constants (local to this module if not from constants.py)
DEFAULT_RETRY_COUNT = 3
DEFAULT_RETRY_DELAY = 1  # seconds

def get_youtube_service() -> Optional[Any]:
    """
    Get an authenticated YouTube API service.

    Returns:
        YouTube API service or None if authentication fails
    """
    if not AUTH_UTILS_AVAILABLE:
        logger.error("Auth utils module not available.")
        return None

    return get_authenticated_service(
        api_name="youtube",
        api_version="v3",
        log_prefix="[YouTube API] "
    )

def get_youtube_analytics_service() -> Optional[Any]:
    """
    Get an authenticated YouTube Analytics API service.

    Returns:
        YouTube Analytics API service or None if authentication fails
    """
    if not AUTH_UTILS_AVAILABLE:
        logger.error("Auth utils module not available.")
        return None

    return get_authenticated_service(
        api_name="youtubeAnalytics",
        api_version="v2",
        log_prefix="[YouTube Analytics API] "
    )

def api_request_with_retry(
    request_func: Callable,
    retry_count: int = DEFAULT_RETRY_COUNT,
    retry_delay: int = DEFAULT_RETRY_DELAY,
    handle_quota: bool = True
) -> Tuple[Optional[Any], Optional[str]]:
    """
    Execute an API request with retry logic and quota handling.

    Args:
        request_func: Function that makes the API request
        retry_count: Number of retries
        retry_delay: Delay between retries in seconds
        handle_quota: Whether to handle quota errors

    Returns:
        Tuple of (response or None, error message or None)
    """
    for attempt in range(retry_count):
        try:
            response = request_func()

            # Update quota usage if handling quota
            if handle_quota and GOOGLE_API_AVAILABLE:
                update_quota_usage(1)  # Assume 1 quota unit per request

            return response, None
        except HttpError as e:
            error_message = str(e)

            # Check for quota errors
            if handle_quota and GOOGLE_API_AVAILABLE and e.resp.status in [403, 429]:
                if "quota" in error_message.lower():
                    logger.error(f"API quota exceeded: {error_message}")
                    update_quota_usage(get_config_value("API_QUOTA_DAILY_LIMIT", 10000))  # Mark as quota exceeded
                    return None, f"API quota exceeded: {error_message}"

            # Check if we should retry
            if attempt < retry_count - 1:
                logger.warning(f"API request failed (attempt {attempt + 1}/{retry_count}): {error_message}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"API request failed after {retry_count} attempts: {error_message}")
                return None, error_message
        except Exception as e:
            error_message = str(e)
            logger.error(f"Unexpected error in API request: {error_message}")
            return None, error_message

    return None, "Maximum retry count exceeded"

def update_quota_usage(units: int) -> None:
    """
    Update the API quota usage tracking.

    Args:
        units: Number of quota units used
    """
    if not CONSTANTS_IMPORTED:
        logger.error("Constants not imported, cannot update quota usage file accurately.")
        return

    try:
        # Load current quota usage
        quota_data = {}
        if os.path.exists(constants.API_QUOTA_FILE):
            with open(constants.API_QUOTA_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if content: # Handle empty file case
                    quota_data = json.loads(content)

        # Get today's date as string
        today = datetime.now().strftime("%Y-%m-%d") # Changed from time.strftime for consistency

        # Initialize today's usage if not present
        if today not in quota_data:
            quota_data[today] = 0

        # Update usage
        quota_data[today] += units

        # Ensure DATA_DIR exists before trying to write
        os.makedirs(os.path.dirname(constants.API_QUOTA_FILE), exist_ok=True)

        # Save updated quota usage
        with open(constants.API_QUOTA_FILE, "w", encoding="utf-8") as f:
            json.dump(quota_data, f, indent=4)

        # Log if approaching limit
        daily_limit = 10000 # Default
        if AUTH_UTILS_AVAILABLE: # Check if config_utils was imported
            daily_limit = get_config_value("API_QUOTA_DAILY_LIMIT", 10000)

        if quota_data[today] > daily_limit * 0.8:
            logger.warning(f"API quota usage is high: {quota_data[today]}/{daily_limit} units ({quota_data[today]/daily_limit:.1%})")
    except Exception as e:
        logger.error(f"Error updating quota usage: {e}")

def get_video_statistics(video_id: str) -> Dict[str, Any]:
    """
    Get statistics for a YouTube video.

    Args:
        video_id: YouTube video ID

    Returns:
        Dict containing video statistics or empty dict if request fails
    """
    youtube = get_youtube_service()
    if not youtube:
        logger.error("Failed to get YouTube service")
        return {}

    # Create the request function
    def request_func():
        return youtube.videos().list(
            part="statistics,snippet",
            id=video_id
        ).execute()

    # Execute the request with retry
    response, error = api_request_with_retry(request_func)

    if error:
        logger.error(f"Error getting video statistics: {error}")
        return {}

    # Extract statistics
    if response and "items" in response and response["items"]:
        item = response["items"][0]
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})

        return {
            "video_id": video_id,
            "title": snippet.get("title", ""),
            "channel_title": snippet.get("channelTitle", ""),
            "published_at": snippet.get("publishedAt", ""),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "favorites": int(stats.get("favoriteCount", 0)),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    return {}

def get_channel_statistics(channel_id: str) -> Dict[str, Any]:
    """
    Get statistics for a YouTube channel.

    Args:
        channel_id: YouTube channel ID

    Returns:
        Dict containing channel statistics or empty dict if request fails
    """
    youtube = get_youtube_service()
    if not youtube:
        logger.error("Failed to get YouTube service")
        return {}

    # Create the request function
    def request_func():
        return youtube.channels().list(
            part="statistics,snippet",
            id=channel_id
        ).execute()

    # Execute the request with retry
    response, error = api_request_with_retry(request_func)

    if error:
        logger.error(f"Error getting channel statistics: {error}")
        return {}

    # Extract statistics
    if response and "items" in response and response["items"]:
        item = response["items"][0]
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})

        return {
            "channel_id": channel_id,
            "title": snippet.get("title", ""),
            "description": snippet.get("description", ""),
            "published_at": snippet.get("publishedAt", ""),
            "subscriber_count": int(stats.get("subscriberCount", 0)),
            "video_count": int(stats.get("videoCount", 0)),
            "view_count": int(stats.get("viewCount", 0)),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    return {}

def get_analytics_data(
    metrics: List[str],
    dimensions: Optional[List[str]] = None,
    start_date: str = "7daysAgo",
    end_date: str = "today",
    filters: Optional[str] = None,
    sort: Optional[str] = None,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Get analytics data from YouTube Analytics API.

    Args:
        metrics: List of metrics to retrieve
        dimensions: List of dimensions to group by
        start_date: Start date in YYYY-MM-DD format or relative date
        end_date: End date in YYYY-MM-DD format or relative date
        filters: Filters to apply
        sort: Sort order
        max_results: Maximum number of results

    Returns:
        List of dicts containing analytics data
    """
    analytics = get_youtube_analytics_service()
    if not analytics:
        logger.error("Failed to get YouTube Analytics service")
        return []

    # Create the request function
    def request_func():
        return analytics.reports().query(
            ids="channel==MINE",
            metrics=",".join(metrics),
            dimensions=",".join(dimensions) if dimensions else None,
            startDate=start_date,
            endDate=end_date,
            filters=filters,
            sort=sort,
            maxResults=max_results
        ).execute()

    # Execute the request with retry
    response, error = api_request_with_retry(request_func)

    if error:
        logger.error(f"Error getting analytics data: {error}")
        return []

    # Extract data
    if response and "rows" in response:
        # Get column headers
        headers = []
        if "columnHeaders" in response:
            headers = [h.get("name") for h in response["columnHeaders"]]

        # Convert rows to dicts
        result = []
        for row in response["rows"]:
            row_dict = {}
            for i, value in enumerate(row):
                if i < len(headers):
                    row_dict[headers[i]] = value
                else:
                    row_dict[f"value_{i}"] = value
            result.append(row_dict)

        return result

    return []
