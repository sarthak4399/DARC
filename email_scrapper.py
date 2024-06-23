import re
import csv
import requests
import sys
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }
    return session

def scrape_website(url, session):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def write_emails_to_csv(url, emails, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        email_writer = csv.writer(csvfile)
        email_writer.writerow(['URL', 'Email'])
        for email in emails:
            email_writer.writerow([url, email])

def main():
    if len(sys.argv) != 2:
        print("Usage: python email_scraper.py <website_url>")
        return

    url = sys.argv[1]
    output_csv_file_path = 'emails.csv' 

    session = get_tor_session()

    page_content = scrape_website(url, session)

    if not page_content:
        print("No content to scrape.")
        return

    emails = extract_emails(page_content)

    write_emails_to_csv(url, emails, output_csv_file_path)

    print(f'Extracted {len(emails)} emails from {url} and saved to {output_csv_file_path}')

if __name__ == '__main__':
    main()
