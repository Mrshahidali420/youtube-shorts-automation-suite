#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Utilities

This script tests the utility modules to ensure they work correctly.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

import os
import sys
import json
import logging
import tempfile
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- NEW: Import constants from the new location ---
try:
    from utils import constants
    CONSTANTS_IMPORTED = True
except ImportError:
    try:
        # Try importing directly if run as a script
        import constants
        CONSTANTS_IMPORTED = True
    except ImportError:
        CONSTANTS_IMPORTED = False
        print("CRITICAL: test_utils.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            DATA_DIR = "data"
            TEST_DATA_DIR = os.path.join("data", "test")
        constants = MinimalConstants()
        print("WARNING: test_utils.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Import utility modules
try:
    from utils.metrics_utils import load_metadata_metrics, save_metadata_metrics, add_error_sample
    from utils.date_utils import parse_date, format_date, is_older_than_days
    from utils.cache_utils import load_cache, save_cache, cleanup_correlation_cache
    from utils.ytdlp_utils import search_videos, download_video, extract_info_from_video
    UTILS_AVAILABLE = True
except ImportError as e:
    UTILS_AVAILABLE = False
    logger.error(f"Error importing utility modules: {e}")
    sys.exit(1)

def test_date_utils():
    """Test date utilities."""
    logger.info("Testing date utilities...")

    # Test parse_date
    date_str = "2023-01-01T12:30:45"
    dt = parse_date(date_str)
    assert dt is not None, f"Failed to parse date: {date_str}"
    logger.info(f"Successfully parsed date: {date_str} -> {dt}")

    # Test format_date
    formatted = format_date(dt, "%Y-%m-%d")
    assert formatted == "2023-01-01", f"Failed to format date: {dt} -> {formatted}"
    logger.info(f"Successfully formatted date: {dt} -> {formatted}")

    # Test is_older_than_days
    old_date = datetime.now() - timedelta(days=10)
    assert is_older_than_days(old_date, 5), f"Failed to detect old date: {old_date}"
    logger.info(f"Successfully detected old date: {old_date}")

    logger.info("Date utilities tests passed!")

def test_cache_utils():
    """Test cache utilities."""
    logger.info("Testing cache utilities...")

    # Create a temporary test cache file
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
        test_cache_path = temp_file.name

    try:
        # Create test cache data
        test_cache = {
            "timestamp": datetime.now().isoformat(),
            "test_key": "test_value",
            "test_list": [1, 2, 3]
        }

        # Test save_cache
        save_result = save_cache(test_cache, test_cache_path, "Test Cache")
        assert save_result, "Failed to save cache"
        logger.info("Successfully saved test cache")

        # Test load_cache
        loaded_cache = load_cache(test_cache_path, "Test Cache")
        assert loaded_cache is not None, "Failed to load cache"
        assert loaded_cache.get("test_key") == "test_value", "Loaded cache has incorrect values"
        logger.info("Successfully loaded test cache")

        logger.info("Cache utilities tests passed!")
    finally:
        # Clean up
        try:
            if os.path.exists(test_cache_path):
                os.remove(test_cache_path)
            if os.path.exists(f"{test_cache_path}.bak"):
                os.remove(f"{test_cache_path}.bak")
        except Exception as e:
            logger.warning(f"Error cleaning up test cache: {e}")

def test_metrics_utils():
    """Test metrics utilities."""
    logger.info("Testing metrics utilities...")

    # Create a temporary test metrics file
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
        test_metrics_path = temp_file.name

    try:
        # Test load_metadata_metrics
        metrics = load_metadata_metrics(test_metrics_path)
        assert metrics is not None, "Failed to load metrics"
        logger.info("Successfully loaded test metrics")

        # Test add_error_sample
        add_error_sample(metrics, "test_error", "Test error details", "Test Video Title")
        assert len(metrics.get("error_samples", [])) > 0, "Failed to add error sample"
        logger.info("Successfully added error sample")

        # Test save_metadata_metrics
        save_result = save_metadata_metrics(metrics, test_metrics_path)
        assert save_result, "Failed to save metrics"
        logger.info("Successfully saved test metrics")

        logger.info("Metrics utilities tests passed!")
    finally:
        # Clean up
        try:
            if os.path.exists(test_metrics_path):
                os.remove(test_metrics_path)
            if os.path.exists(f"{test_metrics_path}.bak"):
                os.remove(f"{test_metrics_path}.bak")
        except Exception as e:
            logger.warning(f"Error cleaning up test metrics: {e}")

def test_ytdlp_utils():
    """Test yt-dlp utilities."""
    logger.info("Testing yt-dlp utilities...")

    # Test search_videos
    search_query = "python programming"
    videos, error_info = search_videos(search_query, max_results=2)

    if error_info["error"]:
        logger.warning(f"Search error: {error_info['error']} - {error_info['details']}")
    else:
        assert len(videos) > 0, "No videos found in search"
        logger.info(f"Successfully searched for videos: found {len(videos)} results")

        # Print first video info
        if videos:
            video = videos[0]
            logger.info(f"First video: {video.get('title')} (ID: {video.get('id')})")

    logger.info("yt-dlp utilities tests completed!")

def main():
    """Run all tests."""
    logger.info("Starting utility tests...")

    try:
        test_date_utils()
        test_cache_utils()
        test_metrics_utils()

        # Only test yt-dlp if explicitly requested (to avoid unnecessary API calls)
        if "--test-ytdlp" in sys.argv:
            test_ytdlp_utils()

        logger.info("All tests passed!")
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
