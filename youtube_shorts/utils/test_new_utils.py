#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test New Utilities

This script tests the new utility modules to ensure they work correctly.

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
        print("CRITICAL: test_new_utils.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            DATA_DIR = "data"
            TEST_DATA_DIR = os.path.join("data", "test")
        constants = MinimalConstants()
        print("WARNING: test_new_utils.py using minimal fallback constants.")
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
    from utils.keyword_manager import (
        load_keywords, save_keywords, load_keyword_scores, save_keyword_scores,
        normalize_scores, update_keyword_score, select_keywords, extract_keywords_from_text,
        get_keyword_performance
    )
    from utils.metadata_generator import (
        configure_genai_api, generate_metadata_prompt, parse_metadata_response,
        generate_metadata, validate_metadata, improve_metadata, analyze_metadata_quality
    )
    from utils.playlist_manager import PlaylistManager
    UTILS_AVAILABLE = True
except ImportError as e:
    UTILS_AVAILABLE = False
    logger.error(f"Error importing utility modules: {e}")
    sys.exit(1)

def test_keyword_manager():
    """Test keyword manager utilities."""
    logger.info("Testing keyword manager utilities...")

    # Test extract_keywords_from_text
    text = "This is a test for extracting keywords from text. Python programming is fun and educational."
    keywords = extract_keywords_from_text(text)
    assert len(keywords) > 0, "Failed to extract keywords from text"
    logger.info(f"Successfully extracted keywords: {keywords}")

    # Test normalize_scores
    scores = {
        "python": 75.0,
        "programming": 60.0,
        "test": 40.0,
        "educational": 80.0
    }
    normalized = normalize_scores(scores)
    assert len(normalized) == len(scores), "Failed to normalize scores"
    logger.info(f"Successfully normalized scores: {normalized}")

    # Test update_keyword_score
    scores_data = {"scores": scores.copy()}  # Make a copy to avoid modifying the original
    original_score = scores_data["scores"]["python"]
    updated = update_keyword_score(scores_data, "python", True, 5, 1000)
    assert updated["scores"]["python"] >= original_score, f"Failed to update keyword score: {updated['scores']['python']} not >= {original_score}"
    logger.info(f"Successfully updated keyword score: {original_score} -> {updated['scores']['python']}")

    # Test select_keywords
    all_keywords = ["python", "programming", "test", "educational", "fun", "learning"]
    selected = select_keywords(all_keywords, scores_data, 3)
    assert len(selected) == 3, "Failed to select keywords"
    logger.info(f"Successfully selected keywords: {selected}")

    # Test get_keyword_performance
    top_keywords = get_keyword_performance(scores_data, 2)
    assert len(top_keywords) == 2, "Failed to get keyword performance"
    logger.info(f"Successfully got top keywords: {top_keywords}")

    logger.info("Keyword manager utilities tests passed!")

def test_metadata_generator():
    """Test metadata generator utilities."""
    logger.info("Testing metadata generator utilities...")

    # Test generate_metadata_prompt
    prompt = generate_metadata_prompt("Test Video", "python", True)
    assert "Test Video" in prompt, "Failed to generate metadata prompt"
    assert "python" in prompt, "Failed to include keyword in metadata prompt"
    logger.info(f"Successfully generated metadata prompt")

    # Test parse_metadata_response
    response = """```json
{
    "title": "Test Video Title",
    "description": "This is a test video description.",
    "tags": ["test", "video", "python"]
}
```"""
    metadata = parse_metadata_response(response)
    assert metadata["title"] == "Test Video Title", "Failed to parse metadata title"
    assert metadata["description"] == "This is a test video description.", "Failed to parse metadata description"
    assert len(metadata["tags"]) == 3, "Failed to parse metadata tags"
    logger.info(f"Successfully parsed metadata response")

    # Test validate_metadata
    validated = validate_metadata(metadata, "Test Video", "python")
    assert validated["title"] == metadata["title"], "Failed to validate metadata title"
    logger.info(f"Successfully validated metadata")

    # Test analyze_metadata_quality
    quality = analyze_metadata_quality(metadata, "python")
    assert "overall_score" in quality, "Failed to analyze metadata quality"
    logger.info(f"Successfully analyzed metadata quality: {quality['overall_score']}")

    logger.info("Metadata generator utilities tests passed!")

def test_playlist_manager():
    """Test playlist manager utilities."""
    logger.info("Testing playlist manager utilities...")

    # Create playlist manager
    manager = PlaylistManager()

    # Test initialization
    assert manager.api_quota_used == 0, "Failed to initialize playlist manager"
    logger.info(f"Successfully initialized playlist manager")

    # Test check_quota
    assert manager.check_quota(100), "Failed to check quota"
    logger.info(f"Successfully checked quota")

    # Test update_quota
    manager.update_quota(100)
    assert manager.api_quota_used == 100, "Failed to update quota"
    logger.info(f"Successfully updated quota")

    # Test reset_quota
    manager.reset_quota()
    assert manager.api_quota_used == 0, "Failed to reset quota"
    logger.info(f"Successfully reset quota")

    logger.info("Playlist manager utilities tests passed!")

def main():
    """Run all tests."""
    logger.info("Starting new utility tests...")

    try:
        test_keyword_manager()
        test_metadata_generator()
        test_playlist_manager()

        logger.info("All tests passed!")
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
