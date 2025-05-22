#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yt-dlp Utilities

This module provides functions for handling yt-dlp operations with improved error handling.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

import os
import json
import logging
import traceback
from typing import Dict, Any, List, Optional, Tuple, Callable

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
        print("CRITICAL: ytdlp_utils.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            LOGS_DIR = "logs"
        constants = MinimalConstants()
        print("WARNING: ytdlp_utils.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "ytdlp_utils.log")
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

# Try to import yt-dlp
try:
    import yt_dlp
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False
    logger.error("yt-dlp not available. Install with: pip install yt-dlp")

def search_videos(search_query: str, max_results: int = 10,
                 ffmpeg_path: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Search for videos using yt-dlp with improved error handling.

    Args:
        search_query: Search query
        max_results: Maximum number of results to return
        ffmpeg_path: Path to ffmpeg executable

    Returns:
        Tuple[List[Dict[str, Any]], Dict[str, Any]]: Tuple of (search results, error info)
    """
    if not YTDLP_AVAILABLE:
        return [], {"error": "yt-dlp not available", "details": "Install with: pip install yt-dlp"}

    error_info = {"error": None, "details": None}

    # Configure yt-dlp options
    ydl_opts = {
        'extract_flat': True,
        'playlist_items': f'1-{max_results}',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'source_address': '0.0.0.0',
        'default_search': 'ytsearch',
    }

    # Add ffmpeg path if provided
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_query, download=False)

        if not result or 'entries' not in result or not result.get('entries'):
            error_info = {"error": "no_results", "details": f"No videos found for query: {search_query}"}
            return [], error_info

        return result['entries'], error_info

    except yt_dlp.utils.DownloadError as e:
        error_info = {"error": "download_error", "details": str(e)}
        logger.error(f"yt-dlp DownloadError during search: {e}")
        return [], error_info

    except yt_dlp.utils.ExtractorError as e:
        error_info = {"error": "extractor_error", "details": str(e)}
        logger.error(f"yt-dlp ExtractorError during search: {e}")
        return [], error_info

    except yt_dlp.utils.UnsupportedError as e:
        error_info = {"error": "unsupported_error", "details": str(e)}
        logger.error(f"yt-dlp UnsupportedError during search: {e}")
        return [], error_info

    except yt_dlp.utils.GeoRestrictedError as e:
        error_info = {"error": "geo_restricted", "details": str(e)}
        logger.error(f"yt-dlp GeoRestrictedError during search: {e}")
        return [], error_info

    except Exception as e:
        error_info = {"error": "unexpected_error", "details": str(e)}
        logger.error(f"Unexpected error during yt-dlp search: {e}")
        traceback.print_exc()
        return [], error_info

def download_video(video_id: str, output_path: str, ffmpeg_path: Optional[str] = None,
                  progress_hook: Optional[Callable] = None) -> Tuple[bool, Dict[str, Any]]:
    """
    Download a video using yt-dlp with improved error handling.

    Args:
        video_id: YouTube video ID
        output_path: Output path for the video
        ffmpeg_path: Path to ffmpeg executable
        progress_hook: Progress hook function

    Returns:
        Tuple[bool, Dict[str, Any]]: Tuple of (success, error info)
    """
    if not YTDLP_AVAILABLE:
        return False, {"error": "yt-dlp not available", "details": "Install with: pip install yt-dlp"}

    error_info = {"error": None, "details": None}

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': {'default': output_path},
        'merge_output_format': 'mp4',
        'writeinfojson': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'source_address': '0.0.0.0',
        'retries': 3,
        'fragment_retries': 3,
    }

    # Add ffmpeg path if provided
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    # Add progress hook if provided
    if progress_hook:
        ydl_opts['progress_hooks'] = [progress_hook]

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Verify the file was downloaded
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1024:
            return True, error_info
        else:
            error_info = {"error": "file_not_found", "details": f"File not found or too small: {output_path}"}
            return False, error_info

    except yt_dlp.utils.DownloadError as e:
        error_info = {"error": "download_error", "details": str(e)}
        logger.error(f"yt-dlp DownloadError: {e}")
        return False, error_info

    except yt_dlp.utils.ExtractorError as e:
        error_info = {"error": "extractor_error", "details": str(e)}
        logger.error(f"yt-dlp ExtractorError: {e}")
        return False, error_info

    except yt_dlp.utils.UnsupportedError as e:
        error_info = {"error": "unsupported_error", "details": str(e)}
        logger.error(f"yt-dlp UnsupportedError: {e}")
        return False, error_info

    except yt_dlp.utils.GeoRestrictedError as e:
        error_info = {"error": "geo_restricted", "details": str(e)}
        logger.error(f"yt-dlp GeoRestrictedError: {e}")
        return False, error_info

    except yt_dlp.utils.PostProcessingError as e:
        error_info = {"error": "post_processing_error", "details": str(e)}
        logger.error(f"yt-dlp PostProcessingError: {e}")
        return False, error_info

    except Exception as e:
        error_info = {"error": "unexpected_error", "details": str(e)}
        logger.error(f"Unexpected error during yt-dlp download: {e}")
        traceback.print_exc()
        return False, error_info

def extract_info_from_video(video_id: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Extract information from a video using yt-dlp with improved error handling.

    Args:
        video_id: YouTube video ID

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: Tuple of (video info, error info)
    """
    if not YTDLP_AVAILABLE:
        return {}, {"error": "yt-dlp not available", "details": "Install with: pip install yt-dlp"}

    error_info = {"error": None, "details": None}

    # Configure yt-dlp options
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'source_address': '0.0.0.0',
    }

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        return info, error_info

    except yt_dlp.utils.DownloadError as e:
        error_info = {"error": "download_error", "details": str(e)}
        logger.error(f"yt-dlp DownloadError during info extraction: {e}")
        return {}, error_info

    except yt_dlp.utils.ExtractorError as e:
        error_info = {"error": "extractor_error", "details": str(e)}
        logger.error(f"yt-dlp ExtractorError during info extraction: {e}")
        return {}, error_info

    except yt_dlp.utils.UnsupportedError as e:
        error_info = {"error": "unsupported_error", "details": str(e)}
        logger.error(f"yt-dlp UnsupportedError during info extraction: {e}")
        return {}, error_info

    except yt_dlp.utils.GeoRestrictedError as e:
        error_info = {"error": "geo_restricted", "details": str(e)}
        logger.error(f"yt-dlp GeoRestrictedError during info extraction: {e}")
        return {}, error_info

    except Exception as e:
        error_info = {"error": "unexpected_error", "details": str(e)}
        logger.error(f"Unexpected error during yt-dlp info extraction: {e}")
        traceback.print_exc()
        return {}, error_info
