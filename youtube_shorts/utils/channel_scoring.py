#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Channel Scoring Module

This module provides functions for scoring and analyzing YouTube channels.
"""

from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timedelta
import statistics
import math
import logging
import os

# --- NEW: Import constants from the new location ---
try:
    from . import constants # Assumes channel_scoring.py is in utils/
    CONSTANTS_IMPORTED = True
except ImportError:
    try:
        # Try importing directly if run as a script
        import constants
        CONSTANTS_IMPORTED = True
    except ImportError:
        CONSTANTS_IMPORTED = False
        print("CRITICAL: channel_scoring.py could not import constants.py.")
        # Define minimal fallbacks if really needed
        class MinimalConstants:
            LOGS_DIR = "logs"
        constants = MinimalConstants()
        print("WARNING: channel_scoring.py using minimal fallback constants.")
# --- End NEW Import ---

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers and CONSTANTS_IMPORTED:
    log_dir = constants.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "channel_scoring.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

def calculate_channel_score(
    channel_data: Dict[str, Any],
    view_weight: float = 0.5,
    like_weight: float = 0.3,
    comment_weight: float = 0.2,
    recency_weight: float = 0.4,
    min_views_threshold: int = 1000,
    min_likes_threshold: int = 100,
    min_comments_threshold: int = 10
) -> float:
    """
    Calculate a score for a channel based on its performance metrics.

    Args:
        channel_data: Dictionary containing channel performance data
        view_weight: Weight for view count in scoring
        like_weight: Weight for like count in scoring
        comment_weight: Weight for comment count in scoring
        recency_weight: Weight for recency in scoring
        min_views_threshold: Minimum views for a video to be considered popular
        min_likes_threshold: Minimum likes for a video to be considered popular
        min_comments_threshold: Minimum comments for a video to be considered popular

    Returns:
        float: Channel score
    """
    if not channel_data or "videos" not in channel_data or not channel_data["videos"]:
        return 0.0

    videos = channel_data["videos"]

    # Calculate base metrics
    view_scores = []
    like_scores = []
    comment_scores = []
    recency_scores = []

    now = datetime.now()

    for video in videos:
        # Skip videos with no views or missing data
        if "view_count" not in video or not video["view_count"]:
            continue

        # View score (logarithmic scale)
        view_count = int(video.get("view_count", 0))
        if view_count > 0:
            view_score = math.log10(max(view_count, 10)) / math.log10(min_views_threshold)
            view_scores.append(min(view_score, 10.0))  # Cap at 10

        # Like score (logarithmic scale)
        like_count = int(video.get("like_count", 0))
        if like_count > 0:
            like_score = math.log10(max(like_count, 10)) / math.log10(min_likes_threshold)
            like_scores.append(min(like_score, 10.0))  # Cap at 10

        # Comment score (logarithmic scale)
        comment_count = int(video.get("comment_count", 0))
        if comment_count > 0:
            comment_score = math.log10(max(comment_count, 2)) / math.log10(min_comments_threshold)
            comment_scores.append(min(comment_score, 10.0))  # Cap at 10

        # Recency score (exponential decay)
        upload_date = video.get("upload_date")
        if upload_date:
            try:
                upload_datetime = datetime.strptime(upload_date, "%Y%m%d")
                days_ago = (now - upload_datetime).days
                recency_score = math.exp(-days_ago / 30)  # 30-day half-life
                recency_scores.append(recency_score)
            except (ValueError, TypeError):
                pass

    # If we don't have enough data, return a low score
    if not view_scores:
        return 0.0

    # Calculate weighted average scores
    avg_view_score = statistics.mean(view_scores) if view_scores else 0
    avg_like_score = statistics.mean(like_scores) if like_scores else 0
    avg_comment_score = statistics.mean(comment_scores) if comment_scores else 0
    avg_recency_score = statistics.mean(recency_scores) if recency_scores else 0.5  # Default to middle value

    # Calculate engagement ratio (likes + comments per view)
    engagement_ratio = 0.0
    total_views = sum(int(v.get("view_count", 0)) for v in videos if "view_count" in v)
    total_likes = sum(int(v.get("like_count", 0)) for v in videos if "like_count" in v)
    total_comments = sum(int(v.get("comment_count", 0)) for v in videos if "comment_count" in v)

    if total_views > 0:
        engagement_ratio = (total_likes + total_comments) / total_views

    # Calculate consistency score (lower standard deviation = more consistent)
    consistency_score = 0.0
    if len(view_scores) > 1:
        try:
            view_stdev = statistics.stdev(view_scores)
            consistency_score = 1.0 / (1.0 + view_stdev)  # Normalize to 0-1 range
        except statistics.StatisticsError:
            consistency_score = 0.5  # Default to middle value

    # Calculate final score
    base_score = (
        avg_view_score * view_weight +
        avg_like_score * like_weight +
        avg_comment_score * comment_weight
    )

    # Apply recency and consistency modifiers
    recency_modifier = 0.8 + (avg_recency_score * recency_weight)
    consistency_modifier = 0.8 + (consistency_score * 0.4)

    # Apply engagement ratio bonus (up to 20% boost)
    engagement_bonus = min(engagement_ratio * 10, 0.2)

    final_score = base_score * recency_modifier * consistency_modifier * (1 + engagement_bonus)

    # Normalize to 0-10 scale
    normalized_score = min(final_score, 10.0)

    return round(normalized_score, 2)

def analyze_channel_performance(
    channel_data: Dict[str, Any],
    time_periods: List[int] = [7, 30, 90]
) -> Dict[str, Any]:
    """
    Analyze channel performance over different time periods.

    Args:
        channel_data: Dictionary containing channel performance data
        time_periods: List of time periods in days to analyze

    Returns:
        Dict[str, Any]: Analysis results
    """
    if not channel_data or "videos" not in channel_data or not channel_data["videos"]:
        return {"error": "No channel data available"}

    videos = channel_data["videos"]
    now = datetime.now()

    results = {
        "channel_url": channel_data.get("channel_url", "Unknown"),
        "total_videos": len(videos),
        "periods": {},
        "trends": {},
        "recommendations": []
    }

    # Analyze each time period
    for period in time_periods:
        period_videos = []
        cutoff_date = now - timedelta(days=period)

        for video in videos:
            upload_date = video.get("upload_date")
            if upload_date:
                try:
                    upload_datetime = datetime.strptime(upload_date, "%Y%m%d")
                    if upload_datetime >= cutoff_date:
                        period_videos.append(video)
                except (ValueError, TypeError):
                    continue

        # Skip if no videos in this period
        if not period_videos:
            results["periods"][f"{period}_days"] = {"videos": 0}
            continue

        # Calculate metrics for this period
        total_views = sum(int(v.get("view_count", 0)) for v in period_videos if "view_count" in v)
        total_likes = sum(int(v.get("like_count", 0)) for v in period_videos if "like_count" in v)
        total_comments = sum(int(v.get("comment_count", 0)) for v in period_videos if "comment_count" in v)

        avg_views = total_views / len(period_videos) if period_videos else 0
        avg_likes = total_likes / len(period_videos) if period_videos else 0
        avg_comments = total_comments / len(period_videos) if period_videos else 0

        # Store period results
        results["periods"][f"{period}_days"] = {
            "videos": len(period_videos),
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "avg_views": round(avg_views, 2),
            "avg_likes": round(avg_likes, 2),
            "avg_comments": round(avg_comments, 2)
        }

    # Calculate trends (compare periods)
    if len(time_periods) >= 2:
        time_periods.sort()
        for i in range(len(time_periods) - 1):
            short_period = f"{time_periods[i]}_days"
            long_period = f"{time_periods[i+1]}_days"

            if short_period in results["periods"] and long_period in results["periods"]:
                short_data = results["periods"][short_period]
                long_data = results["periods"][long_period]

                if short_data["videos"] > 0 and long_data["videos"] > 0:
                    # Calculate view trend
                    view_trend = (short_data["avg_views"] / long_data["avg_views"] - 1) * 100 if long_data["avg_views"] > 0 else 0

                    # Store trend results
                    results["trends"][f"{short_period}_vs_{long_period}"] = {
                        "view_trend_percent": round(view_trend, 2),
                        "trend_direction": "up" if view_trend > 5 else "down" if view_trend < -5 else "stable"
                    }

    # Generate recommendations
    if "periods" in results and "7_days" in results["periods"]:
        recent_data = results["periods"]["7_days"]

        # Check if channel is active
        if recent_data["videos"] == 0:
            results["recommendations"].append("Channel appears inactive in the last 7 days")

        # Check engagement
        if recent_data.get("avg_views", 0) > 0:
            engagement_ratio = (recent_data.get("avg_likes", 0) + recent_data.get("avg_comments", 0)) / recent_data.get("avg_views", 1)
            if engagement_ratio < 0.01:
                results["recommendations"].append("Low engagement ratio. Consider channels with more audience interaction")
            elif engagement_ratio > 0.1:
                results["recommendations"].append("High engagement ratio. This channel has an active audience")

    # Check trends
    if "trends" in results:
        for trend_key, trend_data in results["trends"].items():
            if trend_data.get("trend_direction") == "up":
                results["recommendations"].append(f"Channel is trending upward ({trend_key})")
            elif trend_data.get("trend_direction") == "down":
                results["recommendations"].append(f"Channel is trending downward ({trend_key})")

    return results
