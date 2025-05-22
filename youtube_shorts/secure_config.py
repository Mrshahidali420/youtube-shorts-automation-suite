#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secure Configuration Loader

This module provides a secure way to load configuration settings from config.txt
or environment variables, with a focus on protecting sensitive information like API keys.
"""

import os
import sys
import re
from typing import Dict, Any, Optional
import logging

# --- NEW: Import constants from the new location ---
try:
    # Assuming secure_config.py is in youtube_shorts/
    # and constants.py is in youtube_shorts/utils/
    from .utils import constants
    CONSTANTS_IMPORTED = True
except ImportError:
    try:
        from utils import constants # Fallback if utils is directly in PYTHONPATH
        CONSTANTS_IMPORTED = True
    except ImportError:
        try:
            from youtube_shorts.utils import constants
            CONSTANTS_IMPORTED = True
        except ImportError:
            CONSTANTS_IMPORTED = False
            print("CRITICAL: secure_config.py could not import constants.py. Path issues.")
            class MinimalConstants: # Fallback
                CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "config.txt")
                CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
                # Assuming secure_config.py is in youtube_shorts/, so package_data/ is in youtube_shorts/data/
                PACKAGE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
                CONFIG_TEMPLATE_FILE = os.path.join(PACKAGE_DATA_DIR, "config.txt.template") # Path as per new structure for template
            constants = MinimalConstants()
            print("WARNING: secure_config.py using minimal fallback constants.")
# --- End NEW Import ---

# Set up logging
# This basicConfig will be used if the script is run directly.
# If imported, the importing script's logger config usually takes precedence.
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Constants (local to this module)
ENV_PREFIX = "YT_SHORTS_"  # Prefix for environment variables

def load_config(config_path: Optional[str] = None) -> Dict[str, str]:
    """
    Load configuration from config.txt file or environment variables.

    Args:
        config_path: Optional path to config file. If None, uses default from constants.

    Returns:
        Dictionary containing configuration settings
    """
    # Determine config file path
    if config_path is None:
        # --- UPDATED ---
        config_path = constants.CONFIG_FILE_PATH if CONSTANTS_IMPORTED else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "config.txt")

    config = {}

    # First try to load from config file
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Error reading configuration file '{config_path}': {e}")
    else:
        logger.warning(f"Configuration file not found at {config_path}")

    # Then override with environment variables if they exist
    for env_var, env_value in os.environ.items():
        if env_var.startswith(ENV_PREFIX):
            config_key = env_var[len(ENV_PREFIX):]  # Remove prefix
            config[config_key] = env_value
            # Don't log actual values of sensitive keys
            if is_sensitive_key(config_key):
                logger.info(f"Overriding {config_key} from environment variable")
            else:
                logger.info(f"Overriding {config_key} with value from environment variable")

    validate_config(config)

    return config

def is_sensitive_key(key: str) -> bool:
    """
    Check if a configuration key is considered sensitive (like API keys).

    Args:
        key: Configuration key to check

    Returns:
        True if the key is sensitive, False otherwise
    """
    sensitive_patterns = [
        r".*api.*key.*", r".*gemini.*key.*", # More specific for gemini
        r".*secret.*", r".*password.*", r".*token.*", r".*credential.*"
    ]

    key_lower = key.lower()
    return any(re.match(pattern, key_lower) for pattern in sensitive_patterns)

def get_config_value(config: Dict[str, str], key: str, default: Any = None) -> Any:
    """
    Get a configuration value, with optional default.

    Args:
        config: Configuration dictionary
        key: Key to look up
        default: Default value if key is not found

    Returns:
        Configuration value or default
    """
    return config.get(key, default)

def validate_config(config: Dict[str, str]) -> None:
    """
    Validate that required configuration keys are present.

    Args:
        config: Configuration dictionary to validate
    """
    # API_KEY or GEMINI_API_KEY should be present
    api_key_present = config.get("API_KEY") or config.get("GEMINI_API_KEY")
    missing_keys = []
    if not api_key_present:
        missing_keys.append("API_KEY (or GEMINI_API_KEY)")

    if missing_keys:
        logger.warning(f"Missing required configuration keys: {', '.join(missing_keys)}")
        config_path = constants.CONFIG_FILE_PATH if CONSTANTS_IMPORTED else "config/config.txt"
        logger.warning(f"Please add these keys to '{config_path}' or set them as environment variables.")
        logger.warning(f"Environment variables should be prefixed with {ENV_PREFIX}")
        logger.warning(f"Example: {ENV_PREFIX}API_KEY=your_api_key_here OR {ENV_PREFIX}GEMINI_API_KEY=your_api_key_here")

def create_example_config(output_path: Optional[str] = None) -> None:
    """
    Create an example configuration file with placeholders.

    Args:
        output_path: Path where to save the example config. If None, uses default from constants.
    """
    if output_path is None:
        # --- UPDATED ---
        # Default output is config.example.txt in the config/ directory defined by constants
        config_dir = constants.CONFIG_DIR if CONSTANTS_IMPORTED else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
        os.makedirs(config_dir, exist_ok=True) # Ensure config directory exists
        output_path = os.path.join(config_dir, "config.example.txt")

    # --- UPDATED ---
    # Template path from constants (pointing to youtube_shorts/data/config.txt.template)
    template_path = constants.CONFIG_TEMPLATE_FILE if CONSTANTS_IMPORTED else os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "config.txt.template")

    if os.path.exists(template_path):
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()

            # Ensure output directory exists before writing
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(template_content)

            logger.info(f"Example configuration created at {output_path}")
        except Exception as e:
            logger.error(f"Error creating example configuration: {e}")
    else:
        logger.error(f"Template file not found at {template_path}")

if __name__ == "__main__":
    # If run directly, create an example config file in the new config/ directory
    create_example_config() # Uses constants.CONFIG_DIR internally now for default output

    # Test loading config (will look for config/config.txt by default)
    config_loaded = load_config()
    print("\nConfiguration loaded:")
    for key, value in config_loaded.items():
        if is_sensitive_key(key):
            print(f"{key}=********")
        else:
            print(f"{key}={value}")
