from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import re
import csv
import time
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_email_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Log script start
logger.info("Starting the combined scraping and email generation script")

# List of Classroom URLs to scrape
CLASSROOM_URLS = [
    'https://classroom.google.com/u/2/r/NzU4MzE3MTQ2OTgy/sort-last-name',
    'https://classroom.google.com/u/2/r/NzM2ODE2NDc1ODgw/sort-last-name',
    'https://classroom.google.com/u/2/r/NzM2NzYxMDEyNjAz/sort-last-name',
    'https://classroom.google.com/u/2/r/NzQ2OTM3MjQ0MzU1/sort-last-name',
    'https://classroom.google.com/u/2/r/NzM2NTQwNzM3NjIy/sort-last-name',
    'https://classroom.google.com/u/2/r/NzQ1NzA4ODY4OTIw/sort-last-name',
    'https://classroom.google.com/u/2/r/NzQ1Njc0MDY1MzQy/sort-last-name',
    
]

# Define constants
ENTRY_SELECTOR = 'span.YVvGBb'
WAIT = 60  # Time to manually log in
SCROLL_PAUSE = 2  # Time to wait after each scroll
OUTPUT_CSV = 'classmates_emails.csv'
EMAIL_DOMAIN = '@vitbhopal.ac.in'

# Step 1: Scrape data from all classrooms
logger.info("Setting up Chrome options for scraping")
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=/home/aniket-ramdasi/chrome-profile-selenium')
options.add_argument('--profile-directory=Default')
logger.info(f"Using Chrome profile directory: /home/aniket-ramdasi/chrome-profile-selenium")

logger.info("Initializing ChromeDriver")
service = ChromeService(ChromeDriverManager().install())

try:
    driver = webdriver.Chrome(service=service, options=options)
    logger.info("Driver initialized successfully")
except Exception as e:
    logger.error(f"Error initializing driver: {e}")
    exit(1)

# Collect all student data in memory
all_student_data = []
for course_index, url in enumerate(CLASSROOM_URLS, 1):
    logger.info(f"Processing Classroom {course_index}: {url}")

    # Navigate to the Classroom "People" page and wait for login
    logger.info(f"Navigating to URL: {url}")
    driver.get(url)
    if course_index == 1:
        logger.info(f"Please log in to Google Classroom with your student account. You have {WAIT} seconds to complete the login...")
        time.sleep(WAIT)
        logger.info("Login wait period completed")
    else:
        logger.info(f"Assuming already logged in, waiting {SCROLL_PAUSE} seconds for page load")
        time.sleep(SCROLL_PAUSE)

    # Scroll to load all students
    logger.info("Starting to scroll and load all students")
    scroll_attempts = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        scroll_attempts += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.info(f"Scroll attempt {scroll_attempts}: Scrolled to bottom")
        time.sleep(SCROLL_PAUSE)
        new_height = driver.execute_script("return document.body.scrollHeight")
        logger.info(f"New scroll height: {new_height}, Last scroll height: {last_height}")
        if new_height == last_height:
            logger.info("No more content to load, scrolling complete")
            break
        last_height = new_height

    # Find elements
    logger.info(f"Finding elements with CSS selector: {ENTRY_SELECTOR}")
    elements = driver.find_elements(By.CSS_SELECTOR, ENTRY_SELECTOR)
    logger.info(f"Found {len(elements)} elements")

    # Parse elements
    logger.info("Parsing elements")
    pattern = re.compile(r'(.+)\s+([0-9]{2}[A-Za-z]{3}[0-9]{5})$')
    for i, el in enumerate(elements):
        text = el.text.strip()
        logger.debug(f"Element {i + 1} in Classroom {course_index}: {text}")
        match = pattern.match(text)
        if not match:
            logger.warning(f"Element {i + 1} in Classroom {course_index} does not match pattern: {text}")
            continue
        full, reg = match.groups()
        logger.debug(f"Matched - Name: {full}, Registration: {reg}")
        parts = full.split()
        first = parts[0]
        middle = ' '.join(parts[1:-1])
        last = parts[-1] if len(parts) > 1 else ''
        all_student_data.append({'First': first, 'Middle': middle, 'Last': last, 'Reg': reg})
        logger.debug(f"Parsed - First: {first}, Middle: {middle}, Last: {last}, Reg: {reg}")

# Clean up browser
logger.info("Closing the browser")
driver.quit()

logger.info(f"Collected {len(all_student_data)} total student entries from {len(CLASSROOM_URLS)} classrooms")

# Step 2: Generate emails and update classmates_emails.csv

# Read existing classmates_emails.csv to track existing registration numbers
existing_entries = {}
if os.path.exists(OUTPUT_CSV):
    logger.info(f"Reading existing {OUTPUT_CSV} to check for duplicates")
    try:
        with open(OUTPUT_CSV, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Extract reg from Name (last part after splitting by space)
                reg = row['Name'].split()[-1].strip()
                existing_entries[reg] = row
        logger.info(f"Found {len(existing_entries)} existing entries in {OUTPUT_CSV}")
    except Exception as e:
        logger.error(f"Error reading {OUTPUT_CSV}: {e}")
        exit(1)
else:
    logger.info(f"No existing {OUTPUT_CSV} found, starting fresh")

# Generate full names and emails
logger.info("Generating full names and email addresses")
new_entries = []
for i, student in enumerate(all_student_data):
    try:
        first_name = student['First'].strip()
        middle_name = student['Middle'].strip() if student['Middle'].strip() else ''
        last_name = student['Last'].strip()
        reg = student['Reg'].strip()

        # Validate fields
        if not first_name or not last_name or not reg:
            logger.warning(f"Student {i + 1}: Missing First, Last, or Registration number - {student}")
            continue

        # Check for duplicates based on registration number
        if reg in existing_entries:
            logger.info(f"Student {i + 1}: Duplicate registration number {reg}, skipping")
            continue

        # Construct full name
        name_parts = [part for part in [first_name, middle_name, last_name] if part]
        full_name = ' '.join(name_parts + [reg])
        logger.debug(f"Student {i + 1}: Full Name: {full_name}")

        # Construct email
        first_name_lower = first_name.lower()
        reg_lower = reg.lower()
        email = f"{first_name_lower}.{reg_lower}{EMAIL_DOMAIN}"
        logger.debug(f"Student {i + 1}: Email: {email}")

        # Add to new entries
        new_entries.append({
            'Name': full_name,
            'Email': email,
            'Reg': reg  # Temporary field for duplicate checking
        })
    except Exception as e:
        logger.error(f"Student {i + 1}: Error processing student {student}: {e}")
        continue

logger.info(f"Generated {len(new_entries)} new entries")

# Combine existing and new entries
combined_entries = list(existing_entries.values()) + new_entries
logger.info(f"Total entries after combining: {len(combined_entries)}")

# Write to output CSV
logger.info(f"Writing to output CSV file: {OUTPUT_CSV}")
try:
    with open(OUTPUT_CSV, 'w', newline='') as f:
        fieldnames = ['Name', 'Email']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in combined_entries:
            writer.writerow({'Name': entry['Name'], 'Email': entry['Email']})
    logger.info(f"Successfully wrote {len(combined_entries)} rows to {OUTPUT_CSV}")
except Exception as e:
    logger.error(f"Error writing to {OUTPUT_CSV}: {e}")
    exit(1)

# Log script completion
logger.info("Combined scraping and email generation script completed")