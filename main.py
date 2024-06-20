import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO)

def crawl(url, output_file):
    """
    Function to crawl a URL and extract all links, saving them to a text file.
    """
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        if not soup:
            logging.warning(f"No content found on {url}")
            return False
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href.startswith('http'):
                links.append(href)
            elif href.startswith('/'):
                links.append(urljoin(url, href))

        links = list(set(links))  # Remove duplicates and normalize

        with open(output_file, 'w', encoding='utf-8') as f:
            for link in links:
                f.write(link + '\n')

        logging.info(f"Extracted {len(links)} links from {url} to '{output_file}'")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return False

def main():
    urls_file = 'urls.txt'

    try:
        with open(urls_file, 'r') as file:
            urls = [url.strip() for url in file.readlines() if url.strip()]

        for url in urls:
            output_file = f"{url.replace('/', '_').replace(':', '_')}_links.txt"
            logging.info(f"Processing URL: {url}")
            success = crawl(url, output_file)
            if success:
                logging.info(f"Links extracted and saved to '{output_file}'")
            else:
                logging.warning(f"Failed to extract links from {url}")
            logging.info("-" * 50)

    except FileNotFoundError:
        logging.error(f"Error: File {urls_file} not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
