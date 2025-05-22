#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cache Utilities

This module provides functions for handling cache files.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0
"""

import os
import json
import shutil
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union

# --- NEW: Import constants from the new location ---
try:
    from . import constants # Assumes cache_utils.py is in utils/
    CONSTANTS_IMPORTED = True
except ImportError:
    try:
        # Try importing directly if run as a script
        import constants
        CONSTANTS_IMPORTED = True
    except ImportError:
        CONSTANTS_IMPORTED = False
        print("CRITICAL: cache_utils.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            BACKUPS_DIR = "backups" # Very basic fallback
            JSON_BACKUPS_DIR = os.path.join(BACKUPS_DIR, "json_data")
        constants = MinimalConstants()
        print("WARNING: cache_utils.py using minimal fallback constants.")
# --- End NEW Import ---

# Import local modules
from .date_utils import parse_date, is_older_than_days

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles non-serializable objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)  # Convert to string as a last resort

def load_cache(cache_file_path: str, cache_name: str = "Cache",
              default_value: Any = None) -> Any:
    """
    Loads a cache from a JSON file.

    Args:
        cache_file_path: Path to the cache file
        cache_name: Name of the cache (for logging)
        default_value: Default value to return if cache file doesn't exist or is invalid

    Returns:
        Any: Cache data or default value
    """
    # Use empty dict with timestamp if default_value is None
    if default_value is None:
        default_value = {"timestamp": datetime.now().isoformat()}

    try:
        if os.path.exists(cache_file_path):
            with open(cache_file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if not content:
                    logger.info(f"{cache_name} file exists but is empty. Initializing new cache.")
                    return default_value

                cache = json.loads(content)

                # Validate cache format if default_value is a dict or list
                if isinstance(default_value, dict) and not isinstance(cache, dict):
                    logger.warning(f"{cache_name} file has invalid format (expected dict). Initializing new cache.")
                    return default_value
                elif isinstance(default_value, list) and not isinstance(cache, list):
                    logger.warning(f"{cache_name} file has invalid format (expected list). Initializing new cache.")
                    return default_value

                return cache
        else:
            logger.info(f"{cache_name} file not found. Creating new cache.")
            return default_value
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {cache_name} file. Initializing new cache.")
        return default_value
    except Exception as e:
        logger.error(f"Error loading {cache_name}: {e}")
        return default_value

def save_cache(cache_data: Any, cache_file_path: str, cache_name: str = "Cache") -> bool:
    """
    Saves cache data to a JSON file.

    Args:
        cache_data: Cache data to save
        cache_file_path: Path to the cache file
        cache_name: Name of the cache (for logging)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        # Create backup of existing file if it exists
        if os.path.exists(cache_file_path):
            backup_path = f"{cache_file_path}.bak"
            try:
                shutil.copy2(cache_file_path, backup_path)
                logger.info(f"Created backup of {cache_name} at: {backup_path}")
            except Exception as e:
                logger.warning(f"Could not create backup of {cache_name}: {e}")

        # Save the file
        with open(cache_file_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=4, cls=CustomJSONEncoder)

        # Log success message
        if isinstance(cache_data, dict) and "timestamp" in cache_data:
            logger.info(f"Saved {cache_name} with {len(cache_data) - 1} entries.")
        elif isinstance(cache_data, list):
            logger.info(f"Saved {cache_name} with {len(cache_data)} entries.")
        else:
            logger.info(f"Saved {cache_name}.")

        return True
    except (IOError, PermissionError) as e:
        logger.error(f"Failed to save {cache_name} due to file access error: {e}")
        return False
    except TypeError as e:
        logger.error(f"JSON serialization error: {e}. Data might contain unserializable objects.")
        return False
    except Exception as e:
        logger.error(f"Error saving {cache_name}: {e}")
        return False

