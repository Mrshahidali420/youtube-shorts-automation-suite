"""
YouTube Studio Confirmation Page Object

This module provides the Page Object for the YouTube Studio confirmation page
that appears after a successful upload.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

import re
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage

class ConfirmationPage(BasePage):
    """Page Object for YouTube Studio confirmation page."""
    
    # Locators
    CONFIRMATION_CONTAINER_LOCATORS = [
        (By.XPATH, "//ytcp-uploads-still-processing-dialog"),
        (By.XPATH, "//ytcp-uploads-success-dialog"),
        (By.CSS_SELECTOR, "ytcp-uploads-still-processing-dialog, ytcp-uploads-success-dialog")
    ]
    
    VIDEO_URL_LOCATORS = [
        (By.XPATH, "//a[contains(@href, 'youtu.be/') or contains(@href, 'youtube.com/')]"),
        (By.XPATH, "//div[contains(@class, 'video-url-container')]//a"),
        (By.CSS_SELECTOR, "a[href*='youtu.be/'], a[href*='youtube.com/']")
    ]
    
    SHARE_URL_LOCATORS = [
        (By.XPATH, "//span[contains(text(), 'Video link')]/following-sibling::span"),
        (By.XPATH, "//label[contains(text(), 'Video link')]/following-sibling::div//input"),
        (By.CSS_SELECTOR, "input.share-panel-url")
    ]
    
    CLOSE_BUTTON_LOCATORS = [
        (By.XPATH, "//ytcp-button[@id='close-button']"),
        (By.XPATH, "//div[contains(@class, 'close-button')]"),
        (By.CSS_SELECTOR, "ytcp-button#close-button")
    ]
    
    def __init__(self, driver: webdriver.Firefox):
        """Initialize the Confirmation Page object."""
        super().__init__(driver, log_prefix="ConfirmationPage")
    
    def wait_for_confirmation(self, timeout: int = 60) -> bool:
        """
        Wait for the confirmation dialog to appear.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            True if confirmation dialog appeared, False otherwise
        """
        self.log_info(f"Waiting for confirmation dialog (timeout: {timeout}s)...")
        
        try:
            confirmation = self.find_element_with_multiple_locators(
                self.CONFIRMATION_CONTAINER_LOCATORS,
                wait=WebDriverWait(self.driver, timeout)
            )
            
            if confirmation:
                self.log_success("Confirmation dialog appeared")
                return True
            else:
                self.log_error("Confirmation dialog not found")
                return False
        except TimeoutException:
            self.log_error(f"Timeout waiting for confirmation dialog (waited {timeout} seconds)")
            self.take_screenshot("confirmation_timeout")
            return False
    
    def get_video_id(self) -> Optional[str]:
        """
        Extract the YouTube video ID from the confirmation page.
        
        Returns:
            YouTube video ID or None if not found
        """
        self.log_info("Extracting YouTube video ID...")
        
        # Try to find the video URL element
        url_element = self.find_element_with_multiple_locators(
            self.VIDEO_URL_LOCATORS,
            wait=self.wait_medium
        )
        
        if url_element:
            # Get the href attribute
            video_url = url_element.get_attribute("href")
            self.log_info(f"Found video URL: {video_url}")
            
            # Extract video ID using regex
            match = re.search(r"(?:youtu\.be/|youtube\.com/(?:shorts/|watch\?v=))([^?&]+)", video_url)
            if match:
                video_id = match.group(1)
                self.log_success(f"Extracted YouTube video ID: {video_id}")
                return video_id
        
        # If not found, try the share URL
        share_element = self.find_element_with_multiple_locators(
            self.SHARE_URL_LOCATORS,
            wait=self.wait_short
        )
        
        if share_element:
            # Get the text or value
            share_url = share_element.get_attribute("value") or share_element.text
            self.log_info(f"Found share URL: {share_url}")
            
            # Extract video ID using regex
            match = re.search(r"(?:youtu\.be/|youtube\.com/(?:shorts/|watch\?v=))([^?&]+)", share_url)
            if match:
                video_id = match.group(1)
                self.log_success(f"Extracted YouTube video ID: {video_id}")
                return video_id
        
        # If we get here, we couldn't find the video ID
        self.log_error("Could not extract YouTube video ID")
        self.take_screenshot("video_id_not_found")
        return None
    
    def close_confirmation(self) -> bool:
        """
        Close the confirmation dialog.
        
        Returns:
            True if dialog was closed successfully, False otherwise
        """
        self.log_info("Closing confirmation dialog...")
        
        close_button = self.find_element_with_multiple_locators(
            self.CLOSE_BUTTON_LOCATORS,
            wait=self.wait_medium,
            clickable=True
        )
        
        result = self.click_element_safely(close_button, "Close button")
        if result:
            self.mimic_human_delay(0.5, 1.0)
        return result
