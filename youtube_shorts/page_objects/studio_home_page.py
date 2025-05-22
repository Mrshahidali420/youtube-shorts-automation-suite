"""
YouTube Studio Home Page Object

This module provides the Page Object for the YouTube Studio home page.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage

class StudioHomePage(BasePage):
    """Page Object for YouTube Studio home page."""
    
    # URL
    URL = "https://studio.youtube.com/"
    
    # Locators
    CREATE_BUTTON_LOCATORS = [
        (By.CSS_SELECTOR, "ytcp-button#create-icon"),
        (By.CSS_SELECTOR, "yt-icon-button#create-icon-button"),
        (By.XPATH, "//button[contains(@aria-label, 'Create')]")
    ]
    
    UPLOAD_VIDEOS_LOCATORS = [
        (By.CSS_SELECTOR, "tp-yt-paper-item#text-item-0"),
        (By.XPATH, "//tp-yt-paper-item[contains(., 'Upload videos')]"),
        (By.XPATH, "//div[contains(@class, 'menu-item-label') and contains(text(), 'Upload videos')]")
    ]
    
    def __init__(self, driver: webdriver.Firefox):
        """Initialize the Studio Home Page object."""
        super().__init__(driver, log_prefix="StudioHomePage")
    
    def navigate(self) -> bool:
        """
        Navigate to the YouTube Studio home page.
        
        Returns:
            True if navigation was successful, False otherwise
        """
        self.log_info("Navigating to YouTube Studio...")
        self.driver.get(self.URL)
        
        # Wait for the create button to confirm page is loaded
        create_button = self.find_element_with_multiple_locators(
            self.CREATE_BUTTON_LOCATORS,
            wait=self.wait_very_long,
            clickable=True
        )
        
        if create_button:
            self.log_success("YouTube Studio page loaded successfully")
            return True
        else:
            self.log_error("Failed to load YouTube Studio page")
            return False
    
    def click_create_button(self) -> bool:
        """
        Click the Create button.
        
        Returns:
            True if click was successful, False otherwise
        """
        self.log_info("Clicking Create button...")
        create_button = self.find_element_with_multiple_locators(
            self.CREATE_BUTTON_LOCATORS,
            wait=self.wait_medium,
            clickable=True
        )
        
        result = self.click_element_safely(create_button, "Create button")
        if result:
            self.mimic_human_delay(0.2, 0.5)
        return result
    
    def click_upload_videos(self) -> bool:
        """
        Click the Upload Videos option from the create menu.
        
        Returns:
            True if click was successful, False otherwise
        """
        self.log_info("Clicking Upload Videos option...")
        upload_option = self.find_element_with_multiple_locators(
            self.UPLOAD_VIDEOS_LOCATORS,
            wait=self.wait_short,
            clickable=True
        )
        
        result = self.click_element_safely(upload_option, "Upload Videos option")
        if result:
            self.mimic_human_delay(0.5, 1.0)
        return result
    
    def start_upload_process(self) -> bool:
        """
        Start the upload process by clicking Create and then Upload Videos.
        
        Returns:
            True if the process was started successfully, False otherwise
        """
        if not self.click_create_button():
            return False
        
        return self.click_upload_videos()
