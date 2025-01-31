**Job Scraper**

This Python script automates the process of scraping job listings from TimesJobs based on the keyword "Python". It extracts relevant job details such as title, company name, job description, location, salary, skills required, posting date, and application link, then saves the information into an Excel spreadsheet (scraping.xlsx) for easy access and filtering.

**Features:**
Filters jobs based on unwanted skills specified by the user.
Stores job details in an Excel file, appending new data dynamically.
Deletes the previous Excel file before each run to ensure fresh data.
Runs continuously in a loop, scraping job data every 2 minutes.

**Dependencies:**
This script requires the following Python libraries:

requests – To send HTTP requests and retrieve web pages.
BeautifulSoup (bs4) – To parse and extract job details from HTML.
openpyxl – To handle Excel file operations.
os – To manage file operations.
time – To introduce delays between scrapes.

**How It Works:**
The script asks the user to input a comma-separated list of skills they want to filter out.
It then iterates through 5 pages of job listings on TimesJobs.
For each job posting:
It checks if the job was posted a few days ago.
Extracts job details such as title, company name, description, location, salary range, and skills.
If the job does not contain any unpreferred skills, it prints the details and adds them to the Excel file.
The script deletes any existing Excel file before starting a new scraping session.
The process repeats every 2 minutes, ensuring up-to-date job data.

