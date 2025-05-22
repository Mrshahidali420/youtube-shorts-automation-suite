#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date Utilities

This module provides robust date parsing and handling functions.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0
"""

import re
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Union, List, Tuple

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
        print("CRITICAL: date_utils.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            LOGS_DIR = "logs"
        constants = MinimalConstants()
        print("WARNING: date_utils.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "date_utils.log")
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

# Try to import optional dependencies
try:
    from dateutil import parser as date_parser
    DATEUTIL_AVAILABLE = True
except ImportError:
    DATEUTIL_AVAILABLE = False
    logger.warning("dateutil not available. Date parsing will use basic methods.")

def parse_date(date_str: Union[str, None]) -> Optional[datetime]:
    """
    Parse a date string into a datetime object using multiple methods.

    Args:
        date_str: Date string to parse

    Returns:
        Optional[datetime]: Parsed datetime or None if parsing failed
    """
    if not date_str or not isinstance(date_str, str):
        return None

    # Remove any timezone info for consistency
    date_str = date_str.split('+')[0].split('Z')[0].strip()

    # Try dateutil parser if available (handles many formats)
    if DATEUTIL_AVAILABLE:
        try:
            return date_parser.parse(date_str)
        except Exception:
            pass

    # Try common formats
    formats = [
        "%Y-%m-%dT%H:%M:%S",  # ISO format
        "%Y-%m-%dT%H:%M:%S.%f",  # ISO format with microseconds
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%b %d, %Y",
        "%d %b %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # Try to handle Excel date numbers
    try:
        if date_str.replace('.', '', 1).isdigit():
            # Could be an Excel date number (days since 1899-12-30)
            excel_date = float(date_str)
            if excel_date > 60:  # Account for Excel's leap year bug
                excel_date -= 1
            delta = timedelta(days=excel_date)
            return datetime(1899, 12, 30) + delta
    except Exception:
        pass

    logger.warning(f"Could not parse date: {date_str}")
    return None

def format_date(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object as a string.

    Args:
        dt: Datetime object to format
        format_str: Format string to use

    Returns:
        str: Formatted date string or empty string if dt is None
    """
    if dt is None:
        return ""

    try:
        return dt.strftime(format_str)
    except Exception as e:
        logger.warning(f"Error formatting date: {e}")
        return ""

def get_days_ago(days: int) -> datetime:
    """
    Get a datetime object for a specified number of days ago.

    Args:
        days: Number of days ago

    Returns:
        datetime: Datetime object for the specified number of days ago
    """
    return datetime.now() - timedelta(days=days)

def is_older_than_days(dt: Optional[datetime], days: int) -> bool:
    """
    Check if a datetime is older than a specified number of days.

    Args:
        dt: Datetime object to check
        days: Number of days

    Returns:
        bool: True if the datetime is older than the specified number of days, False otherwise
    """
    if dt is None:
        return False

    cutoff_date = get_days_ago(days)
    return dt < cutoff_date

def get_relative_date(days: int) -> str:
    """
    Get a date relative to today.

    Args:
        days: Number of days to add (negative for past)

    Returns:
        Date string in YYYY-MM-DD format
    """
    dt = datetime.now() + timedelta(days=days)
    return dt.strftime("%Y-%m-%d")

def parse_time_of_day(time_str: str) -> Optional[Tuple[int, int]]:
    """
    Parse a time string into hours and minutes.

    Args:
        time_str: Time string (e.g., "3:30 PM", "15:30")

    Returns:
        Tuple of (hour, minute) or None if parsing fails
    """
    if not time_str:
        return None

    # Try 12-hour format with AM/PM
    match = re.match(r'(\d{1,2}):(\d{2})\s*(AM|PM)', time_str.upper())
    if match:
        hour, minute, period = match.groups()
        hour = int(hour)
        minute = int(minute)

        # Convert to 24-hour format
        if period == "PM" and hour < 12:
            hour += 12
        elif period == "AM" and hour == 12:
            hour = 0

        return (hour, minute)

    # Try 24-hour format
    match = re.match(r'(\d{1,2}):(\d{2})', time_str)
    if match:
        hour, minute = match.groups()
        return (int(hour), int(minute))

    logger.warning(f"Failed to parse time: {time_str}")
    return None

def is_same_day(dt1: Optional[datetime], dt2: Optional[datetime]) -> bool:
    """
    Check if two datetime objects represent the same day.

    Args:
        dt1: First datetime object
        dt2: Second datetime object

    Returns:
        True if both dates are on the same day, False otherwise
    """
    if dt1 is None or dt2 is None:
        return False

    return (dt1.year == dt2.year and dt1.month == dt2.month and dt1.day == dt2.day)

def days_between(dt1: Optional[datetime], dt2: Optional[datetime]) -> Optional[int]:
    """
    Calculate the number of days between two dates.

    Args:
        dt1: First datetime object
        dt2: Second datetime object

    Returns:
        Number of days between dates or None if either date is None
    """
    if dt1 is None or dt2 is None:
        return None

    delta = dt2.date() - dt1.date()
    return delta.days

def parse_youtube_timestamp(timestamp: str) -> Optional[datetime]:
    """
    Parse a YouTube timestamp (ISO 8601 format).

    Args:
        timestamp: YouTube timestamp string

    Returns:
        datetime object or None if parsing fails
    """
    if not timestamp:
        return None

    try:
        # YouTube timestamps are in ISO 8601 format
        if 'Z' in timestamp:
            # Remove the 'Z' and parse
            timestamp = timestamp.replace('Z', '+00:00')

        if DATEUTIL_AVAILABLE:
            return date_parser.parse(timestamp)
        else:
            # Try to parse with strptime
            formats = [
                "%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S"
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(timestamp, fmt)
                except ValueError:
                    continue

            logger.warning(f"Failed to parse YouTube timestamp: {timestamp}")
            return None
    except Exception as e:
        logger.error(f"Error parsing YouTube timestamp '{timestamp}': {e}")
        return None
