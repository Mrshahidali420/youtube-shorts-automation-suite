#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metadata Generator

This module provides functions for generating and validating video metadata.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0
"""

import os
import json
import logging
import re
import time
import random
import collections
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
        print("CRITICAL: metadata_generator.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            CONFIG_FILE_PATH = "config/config.txt"
            LOGS_DIR = "logs"
        constants = MinimalConstants()
        print("WARNING: metadata_generator.py using minimal fallback constants.")
# --- End NEW Import ---

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logging.warning("Google Generative AI not available. Install with: pip install google-generativeai")

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "metadata_generator.log")
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

# Constants for metadata
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 5000
MAX_TAGS = 500
MAX_TAG_LENGTH = 30
MIN_TAGS = 5
MAX_KEYWORD_STUFFING_RATIO = 0.3  # Maximum ratio of keyword repetition

# Constants for API
DEFAULT_API_TIMEOUT = 30
DEFAULT_API_RETRIES = 3
DEFAULT_API_BACKOFF = 2  # Exponential backoff factor

# Constants for metrics keys
TOTAL_API_CALLS = "total_api_calls"
PARSE_FAILURES = "parse_failures"
TIMEOUTS = "timeouts"
EMPTY_TITLE_ERRORS = "empty_title_errors"
EMPTY_DESCRIPTION_ERRORS = "empty_description_errors"
EMPTY_TAGS_ERRORS = "empty_tags_errors"
VALIDATION_TITLE_MISMATCHES = "validation_title_mismatches"
VALIDATION_TAG_LIST_ERRORS = "validation_tag_list_errors"
VALIDATION_KEYWORD_STUFFING = "validation_keyword_stuffing"

def configure_genai_api() -> bool:
    """
    Configure the Google Generative AI API using the API key from config.

    Returns:
        bool: True if successful, False otherwise
    """
    if not GENAI_AVAILABLE:
        logger.error("Google Generative AI not available. Cannot configure API.")
        return False

    try:
        # Try to import config_utils
        try:
            from .config_utils import load_config, get_config_value
            # Use constants.CONFIG_FILE_PATH via load_config
            config = load_config()
            api_key = get_config_value("GEMINI_API_KEY", None, config) or get_config_value("API_KEY", None, config)
        except ImportError:
            try:
                # Try direct import
                from config_utils import load_config, get_config_value
                config = load_config()
                api_key = get_config_value("GEMINI_API_KEY", None, config) or get_config_value("API_KEY", None, config)
            except ImportError:
                # Fallback to loading from config.txt directly using constants
                config = {}
                config_path = constants.CONFIG_FILE_PATH if CONSTANTS_IMPORTED else "config/config.txt"

                if os.path.exists(config_path):
                    with open(config_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and "=" in line:
                                key, value = line.split("=", 1)
                                config[key.strip()] = value.strip()
                api_key = config.get("GEMINI_API_KEY") or config.get("API_KEY")

        if not api_key:
            logger.error("API key not found in config.")
            return False

        genai.configure(api_key=api_key)
        logger.info("Google Generative AI API configured successfully.")
        return True
    except Exception as e:
        logger.error(f"Error configuring Google Generative AI API: {e}")
        return False

def generate_metadata_prompt(video_title: str, keyword: str = "",
                           include_tags: bool = True) -> str:
    """
    Generate a prompt for metadata generation.

    Args:
        video_title: Title of the video
        keyword: Keyword to focus on
        include_tags: Whether to include tags in the prompt

    Returns:
        str: Generated prompt
    """
    base_prompt = f"""Generate YouTube metadata for a short video titled "{video_title}".