def cleanup_correlation_cache(cache_file_path: str, days_to_keep: int = 7) -> bool:
    """
    Removes entries older than specified days from the correlation cache.

    Args:
        cache_file_path: Path to the correlation cache file
        days_to_keep: Number of days to keep entries for

    Returns:
        bool: True if successful, False otherwise
    """
    # Load the cache
    cache = load_cache(cache_file_path, "Correlation Cache", default_value=[])
    if not cache:
        logger.info("No correlation cache to cleanup.")
        return True  # Nothing to cleanup

    now = datetime.now()
    cutoff_date = now - timedelta(days=days_to_keep)
    original_count = len(cache)
    cleaned_cache = []
    removed_count = 0
    invalid_count = 0

    for entry in cache:
        try:
            timestamp_str = entry.get("added_timestamp")
            if not timestamp_str:
                logger.warning(f"Missing timestamp in correlation cache entry: {entry.get('video_index', 'Unknown')}. Keeping entry.")
                cleaned_cache.append(entry)
                invalid_count += 1
                continue

            # Use robust date parsing
            added_time = parse_date(timestamp_str)

            # If we couldn't parse the date, keep the entry
            if added_time is None:
                logger.warning(f"Could not parse timestamp '{timestamp_str}' in correlation cache entry: {entry.get('video_index', 'Unknown')}. Keeping entry.")
                cleaned_cache.append(entry)
                invalid_count += 1
                continue

            # Check if the entry is newer than the cutoff date
            if added_time >= cutoff_date:
                cleaned_cache.append(entry)
            else:
                removed_count += 1

        except Exception as e:
            # Keep entries that cause errors
            logger.warning(f"Error processing cache entry: {e}")
            cleaned_cache.append(entry)
            invalid_count += 1

    if removed_count > 0:
        success = save_cache(cleaned_cache, cache_file_path, "Correlation Cache")
        if success:
            logger.info(f"Cleaned correlation cache: removed {removed_count} of {original_count} entries older than {days_to_keep} days.")
        else:
            logger.error("Failed to save cleaned correlation cache.")
            return False
    else:
        logger.info(f"No old entries to remove from correlation cache (keeping all {original_count} entries).")

    if invalid_count > 0:
        logger.warning(f"Found {invalid_count} entries with invalid or missing timestamps in correlation cache.")

    return True

def is_cache_valid(cache_file_path: str, max_age_days: int = 7) -> bool:
    """
    Check if a cache file is valid and not expired.

    Args:
        cache_file_path: Path to the cache file
        max_age_days: Maximum age of the cache in days

    Returns:
        bool: True if cache is valid and not expired, False otherwise
    """
    try:
        if not os.path.exists(cache_file_path):
            logger.debug(f"Cache file not found: {cache_file_path}")
            return False

        # Check if file is empty
        if os.path.getsize(cache_file_path) == 0:
            logger.debug(f"Cache file is empty: {cache_file_path}")
            return False

        # Check if file is too old
        file_age_days = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file_path))).days
        if file_age_days > max_age_days:
            logger.debug(f"Cache file expired ({file_age_days} days old): {cache_file_path}")
            return False

        # Try to load the file to verify it's valid JSON
        try:
            with open(cache_file_path, "r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError:
            logger.debug(f"Cache file contains invalid JSON: {cache_file_path}")
            return False

        return True
    except Exception as e:
        logger.warning(f"Error checking cache validity: {e}")
        return False

def get_cache_age_days(cache_file_path: str) -> Optional[int]:
    """
    Get the age of a cache file in days.

    Args:
        cache_file_path: Path to the cache file

    Returns:
        int: Age of the cache in days or None if file doesn't exist
    """
    try:
        if not os.path.exists(cache_file_path):
            return None

        file_age_days = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file_path))).days
        return file_age_days
    except Exception as e:
        logger.warning(f"Error getting cache age: {e}")
        return None

def clear_cache(cache_file_path: str, cache_name: str = "Cache") -> bool:
    """
    Clear a cache file.

    Args:
        cache_file_path: Path to the cache file
        cache_name: Name of the cache (for logging)

    Returns:
        bool: True if clear was successful, False otherwise
    """
    try:
        if os.path.exists(cache_file_path):
            # Create backup before deleting
            backup_path = f"{cache_file_path}.bak"
            try:
                shutil.copy2(cache_file_path, backup_path)
                logger.info(f"Created backup of {cache_name} at: {backup_path}")
            except Exception as e:
                logger.warning(f"Could not create backup of {cache_name}: {e}")

            # Delete the file
            os.remove(cache_file_path)
            logger.info(f"Cleared {cache_name} file: {cache_file_path}")
        else:
            logger.info(f"{cache_name} file not found: {cache_file_path}")

        return True
    except Exception as e:
        logger.error(f"Error clearing {cache_name} file: {e}")
        return False
