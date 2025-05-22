#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Utilities

This module provides functions for loading and managing configuration.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List, Union

# --- NEW: Import constants ---
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
        print("CRITICAL: config_utils.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            CONFIG_FILE_PATH = "config/config.txt"
            LOGS_DIR = "logs"
        constants = MinimalConstants()
        print("WARNING: config_utils.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "config_utils.log")
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

# Default configuration values
DEFAULT_CONFIG = {
    # API Keys
    "API_KEY": "",
    "GEMINI_API_KEY": "",

    # Download and Upload Limits
    "MAX_DOWNLOADS": 24,
    "MAX_UPLOADS": 24,
    "MAX_KEYWORDS": 200,

    # Upload Settings
    "UPLOAD_CATEGORY": "Gaming",

    # Scheduling Settings
    "SCHEDULING_MODE": "analytics_priority",
    "SCHEDULE_INTERVAL_MINUTES": 120,
    "CUSTOM_SCHEDULE_TIMES": "6:00 AM, 9:00 AM, 11:30 AM, 3:00 PM, 6:00 PM, 10:00 PM",
    "MIN_SCHEDULE_AHEAD_MINUTES": 20,

    # Analytics-Based Scheduling Settings
    "ANALYTICS_DAYS_TO_ANALYZE": 7,
    "ANALYTICS_PEAK_HOURS_COUNT": 5,
    "ANALYTICS_CACHE_EXPIRY_HOURS": 24,

    # Browser Profile
    "PROFILE_PATH": "",

    # YouTube Limits
    "YOUTUBE_DESCRIPTION_LIMIT": 4950,
    "YOUTUBE_TAG_LIMIT": 100,
    "YOUTUBE_TOTAL_TAGS_LIMIT": 450,
    "YOUTUBE_MAX_TAGS_COUNT": 40,

    # Debug Recording Settings
    "ENABLE_DEBUG_RECORDING": False,
    "FFMPEG_PATH": "",

    # Excel Archiving Settings
    "EXCEL_ARCHIVE_DAYS": 180,

    # Retry Settings
    "MAX_RETRIES": 3,
    "RETRY_DELAY_BASE": 5,
    "RETRY_DELAY_MAX": 30,

    # Scoring Settings
    "WEIGHT_VIEWS": 0.3,
    "WEIGHT_ENGAGEMENT": 0.3,
    "WEIGHT_TRENDING": 0.2,
    "WEIGHT_HISTORICAL": 0.2,
    "DIVERSITY_FACTOR": 0.2
}

def load_config(config_file_arg: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from config.txt file.

    Args:
        config_file_arg: Path to the configuration file

    Returns:
        Dict containing configuration values
    """
    actual_config_path = config_file_arg or (constants.CONFIG_FILE_PATH if CONSTANTS_IMPORTED else "config/config.txt")
    config = DEFAULT_CONFIG.copy()

    try:
        if os.path.exists(actual_config_path):
            with open(actual_config_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()

                        # Convert value to appropriate type
                        if key in config and isinstance(config[key], bool):
                            config[key] = value.lower() in ("true", "yes", "1", "t", "y")
                        elif key in config and isinstance(config[key], int):
                            try:
                                config[key] = int(value)
                            except ValueError:
                                logger.warning(f"Could not convert {key}={value} to int. Using default: {config[key]}")
                        elif key in config and isinstance(config[key], float):
                            try:
                                config[key] = float(value)
                            except ValueError:
                                logger.warning(f"Could not convert {key}={value} to float. Using default: {config[key]}")
                        else:
                            config[key] = value

            logger.info(f"Loaded configuration from {actual_config_path}")
        else:
            logger.warning(f"Configuration file not found at {actual_config_path}. Using default values.")
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        logger.warning("Using default configuration values.")

    return config

def save_config(config: Dict[str, Any], config_file_arg: Optional[str] = None) -> bool:
    """
    Save configuration to config.txt file.

    Args:
        config: Dict containing configuration values
        config_file_arg: Path to the configuration file

    Returns:
        bool: True if save was successful, False otherwise
    """
    actual_config_path = config_file_arg or (constants.CONFIG_FILE_PATH if CONSTANTS_IMPORTED else "config/config.txt")

    try:
        # Ensure config directory exists before writing
        os.makedirs(os.path.dirname(actual_config_path), exist_ok=True)

        with open(actual_config_path, "w", encoding="utf-8") as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")

        logger.info(f"Configuration saved to {actual_config_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return False

def get_config_value(key: str, default: Any = None, config: Optional[Dict[str, Any]] = None) -> Any:
    """
    Get a configuration value with fallback to default.

    Args:
        key: Configuration key
        default: Default value if key is not found
        config: Configuration dict (if None, will load from file)

    Returns:
        Configuration value or default
    """
    if config is None:
        config = load_config()

    return config.get(key, default)

def set_config_value(key: str, value: Any, save: bool = True, config_file_arg: Optional[str] = None) -> bool:
    """
    Set a configuration value and optionally save to file.

    Args:
        key: Configuration key
        value: Configuration value
        save: Whether to save to file
        config_file_arg: Path to the configuration file

    Returns:
        bool: True if operation was successful, False otherwise
    """
    config = load_config(config_file_arg)
    config[key] = value

    if save:
        return save_config(config, config_file_arg)

    return True
