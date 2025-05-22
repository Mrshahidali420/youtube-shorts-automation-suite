@echo off
setlocal enabledelayedexpansion
REM YouTube Shorts Automation - Script Runner
REM This batch file provides an easy way to run the various scripts in the project

REM Set title
title YouTube Shorts Automation - Script Runner

:main_menu
cls
echo =====================================================
echo   YouTube Shorts Automation - Script Runner v1.0
echo =====================================================
echo.
echo MAIN MENU:
echo.
echo 1. Download Videos
echo 2. Upload Videos
echo 3. Performance Tracking
echo 4. Utilities
echo 5. Maintenance
echo 6. Exit
echo.
set /p main_choice=Enter your choice (1-6):

if "%main_choice%"=="1" goto download_menu
if "%main_choice%"=="2" goto upload_menu
if "%main_choice%"=="3" goto performance_menu
if "%main_choice%"=="4" goto utilities_menu
if "%main_choice%"=="5" goto maintenance_menu
if "%main_choice%"=="6" goto end

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto main_menu

:download_menu
cls
echo =====================================================
echo   Download Videos
echo =====================================================
echo.
echo 1. Download videos by keyword
echo 2. Download videos by channel
echo 3. Back to main menu
echo.
set /p download_choice=Enter your choice (1-3):

if "%download_choice%"=="1" goto download_keyword
if "%download_choice%"=="2" goto download_channel
if "%download_choice%"=="3" goto main_menu

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto download_menu

:download_keyword
cls
echo =====================================================
echo   Download Videos by Keyword
echo =====================================================
echo.
set /p keyword=Enter keyword (leave empty to use niche.txt):
set /p max=Enter maximum number of videos to download (leave empty for default):

set cmd=python -m youtube_shorts.downloader_keyword

if not "%keyword%"=="" (
    set cmd=!cmd! --keyword "%keyword%"
)

if not "%max%"=="" (
    set cmd=!cmd! --max %max%
)

echo.
echo Running command: !cmd!
echo.
!cmd!

echo.
echo Operation completed.
pause
goto download_menu

:download_channel
cls
echo =====================================================
echo   Download Videos by Channel
echo =====================================================
echo.
set /p channel=Enter channel URL (leave empty to use channels.txt):
set /p max=Enter maximum number of videos to download (leave empty for default):

set cmd=python -m youtube_shorts.downloader_channel

if not "%channel%"=="" (
    set cmd=!cmd! --channel "%channel%"
)

if not "%max%"=="" (
    set cmd=!cmd! --max %max%
)

echo.
echo Running command: !cmd!
echo.
!cmd!

echo.
echo Operation completed.
pause
goto download_menu

:upload_menu
cls
echo =====================================================
echo   Upload Videos
echo =====================================================
echo.
echo 1. Upload videos (standard)
echo 2. Upload videos (publish immediately)
echo 3. Upload videos (schedule only)
echo 4. Analyze upload errors
echo 5. Back to main menu
echo.
set /p upload_choice=Enter your choice (1-5):

if "%upload_choice%"=="1" goto upload_standard
if "%upload_choice%"=="2" goto upload_publish
if "%upload_choice%"=="3" goto upload_schedule
if "%upload_choice%"=="4" goto upload_analyze
if "%upload_choice%"=="5" goto main_menu

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto upload_menu

:upload_standard
cls
echo =====================================================
echo   Upload Videos (Standard)
echo =====================================================
echo.
set /p max=Enter maximum number of videos to upload (leave empty for default):

set cmd=python -m youtube_shorts.uploader

if not "%max%"=="" (
    set cmd=!cmd! --max %max%
)

echo.
echo Running command: !cmd!
echo.
!cmd!

echo.
echo Operation completed.
pause
goto upload_menu

:upload_publish
cls
echo =====================================================
echo   Upload Videos (Publish Immediately)
echo =====================================================
echo.
set /p max=Enter maximum number of videos to upload (leave empty for default):

set cmd=python -m youtube_shorts.uploader --publish

if not "%max%"=="" (
    set cmd=!cmd! --max %max%
)

echo.
echo Running command: !cmd!
echo.
!cmd!

echo.
echo Operation completed.
pause
goto upload_menu

:upload_schedule
cls
echo =====================================================
echo   Upload Videos (Schedule Only)
echo =====================================================
echo.
set /p max=Enter maximum number of videos to upload (leave empty for default):

set cmd=python -m youtube_shorts.uploader --schedule

if not "%max%"=="" (
    set cmd=!cmd! --max %max%
)

echo.
echo Running command: !cmd!
echo.
!cmd!

echo.
echo Operation completed.
pause
goto upload_menu

:upload_analyze
cls
echo =====================================================
echo   Analyze Upload Errors
echo =====================================================
echo.
echo Running command: python -m youtube_shorts.uploader --analyze
echo.
python -m youtube_shorts.uploader --analyze

echo.
echo Operation completed.
pause
goto upload_menu

