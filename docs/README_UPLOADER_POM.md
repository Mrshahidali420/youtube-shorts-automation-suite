# YouTube Uploader with Page Object Model

This document explains the new implementation of the YouTube uploader using the Page Object Model pattern.

## Overview

The original `uploader.py` script has been refactored to use the Page Object Model (POM) pattern, which provides several benefits:

1. **Better Maintainability**: Each page in the YouTube Studio interface is represented by its own class
2. **Improved Readability**: The upload process is broken down into smaller, focused functions
3. **Enhanced Error Handling**: Each step has specific error handling and screenshots
4. **Dynamic Waits**: Fixed `time.sleep()` calls are replaced with dynamic `WebDriverWait`
5. **Easier Updates**: When YouTube changes its UI, only the affected page object needs to be updated

## Files Structure

- `page_objects/`: Package containing all page object classes
  - `__init__.py`: Package initialization
  - `base_page.py`: Base class with common functionality
  - `studio_home_page.py`: YouTube Studio home page
  - `upload_page.py`: File selection and upload progress page
  - `details_page.py`: Title, description, and tags input page
  - `visibility_page.py`: Publishing options page
  - `confirmation_page.py`: Upload confirmation page
- `uploader_pom.py`: Main module with the new implementation

## How to Use

### Basic Usage

```python
from selenium import webdriver
from uploader_pom import upload_video_pom

# Set up browser
driver = webdriver.Firefox()

# Prepare metadata
metadata = {
    "title": "My Video Title",
    "description": "Video description",
    "tags": ["tag1", "tag2", "tag3"],
    "video_index": "1"
}

# Upload video
video_id = upload_video_pom(
    driver=driver,
    video_file="path/to/video.mp4",
    metadata=metadata,
    publish_now=True
)

if video_id:
    print(f"Upload successful! Video ID: {video_id}")
else:
    print("Upload failed.")

# Close browser
driver.quit()
```

### Command Line Usage

```bash
python uploader_pom.py --video path/to/video.mp4 --title "My Video Title" --description "Video description" --tags "tag1,tag2,tag3"
```

### Scheduling a Video

```bash
python uploader_pom.py --video path/to/video.mp4 --title "My Video Title" --schedule --schedule-time "2023-12-31 12:00"
```

### Debug Recording

```bash
python uploader_pom.py --video path/to/video.mp4 --record
```

## Key Improvements

### 1. Page Object Model

Each page in the YouTube Studio interface is represented by its own class:

- `BasePage`: Common functionality for all pages
- `StudioHomePage`: YouTube Studio home page
- `UploadPage`: File selection and upload progress
- `DetailsPage`: Title, description, and tags input
- `VisibilityPage`: Publishing options
- `ConfirmationPage`: Upload confirmation

### 2. Smaller, Focused Functions

The monolithic `upload_video` function has been broken down into smaller, focused functions:

- `navigate()`: Navigate to YouTube Studio
- `start_upload_process()`: Click Create and Upload Videos
- `select_file()`: Select the video file
- `wait_for_upload_progress()`: Wait for upload to start
- `wait_for_upload_complete()`: Wait for upload to complete
- `fill_details()`: Fill in title, description, and tags
- `set_visibility()`: Set publishing options
- `wait_for_confirmation()`: Wait for confirmation dialog
- `get_video_id()`: Extract YouTube video ID

### 3. Dynamic Waits

Fixed `time.sleep()` calls have been replaced with dynamic `WebDriverWait`:

```python
# Old approach
time.sleep(5)  # Wait 5 seconds regardless of whether the element appears

# New approach
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "element-id")))
```

### 4. Multiple Locator Strategies

Each element can be located using multiple strategies, improving robustness:

```python
TITLE_INPUT_LOCATORS = [
    (By.XPATH, "//ytcp-mention-textbox[@label='Title']//div[@contenteditable='true']"),
    (By.XPATH, "//div[@aria-label='Add a title that describes your video']"),
    (By.CSS_SELECTOR, "ytcp-mention-textbox[label='Title'] div[contenteditable='true']")
]
```

### 5. Screenshots on Failure

Screenshots are automatically taken when errors occur:

```python
def take_screenshot(self, name: str = None) -> str:
    """Take a screenshot and save it to the screenshots directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{name}.png"
    filepath = os.path.join(self.screenshot_dir, filename)
    self.driver.save_screenshot(filepath)
    return filepath
```

## Migration Guide

To migrate from the old `uploader.py` to the new POM-based implementation:

1. Replace calls to `upload_video()` with `upload_video_pom()`
2. Ensure the `page_objects` package is in your Python path
3. Update any code that depends on the specific behavior of the old function

## Future Improvements

- Add more robust error recovery mechanisms
- Implement retry logic for flaky steps
- Add support for custom thumbnails
- Enhance playlist management functionality
- Add support for additional YouTube Studio features
