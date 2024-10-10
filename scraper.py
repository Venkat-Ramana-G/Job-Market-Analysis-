import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_remoteok_jobs(job_title, num_pages=1):
    job_listings = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    base_url = f"https://remoteok.com/remote-{job_title}-jobs"

    for page in range(1, num_pages+1):
        url = f"{base_url}?page={page}" if page > 1 else base_url
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('tr', class_='job')

        for job in jobs:
            title = job.find('h2', itemprop='title').text.strip() if job.find('h2', itemprop='title') else 'N/A'
            company = job.find('h3', itemprop='name').text.strip() if job.find('h3', itemprop='name') else 'N/A'
            location = job.find('div', class_='location').text.strip() if job.find('div', class_='location') else 'Remote'
            date_posted = job.find('time')['datetime'] if job.find('time') else 'N/A'

            if title != 'N/A' and company != 'N/A':
                job_listings.append({
                    'Title': title,
                    'Company': company,
                    'Location': location,
                    'Date Posted': date_posted
                })

        time.sleep(1)  # Respect rate limits

    return pd.DataFrame(job_listings)

def save_to_csv(dataframe, filename='job_listings.csv'):
    dataframe.to_csv(filename, index=False)
    print(f"Saved {len(dataframe)} job listings to {filename}")

if __name__ == "__main__":
    job_title = input("Enter job title to search for (e.g., data-scientist): ").strip().replace(' ', '-')
    num_pages = int(input("Enter number of pages to scrape (e.g., 2): "))

    jobs_df = scrape_remoteok_jobs(job_title, num_pages)
    if not jobs_df.empty:
        save_to_csv(jobs_df)
    else:
        print("No job listings found.")