:performance_menu
cls
echo =====================================================
echo   Performance Tracking
echo =====================================================
echo.
echo 1. Track all videos
echo 2. Track specific video
echo 3. Generate performance report
echo 4. Back to main menu
echo.
set /p perf_choice=Enter your choice (1-4):

if "%perf_choice%"=="1" goto track_all
if "%perf_choice%"=="2" goto track_specific
if "%perf_choice%"=="3" goto generate_report
if "%perf_choice%"=="4" goto main_menu

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto performance_menu

:track_all
cls
echo =====================================================
echo   Track All Videos
echo =====================================================
echo.
set /p days=Enter number of days to track (leave empty for default):

set cmd=python -m youtube_shorts.performance_tracker

if not "%days%"=="" (
    set cmd=!cmd! --days %days%
)

echo.
echo Running command: !cmd!
echo.
!cmd!

echo.
echo Operation completed.
pause
goto performance_menu

:track_specific
cls
echo =====================================================
echo   Track Specific Video
echo =====================================================
echo.
set /p video_id=Enter YouTube video ID:

if "%video_id%"=="" (
    echo Video ID is required.
    timeout /t 2 >nul
    goto track_specific
)

echo.
echo Running command: python -m youtube_shorts.performance_tracker --video-id "%video_id%"
echo.
python -m youtube_shorts.performance_tracker --video-id "%video_id%"

echo.
echo Operation completed.
pause
goto performance_menu

:generate_report
cls
echo =====================================================
echo   Generate Performance Report
echo =====================================================
echo.
echo Running command: python -m youtube_shorts.performance_tracker --report
echo.
python -m youtube_shorts.performance_tracker --report

echo.
echo Operation completed.
pause
goto performance_menu

:utilities_menu
cls
echo =====================================================
echo   Utilities
echo =====================================================
echo.
echo 1. Create directory structure
echo 2. Backup Excel data
echo 3. Backup JSON data
echo 4. Clean temporary files
echo 5. Back to main menu
echo.
set /p util_choice=Enter your choice (1-5):

if "%util_choice%"=="1" goto create_dirs
if "%util_choice%"=="2" goto backup_excel
if "%util_choice%"=="3" goto backup_json
if "%util_choice%"=="4" goto clean_temp
if "%util_choice%"=="5" goto main_menu

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto utilities_menu

:create_dirs
cls
echo =====================================================
echo   Create Directory Structure
echo =====================================================
echo.
echo This will create all directories defined in constants.py.
echo.
set /p confirm=Are you sure you want to continue? (y/n):

if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    timeout /t 2 >nul
    goto utilities_menu
)

echo.
echo Running command: python -c "from youtube_shorts.utils import constants; import os; [os.makedirs(d, exist_ok=True) for d in [constants.CONFIG_DIR, constants.DATA_DIR, constants.LOGS_DIR, constants.BACKUPS_DIR, constants.DRIVERS_DIR, constants.OUTPUT_DIR, constants.SHORTS_METADATA_DIR, constants.SHORTS_DOWNLOADS_DIR, constants.DEBUG_RECORDINGS_DIR]]"
echo.
python -c "from youtube_shorts.utils import constants; import os; [os.makedirs(d, exist_ok=True) for d in [constants.CONFIG_DIR, constants.DATA_DIR, constants.LOGS_DIR, constants.BACKUPS_DIR, constants.DRIVERS_DIR, constants.OUTPUT_DIR, constants.SHORTS_METADATA_DIR, constants.SHORTS_DOWNLOADS_DIR, constants.DEBUG_RECORDINGS_DIR]]"

echo.
echo Directory structure created.
pause
goto utilities_menu

:backup_excel
cls
echo =====================================================
echo   Backup Excel Data
echo =====================================================
echo.
echo This will create a backup of the Excel data file.
echo.
set /p confirm=Are you sure you want to continue? (y/n):

if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    timeout /t 2 >nul
    goto utilities_menu
)

echo.
echo Running command: python -c "from youtube_shorts.utils import constants; import os, shutil, datetime; os.makedirs(constants.EXCEL_BACKUPS_DIR, exist_ok=True); backup_path = os.path.join(constants.EXCEL_BACKUPS_DIR, f'shorts_data_{datetime.datetime.now().strftime(\"%%Y%%m%%d_%%H%%M%%S\")}.xlsx'); shutil.copy2(constants.EXCEL_FILE_PATH, backup_path) if os.path.exists(constants.EXCEL_FILE_PATH) else print('Excel file not found'); print(f'Backup created: {backup_path}') if os.path.exists(constants.EXCEL_FILE_PATH) else None"
echo.
python -c "from youtube_shorts.utils import constants; import os, shutil, datetime; os.makedirs(constants.EXCEL_BACKUPS_DIR, exist_ok=True); backup_path = os.path.join(constants.EXCEL_BACKUPS_DIR, f'shorts_data_{datetime.datetime.now().strftime(\"%%Y%%m%%d_%%H%%M%%S\")}.xlsx'); shutil.copy2(constants.EXCEL_FILE_PATH, backup_path) if os.path.exists(constants.EXCEL_FILE_PATH) else print('Excel file not found'); print(f'Backup created: {backup_path}') if os.path.exists(constants.EXCEL_FILE_PATH) else None"

