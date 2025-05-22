#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playlist Manager

This module provides functions for managing YouTube playlists.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

import os
import json
import logging
import time
from typing import Dict, List, Tuple, Any, Optional, Union
from datetime import datetime

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
        print("CRITICAL: playlist_manager.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            CLIENT_SECRETS_FILE = "data/client_secret.json"
            TOKEN_FILE = "data/token.json"
            API_QUOTA_FILE = "data/api_quota.json"
            LOGS_DIR = "logs"
        constants = MinimalConstants()
        print("WARNING: playlist_manager.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "playlist_manager.log")
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

# Try to import Google API client
try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    logger.warning("Google API client not available. Install with: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")

# Constants
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube"]
DEFAULT_API_QUOTA_PER_DAY = 10000
DEFAULT_API_QUOTA_BUFFER = 1000  # Buffer to avoid hitting quota limit
DEFAULT_API_RETRIES = 3
DEFAULT_API_BACKOFF = 2  # Exponential backoff factor

class PlaylistManager:
    """Class for managing YouTube playlists."""

    def __init__(self, client_secrets_file_arg: Optional[str] = None,
                token_file_arg: Optional[str] = None,
                api_quota_per_day: int = DEFAULT_API_QUOTA_PER_DAY):
        """
        Initialize the PlaylistManager.

        Args:
            client_secrets_file_arg: Path to the client secrets file
            token_file_arg: Path to the token file
            api_quota_per_day: API quota per day
        """
        self.client_secrets_file = client_secrets_file_arg or (constants.CLIENT_SECRETS_FILE if CONSTANTS_IMPORTED else "data/client_secret.json")
        self.token_file = token_file_arg or (constants.TOKEN_FILE if CONSTANTS_IMPORTED else "data/token.json")
        self.api_quota_per_day = api_quota_per_day
        self.api_quota_used = 0
        self.youtube = None
        self.authenticated = False

    def authenticate(self) -> bool:
        """
        Authenticate with the YouTube API.

        Returns:
            bool: True if authentication was successful, False otherwise
        """
        if not GOOGLE_API_AVAILABLE:
            logger.error("Google API client not available. Cannot authenticate.")
            return False

        try:
            # Check if token file exists
            credentials = None
            if os.path.exists(self.token_file):
                try:
                    credentials = Credentials.from_authorized_user_info(
                        json.loads(open(self.token_file, "r").read()),
                        YOUTUBE_SCOPES
                    )
                except Exception as e:
                    logger.warning(f"Error loading credentials from token file: {e}")

            # If credentials are invalid or don't exist, run the OAuth flow
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    try:
                        credentials.refresh(Request())
                    except Exception as e:
                        logger.warning(f"Error refreshing credentials: {e}")
                        credentials = None

                if not credentials:
                    # Check if client secrets file exists
                    if not os.path.exists(self.client_secrets_file):
                        logger.error(f"Client secrets file not found: {self.client_secrets_file}")
                        return False

                    # Run the OAuth flow
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file, YOUTUBE_SCOPES)
                    credentials = flow.run_local_server(port=0)

                    # Save the credentials
                    with open(self.token_file, "w") as token:
                        token.write(credentials.to_json())

            # Build the YouTube API client
            self.youtube = build(
                YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                credentials=credentials
            )

            self.authenticated = True
            logger.info("Successfully authenticated with YouTube API")
            return True
        except Exception as e:
            logger.error(f"Error authenticating with YouTube API: {e}")
            self.authenticated = False
            return False

    def check_quota(self, units: int = 1) -> bool:
        """
        Check if there's enough API quota available.

        Args:
            units: Number of quota units to check

        Returns:
            bool: True if there's enough quota, False otherwise
        """
        if self.api_quota_used + units + DEFAULT_API_QUOTA_BUFFER > self.api_quota_per_day:
            logger.warning(f"API quota limit approaching: {self.api_quota_used}/{self.api_quota_per_day} units used")
            return False
        return True

    def update_quota(self, units: int = 1) -> None:
        """
        Update the API quota usage.

        Args:
            units: Number of quota units used
        """
        self.api_quota_used += units
        logger.debug(f"API quota usage: {self.api_quota_used}/{self.api_quota_per_day} units")

    def reset_quota(self) -> None:
        """Reset the API quota usage."""
        self.api_quota_used = 0
        logger.info("API quota usage reset")

    def get_playlists(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get the user's playlists.

        Args:
            max_results: Maximum number of results to return

        Returns:
            List[Dict[str, Any]]: List of playlists
        """
        if not self.authenticated:
            if not self.authenticate():
                return []

        if not self.check_quota(units=1):
            logger.warning("API quota limit reached. Cannot get playlists.")
            return []

        playlists = []
        next_page_token = None

        try:
            while True:
                # Get playlists
                request = self.youtube.playlists().list(
                    part="snippet,contentDetails",
                    mine=True,
                    maxResults=min(max_results, 50),
                    pageToken=next_page_token
                )

                response = request.execute()
                self.update_quota(units=1)

                # Add playlists to list
                playlists.extend(response.get("items", []))

                # Check if there are more pages
                next_page_token = response.get("nextPageToken")
                if not next_page_token or len(playlists) >= max_results:
                    break

            logger.info(f"Retrieved {len(playlists)} playlists")
            return playlists
        except HttpError as e:
            logger.error(f"HTTP error getting playlists: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting playlists: {e}")
            return []

    def create_playlist(self, title: str, description: str = "",
                       privacy_status: str = "private") -> Optional[str]:
        """
        Create a new playlist.

        Args:
            title: Playlist title
            description: Playlist description
            privacy_status: Privacy status (private, public, unlisted)

        Returns:
            Optional[str]: Playlist ID if successful, None otherwise
        """
        if not self.authenticated:
            if not self.authenticate():
                return None

        if not self.check_quota(units=50):
            logger.warning("API quota limit reached. Cannot create playlist.")
            return None

        try:
            # Create playlist
            request = self.youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description
                    },
                    "status": {
                        "privacyStatus": privacy_status
                    }
                }
            )

            response = request.execute()
            self.update_quota(units=50)

            playlist_id = response.get("id")
            logger.info(f"Created playlist: {title} (ID: {playlist_id})")
            return playlist_id
        except HttpError as e:
            logger.error(f"HTTP error creating playlist: {e}")
            return None
        except Exception as e:
            logger.error(f"Error creating playlist: {e}")
            return None

    def get_playlist_items(self, playlist_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get items in a playlist.

        Args:
            playlist_id: Playlist ID
            max_results: Maximum number of results to return

        Returns:
            List[Dict[str, Any]]: List of playlist items
        """
        if not self.authenticated:
            if not self.authenticate():
                return []

        if not self.check_quota(units=1):
            logger.warning("API quota limit reached. Cannot get playlist items.")
            return []

        items = []
        next_page_token = None

        try:
            while True:
                # Get playlist items
                request = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=min(max_results, 50),
                    pageToken=next_page_token
                )

                response = request.execute()
                self.update_quota(units=1)

                # Add items to list
                items.extend(response.get("items", []))

                # Check if there are more pages
                next_page_token = response.get("nextPageToken")
                if not next_page_token or len(items) >= max_results:
                    break

            logger.info(f"Retrieved {len(items)} items from playlist {playlist_id}")
            return items
        except HttpError as e:
            logger.error(f"HTTP error getting playlist items: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting playlist items: {e}")
            return []

    def add_video_to_playlist(self, playlist_id: str, video_id: str,
                             position: Optional[int] = None) -> bool:
        """
        Add a video to a playlist.

        Args:
            playlist_id: Playlist ID
            video_id: Video ID
            position: Position in the playlist (0-based index)

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.authenticated:
            if not self.authenticate():
                return False

        if not self.check_quota(units=50):
            logger.warning("API quota limit reached. Cannot add video to playlist.")
            return False

        try:
            # Create request body
            body = {
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }

            # Add position if specified
            if position is not None:
                body["snippet"]["position"] = position

            # Add video to playlist
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body=body
            )

            response = request.execute()
            self.update_quota(units=50)

            logger.info(f"Added video {video_id} to playlist {playlist_id}")
            return True
        except HttpError as e:
            logger.error(f"HTTP error adding video to playlist: {e}")
            return False
        except Exception as e:
            logger.error(f"Error adding video to playlist: {e}")
            return False

    def remove_video_from_playlist(self, playlist_item_id: str) -> bool:
        """
        Remove a video from a playlist.

        Args:
            playlist_item_id: Playlist item ID

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.authenticated:
            if not self.authenticate():
                return False

        if not self.check_quota(units=50):
            logger.warning("API quota limit reached. Cannot remove video from playlist.")
            return False

        try:
            # Remove video from playlist
            request = self.youtube.playlistItems().delete(
                id=playlist_item_id
            )

            response = request.execute()
            self.update_quota(units=50)

            logger.info(f"Removed playlist item {playlist_item_id}")
            return True
        except HttpError as e:
            logger.error(f"HTTP error removing video from playlist: {e}")
            return False
        except Exception as e:
            logger.error(f"Error removing video from playlist: {e}")
            return False

    def get_or_create_playlist(self, title: str, description: str = "",
                              privacy_status: str = "private") -> Optional[str]:
        """
        Get a playlist by title or create it if it doesn't exist.

        Args:
            title: Playlist title
            description: Playlist description
            privacy_status: Privacy status (private, public, unlisted)

        Returns:
            Optional[str]: Playlist ID if successful, None otherwise
        """
        # Get existing playlists
        playlists = self.get_playlists()

        # Check if playlist already exists
        for playlist in playlists:
            if playlist.get("snippet", {}).get("title") == title:
                playlist_id = playlist.get("id")
                logger.info(f"Found existing playlist: {title} (ID: {playlist_id})")
                return playlist_id

        # Create new playlist
        return self.create_playlist(title, description, privacy_status)

    def check_video_in_playlist(self, playlist_id: str, video_id: str) -> bool:
        """
        Check if a video is already in a playlist.

        Args:
            playlist_id: Playlist ID
            video_id: Video ID

        Returns:
            bool: True if the video is in the playlist, False otherwise
        """
        # Get playlist items
        items = self.get_playlist_items(playlist_id)

        # Check if video is in playlist
        for item in items:
            if item.get("contentDetails", {}).get("videoId") == video_id:
                return True

        return False

    def add_video_if_not_exists(self, playlist_id: str, video_id: str,
                               position: Optional[int] = None) -> bool:
        """
        Add a video to a playlist if it doesn't already exist.

        Args:
            playlist_id: Playlist ID
            video_id: Video ID
            position: Position in the playlist (0-based index)

        Returns:
            bool: True if successful, False otherwise
        """
        # Check if video is already in playlist
        if self.check_video_in_playlist(playlist_id, video_id):
            logger.info(f"Video {video_id} already in playlist {playlist_id}")
            return True

        # Add video to playlist
        return self.add_video_to_playlist(playlist_id, video_id, position)

    def create_playlist_for_keyword(self, keyword: str, description: str = "",
                                  privacy_status: str = "private") -> Optional[str]:
        """
        Create a playlist for a keyword.

        Args:
            keyword: Keyword
            description: Playlist description
            privacy_status: Privacy status (private, public, unlisted)

        Returns:
            Optional[str]: Playlist ID if successful, None otherwise
        """
        # Format title
        title = f"Shorts - {keyword.title()}"

        # Format description
        if not description:
            description = f"YouTube Shorts related to {keyword.title()}"

        # Get or create playlist
        return self.get_or_create_playlist(title, description, privacy_status)

    def add_video_to_keyword_playlist(self, keyword: str, video_id: str,
                                     description: str = "",
                                     privacy_status: str = "private") -> bool:
        """
        Add a video to a keyword playlist.

        Args:
            keyword: Keyword
            video_id: Video ID
            description: Playlist description
            privacy_status: Privacy status (private, public, unlisted)

        Returns:
            bool: True if successful, False otherwise
        """
        # Get or create playlist
        playlist_id = self.create_playlist_for_keyword(keyword, description, privacy_status)

        if not playlist_id:
            return False

        # Add video to playlist
        return self.add_video_if_not_exists(playlist_id, video_id)

    def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a video.

        Args:
            video_id: Video ID

        Returns:
            Optional[Dict[str, Any]]: Video details if successful, None otherwise
        """
        if not self.authenticated:
            if not self.authenticate():
                return None

        if not self.check_quota(units=1):
            logger.warning("API quota limit reached. Cannot get video details.")
            return None

        try:
            # Get video details
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )

            response = request.execute()
            self.update_quota(units=1)

            # Check if video exists
            items = response.get("items", [])
            if not items:
                logger.warning(f"Video not found: {video_id}")
                return None

            logger.info(f"Retrieved details for video {video_id}")
            return items[0]
        except HttpError as e:
            logger.error(f"HTTP error getting video details: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting video details: {e}")
            return None
