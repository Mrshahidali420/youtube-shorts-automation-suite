# Manual Workflow Guide

This guide explains how to use the individual components of the GTA YouTube Automation Tool manually, without relying on the automated pipeline.

## Overview

The manual workflow consists of these main steps:

1. **Download videos with optimized metadata** using keywords or channels
2. **Manually select videos** to process further
3. **Upload videos** to YouTube
4. **Track performance** of uploaded videos

## Step 1: Download Videos with Optimized Metadata

You can download videos using either keywords or channels. Both methods now include integrated metadata optimization.

### Keyword-Based Downloads

```bash
python downloader_keyword.py
```

This will:
- Read the niche from `niche.txt` (should contain "GTA VI")
- Generate keywords related to the niche
- Download videos based on those keywords
- Generate and optimize metadata using AI
- Save videos to `shorts_downloads/` folder
- Save optimized metadata to `shorts_metadata/` folder
- Update the Excel file with downloaded videos

**Optional parameters:**
- `--keyword "your keyword"` - Use a specific keyword instead of generating from niche
- `--max 5` - Download up to 5 videos (default is from config.txt)

Example:
```bash
python downloader_keyword.py --keyword "GTA 6 trailer" --max 3
```

### Channel-Based Downloads

```bash
python downloader_channel.py
```

This will:
- Read channel URLs from `channels.txt`
- Download videos from those channels
- Generate and optimize metadata using AI
- Save videos and metadata in the same format as keyword-based downloads

**Optional parameters:**
- `--channel "https://www.youtube.com/@ChannelName"` - Download from a specific channel
- `--max 5` - Download up to 5 videos per channel

Example:
```bash
python downloader_channel.py --channel "https://www.youtube.com/@RockstarGames" --max 3
```

## Step 2: Manually Select Videos

After downloading videos with optimized metadata, you need to manually select which ones to upload:

1. Open the `shorts_data.xlsx` file and review the "Downloaded" sheet
2. Look at the video files in `shorts_downloads/` to determine which ones are suitable
3. Review the metadata files in `shorts_metadata/` to see the optimized titles, descriptions, and tags
4. You can optionally edit the metadata files to make manual adjustments
5. Make note of which videos you want to upload (you can create a list or rename files)

## Step 3: Prepare for Upload (Optional)

If you want to schedule videos for upload at specific times, you can:

1. Create a `scheduled_videos/` folder if it doesn't exist:
   ```bash
   mkdir -p scheduled_videos
   ```

2. Copy the selected video files and their metadata to the `scheduled_videos/` folder:
   ```bash
   # For each video you want to upload (replace "video1" with actual filename)
   cp shorts_downloads/video1.mp4 scheduled_videos/
   cp shorts_metadata/video1.json scheduled_videos/
   ```

3. Edit the metadata files to include scheduling information if desired

## Step 4: Upload Videos

```bash
python uploader.py
```

This will:
- Upload videos from the `shorts_downloads/` folder to YouTube (or from `scheduled_videos/` if you created it)
- Use the optimized metadata from `shorts_metadata/` folder
- Update the Excel file with upload status

**Optional parameters:**
- `--max 3` - Upload up to 3 videos
- `--schedule-only` - Only schedule videos, don't publish immediately
- `--analyze` - Analyze upload errors and suggest improvements
- `--folder "path/to/folder"` - Specify a different folder containing videos to upload

Example:
```bash
python uploader.py --max 3 --schedule-only
```

## Step 5: Track Performance

```bash
python performance_tracker.py
```

This will:
- Track the performance of uploaded videos
- Update the Excel file with performance metrics
- Generate performance reports

**Optional parameters:**
- `--days 7` - Track performance for the last 7 days
- `--video-id "youtube_video_id"` - Track a specific video

Example:
```bash
python performance_tracker.py --days 7
```

## Configuration

All components use the same configuration files:

- `config.txt` - Main configuration file
- `niche.txt` - Contains the niche (e.g., "GTA VI")
- `channels.txt` - Contains channel URLs (for channel-based downloads)

Make sure to set your API keys and other settings in `config.txt` before running any components. The script is configured to use Gemini 2.0 Flash for AI-generated metadata.

## Data Files

- `shorts_data.xlsx` - Excel file tracking downloaded and uploaded videos
- `generated_keywords_cache.json` - Cache of generated keywords
- `metadata_metrics.json` - Tracks metadata generation and optimization metrics
- `performance_metrics.json` - Tracks overall performance metrics
- `upload_correlation_cache.json` - Links videos with their discovery keywords and YouTube IDs

## Folders

- `shorts_downloads/` - Where downloaded videos are stored
- `shorts_metadata/` - Where optimized metadata files are stored
- `scheduled_videos/` - Optional folder where you can place videos ready for upload
- `analytics_data/` - Analytics data cache

## Data Flow Between Steps

1. **Download & Optimize**: Videos are downloaded to `shorts_downloads/` and optimized metadata to `shorts_metadata/`
2. **Select**: You manually select which videos to upload (by reviewing files or creating a list)
3. **Schedule** (Optional): You can copy videos and metadata to `scheduled_videos/` for scheduled uploading
4. **Upload**: Videos are uploaded from `shorts_downloads/` (or `scheduled_videos/` if used) to YouTube
5. **Track**: Performance is tracked for uploaded videos

## Tips for Manual Workflow

1. **Start small**: Begin with downloading just a few videos (use `--max 3`)
2. **Check the Excel file**: After each step, check `shorts_data.xlsx` to see the status
3. **Inspect metadata**: Look at the JSON files to verify the quality of the optimized metadata
4. **Edit metadata if needed**: You can manually edit the JSON files to make adjustments
5. **Run one step at a time**: Complete each step before moving to the next
6. **Use command-line arguments**: Customize each run with specific parameters
7. **Create a batch file**: Consider creating a batch file with all the commands for your workflow

## Troubleshooting

- If downloads fail, check your API key in `config.txt`
- If metadata optimization fails during download, check your Gemini API key
- If uploads fail, make sure Firefox is installed and the profile path is correct
- If Excel operations fail, close Excel before running the scripts
- If you see errors about missing directories, make sure all required folders exist

For more detailed information, refer to the main README.md file.