The metadata should include:
1. An engaging, clickable title (max 100 characters)
2. A detailed description that includes relevant information, hashtags, and calls to action (max 5000 characters)"""

    if include_tags:
        base_prompt += f"\n3. A list of relevant tags (at least 5, max 30 characters each)"

    if keyword:
        base_prompt += f"\n\nThe content is related to the keyword: {keyword}. Please optimize the metadata for this keyword."

    base_prompt += "\n\nFormat the response as a JSON object with keys: 'title', 'description'"

    if include_tags:
        base_prompt += ", 'tags'"

    base_prompt += "."

    return base_prompt

def parse_metadata_response(response_text: str) -> Dict[str, Any]:
    """
    Parse the metadata response from the API.

    Args:
        response_text: Response text from the API

    Returns:
        Dict[str, Any]: Parsed metadata
    """
    metadata = {
        "title": "",
        "description": "",
        "tags": []
    }

    # Try to extract JSON
    try:
        # Find JSON block in the response
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            parsed_data = json.loads(json_str)

            # Extract fields
            if isinstance(parsed_data, dict):
                metadata["title"] = parsed_data.get("title", "")
                metadata["description"] = parsed_data.get("description", "")
                metadata["tags"] = parsed_data.get("tags", [])
                return metadata

        # Try direct JSON parsing
        parsed_data = json.loads(response_text)
        if isinstance(parsed_data, dict):
            metadata["title"] = parsed_data.get("title", "")
            metadata["description"] = parsed_data.get("description", "")
            metadata["tags"] = parsed_data.get("tags", [])
            return metadata
    except json.JSONDecodeError:
        pass

    # Fallback to regex extraction
    title_match = re.search(r'"title"\s*:\s*"(.*?)"', response_text, re.DOTALL)
    if title_match:
        metadata["title"] = title_match.group(1).strip()

    desc_match = re.search(r'"description"\s*:\s*"(.*?)"', response_text, re.DOTALL)
    if desc_match:
        metadata["description"] = desc_match.group(1).strip()

    tags_match = re.search(r'"tags"\s*:\s*\[(.*?)\]', response_text, re.DOTALL)
    if tags_match:
        tags_str = tags_match.group(1)
        # Extract tags from the string
        tags = re.findall(r'"(.*?)"', tags_str)
        metadata["tags"] = [tag.strip() for tag in tags if tag.strip()]

    return metadata

def generate_metadata(prompt: str, metrics: Dict[str, Any],
                     timeout: int = DEFAULT_API_TIMEOUT,
                     retries: int = DEFAULT_API_RETRIES) -> Tuple[Dict[str, Any], bool]:
    """
    Generate metadata using the Google Generative AI API.

    Args:
        prompt: Prompt for metadata generation
        metrics: Metrics dictionary to update
        timeout: API timeout in seconds
        retries: Number of API retries

    Returns:
        Tuple[Dict[str, Any], bool]: Tuple of (metadata, success)
    """
    if not GENAI_AVAILABLE:
        logger.error("Google Generative AI not available. Cannot generate metadata.")
        return {"title": "", "description": "", "tags": []}, False

    # Update API call count
    metrics[TOTAL_API_CALLS] = metrics.get(TOTAL_API_CALLS, 0) + 1

    # Initialize metadata
    metadata = {
        "title": "",
        "description": "",
        "tags": []
    }

    # Try to generate metadata
    for attempt in range(retries):
        try:
            # Create a model - using gemini-2.0-flash as specified
            try:
                model = genai.GenerativeModel('gemini-2.0-flash')
                logger.info("Using gemini-2.0-flash model")
            except Exception as model_error:
                # Fallback options if the specified model is not available
                try:
                    # Try other model names
                    model = genai.GenerativeModel('gemini-pro')
                    logger.info("Fallback to gemini-pro model")
                except Exception:
                    try:
                        # Get available models and use the first one
                        available_models = genai.list_models()
                        if available_models:
                            model_name = available_models[0].name
                            logger.info(f"Using available model: {model_name}")
                            model = genai.GenerativeModel(model_name)
                        else:
                            raise Exception("No available models found")
                    except Exception as e:
                        # Re-raise the original error if all attempts fail
                        logger.error(f"Failed to initialize any Gemini model: {model_error}")
                        raise model_error

            # Generate content
            # Note: timeout parameter is not supported in newer versions of the API
            try:
                response = model.generate_content(prompt, timeout=timeout)
            except TypeError:
                # Fallback for newer versions that don't support timeout
                response = model.generate_content(prompt)

            # Parse response
            if hasattr(response, 'text'):
                response_text = response.text
                metadata = parse_metadata_response(response_text)

                # Validate metadata
                if not metadata["title"]:
                    metrics[EMPTY_TITLE_ERRORS] = metrics.get(EMPTY_TITLE_ERRORS, 0) + 1
                    logger.warning("Empty title in generated metadata")
                    continue

                if not metadata["description"]:
                    metrics[EMPTY_DESCRIPTION_ERRORS] = metrics.get(EMPTY_DESCRIPTION_ERRORS, 0) + 1
                    logger.warning("Empty description in generated metadata")
                    continue

                if not metadata["tags"]:
                    metrics[EMPTY_TAGS_ERRORS] = metrics.get(EMPTY_TAGS_ERRORS, 0) + 1
                    logger.warning("Empty tags in generated metadata")
                    # Continue anyway, as tags are optional

                return metadata, True
            else:
                metrics[PARSE_FAILURES] = metrics.get(PARSE_FAILURES, 0) + 1
                logger.warning(f"Failed to parse API response (attempt {attempt + 1}/{retries})")

                # Exponential backoff
                if attempt < retries - 1:
                    backoff_time = DEFAULT_API_BACKOFF ** attempt
                    time.sleep(backoff_time)
        except TimeoutError:
            metrics[TIMEOUTS] = metrics.get(TIMEOUTS, 0) + 1
            logger.warning(f"API timeout (attempt {attempt + 1}/{retries})")

            # Exponential backoff
            if attempt < retries - 1:
                backoff_time = DEFAULT_API_BACKOFF ** attempt
                time.sleep(backoff_time)
        except Exception as e:
            metrics[PARSE_FAILURES] = metrics.get(PARSE_FAILURES, 0) + 1
            logger.error(f"Error generating metadata (attempt {attempt + 1}/{retries}): {e}")

            # Exponential backoff
            if attempt < retries - 1:
                backoff_time = DEFAULT_API_BACKOFF ** attempt
                time.sleep(backoff_time)

    # All attempts failed
    return metadata, False

def validate_metadata(metadata: Dict[str, Any], original_title: str,
                     keyword: str = "", metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Validate and clean up metadata.

    Args:
        metadata: Metadata to validate
        original_title: Original video title
        keyword: Keyword to check for
        metrics: Metrics dictionary to update

    Returns:
        Dict[str, Any]: Validated metadata
    """
    validated = metadata.copy()

    # Initialize metrics if not provided
    if metrics is None:
        metrics = {}

    # Validate title
    if validated.get("title"):
        # Truncate title if too long
        if len(validated["title"]) > MAX_TITLE_LENGTH:
            validated["title"] = validated["title"][:MAX_TITLE_LENGTH]

        # Check if title is similar to original
        if original_title and original_title.lower() not in validated["title"].lower():
            metrics[VALIDATION_TITLE_MISMATCHES] = metrics.get(VALIDATION_TITLE_MISMATCHES, 0) + 1
            logger.warning(f"Title mismatch: '{validated['title']}' does not contain '{original_title}'")

    # Validate description
    if validated.get("description"):
        # Truncate description if too long
        if len(validated["description"]) > MAX_DESCRIPTION_LENGTH:
            validated["description"] = validated["description"][:MAX_DESCRIPTION_LENGTH]

        # Check for keyword stuffing
        if keyword:
            keyword_lower = keyword.lower()
            description_lower = validated["description"].lower()

            # Count keyword occurrences
            keyword_count = description_lower.count(keyword_lower)
            word_count = len(description_lower.split())

            if word_count > 0:
                keyword_ratio = keyword_count / word_count

                if keyword_ratio > MAX_KEYWORD_STUFFING_RATIO:
                    metrics[VALIDATION_KEYWORD_STUFFING] = metrics.get(VALIDATION_KEYWORD_STUFFING, 0) + 1
                    logger.warning(f"Keyword stuffing detected: '{keyword}' appears {keyword_count} times in description")

    # Validate tags
    if validated.get("tags"):
        # Ensure tags is a list
        if not isinstance(validated["tags"], list):
            if isinstance(validated["tags"], str):
                # Convert comma-separated string to list
                validated["tags"] = [tag.strip() for tag in validated["tags"].split(",") if tag.strip()]
            else:
                validated["tags"] = []
                metrics[VALIDATION_TAG_LIST_ERRORS] = metrics.get(VALIDATION_TAG_LIST_ERRORS, 0) + 1
                logger.warning("Tags is not a list or string")

        # Clean up tags
        cleaned_tags = []
        for tag in validated["tags"]:
            # Skip empty tags
            if not tag:
                continue

            # Truncate tag if too long
            if len(tag) > MAX_TAG_LENGTH:
                tag = tag[:MAX_TAG_LENGTH]

            # Remove special characters
            tag = re.sub(r'[^\w\s]', '', tag).strip()

            if tag:
                cleaned_tags.append(tag)

        # Ensure we have enough tags
        if len(cleaned_tags) < MIN_TAGS:
            metrics[VALIDATION_TAG_LIST_ERRORS] = metrics.get(VALIDATION_TAG_LIST_ERRORS, 0) + 1
            logger.warning(f"Not enough tags: {len(cleaned_tags)} < {MIN_TAGS}")

            # Add keyword as a tag if provided
            if keyword and keyword not in cleaned_tags:
                cleaned_tags.append(keyword)

        # Limit number of tags
        if len(cleaned_tags) > MAX_TAGS:
            cleaned_tags = cleaned_tags[:MAX_TAGS]

        validated["tags"] = cleaned_tags

    return validated

