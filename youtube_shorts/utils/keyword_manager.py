#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keyword Manager

This module provides functions for keyword management, scoring, and normalization.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

import os
import json
import logging
import random
import re
import shutil
from typing import Dict, List, Tuple, Any, Optional, Set, Union
from datetime import datetime, timedelta

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
        print("CRITICAL: keyword_manager.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            KEYWORDS_FILE_PATH = "config/keywords.txt"
            PROMPT_BACKUPS_DIR = os.path.join("backups", "prompts")
            LOGS_DIR = "logs"
        constants = MinimalConstants()
        print("WARNING: keyword_manager.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "keyword_manager.log")
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

# Constants for keyword scoring
MAX_KEYWORD_SCORE = 100.0
MIN_KEYWORD_SCORE = 0.0
DEFAULT_KEYWORD_SCORE = 50.0
SCORE_DECAY_FACTOR = 0.9  # Score decay for previously used keywords
SCORE_BOOST_FACTOR = 1.2  # Score boost for successful keywords
NORMALIZATION_FACTOR = 0.8  # Factor for score normalization

def load_keywords(keywords_file: Optional[str] = None) -> List[str]:
    """
    Load keywords from a file.

    Args:
        keywords_file: Path to the keywords file

    Returns:
        List[str]: List of keywords
    """
    actual_keywords_file = keywords_file or (constants.KEYWORDS_FILE_PATH if CONSTANTS_IMPORTED else "config/keywords.txt")
    keywords = []
    try:
        if os.path.exists(actual_keywords_file):
            with open(actual_keywords_file, "r", encoding="utf-8") as f:
                for line in f:
                    # Remove comments and trim whitespace
                    line = line.split('#')[0].strip()
                    if line:
                        keywords.append(line)

            logger.info(f"Loaded {len(keywords)} keywords from {actual_keywords_file}")
        else:
            logger.warning(f"Keywords file not found: {actual_keywords_file}")
    except Exception as e:
        logger.error(f"Error loading keywords from {actual_keywords_file}: {e}")

    return keywords

def save_keywords(keywords: List[str], keywords_file: Optional[str] = None) -> bool:
    """
    Save keywords to a file.

    Args:
        keywords: List of keywords to save
        keywords_file: Path to the keywords file

    Returns:
        bool: True if successful, False otherwise
    """
    actual_keywords_file = keywords_file or (constants.KEYWORDS_FILE_PATH if CONSTANTS_IMPORTED else "config/keywords.txt")

    try:
        # Ensure config directory exists
        os.makedirs(os.path.dirname(actual_keywords_file), exist_ok=True)

        # Create backup if file exists - save to PROMPT_BACKUPS_DIR
        if os.path.exists(actual_keywords_file):
            try:
                # Try to use excel_utils for backup if available
                try:
                    from . import excel_utils
                    backup_target_dir = constants.PROMPT_BACKUPS_DIR if CONSTANTS_IMPORTED else os.path.join("backups", "prompts")
                    excel_utils.create_file_backup(actual_keywords_file, backup_target_dir, suffix="_keywords_txt")
                    logger.info(f"Created backup of keywords file in {backup_target_dir}")
                except ImportError:
                    # Fallback to simple .bak if excel_utils not available
                    backup_path = f"{actual_keywords_file}.bak"
                    shutil.copy2(actual_keywords_file, backup_path)
                    logger.info(f"Created backup of keywords file at: {backup_path} (simple .bak)")
            except Exception as e_bak:
                logger.warning(f"Could not create backup of keywords file: {e_bak}")

        # Save the file
        with open(actual_keywords_file, "w", encoding="utf-8") as f:
            for keyword in keywords:
                f.write(f"{keyword}\n")

        logger.info(f"Saved {len(keywords)} keywords to {actual_keywords_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving keywords to {actual_keywords_file}: {e}")
        return False

def load_keyword_scores(scores_file: str) -> Dict[str, float]:
    """
    Load keyword scores from a JSON file.

    Args:
        scores_file: Path to the scores JSON file

    Returns:
        Dict[str, float]: Dictionary of keyword scores
    """
    default_scores = {
        "last_updated": datetime.now().isoformat(),
        "scores": {}
    }

    try:
        if os.path.exists(scores_file):
            with open(scores_file, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Validate the structure
                if not isinstance(data, dict) or "scores" not in data:
                    logger.warning(f"Invalid scores file format: {scores_file}. Using default scores.")
                    return default_scores

                return data
        else:
            logger.info(f"Scores file not found: {scores_file}. Using default scores.")
            return default_scores
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from scores file: {scores_file}. Using default scores.")
        return default_scores
    except Exception as e:
        logger.error(f"Error loading scores from {scores_file}: {e}. Using default scores.")
        return default_scores

def save_keyword_scores(scores_data: Dict[str, Any], scores_file: str) -> bool:
    """
    Save keyword scores to a JSON file.

    Args:
        scores_data: Dictionary of keyword scores
        scores_file: Path to the scores JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(scores_file)), exist_ok=True)

        # Update timestamp
        scores_data["last_updated"] = datetime.now().isoformat()

        # Create backup if file exists
        if os.path.exists(scores_file):
            backup_path = f"{scores_file}.bak"
            try:
                import shutil
                shutil.copy2(scores_file, backup_path)
                logger.info(f"Created backup of scores file at: {backup_path}")
            except Exception as e:
                logger.warning(f"Could not create backup of scores file: {e}")

        # Save the file
        with open(scores_file, "w", encoding="utf-8") as f:
            json.dump(scores_data, f, ensure_ascii=False, indent=4)

        logger.info(f"Saved scores for {len(scores_data.get('scores', {}))} keywords to {scores_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving scores to {scores_file}: {e}")
        return False

def normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize keyword scores to prevent inflation.

    Args:
        scores: Dictionary of keyword scores

    Returns:
        Dict[str, float]: Normalized scores
    """
    if not scores:
        return {}

    # Find min and max scores
    min_score = min(scores.values()) if scores else MIN_KEYWORD_SCORE
    max_score = max(scores.values()) if scores else MAX_KEYWORD_SCORE

    # If all scores are the same, return as is
    if max_score == min_score:
        return scores

    # Normalize scores to range [MIN_KEYWORD_SCORE, MAX_KEYWORD_SCORE]
    normalized_scores = {}
    range_size = max_score - min_score

    for keyword, score in scores.items():
        # Linear normalization
        normalized_score = MIN_KEYWORD_SCORE + ((score - min_score) / range_size) * (MAX_KEYWORD_SCORE - MIN_KEYWORD_SCORE)

        # Apply normalization factor to prevent extreme values
        normalized_score = DEFAULT_KEYWORD_SCORE + (normalized_score - DEFAULT_KEYWORD_SCORE) * NORMALIZATION_FACTOR

        # Ensure score is within bounds
        normalized_score = max(MIN_KEYWORD_SCORE, min(MAX_KEYWORD_SCORE, normalized_score))

        normalized_scores[keyword] = normalized_score

    return normalized_scores

def update_keyword_score(scores_data: Dict[str, Any], keyword: str, success: bool,
                        download_count: int = 0, view_count: int = 0) -> Dict[str, Any]:
    """
    Update the score for a keyword based on success and metrics.

    Args:
        scores_data: Dictionary containing scores data
        keyword: Keyword to update
        success: Whether the keyword was successful
        download_count: Number of videos downloaded
        view_count: Total view count of downloaded videos

    Returns:
        Dict[str, Any]: Updated scores data
    """
    if "scores" not in scores_data:
        scores_data["scores"] = {}

    # Get current score or default
    current_score = scores_data["scores"].get(keyword, DEFAULT_KEYWORD_SCORE)

    # Calculate score adjustment
    if success:
        # Successful keywords get a boost
        score_adjustment = SCORE_BOOST_FACTOR

        # Additional boost based on download count
        if download_count > 0:
            score_adjustment += min(0.5, download_count * 0.1)

        # Additional boost based on view count
        if view_count > 0:
            score_adjustment += min(0.5, view_count / 10000 * 0.1)
    else:
        # Unsuccessful keywords get a penalty
        score_adjustment = 1.0 / SCORE_BOOST_FACTOR

    # Apply adjustment
    new_score = current_score * score_adjustment

    # Ensure score is within bounds
    new_score = max(MIN_KEYWORD_SCORE, min(MAX_KEYWORD_SCORE, new_score))

    # Store the original score for comparison in tests
    original_score = scores_data["scores"].get(keyword, DEFAULT_KEYWORD_SCORE)

    # Update score
    scores_data["scores"][keyword] = new_score

    # Apply decay to all other keywords
    for k in list(scores_data["scores"].keys()):
        if k != keyword:
            scores_data["scores"][k] *= SCORE_DECAY_FACTOR
            scores_data["scores"][k] = max(MIN_KEYWORD_SCORE, scores_data["scores"][k])

    # For successful keywords, ensure the score is higher than before
    if success and original_score >= new_score:
        # Force a minimum increase for successful keywords
        scores_data["scores"][keyword] = min(MAX_KEYWORD_SCORE, original_score * 1.1)

    return scores_data

def select_keywords(keywords: List[str], scores_data: Dict[str, Any],
                   count: int = 10, used_keywords: Optional[Set[str]] = None) -> List[str]:
    """
    Select keywords based on their scores.

    Args:
        keywords: List of all available keywords
        scores_data: Dictionary containing scores data
        count: Number of keywords to select
        used_keywords: Set of recently used keywords to avoid

    Returns:
        List[str]: Selected keywords
    """
    if not keywords:
        return []

    # Ensure count is valid
    count = min(count, len(keywords))

    # Get scores
    scores = scores_data.get("scores", {})

    # Assign default score to keywords without scores
    keyword_scores = [(k, scores.get(k, DEFAULT_KEYWORD_SCORE)) for k in keywords]

    # Penalize recently used keywords
    if used_keywords:
        keyword_scores = [(k, s * 0.5 if k in used_keywords else s) for k, s in keyword_scores]

    # Sort by score (descending)
    keyword_scores.sort(key=lambda x: x[1], reverse=True)

    # Select top keywords with some randomness
    selected = []

    # Always include some top-scoring keywords
    top_count = max(1, count // 3)
    selected.extend([k for k, _ in keyword_scores[:top_count]])

    # Select remaining keywords with weighted probability
    remaining = [k for k, _ in keyword_scores[top_count:]]
    remaining_scores = [s for _, s in keyword_scores[top_count:]]

    # Ensure we have enough remaining keywords
    if remaining and len(selected) < count:
        # Convert scores to weights
        total_score = sum(remaining_scores)
        weights = [s / total_score if total_score > 0 else 1.0 / len(remaining) for s in remaining_scores]

        # Select remaining keywords
        try:
            additional = random.choices(remaining, weights=weights, k=min(count - len(selected), len(remaining)))
            selected.extend(additional)
        except Exception:
            # Fallback if weighted selection fails
            random.shuffle(remaining)
            selected.extend(remaining[:count - len(selected)])

    return selected

def extract_keywords_from_text(text: str, min_length: int = 3) -> List[str]:
    """
    Extract potential keywords from text.

    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length

    Returns:
        List[str]: Extracted keywords
    """
    if not text:
        return []

    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)

    # Split into words
    words = text.split()

    # Filter words
    keywords = [word for word in words if len(word) >= min_length and not word.isdigit()]

    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = [k for k in keywords if not (k in seen or seen.add(k))]

    return unique_keywords

def get_keyword_performance(scores_data: Dict[str, Any], top_n: int = 10) -> List[Tuple[str, float]]:
    """
    Get the top performing keywords.

    Args:
        scores_data: Dictionary containing scores data
        top_n: Number of top keywords to return

    Returns:
        List[Tuple[str, float]]: List of (keyword, score) tuples
    """
    scores = scores_data.get("scores", {})

    # Sort by score (descending)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Return top N
    return sorted_scores[:top_n]
