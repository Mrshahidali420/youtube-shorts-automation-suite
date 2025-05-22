"""
YouTube Studio Upload Page Object

This module provides the Page Object for the YouTube Studio upload page.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

import os
import time
from typing import Optional, Dict, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage

class UploadPage(BasePage):
    """Page Object for YouTube Studio upload page."""
    
    # Locators
    FILE_INPUT_LOCATORS = [
        (By.XPATH, "//input[@type='file']"),
        (By.CSS_SELECTOR, "input[type='file']")
    ]
    
    UPLOAD_PROGRESS_LOCATORS = [
        (By.XPATH, "//ytcp-video-upload-progress"),
        (By.XPATH, "//ytcp-upload-progress-bar"),
        (By.CSS_SELECTOR, "ytcp-video-upload-progress")
    ]
    
    UPLOAD_COMPLETE_LOCATORS = [
        (By.XPATH, "//ytcp-video-upload-progress[contains(., '100%')]"),
        (By.XPATH, "//ytcp-upload-progress-bar[contains(., '100%')]"),
        (By.XPATH, "//span[contains(text(), 'Video upload complete')]")
    ]
    
    UPLOAD_PROCESSING_LOCATORS = [
        (By.XPATH, "//span[contains(text(), 'Processing')]"),
        (By.XPATH, "//ytcp-video-upload-progress[contains(., 'Processing')]")
    ]
    
    UPLOAD_ERROR_LOCATORS = [
        (By.XPATH, "//ytcp-video-upload-error"),
        (By.XPATH, "//div[contains(@class, 'error-message')]"),
        (By.XPATH, "//span[contains(text(), 'Error')]")
    ]
    
    def __init__(self, driver: webdriver.Firefox):
        """Initialize the Upload Page object."""
        super().__init__(driver, log_prefix="UploadPage")
    
    def select_file(self, video_file_path: str) -> bool:
        """
        Select a file for upload.
        
        Args:
            video_file_path: Path to the video file
            
        Returns:
            True if file selection was successful, False otherwise
        """
        self.log_info(f"Selecting file for upload: {video_file_path}")
        
        # Verify file exists
        abs_video_path = os.path.abspath(video_file_path)
        if not os.path.exists(abs_video_path):
            self.log_error(f"Video file does not exist at path: {abs_video_path}")
            return False
        
        # Find file input element
        file_input = self.find_element_with_multiple_locators(
            self.FILE_INPUT_LOCATORS,
            wait=self.wait_long
        )
        
        if not file_input:
            self.log_error("File input element not found")
            return False
        
        try:
            # Send file path to input element
            file_input.send_keys(abs_video_path)
            self.log_success(f"File selected: {abs_video_path}")
            return True
        except Exception as e:
            self.log_error(f"Failed to select file: {e}")
            self.take_screenshot("file_selection_failed")
            return False
    
    def wait_for_upload_progress(self, timeout: int = 300) -> Optional[float]:
        """
        Wait for upload progress to appear and return the progress percentage.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Progress percentage (0-100) or None if progress element not found
        """
        self.log_info("Waiting for upload progress to appear...")
        
        try:
            progress_element = self.find_element_with_multiple_locators(
                self.UPLOAD_PROGRESS_LOCATORS,
                wait=WebDriverWait(self.driver, timeout)
            )
            
            if progress_element:
                self.log_success("Upload progress element found")
                # Try to extract percentage
                try:
                    progress_text = progress_element.text
                    import re
                    percentage_match = re.search(r'(\d+)%', progress_text)
                    if percentage_match:
                        percentage = float(percentage_match.group(1))
                        self.log_info(f"Current upload progress: {percentage}%")
                        return percentage
                except Exception as e:
                    self.log_warning(f"Could not extract progress percentage: {e}")
                return 0.0  # Return 0 if we found the element but couldn't extract percentage
            else:
                self.log_error("Upload progress element not found")
                return None
        except TimeoutException:
            self.log_error(f"Timeout waiting for upload progress (waited {timeout} seconds)")
            self.take_screenshot("upload_progress_timeout")
            return None
    
    def wait_for_upload_complete(self, timeout: int = 1800, check_interval: int = 10) -> bool:
        """
        Wait for the upload to complete.
        
        Args:
            timeout: Total timeout in seconds
            check_interval: Interval between checks in seconds
            
        Returns:
            True if upload completed successfully, False otherwise
        """
        self.log_info(f"Waiting for upload to complete (timeout: {timeout}s)...")
        
        start_time = time.time()
        last_progress = -1
        last_progress_time = start_time
        
        while time.time() - start_time < timeout:
            # Check for upload complete
            try:
                complete_element = self.find_element_with_multiple_locators(
                    self.UPLOAD_COMPLETE_LOCATORS,
                    wait=self.wait_very_short,
                    take_screenshot_on_failure=False
                )
                
                if complete_element:
                    self.log_success("Upload completed successfully")
                    return True
            except Exception:
                pass  # Ignore exceptions during quick checks
            
            # Check for errors
            try:
                error_element = self.find_element_with_multiple_locators(
                    self.UPLOAD_ERROR_LOCATORS,
                    wait=self.wait_very_short,
                    take_screenshot_on_failure=False
                )
                
                if error_element:
                    error_text = error_element.text
                    self.log_error(f"Upload error detected: {error_text}")
                    self.take_screenshot("upload_error")
                    return False
            except Exception:
                pass  # Ignore exceptions during quick checks
            
            # Check progress
            try:
                progress_element = self.find_element_with_multiple_locators(
                    self.UPLOAD_PROGRESS_LOCATORS,
                    wait=self.wait_very_short,
                    take_screenshot_on_failure=False
                )
                
                if progress_element:
                    progress_text = progress_element.text
                    import re
                    percentage_match = re.search(r'(\d+)%', progress_text)
                    if percentage_match:
                        current_progress = float(percentage_match.group(1))
                        
                        # Only log if progress has changed
                        if current_progress != last_progress:
                            self.log_info(f"Upload progress: {current_progress}%")
                            last_progress = current_progress
                            last_progress_time = time.time()
                        
                        # Check for stalled upload (no progress for 5 minutes)
                        elif time.time() - last_progress_time > 300 and current_progress < 100:
                            self.log_warning(f"Upload appears stalled at {current_progress}% for 5 minutes")
                            self.take_screenshot("upload_stalled")
                            # Don't return False, just warn and continue waiting
            except Exception:
                pass  # Ignore exceptions during quick checks
            
            # Check for processing state
            try:
                processing_element = self.find_element_with_multiple_locators(
                    self.UPLOAD_PROCESSING_LOCATORS,
                    wait=self.wait_very_short,
                    take_screenshot_on_failure=False
                )
                
                if processing_element:
                    self.log_info("Video upload complete, now processing...")
                    # Processing is considered success for our purposes
                    return True
            except Exception:
                pass  # Ignore exceptions during quick checks
            
            # Wait before next check
            time.sleep(check_interval)
            elapsed = int(time.time() - start_time)
            if elapsed % 60 == 0:  # Log every minute
                self.log_info(f"Still waiting for upload to complete... (elapsed: {elapsed}s)")
        
        # If we get here, we timed out
        self.log_error(f"Timeout waiting for upload to complete (waited {timeout} seconds)")
        self.take_screenshot("upload_timeout")
        return False
