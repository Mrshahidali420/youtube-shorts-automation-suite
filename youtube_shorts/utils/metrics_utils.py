#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metrics Utilities

This module provides functions for handling metadata and performance metrics.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# --- NEW: Import constants from the new location ---
try:
    from . import constants
    CONSTANTS_IMPORTED = True
except ImportError:
    try:
        # Try importing directly if run as a script
        import constants
        CONSTANTS_IMPORTED = True
    except ImportError:
        CONSTANTS_IMPORTED = False
        print("CRITICAL: metrics_utils.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            METADATA_METRICS_FILE = "data/metadata_metrics.json"
            PERFORMANCE_METRICS_FILE = "data/performance_metrics.json"
            LOGS_DIR = "logs"
        constants = MinimalConstants()
        print("WARNING: metrics_utils.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "metrics_utils.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
else:
    # Basic config if no handlers or constants not imported
    if not logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

# Constants for metrics keys
TOTAL_API_CALLS = "total_api_calls"
PARSE_FAILURES = "parse_failures"
TIMEOUTS = "timeouts"
EMPTY_TITLE_ERRORS = "empty_title_errors"
EMPTY_DESCRIPTION_ERRORS = "empty_description_errors"
EMPTY_TAGS_ERRORS = "empty_tags_errors"
VALIDATION_TITLE_MISMATCHES = "validation_title_mismatches"
VALIDATION_TAG_LIST_ERRORS = "validation_tag_list_errors"
VALIDATION_KEYWORD_STUFFING = "validation_keyword_stuffing"
LAST_RUN_DATE = "last_run_date"
ERROR_SAMPLES = "error_samples"
TOTAL_API_CALLS_PREVIOUS = "total_api_calls_previous"
TOTAL_ERRORS_PREVIOUS = "total_errors_previous"

def load_metadata_metrics(metrics_file_path: str) -> Dict[str, Any]:
    """
    Loads metadata generation metrics from the JSON file.

    Args:
        metrics_file_path: Path to the metrics file

    Returns:
        Dict[str, Any]: Metadata metrics dictionary
    """
    default_metrics = {
        TOTAL_API_CALLS: 0,
        PARSE_FAILURES: 0,
        TIMEOUTS: 0,
        EMPTY_TITLE_ERRORS: 0,
        EMPTY_DESCRIPTION_ERRORS: 0,
        EMPTY_TAGS_ERRORS: 0,
        VALIDATION_TITLE_MISMATCHES: 0,
        VALIDATION_TAG_LIST_ERRORS: 0,
        VALIDATION_KEYWORD_STUFFING: 0,
        LAST_RUN_DATE: datetime.now().isoformat(),
        ERROR_SAMPLES: [],
        TOTAL_API_CALLS_PREVIOUS: 0,
        TOTAL_ERRORS_PREVIOUS: 0
    }

    try:
        if os.path.exists(metrics_file_path):
            with open(metrics_file_path, "r", encoding="utf-8") as f:
                metrics = json.load(f)

            # Ensure all keys exist
            for key, value in default_metrics.items():
                metrics.setdefault(key, value)

            # Return a copy to prevent mutation of default values
            return metrics.copy()
        else:
            # If file doesn't exist, create a new file with default metrics
            logger.info(f"Metadata metrics file not found: {metrics_file_path}. Creating new file with default values.")
            try:
                os.makedirs(os.path.dirname(metrics_file_path), exist_ok=True)
                with open(metrics_file_path, "w", encoding="utf-8") as f:
                    json.dump(default_metrics, f, ensure_ascii=False, indent=4)
                logger.info(f"Created new metadata metrics file: {metrics_file_path}")
            except Exception as write_err:
                logger.error(f"Error creating new metadata metrics file: {write_err}")

            # Return a copy of the default dictionary
            return default_metrics.copy()
    except Exception as e:
        logger.warning(f"Error loading metadata metrics: {e}. Using default values.")
        # Return a copy of the default dictionary on error
        return default_metrics.copy()

def save_metadata_metrics(metrics: Dict[str, Any], metrics_file_path: str) -> bool:
    """
    Saves metadata generation metrics to the JSON file.

    Args:
        metrics: Metadata metrics dictionary
        metrics_file_path: Path to the metrics file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Update last run date
        metrics[LAST_RUN_DATE] = datetime.now().isoformat()

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(metrics_file_path), exist_ok=True)

        # Save metrics
        with open(metrics_file_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, ensure_ascii=False, indent=4)

        logger.info(f"Saved metadata metrics to: {metrics_file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving metadata metrics: {e}")
        return False

def add_error_sample(metrics: Dict[str, Any], error_type: str, error_details: str,
                    video_title: str, max_samples: int = 10) -> None:
    """
    Adds an error sample to the metadata metrics.

    Args:
        metrics: Metadata metrics dictionary
        error_type: Type of error
        error_details: Error details
        video_title: Title of the video
        max_samples: Maximum number of error samples to keep
    """
    if ERROR_SAMPLES not in metrics:
        metrics[ERROR_SAMPLES] = []

    # Add new error sample
    error_sample = {
        "type": error_type,
        "details": error_details,
        "video_title": video_title,
        "timestamp": datetime.now().isoformat()
    }

    # Add to beginning of list (most recent first)
    metrics[ERROR_SAMPLES].insert(0, error_sample)

    # Limit the number of samples
    if len(metrics[ERROR_SAMPLES]) > max_samples:
        metrics[ERROR_SAMPLES] = metrics[ERROR_SAMPLES][:max_samples]

def calculate_error_rates(metrics: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculates error rates from metadata metrics.

    Args:
        metrics: Metadata metrics dictionary

    Returns:
        Dict[str, float]: Dictionary of error rates
    """
    total_api_calls = metrics.get(TOTAL_API_CALLS, 0)
    if total_api_calls == 0:
        return {
            "parse_failure_rate": 0.0,
            "timeout_rate": 0.0,
            "empty_description_rate": 0.0,
            "empty_tags_rate": 0.0,
            "title_mismatch_rate": 0.0,
            "tag_list_error_rate": 0.0,
            "keyword_stuffing_rate": 0.0,
            "overall_error_rate": 0.0
        }

    # Calculate individual error rates
    parse_failure_rate = metrics.get(PARSE_FAILURES, 0) / total_api_calls
    timeout_rate = metrics.get(TIMEOUTS, 0) / total_api_calls
    empty_description_rate = metrics.get(EMPTY_DESCRIPTION_ERRORS, 0) / total_api_calls
    empty_tags_rate = metrics.get(EMPTY_TAGS_ERRORS, 0) / total_api_calls
    title_mismatch_rate = metrics.get(VALIDATION_TITLE_MISMATCHES, 0) / total_api_calls
    tag_list_error_rate = metrics.get(VALIDATION_TAG_LIST_ERRORS, 0) / total_api_calls
    keyword_stuffing_rate = metrics.get(VALIDATION_KEYWORD_STUFFING, 0) / total_api_calls

    # Calculate overall error rate
    total_errors = sum(metrics.get(err_type, 0) for err_type in [
        PARSE_FAILURES, TIMEOUTS, EMPTY_TITLE_ERRORS,
        EMPTY_DESCRIPTION_ERRORS, EMPTY_TAGS_ERRORS
    ])
    overall_error_rate = total_errors / total_api_calls

    return {
        "parse_failure_rate": parse_failure_rate,
        "timeout_rate": timeout_rate,
        "empty_description_rate": empty_description_rate,
        "empty_tags_rate": empty_tags_rate,
        "title_mismatch_rate": title_mismatch_rate,
        "tag_list_error_rate": tag_list_error_rate,
        "keyword_stuffing_rate": keyword_stuffing_rate,
        "overall_error_rate": overall_error_rate
    }

# Performance metrics constants
TOTAL_UPLOADS = "total_uploads"
SUCCESSFUL_UPLOADS = "successful_uploads"
FAILED_UPLOADS = "failed_uploads"
SUCCESS_RATE = "success_rate"
AVERAGE_VIEWS = "average_views"
AVERAGE_LIKES = "average_likes"
AVERAGE_COMMENTS = "average_comments"
TOP_PERFORMING_VIDEOS = "top_performing_videos"
ERROR_COUNTS = "error_counts"

def load_performance_metrics(metrics_file_path: str) -> Dict[str, Any]:
    """
    Loads performance metrics from the JSON file.

    Args:
        metrics_file_path: Path to the metrics file

    Returns:
        Dict[str, Any]: Performance metrics dictionary
    """
    default_metrics = {
        TOTAL_UPLOADS: 0,
        SUCCESSFUL_UPLOADS: 0,
        FAILED_UPLOADS: 0,
        SUCCESS_RATE: 0.0,
        AVERAGE_VIEWS: 0,
        AVERAGE_LIKES: 0,
        AVERAGE_COMMENTS: 0,
        TOP_PERFORMING_VIDEOS: [],
        ERROR_COUNTS: {},
        LAST_RUN_DATE: datetime.now().isoformat()
    }

    try:
        if os.path.exists(metrics_file_path):
            with open(metrics_file_path, "r", encoding="utf-8") as f:
                metrics = json.load(f)

            # Ensure all keys exist
            for key, value in default_metrics.items():
                metrics.setdefault(key, value)

            # Return a copy to prevent mutation of default values
            return metrics.copy()
        else:
            # If file doesn't exist, create a new file with default metrics
            logger.info(f"Performance metrics file not found: {metrics_file_path}. Creating new file with default values.")
            try:
                os.makedirs(os.path.dirname(metrics_file_path), exist_ok=True)
                with open(metrics_file_path, "w", encoding="utf-8") as f:
                    json.dump(default_metrics, f, ensure_ascii=False, indent=4)
                logger.info(f"Created new performance metrics file: {metrics_file_path}")
            except Exception as write_err:
                logger.error(f"Error creating new performance metrics file: {write_err}")

            # Return a copy of the default dictionary
            return default_metrics.copy()
    except Exception as e:
        logger.warning(f"Error loading performance metrics: {e}. Using default values.")
        # Return a copy of the default dictionary on error
        return default_metrics.copy()

def save_performance_metrics(metrics: Dict[str, Any], metrics_file_path: str) -> bool:
    """
    Saves performance metrics to the JSON file.

    Args:
        metrics: Performance metrics dictionary
        metrics_file_path: Path to the metrics file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Update last run date
        metrics[LAST_RUN_DATE] = datetime.now().isoformat()

        # Calculate success rate
        if metrics.get(TOTAL_UPLOADS, 0) > 0:
            metrics[SUCCESS_RATE] = metrics.get(SUCCESSFUL_UPLOADS, 0) / metrics.get(TOTAL_UPLOADS, 1)
        else:
            metrics[SUCCESS_RATE] = 0.0

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(metrics_file_path), exist_ok=True)

        # Save metrics
        with open(metrics_file_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, ensure_ascii=False, indent=4)

        logger.info(f"Saved performance metrics to: {metrics_file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving performance metrics: {e}")
        return False

def update_upload_metrics(metrics: Dict[str, Any], success: bool,
                         error_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Updates upload metrics with a new upload attempt.

    Args:
        metrics: Performance metrics dictionary
        success: Whether the upload was successful
        error_type: Type of error if upload failed

    Returns:
        Dict[str, Any]: Updated metrics dictionary
    """
    # Increment total uploads
    metrics[TOTAL_UPLOADS] = metrics.get(TOTAL_UPLOADS, 0) + 1

    if success:
        # Increment successful uploads
        metrics[SUCCESSFUL_UPLOADS] = metrics.get(SUCCESSFUL_UPLOADS, 0) + 1
    else:
        # Increment failed uploads
        metrics[FAILED_UPLOADS] = metrics.get(FAILED_UPLOADS, 0) + 1

        # Update error counts if error type is provided
        if error_type:
            error_counts = metrics.get(ERROR_COUNTS, {})
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
            metrics[ERROR_COUNTS] = error_counts

    # Calculate success rate
    if metrics[TOTAL_UPLOADS] > 0:
        metrics[SUCCESS_RATE] = metrics[SUCCESSFUL_UPLOADS] / metrics[TOTAL_UPLOADS]

    return metrics

def update_video_performance(metrics: Dict[str, Any], video_id: str, title: str,
                            views: int, likes: int, comments: int,
                            upload_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Updates video performance metrics.

    Args:
        metrics: Performance metrics dictionary
        video_id: YouTube video ID
        title: Video title
        views: View count
        likes: Like count
        comments: Comment count
        upload_date: Upload date (ISO format)

    Returns:
        Dict[str, Any]: Updated metrics dictionary
    """
    # Update average metrics if there are successful uploads
    successful_uploads = metrics.get(SUCCESSFUL_UPLOADS, 0)
    if successful_uploads > 0:
        # Calculate new averages
        current_avg_views = metrics.get(AVERAGE_VIEWS, 0)
        current_avg_likes = metrics.get(AVERAGE_LIKES, 0)
        current_avg_comments = metrics.get(AVERAGE_COMMENTS, 0)

        # Update with exponential moving average (more weight to recent videos)
        alpha = 0.3  # Weight for new data
        metrics[AVERAGE_VIEWS] = (1 - alpha) * current_avg_views + alpha * views
        metrics[AVERAGE_LIKES] = (1 - alpha) * current_avg_likes + alpha * likes
        metrics[AVERAGE_COMMENTS] = (1 - alpha) * current_avg_comments + alpha * comments

    # Update top performing videos
    top_videos = metrics.get(TOP_PERFORMING_VIDEOS, [])

    # Check if video already exists in top videos
    existing_index = None
    for i, video in enumerate(top_videos):
        if video.get("video_id") == video_id:
            existing_index = i
            break

    # Create video entry
    video_entry = {
        "video_id": video_id,
        "title": title,
        "views": views,
        "likes": likes,
        "comments": comments,
        "upload_date": upload_date or datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat()
    }

    # Update or add video
    if existing_index is not None:
        top_videos[existing_index] = video_entry
    else:
        top_videos.append(video_entry)

    # Sort by views in descending order
    top_videos.sort(key=lambda x: x.get("views", 0), reverse=True)

    # Keep only top 10
    metrics[TOP_PERFORMING_VIDEOS] = top_videos[:10]

    return metrics