def improve_metadata(metadata: Dict[str, Any], keyword: str = "",
                    metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Improve existing metadata.

    Args:
        metadata: Existing metadata
        keyword: Keyword to focus on
        metrics: Metrics dictionary to update

    Returns:
        Dict[str, Any]: Improved metadata
    """
    if not GENAI_AVAILABLE:
        logger.error("Google Generative AI not available. Cannot improve metadata.")
        return metadata

    # Initialize metrics if not provided
    if metrics is None:
        metrics = {}

    # Update API call count
    metrics[TOTAL_API_CALLS] = metrics.get(TOTAL_API_CALLS, 0) + 1

    # Generate improvement prompt
    prompt = f"""Improve the following YouTube metadata:

Title: {metadata.get('title', '')}
Description: {metadata.get('description', '')}
Tags: {', '.join(metadata.get('tags', []))}

Make the title more engaging and clickable (max 100 characters).
Make the description more detailed and include relevant information, hashtags, and calls to action (max 5000 characters).
Improve the tags to be more relevant and searchable (at least 5, max 30 characters each).
"""

    if keyword:
        prompt += f"\nOptimize the metadata for the keyword: {keyword}."

    prompt += "\n\nFormat the response as a JSON object with keys: 'title', 'description', 'tags'."

    try:
        # Create a model - using gemini-2.0-flash as specified
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("Using gemini-2.0-flash model for metadata improvement")
        except Exception as model_error:
            # Fallback options if the specified model is not available
            try:
                model = genai.GenerativeModel('gemini-pro')
                logger.info("Fallback to gemini-pro model for metadata improvement")
            except Exception:
                # Re-raise the original error if all attempts fail
                logger.error(f"Failed to initialize any Gemini model for metadata improvement: {model_error}")
                raise model_error

        # Generate content
        # Note: timeout parameter is not supported in newer versions of the API
        try:
            response = model.generate_content(prompt, timeout=DEFAULT_API_TIMEOUT)
        except TypeError:
            # Fallback for newer versions that don't support timeout
            response = model.generate_content(prompt)

        # Parse response
        if hasattr(response, 'text'):
            response_text = response.text
            improved = parse_metadata_response(response_text)

            # Validate improved metadata
            if not improved["title"]:
                improved["title"] = metadata.get("title", "")
                metrics[EMPTY_TITLE_ERRORS] = metrics.get(EMPTY_TITLE_ERRORS, 0) + 1
                logger.warning("Empty title in improved metadata")

            if not improved["description"]:
                improved["description"] = metadata.get("description", "")
                metrics[EMPTY_DESCRIPTION_ERRORS] = metrics.get(EMPTY_DESCRIPTION_ERRORS, 0) + 1
                logger.warning("Empty description in improved metadata")

            if not improved["tags"]:
                improved["tags"] = metadata.get("tags", [])
                metrics[EMPTY_TAGS_ERRORS] = metrics.get(EMPTY_TAGS_ERRORS, 0) + 1
                logger.warning("Empty tags in improved metadata")

            # Validate and clean up
            return validate_metadata(improved, metadata.get("title", ""), keyword, metrics)
        else:
            metrics[PARSE_FAILURES] = metrics.get(PARSE_FAILURES, 0) + 1
            logger.warning("Failed to parse API response for metadata improvement")
            return metadata
    except Exception as e:
        metrics[PARSE_FAILURES] = metrics.get(PARSE_FAILURES, 0) + 1
        logger.error(f"Error improving metadata: {e}")
        return metadata

def analyze_metadata_quality(metadata: Dict[str, Any], keyword: str = "") -> Dict[str, float]:
    """
    Analyze the quality of metadata.

    Args:
        metadata: Metadata to analyze
        keyword: Keyword to check for

    Returns:
        Dict[str, float]: Quality scores
    """
    scores = {
        "title_score": 0.0,
        "description_score": 0.0,
        "tags_score": 0.0,
        "keyword_score": 0.0,
        "overall_score": 0.0
    }

    # Title quality
    title = metadata.get("title", "")
    if title:
        # Length score (optimal length is 50-70 characters)
        title_length = len(title)
        if 50 <= title_length <= 70:
            length_score = 1.0
        elif 30 <= title_length < 50 or 70 < title_length <= 100:
            length_score = 0.8
        else:
            length_score = 0.5

        # Engagement score (presence of engaging words)
        engaging_words = ["how", "why", "best", "top", "ultimate", "guide", "tutorial", "review", "tips", "secrets"]
        engagement_score = 0.0
        for word in engaging_words:
            if word.lower() in title.lower():
                engagement_score += 0.2
        engagement_score = min(1.0, engagement_score)

        # Calculate title score
        scores["title_score"] = (length_score + engagement_score) / 2

    # Description quality
    description = metadata.get("description", "")
    if description:
        # Length score
        desc_length = len(description)
        if desc_length >= 1000:
            length_score = 1.0
        elif 500 <= desc_length < 1000:
            length_score = 0.8
        elif 200 <= desc_length < 500:
            length_score = 0.6
        elif 100 <= desc_length < 200:
            length_score = 0.4
        else:
            length_score = 0.2

        # Structure score (presence of paragraphs, links, hashtags)
        structure_score = 0.0
        if "\n\n" in description:
            structure_score += 0.3  # Multiple paragraphs
        if "http" in description:
            structure_score += 0.3  # Contains links
        if "#" in description:
            structure_score += 0.4  # Contains hashtags

        # Calculate description score
        scores["description_score"] = (length_score + structure_score) / 2

    # Tags quality
    tags = metadata.get("tags", [])
    if tags:
        # Count score
        count_score = min(1.0, len(tags) / 20)

        # Length score (average tag length, optimal is 15-25 characters)
        avg_length = sum(len(tag) for tag in tags) / len(tags) if tags else 0
        if 15 <= avg_length <= 25:
            length_score = 1.0
        elif 10 <= avg_length < 15 or 25 < avg_length <= 30:
            length_score = 0.8
        else:
            length_score = 0.6

        # Calculate tags score
        scores["tags_score"] = (count_score + length_score) / 2

    # Keyword optimization
    if keyword:
        keyword_lower = keyword.lower()
        keyword_score = 0.0

        # Check title
        if keyword_lower in title.lower():
            keyword_score += 0.4

        # Check description
        if keyword_lower in description.lower():
            # Count occurrences
            keyword_count = description.lower().count(keyword_lower)
            word_count = len(description.split())

            if word_count > 0:
                keyword_ratio = keyword_count / word_count

                # Optimal ratio is 0.01-0.05
                if 0.01 <= keyword_ratio <= 0.05:
                    keyword_score += 0.4
                elif 0.05 < keyword_ratio <= 0.1:
                    keyword_score += 0.3
                elif 0.1 < keyword_ratio <= 0.2:
                    keyword_score += 0.2
                elif keyword_ratio > 0.2:
                    keyword_score += 0.1  # Keyword stuffing penalty

        # Check tags
        if any(keyword_lower in tag.lower() for tag in tags):
            keyword_score += 0.2

        scores["keyword_score"] = keyword_score

    # Calculate overall score
    weights = {
        "title_score": 0.3,
        "description_score": 0.3,
        "tags_score": 0.2,
        "keyword_score": 0.2
    }

    overall_score = sum(scores[key] * weights[key] for key in weights)
    scores["overall_score"] = overall_score

    return scores