echo.
echo Operation completed.
pause
goto utilities_menu

:backup_json
cls
echo =====================================================
echo   Backup JSON Data
echo =====================================================
echo.
echo This will create backups of important JSON data files.
echo.
set /p confirm=Are you sure you want to continue? (y/n):

if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    timeout /t 2 >nul
    goto utilities_menu
)

echo.
echo Running command: python -c "from youtube_shorts.utils import constants; import os, shutil, datetime, glob; os.makedirs(constants.JSON_BACKUPS_DIR, exist_ok=True); timestamp = datetime.datetime.now().strftime('%%Y%%m%%d_%%H%%M%%S'); [shutil.copy2(f, os.path.join(constants.JSON_BACKUPS_DIR, os.path.basename(f) + '.' + timestamp + '.bak')) for f in glob.glob(os.path.join(constants.DATA_DIR, '*.json')) if os.path.exists(f)]; print('JSON backups created in ' + constants.JSON_BACKUPS_DIR)"
echo.
python -c "from youtube_shorts.utils import constants; import os, shutil, datetime, glob; os.makedirs(constants.JSON_BACKUPS_DIR, exist_ok=True); timestamp = datetime.datetime.now().strftime('%%Y%%m%%d_%%H%%M%%S'); [shutil.copy2(f, os.path.join(constants.JSON_BACKUPS_DIR, os.path.basename(f) + '.' + timestamp + '.bak')) for f in glob.glob(os.path.join(constants.DATA_DIR, '*.json')) if os.path.exists(f)]; print('JSON backups created in ' + constants.JSON_BACKUPS_DIR)"

echo.
echo Operation completed.
pause
goto utilities_menu

:clean_temp
cls
echo =====================================================
echo   Clean Temporary Files
echo =====================================================
echo.
echo This will remove temporary files (*.tmp, *.log.old, etc.).
echo.
set /p confirm=Are you sure you want to continue? (y/n):

if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    timeout /t 2 >nul
    goto utilities_menu
)

echo.
echo Cleaning temporary files...
echo.
del /s /q *.tmp 2>nul
del /s /q *.log.old 2>nul
del /s /q *.pyc 2>nul
del /s /q __pycache__\*.* 2>nul

echo.
echo Temporary files cleaned.
pause
goto utilities_menu

:maintenance_menu
cls
echo =====================================================
echo   Maintenance
echo =====================================================
echo.
echo 1. Check for updates
echo 2. Run cleanup script
echo 3. Verify installation
echo 4. Back to main menu
echo.
set /p maint_choice=Enter your choice (1-4):

if "%maint_choice%"=="1" goto check_updates
if "%maint_choice%"=="2" goto run_cleanup
if "%maint_choice%"=="3" goto verify_install
if "%maint_choice%"=="4" goto main_menu

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto maintenance_menu

:check_updates
cls
echo =====================================================
echo   Check for Updates
echo =====================================================
echo.
echo Checking for updates...
echo.
echo This feature is not yet implemented.
echo Please check the GitHub repository manually for updates.
echo.
echo Operation completed.
pause
goto maintenance_menu

:run_cleanup
cls
echo =====================================================
echo   Run Cleanup Script
echo =====================================================
echo.
echo This will run the cleanup_old_files.bat script.
echo.
set /p confirm=Are you sure you want to continue? (y/n):

if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    timeout /t 2 >nul
    goto maintenance_menu
)

echo.
echo Running cleanup_old_files.bat...
echo.
call cleanup_old_files.bat

echo.
echo Operation completed.
pause
goto maintenance_menu

:verify_install
cls
echo =====================================================
echo   Verify Installation
echo =====================================================
echo.
echo Verifying installation...
echo.
python -c "import sys; print(f'Python version: {sys.version}')"
python -c "import youtube_shorts; print(f'YouTube Shorts Automation version: {getattr(youtube_shorts, \"__version__\", \"Unknown\")}')"
python -c "import os, youtube_shorts.utils.constants as constants; print('Directory structure:'); [print(f'- {d}: {"Exists" if os.path.exists(d) else "Missing"}') for d in [constants.CONFIG_DIR, constants.DATA_DIR, constants.LOGS_DIR, constants.BACKUPS_DIR, constants.DRIVERS_DIR, constants.OUTPUT_DIR]]"

echo.
echo Verification completed.
pause
goto maintenance_menu

:end
cls
echo =====================================================
echo   Thank you for using YouTube Shorts Automation!
echo =====================================================
echo.
echo Goodbye!
echo.
timeout /t 3 >nul
endlocal
exit /b 0
