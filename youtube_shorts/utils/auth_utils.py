#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authentication Utilities

This module provides functions for authenticating with various APIs.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0
"""

import os
import pickle
import logging
from typing import Optional, List, Dict, Any, Tuple

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
        print("CRITICAL: auth_utils.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            CLIENT_SECRETS_FILE = "data/client_secret.json"
            TOKEN_FILE = "data/token.json"
            CONFIG_FILE_PATH = "config/config.txt"
            LOGS_DIR = "logs"
            SCOPES = [
                "https://www.googleapis.com/auth/youtube.readonly",
                "https://www.googleapis.com/auth/yt-analytics.readonly",
                "https://www.googleapis.com/auth/youtube"
            ]
        constants = MinimalConstants()
        print("WARNING: auth_utils.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "auth_utils.log")
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

# Try to import Google API libraries
try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    logger.warning("Google API libraries not found. Install with:")
    logger.warning("pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    GOOGLE_API_AVAILABLE = False

# Try to import Gemini API
try:
    import google.generativeai as genai
    GEMINI_API_AVAILABLE = True
except ImportError:
    logger.warning("Google Generative AI library not found. Install with:")
    logger.warning("pip install google-generativeai")
    GEMINI_API_AVAILABLE = False

def load_config() -> Dict[str, str]:
    """Load configuration from config.txt file."""
    config = {}
    try:
        config_path = constants.CONFIG_FILE_PATH if CONSTANTS_IMPORTED else "config/config.txt"
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}

def get_authenticated_service(
    api_name: str = "youtube",
    api_version: str = "v3",
    scopes: Optional[List[str]] = None,
    client_secrets_file_arg: Optional[str] = None,
    token_file_arg: Optional[str] = None,
    log_prefix: str = ""
) -> Optional[Any]:
    """
    Authenticates with the Google API using OAuth2.

    Args:
        api_name: API name (e.g., "youtube", "youtubeAnalytics")
        api_version: API version (e.g., "v3")
        scopes: OAuth scopes to request
        client_secrets_file_arg: Path to client secrets file
        token_file_arg: Path to token file
        log_prefix: Prefix for log messages

    Returns:
        API service object or None if authentication fails
    """
    if not GOOGLE_API_AVAILABLE:
        logger.error(f"{log_prefix}Google API libraries not available.")
        return None

    # Use provided values or defaults from constants
    scopes_to_use = scopes or (constants.SCOPES if CONSTANTS_IMPORTED else [
        "https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/yt-analytics.readonly",
        "https://www.googleapis.com/auth/youtube"
    ])
    client_secrets_path = client_secrets_file_arg or (constants.CLIENT_SECRETS_FILE if CONSTANTS_IMPORTED else "data/client_secret.json")
    token_path = token_file_arg or (constants.TOKEN_FILE if CONSTANTS_IMPORTED else "data/token.json")

    creds = None

    # Load cached credentials if they exist
    if os.path.exists(token_path):
        logger.info(f"{log_prefix}Attempting to load cached credentials from: {token_path}")
        try:
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
            logger.info(f"{log_prefix}Cached credentials loaded.")
        except Exception as e:
            logger.warning(f"{log_prefix}Failed to load cached credentials: {e}. Will re-authenticate.")
            creds = None

    # If credentials don't exist or are invalid, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info(f"{log_prefix}Cached credentials expired. Attempting to refresh...")
            try:
                creds.refresh(Request())
                logger.info(f"{log_prefix}Credentials refreshed successfully.")
            except Exception as e:
                logger.warning(f"{log_prefix}Failed to refresh credentials: {e}. Will perform new authentication flow.")
                creds = None

        # If still no valid credentials, need to authenticate
        if not creds or not creds.valid:
            logger.info(f"{log_prefix}No valid cached credentials found or refresh failed. Starting new authentication flow.")
            if not os.path.exists(client_secrets_path):
                logger.error(f"{log_prefix}FATAL: Client secrets file not found at: {client_secrets_path}")
                logger.error(f"{log_prefix}Please download 'client_secret.json' from Google Cloud Console and place it in the script directory.")
                return None

            try:
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, scopes_to_use)
                creds = flow.run_local_server(port=0)
                logger.info(f"{log_prefix}Authentication flow completed via browser.")

                # Save the credentials for future use
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
                logger.info(f"{log_prefix}New credentials saved to: {token_path}")
            except Exception as e:
                logger.error(f"{log_prefix}An error occurred during the authentication flow: {e}")
                logger.error(f"{log_prefix}Authentication failed.")
                return None

    # Build the API service object
    if creds and creds.valid:
        try:
            service = build(api_name, api_version, credentials=creds)
            logger.info(f"{log_prefix}{api_name.capitalize()} {api_version} API service built successfully.")
            return service
        except HttpError as e:
            logger.error(f"{log_prefix}API error building service: {e}")
            logger.error(f"{log_prefix}API service initialization failed.")
            return None
        except Exception as e:
            logger.error(f"{log_prefix}An unexpected error occurred while building the API service: {e}")
            logger.error(f"{log_prefix}API service initialization failed.")
            return None
    else:
        logger.error(f"{log_prefix}Authentication did not result in valid credentials. API service not built.")
        return None

def initialize_gemini_api() -> bool:
    """
    Initialize the Gemini API with the API key from config.

    Returns:
        bool: True if initialization was successful, False otherwise
    """
    if not GEMINI_API_AVAILABLE:
        logger.error("Google Generative AI library not available.")
        return False

    config = load_config()
    api_key = config.get("GEMINI_API_KEY") or config.get("API_KEY")

    if not api_key:
        logger.error("API key not found in config.txt")
        return False

    try:
        genai.configure(api_key=api_key)
        logger.info("Gemini API initialized successfully.")
        return True
    except Exception as e:
        logger.error(f"Error initializing Gemini API: {e}")
        return False

def get_gemini_model(model_name: str = "gemini-pro") -> Optional[Any]:
    """
    Get a Gemini model for text generation.

    Args:
        model_name: Name of the Gemini model to use

    Returns:
        Gemini model or None if initialization fails
    """
    if not initialize_gemini_api():
        return None

    try:
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        logger.error(f"Error getting Gemini model: {e}")
        return None
