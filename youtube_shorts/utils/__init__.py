#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Modules Package

This package contains utility modules for the YouTube Shorts Automation project.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

# Import utility modules for easier access
try:
    # Constants
    from .constants import *

    # Metrics utilities
    from .metrics_utils import load_metadata_metrics, save_metadata_metrics, add_error_sample

    # Date utilities
    from .date_utils import parse_date, format_date, is_older_than_days

    # Cache utilities
    from .cache_utils import load_cache, save_cache, cleanup_correlation_cache

    # yt-dlp utilities
    from .ytdlp_utils import search_videos, download_video, extract_info_from_video

    # Keyword management
    from .keyword_manager import (
        load_keywords, save_keywords, load_keyword_scores, save_keyword_scores,
        normalize_scores, update_keyword_score, select_keywords, extract_keywords_from_text,
        get_keyword_performance
    )

    # Metadata generation
    from .metadata_generator import (
        configure_genai_api, generate_metadata_prompt, parse_metadata_response,
        generate_metadata, validate_metadata, improve_metadata, analyze_metadata_quality
    )

    # Playlist management
    from .playlist_manager import PlaylistManager

    # Channel scoring
    from .channel_scoring import calculate_channel_score, analyze_channel_performance

    __all__ = [
        # Constants - all constants are imported with *

        # Metrics utilities
        'load_metadata_metrics', 'save_metadata_metrics', 'add_error_sample',

        # Date utilities
        'parse_date', 'format_date', 'is_older_than_days',

        # Cache utilities
        'load_cache', 'save_cache', 'cleanup_correlation_cache',

        # yt-dlp utilities
        'search_videos', 'download_video', 'extract_info_from_video',

        # Keyword management
        'load_keywords', 'save_keywords', 'load_keyword_scores', 'save_keyword_scores',
        'normalize_scores', 'update_keyword_score', 'select_keywords', 'extract_keywords_from_text',
        'get_keyword_performance',

        # Metadata generation
        'configure_genai_api', 'generate_metadata_prompt', 'parse_metadata_response',
        'generate_metadata', 'validate_metadata', 'improve_metadata', 'analyze_metadata_quality',

        # Playlist management
        'PlaylistManager',

        # Channel scoring
        'calculate_channel_score', 'analyze_channel_performance'
    ]
except ImportError as e:
    # Some modules might not be available
    import logging
    logging.warning(f"Error importing utility modules: {e}")
    __all__ = []
