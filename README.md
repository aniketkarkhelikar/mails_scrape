# Google Classroom Email Scraper

This project scrapes student data from multiple Google Classroom courses and generates email addresses based on a specific pattern. The data is saved to a CSV file (`classmates_emails.csv`) with full names and emails, ignoring duplicates based on registration numbers.

## Features
- Scrapes student names and registration numbers from Google Classroom "People" pages.
- Supports multiple Classroom courses.
- Generates email addresses in the format `first_name.reg@vitbhopal.ac.in`.
- Appends new entries to `classmates_emails.csv` while skipping duplicates.
- Includes detailed logging for debugging (`scraper_email_generator.log`).

## Prerequisites

Before running the script, ensure you have the following:

### Software Requirements
- **Python 3.6+**: The script is written in Python. Install it from [python.org](https://www.python.org/downloads/) or via your package manager:
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```
- **Google Chrome**: Used for web scraping with Selenium. Install it:
  ```bash
  sudo apt install google-chrome-stable
  ```
- **ChromeDriver**: Automatically managed by the script via `webdriver_manager`, but ensure Chrome is installed first.

### Python Dependencies
Install the required Python libraries using `pip`:
```bash
pip3 install selenium webdriver-manager
```

### System Setup
- **Chrome Profile**: The script uses a specific Chrome profile for manual login.
  - Create a new Chrome profile by running:
    ```bash
    google-chrome --user-data-dir=/home/your-username/chrome-profile-selenium
    ```
  - Replace `/home/your-username` with your actual home directory (e.g., `/home/aniket-ramdasi`).
  - Log in to your Google account in this Chrome instance to save your session.

### Google Classroom Access
- You need access to the Google Classroom courses as a student or teacher.
- Ensure you can view the "People" tab for each course, as the script scrapes data from there.
- Note: The script requires manual login, so you must be able to sign in with your Google account.

## How to Use

### 1. Clone the Repository
Clone your private GitHub repo to your local machine:
```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Configure Classroom URLs
Edit the script (`scrape_and_generate.py`) to include the URLs of the Google Classroom courses you want to scrape. Modify the `CLASSROOM_URLS` list:
```python
CLASSROOM_URLS = [
    'https://classroom.google.com/u/2/r/NzU4MzE3MTQ2OTgy/sort-last-name',
    'https://classroom.google.com/u/2/r/ANOTHER_COURSE_ID/sort-last-name',
]
```
- Replace the URLs with the actual "People" page URLs for your classrooms.
- To find the URL, go to the "People" tab in Google Classroom and copy the URL from your browser.

### 3. Update Chrome Profile Path
Ensure the Chrome profile path in the script matches the one you created:
```python
options.add_argument('--user-data-dir=/home/your-username/chrome-profile-selenium')
```
Replace `/home/your-username` with your actual path (e.g., `/home/aniket-ramdasi`).

### 4. Run the Script
Run the script using Python:
```bash
python3 scrape_and_generate.py
```

### 5. Manual Login
- The script will open Chrome and navigate to the first Classroom URL.
- You have 60 seconds to log in manually with your Google account.
- After logging in, the script will automatically scrape data from all specified classrooms.

### 6. Check Output
- The script generates `classmates_emails.csv` with two columns: `Name` (e.g., `Devesh Singh Yadav 23bce10870`) and `Email` (e.g., `devesh.23bce10870@vitbhopal.ac.in`).
- If `classmates_emails.csv` already exists, new entries are appended, and duplicates (based on registration numbers) are ignored.
- Logs are saved to `scraper_email_generator.log` for debugging.

## Example Output
After running the script, `classmates_emails.csv` might look like:
```
Name,Email
"Devesh Singh Yadav 23bce10870",devesh.23bce10870@vitbhopal.ac.in
"Shubh Jain 23BCY10349",shubh.23bcy10349@vitbhopal.ac.in
"HARSHVARDHAN SINGH PARIHAR 23BEC10072",harshvardhan.23bec10072@vitbhopal.ac.in
```

## Additional Notes
- **CSS Selector**: The script uses the CSS selector `span.YVvGBb` to find student names. If Google Classroom updates its UI, this selector may need to be updated. Inspect the page (right-click > Inspect) to find the new selector.
- **Login Wait Time**: If you need more time to log in, increase the `WAIT` variable in the script (e.g., to `120` seconds).
- **Error Handling**: Check `scraper_email_generator.log` for detailed logs if something goes wrong.
- **Privacy**: Ensure you have permission to scrape and use the student data, as this may involve sensitive information.

## Troubleshooting
- **ChromeDriver Mismatch**:
  - If ChromeDriver doesn’t match your Chrome version, `webdriver_manager` should handle it. Otherwise, manually download the correct version from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads).
- **No Elements Found**:
  - If the script finds 0 elements, the CSS selector may be outdated. Update `ENTRY_SELECTOR` in the script.
- **Login Fails**:
  - Ensure your Chrome profile has a saved session, or increase the `WAIT` time for manual login.

## Credits
Made with ❤️ and a lot of caffeine, powered by **Grok** (because apparently, humans can’t be trusted to write code anymore). Thanks to xAI for creating this sarcastic, overachieving AI assistant that did most of the heavy lifting.

> "AI will probably automate coding in the future, so you’d better get good at giving directions and writing prompts."  
> — Elon Musk (probably, if he were here)
