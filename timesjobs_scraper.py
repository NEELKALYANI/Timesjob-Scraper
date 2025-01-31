import requests
from bs4 import BeautifulSoup
import openpyxl
import os
import time

def find_jobs(unpreferred_skills):
    for i in range(1, 6):
        current_url = f'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords=python&postWeek=60&searchType=personalizedSearch&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&pDate=I&sequence={i}&startPage=1'
        response = requests.get(current_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

        filename = 'scraping.xlsx'
        file_exists = os.path.isfile(filename)

        # Load the workbook if it exists, otherwise create a new one
        if file_exists:
            workbook = openpyxl.load_workbook(filename)
            sheet = workbook.active
        else:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Scraped Data"
            sheet.append(["Job Title", "Company Name", "Job Description", "Job Location", "Salary", "Skills", "Posted", "Apply Here"])

        for job in jobs:
            posted = job.find('span', class_='sim-posted').text.strip()
            if 'few days ago' in posted:
                job_title = job.find('h2', class_='heading-trun').text.strip()
                company_name = job.find('h3', class_='joblist-comp-name').text.strip()
                job_description = job.find('li', class_='job-description__').text.strip()
                location = job.find('li', class_='srp-zindex location-tru').text.strip()
                salary_tag = job.find('i', class_='srp-icons salary')
                salary_low = salary_tag.get('data-lowsalary') if salary_tag else 'N/A'
                salary_high = salary_tag.get('data-highsalary') if salary_tag else 'N/A'
                skills_tag = job.find('div', class_='more-skills-sections')
                skills = [skill.strip().lower() for skill in skills_tag.stripped_strings] if skills_tag else []
                apply_link = job.find('a', class_='posoverlay_srp')['href']

                if not any(skill in skills for skill in unpreferred_skills):
                    print(f'''Job Title: {job_title}
                    Company Name: {company_name}
                    Job Description: {job_description}
                    Job Location: {location}
                    Salary: {salary_low} - {salary_high}
                    Skills: {', '.join(skills)}
                    Posted: {posted}
                    Apply Here: {apply_link}
                    ''')

                    row_data = [
                        job_title,
                        company_name,
                        job_description,
                        location,
                        f'{salary_low} - {salary_high}',
                        ', '.join(skills),
                        posted,
                        apply_link
                    ]
                    sheet.append(row_data)

        workbook.save(filename)
        print(f"Data saved to {filename}")

if __name__ == '__main__':
    unpreferred_skills_input = input('Please enter skills you want to filter out (comma-separated): ')
    unpreferred_skills = [skill.strip().lower() for skill in unpreferred_skills_input.split(',')]
    print(f'Filtering out the unpreferred skills: {unpreferred_skills}...')
    file_exists = os.path.exists('C:/Users/HP/Desktop/Web Scrapping/scraping.xlsx')
    if file_exists:
        os.remove('scraping.xlsx')
        print("File Deleted!!")

    while True:
        find_jobs(unpreferred_skills)
        print("Waiting for 2 minutes before the next scrape...")
        time.sleep(120)
