# --- START OF FILE youtube_limits.py ---

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Limits Validation Module

This module provides functions to validate and enforce YouTube's limits for
video metadata such as descriptions and tags. It handles edge cases and provides
detailed warnings when limits are enforced.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.5.0 # Match version used elsewhere if consistent
"""

import re
from typing import List, Tuple, Any

# --- YouTube Limits Constants (Defaults) ---
# These act as fallbacks if not provided by the calling script

# YouTube description character limit
DEFAULT_YOUTUBE_DESCRIPTION_LIMIT = 4950 # Safe default below 5000

# YouTube individual tag character limit
DEFAULT_YOUTUBE_TAG_LIMIT = 100

# Adjusted total tags limit (accounts for implicit quotes around tags with spaces)
# YouTube adds 2 quote chars per tag with spaces. This limit aims for safety below ~500 actual.
DEFAULT_YOUTUBE_TOTAL_TAGS_LIMIT = 460

# Maximum number of tags allowed
DEFAULT_YOUTUBE_MAX_TAGS_COUNT = 40 # Current limit is often cited around 30-60, 40 is safe middle ground

# YouTube title character limit
DEFAULT_YOUTUBE_TITLE_LIMIT = 100

# --- End Constants ---


def validate_title(
    title: Any, # Accept Any type initially for robustness
    limit: int = DEFAULT_YOUTUBE_TITLE_LIMIT,
    add_ellipsis: bool = True
) -> Tuple[str, List[str]]:
    """
    Validates and truncates a video title to meet YouTube's character limit.

    Handles various edge cases including:
    - None or non-string inputs
    - Empty or whitespace-only titles
    - Titles exceeding the character limit
    - Removal of problematic characters

    Args:
        title: The original video title string.
        limit: The character limit to enforce (default: 100).
        add_ellipsis: Whether to add ellipsis (...) when truncating (default: True).

    Returns:
        A tuple containing:
            - The validated (potentially truncated) title string.
            - A list of warning messages generated during validation.
    """
    warnings = []

    # 1. Input Type Handling & Conversion
    if title is None:
        warnings.append("Title is None, returning empty string.")
        return "", warnings

    if not isinstance(title, (str, int, float, bool)):
        warnings.append(f"Title is not a string-compatible type ({type(title).__name__}), converting to string.")

    try:
        title_str = str(title) # Convert potential numbers/bools to string
    except Exception as e:
        warnings.append(f"Error converting title to string: {e}. Returning empty string.")
        return "", warnings

    # 2. Handle Empty/Whitespace Title
    if not title_str.strip():
        warnings.append("Title is empty or contains only whitespace.")
        return "", warnings

    # 3. Validate Limit Parameter
    if not isinstance(limit, int) or limit <= 0:
        warnings.append(f"Invalid title limit value: {limit}. Using default: {DEFAULT_YOUTUBE_TITLE_LIMIT}")
        limit = DEFAULT_YOUTUBE_TITLE_LIMIT

    # 4. Clean Problematic Characters (Control Chars except \n\r\t)
    original_length = len(title_str)
    cleaned_title = ''.join(char for char in title_str if ord(char) >= 32 or char in '\n\r\t')
    if len(cleaned_title) != original_length:
        warnings.append(f"Removed {original_length - len(cleaned_title)} invalid control characters from title.")

    # 5. Truncation Logic
    validated_title = cleaned_title # Start with the cleaned title
    if len(cleaned_title) > limit:
        warnings.append(f"Title length ({len(cleaned_title)}) exceeds limit ({limit}), truncating.")

        # Find the last space within the limit for cleaner truncation
        truncated_part = cleaned_title[:limit]
        last_space = truncated_part.rfind(' ')

        # Truncate at word boundary if space is found reasonably close to the end
        # (e.g., within the last 20% of the allowed limit)
        if last_space > limit * 0.8:
            validated_title = truncated_part[:last_space].strip()
            warnings.append(f"Truncated at word boundary (position {last_space}).")
        else:
            # Hard truncation if no suitable space found near the end
            validated_title = truncated_part.strip()
            warnings.append("Hard truncation applied (no suitable space found near limit).")

        # Add ellipsis if requested and space allows
        if add_ellipsis and validated_title:
            ellipsis = "..."
            ellipsis_len = len(ellipsis)
            if len(validated_title) + ellipsis_len <= limit:
                validated_title += ellipsis
            else:
                # Make room for ellipsis if necessary
                validated_title = validated_title[:limit - ellipsis_len] + ellipsis
    else:
        validated_title = cleaned_title # Use cleaned title if within limit

    # 6. Final check for empty title after potential truncation/cleaning
    if not validated_title.strip():
         warnings.append("Title became empty after cleaning/truncation.")
         return "", warnings

    return validated_title, warnings


def validate_description(
    description: Any, # Accept Any type
    limit: int = DEFAULT_YOUTUBE_DESCRIPTION_LIMIT
) -> Tuple[str, List[str]]:
    """
    Validates and truncates a description to meet YouTube's character limit.

    Handles various edge cases including:
    - None or non-string inputs
    - Empty or whitespace-only descriptions
    - Descriptions exceeding the character limit
    - Smart truncation to avoid cutting words in the middle
    - Removal of problematic characters

    Args:
        description: The original video description string.
        limit: The character limit to enforce (default: 4950).

    Returns:
        A tuple containing:
            - The validated (potentially truncated) description string.
            - A list of warning messages generated during validation.
    """
    warnings = []

    # 1. Input Type Handling & Conversion
    if description is None:
        warnings.append("Description is None, returning empty string.")
        return "", warnings

    if not isinstance(description, (str, int, float, bool)):
        warnings.append(f"Description is not a string-compatible type ({type(description).__name__}), converting to string.")

    try:
        desc_str = str(description)
    except Exception as e:
        warnings.append(f"Error converting description to string: {e}. Returning empty string.")
        return "", warnings

    # 2. Handle Empty/Whitespace Description
    if not desc_str.strip():
        warnings.append("Description is empty or contains only whitespace.")
        return "", warnings

    # 3. Validate Limit Parameter
    if not isinstance(limit, int) or limit <= 0:
        warnings.append(f"Invalid description limit value: {limit}. Using default: {DEFAULT_YOUTUBE_DESCRIPTION_LIMIT}")
        limit = DEFAULT_YOUTUBE_DESCRIPTION_LIMIT

    # 4. Clean Problematic Characters
    original_length = len(desc_str)
    cleaned_desc = ''.join(char for char in desc_str if ord(char) >= 32 or char in '\n\r\t')
    if len(cleaned_desc) != original_length:
        warnings.append(f"Removed {original_length - len(cleaned_desc)} invalid control characters from description.")

    # 5. Truncation Logic
    validated_description = cleaned_desc # Start with cleaned description
    if len(cleaned_desc) > limit:
        warnings.append(f"Description length ({len(cleaned_desc)}) exceeds limit ({limit}), truncating.")

        # Find the last sensible break point within the limit
        truncated_part = cleaned_desc[:limit]
        last_paragraph = truncated_part.rfind('\n\n')
        last_newline = truncated_part.rfind('\n')
        last_space = truncated_part.rfind(' ')

        # Prioritize truncating at paragraph, then newline, then space
        if last_paragraph > limit * 0.8: # Found paragraph break near end
            validated_description = truncated_part[:last_paragraph].strip()
            warnings.append(f"Truncated at paragraph break (position {last_paragraph}).")
        elif last_newline > limit * 0.9: # Found newline near end
            validated_description = truncated_part[:last_newline].strip()
            warnings.append(f"Truncated at newline (position {last_newline}).")
        elif last_space > limit * 0.95: # Found space near end
            validated_description = truncated_part[:last_space].strip()
            warnings.append(f"Truncated at word boundary (position {last_space}).")
        else: # Hard truncation
            validated_description = truncated_part.strip()
            warnings.append("Hard truncation applied (no suitable break point found near limit).")

        # Add ellipsis to indicate truncation if space allows
        ellipsis = "..."
        if validated_description and not validated_description.endswith(ellipsis):
             if len(validated_description) + len(ellipsis) <= limit:
                 validated_description += ellipsis
             else: # Make space for ellipsis
                 validated_description = validated_description[:limit - len(ellipsis)] + ellipsis
    else:
        validated_description = cleaned_desc # Use cleaned description if within limit

    # 6. Final check for empty description
    if not validated_description.strip():
        warnings.append("Description became empty after cleaning/truncation.")
        return "", warnings

    return validated_description, warnings


def validate_tags(
    tags: Any, # Accept Any type
    tag_char_limit: int = DEFAULT_YOUTUBE_TAG_LIMIT,
    total_char_limit: int = DEFAULT_YOUTUBE_TOTAL_TAGS_LIMIT,
    max_count_limit: int = DEFAULT_YOUTUBE_MAX_TAGS_COUNT,
    prioritize_shorter_tags: bool = False,
    preserve_order: bool = True
) -> Tuple[List[str], List[str]]:
    """
    Validates and optimizes a list of tags to meet YouTube's limits, accounting for implicit quotes.

    Args:
        tags: A list of tag strings (or something convertible to a list).
        tag_char_limit: Max characters per individual tag.
        total_char_limit: Max total effective characters for all tags combined.
        max_count_limit: Max number of tags allowed.
        prioritize_shorter_tags: If True and preserve_order is False, keeps shorter tags first when truncating.
        preserve_order: If True, maintains the original order when applying limits.

    Returns:
        A tuple containing:
            - The validated list of tag strings.
            - A list of warning messages generated during validation.
    """
    warnings = []

    # 1. Input Type Handling
    if tags is None: tags = []
    if not isinstance(tags, list):
        warnings.append(f"Tags input is not a list ({type(tags).__name__}). Attempting conversion.")
        try: tags = list(tags)
        except TypeError: warnings.append("Could not convert tags to list. Using empty list."); return [], warnings
        except Exception as e: warnings.append(f"Unexpected error converting tags: {e}. Using empty list."); return [], warnings

    # 2. Validate Limit Parameters
    if not isinstance(tag_char_limit, int) or tag_char_limit <= 0: warnings.append(f"Invalid tag_char_limit. Using default: {DEFAULT_YOUTUBE_TAG_LIMIT}"); tag_char_limit = DEFAULT_YOUTUBE_TAG_LIMIT
    if not isinstance(total_char_limit, int) or total_char_limit <= 0: warnings.append(f"Invalid total_char_limit. Using default: {DEFAULT_YOUTUBE_TOTAL_TAGS_LIMIT}"); total_char_limit = DEFAULT_YOUTUBE_TOTAL_TAGS_LIMIT
    if not isinstance(max_count_limit, int) or max_count_limit <= 0: warnings.append(f"Invalid max_count_limit. Using default: {DEFAULT_YOUTUBE_MAX_TAGS_COUNT}"); max_count_limit = DEFAULT_YOUTUBE_MAX_TAGS_COUNT

    # 3. Clean, Normalize, Calculate Effective Lengths, Remove Duplicates
    tag_info = []
    seen_tags_lower = set() # Use lowercase for duplicate check
    skipped_initial = 0

    for i, tag in enumerate(tags):
        if tag is None: skipped_initial += 1; continue
        try: tag_str = str(tag).strip() # Convert to string and strip whitespace
        except: warnings.append(f"Could not convert tag at index {i} to string. Skipping."); skipped_initial += 1; continue
        if not tag_str: skipped_initial += 1; continue # Skip empty

        tag_lower = tag_str.lower()
        if tag_lower in seen_tags_lower: skipped_initial += 1; continue # Skip duplicate
        seen_tags_lower.add(tag_lower)

        # Truncate individual tag if needed *before* calculating effective length
        original_tag = tag_str
        if len(tag_str) > tag_char_limit:
            tag_str = tag_str[:tag_char_limit].strip()
            warnings.append(f"Tag '{original_tag[:30]}...' truncated to '{tag_str}'.")
            # Recheck for emptiness after truncation
            if not tag_str: skipped_initial += 1; continue

        # Calculate effective length (add 2 for quotes if space exists)
        has_spaces = ' ' in tag_str
        effective_length = len(tag_str) + (2 if has_spaces else 0)

        tag_info.append({
            'original_tag': original_tag, # Keep original for reference
            'tag': tag_str, # The potentially truncated tag
            'raw_length': len(tag_str),
            'effective_length': effective_length
        })

    if skipped_initial > 0: warnings.append(f"Skipped {skipped_initial} initial tags (None, empty, duplicate).")
    if not tag_info: warnings.append("No valid tags remaining after initial cleaning."); return [], warnings

    # 4. Sort if requested (and order doesn't need preserving)
    if not preserve_order:
        if prioritize_shorter_tags: tag_info.sort(key=lambda x: x['effective_length']) # Shortest first
        else: tag_info.sort(key=lambda x: x['raw_length'], reverse=True) # Longest first (often better SEO)
        warnings.append("Tags reordered based on sorting criteria.")

    # 5. Apply Limits (Count and Total Length)
    validated_tags = []
    current_total_chars = 0
    skipped_limits = 0

    for info in tag_info:
        tag = info['tag']
        effective_length = info['effective_length']

        # Check max tag count
        if len(validated_tags) >= max_count_limit:
            skipped_limits += 1
            continue # Stop adding tags

        # Check total character limit
        # Add 1 for comma separator if it's not the first tag being added
        separator_len = 1 if validated_tags else 0
        prospective_total = current_total_chars + effective_length + separator_len

        if prospective_total <= total_char_limit:
            validated_tags.append(tag)
            current_total_chars = prospective_total
        else:
            skipped_limits += 1 # Tag doesn't fit

    if skipped_limits > 0: warnings.append(f"Skipped {skipped_limits} tags due to exceeding max count ({max_count_limit}) or total character limit (~{total_char_limit}).")

    # 6. Final check for empty list
    if not validated_tags: warnings.append("No tags remained after applying all limits.")

    return validated_tags, warnings


# --- Example Usage (if run directly) ---
if __name__ == "__main__":
    print("Testing youtube_limits functions...")

    # Test Title Validation
    print("\n--- Title Tests ---")
    titles = [
        "This is a perfectly normal title",
        "This title is definitely way too long because it keeps going on and on and on and doesn't seem to stop anytime soon, exceeding the one hundred character limit imposed by YouTube.",
        None,
        "",
        " Title with spaces ",
        "Title with\x00null char",
        12345
    ]
    for title in titles:
        validated, warnings = validate_title(title)
        print(f"Original: '{title}'")
        print(f"Validated: '{validated}' (Length: {len(validated)})")
        if warnings: print(f"Warnings: {warnings}")
        print("-" * 10)

    # Test Description Validation
    print("\n--- Description Tests ---")
    desc = "This is a short description.\n\nThis is another paragraph."
    long_desc = "Line " * 1000 # ~6000 chars
    validated, warnings = validate_description(desc)
    print(f"Original (Short): '{desc[:50]}...'")
    print(f"Validated: '{validated[:50]}...' (Length: {len(validated)})")
    if warnings: print(f"Warnings: {warnings}")
    print("-" * 10)
    validated, warnings = validate_description(long_desc)
    print(f"Original (Long): '{long_desc[:50]}...' (Length: {len(long_desc)})")
    print(f"Validated: '{validated}' (Length: {len(validated)})") # Print full truncated
    if warnings: print(f"Warnings: {warnings}")
    print("-" * 10)
    validated, warnings = validate_description(None)
    print(f"Original (None): None")
    print(f"Validated: '{validated}' (Length: {len(validated)})")
    if warnings: print(f"Warnings: {warnings}")
    print("-" * 10)

    # Test Tag Validation
    print("\n--- Tag Tests ---")
    tags1 = ["tag1", "tag2", "tag with spaces", "tag1", None, "", "  another tag  ", "a" * 110]
    validated, warnings = validate_tags(tags1)
    print(f"Original: {tags1}")
    print(f"Validated: {validated} (Count: {len(validated)})")
    if warnings: print(f"Warnings: {warnings}")
    print("-" * 10)

    tags2 = ["very long tag that will exceed the limit"] * 30 # Many long tags
    validated, warnings = validate_tags(tags2)
    print(f"Original: Many long tags...")
    print(f"Validated: {validated} (Count: {len(validated)})")
    if warnings: print(f"Warnings: {warnings}")
    print("-" * 10)

    tags3 = [f"tag{i}" for i in range(50)] # Exceed count limit
    validated, warnings = validate_tags(tags3)
    print(f"Original: 50 tags...")
    print(f"Validated: {validated} (Count: {len(validated)})")
    if warnings: print(f"Warnings: {warnings}")
    print("-" * 10)

    tags4 = ["short", "tag", "medium tag", "very very long tag with spaces"]
    validated, warnings = validate_tags(tags4, preserve_order=False, prioritize_shorter_tags=True)
    print(f"Original: {tags4}")
    print(f"Validated (Shortest First): {validated} (Count: {len(validated)})")
    if warnings: print(f"Warnings: {warnings}")
    print("-" * 10)


# --- END OF FILE ---