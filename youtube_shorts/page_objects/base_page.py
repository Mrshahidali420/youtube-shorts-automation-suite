"""
Base Page Object

This module provides the base class for all Page Objects.
It includes common functionality for all pages.

Copyright (c) 2023-2025 Shahid Ali
License: MIT License
GitHub: https://github.com/Mrshahidali420/youtube-shorts-automation
Version: 1.0.0
"""

import os
import time
import logging
from typing import Optional, List, Tuple, Any, Union
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException
)

class BasePage:
    """Base class for all Page Objects."""
    
    def __init__(self, driver: webdriver.Firefox, log_prefix: str = ""):
        """
        Initialize the base page.
        
        Args:
            driver: The Selenium WebDriver instance
            log_prefix: Prefix for log messages (usually the page name)
        """
        self.driver = driver
        self.log_prefix = log_prefix
        
        # Define standard wait times
        self.wait_very_short = WebDriverWait(driver, 5)
        self.wait_short = WebDriverWait(driver, 15)
        self.wait_medium = WebDriverWait(driver, 30)
        self.wait_long = WebDriverWait(driver, 60)
        self.wait_very_long = WebDriverWait(driver, 120)
        
        # Screenshot directory
        self.screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "error_screenshots")
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
    
    def log_info(self, message: str, indent: int = 0) -> None:
        """Log an info message with the page prefix."""
        prefix = "  " * indent
        logging.info(f"{prefix}{self.log_prefix}: {message}")
    
    def log_success(self, message: str, indent: int = 0) -> None:
        """Log a success message with the page prefix."""
        prefix = "  " * indent
        logging.info(f"{prefix}{self.log_prefix} SUCCESS: {message}")
    
    def log_warning(self, message: str, indent: int = 0) -> None:
        """Log a warning message with the page prefix."""
        prefix = "  " * indent
        logging.warning(f"{prefix}{self.log_prefix} WARNING: {message}")
    
    def log_error(self, message: str, indent: int = 0) -> None:
        """Log an error message with the page prefix."""
        prefix = "  " * indent
        logging.error(f"{prefix}{self.log_prefix} ERROR: {message}")
    
    def take_screenshot(self, name: str = None) -> str:
        """
        Take a screenshot and save it to the screenshots directory.
        
        Args:
            name: Optional name for the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if name:
                filename = f"{timestamp}_{name}.png"
            else:
                filename = f"{timestamp}_{self.log_prefix.replace(' ', '_')}.png"
            
            filepath = os.path.join(self.screenshot_dir, filename)
            self.driver.save_screenshot(filepath)
            self.log_info(f"Screenshot saved to {filepath}")
            return filepath
        except Exception as e:
            self.log_error(f"Failed to take screenshot: {e}")
            return ""
    
    def find_element_with_multiple_locators(self, locators: List[Tuple[By, str]], 
                                           wait: WebDriverWait = None, 
                                           clickable: bool = False,
                                           take_screenshot_on_failure: bool = True) -> Optional[Any]:
        """
        Try to find an element using multiple locators.
        
        Args:
            locators: List of (By, locator_string) tuples to try
            wait: WebDriverWait instance to use (defaults to medium wait)
            clickable: Whether to wait for the element to be clickable
            take_screenshot_on_failure: Whether to take a screenshot on failure
            
        Returns:
            The found element or None if not found
        """
        if wait is None:
            wait = self.wait_medium
        
        for by, locator in locators:
            try:
                self.log_info(f"Trying to find element with {by}={locator}", indent=1)
                if clickable:
                    element = wait.until(EC.element_to_be_clickable((by, locator)))
                else:
                    element = wait.until(EC.presence_of_element_located((by, locator)))
                self.log_success(f"Found element with {by}={locator}", indent=1)
                return element
            except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
                self.log_warning(f"Element not found with {by}={locator}: {e}", indent=1)
        
        # If we get here, all locators failed
        self.log_error("Failed to find element with any of the provided locators")
        if take_screenshot_on_failure:
            self.take_screenshot("element_not_found")
        return None
    
    def click_element_safely(self, element: Any, element_name: str = "element", 
                            retry_js: bool = True, scroll_into_view: bool = True) -> bool:
        """
        Click an element safely, with fallbacks for common issues.
        
        Args:
            element: The element to click
            element_name: Name of the element for logging
            retry_js: Whether to retry with JavaScript click if normal click fails
            scroll_into_view: Whether to scroll the element into view before clicking
            
        Returns:
            True if click was successful, False otherwise
        """
        try:
            if element is None:
                self.log_error(f"Cannot click {element_name}: Element is None")
                return False
            
            if scroll_into_view:
                self.log_info(f"Scrolling {element_name} into view", indent=1)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
                time.sleep(0.5)  # Give time for scroll to complete
            
            self.log_info(f"Attempting to click {element_name}", indent=1)
            element.click()
            self.log_success(f"Successfully clicked {element_name}", indent=1)
            return True
        except ElementClickInterceptedException as e:
            self.log_warning(f"Click intercepted for {element_name}: {e}", indent=1)
            if retry_js:
                try:
                    self.log_info(f"Trying JavaScript click for {element_name}", indent=1)
                    self.driver.execute_script("arguments[0].click();", element)
                    self.log_success(f"Successfully clicked {element_name} with JavaScript", indent=1)
                    return True
                except Exception as js_e:
                    self.log_error(f"JavaScript click failed for {element_name}: {js_e}", indent=1)
                    self.take_screenshot(f"js_click_failed_{element_name}")
                    return False
            return False
        except Exception as e:
            self.log_error(f"Failed to click {element_name}: {e}", indent=1)
            self.take_screenshot(f"click_failed_{element_name}")
            return False
    
    def enter_text(self, element: Any, text: str, element_name: str = "input field", 
                  clear_first: bool = True, click_first: bool = True) -> bool:
        """
        Enter text into an input element safely.
        
        Args:
            element: The input element
            text: Text to enter
            element_name: Name of the element for logging
            clear_first: Whether to clear the field first
            click_first: Whether to click the element first
            
        Returns:
            True if text entry was successful, False otherwise
        """
        try:
            if element is None:
                self.log_error(f"Cannot enter text in {element_name}: Element is None")
                return False
            
            if click_first:
                self.click_element_safely(element, element_name, scroll_into_view=True)
            
            if clear_first:
                self.log_info(f"Clearing {element_name}", indent=1)
                element.clear()
                # Additional clearing with keyboard shortcuts
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.DELETE)
            
            self.log_info(f"Entering text in {element_name}: '{text[:30]}...' (truncated for log)", indent=1)
            element.send_keys(text)
            self.log_success(f"Successfully entered text in {element_name}", indent=1)
            return True
        except Exception as e:
            self.log_error(f"Failed to enter text in {element_name}: {e}", indent=1)
            self.take_screenshot(f"text_entry_failed_{element_name}")
            return False
    
    def wait_for_url_contains(self, text: str, timeout: int = 30) -> bool:
        """
        Wait for the URL to contain specific text.
        
        Args:
            text: Text to wait for in URL
            timeout: Timeout in seconds
            
        Returns:
            True if URL contains the text within timeout, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(text))
            self.log_success(f"URL now contains '{text}'", indent=1)
            return True
        except TimeoutException:
            self.log_error(f"Timeout waiting for URL to contain '{text}'")
            self.take_screenshot("url_timeout")
            return False
    
    def mimic_human_delay(self, min_seconds: float = 0.5, max_seconds: float = 2.0) -> None:
        """
        Wait a random amount of time to mimic human behavior.
        
        Args:
            min_seconds: Minimum seconds to wait
            max_seconds: Maximum seconds to wait
        """
        import random
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
