import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from processor import process_data
from request_check import check_request
import logging
import time

logging.basicConfig(level=logging.INFO)

def crawl(url):
    """
    Function to crawl a dark web URL and extract all links.
    """
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        if check_request(response):
            soup = BeautifulSoup(response.content, 'html.parser')
            if not soup:
                return []

            links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href.startswith('http'):
                    links.append(href)
                elif href.startswith('/'):
                    links.append(urljoin(url, href))
            links = list(set(links))
            return links
        else:
            logging.warning(f"Request to {url} failed or was blocked.")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return []

def main():
    print(r'''
          _____                    _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\    \                /::\    \        
       /::::\    \              /::::\    \              /::::\    \              /::::\    \       
      /::::::\    \            /::::::\    \            /::::::\    \            /::::::\    \      
     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \     
    /:::/  \:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/  \:::\    \    
   /:::/    \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /:::/    \:::\    \   
  /:::/    / \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /:::/    / \:::\    \  
 /:::/    /   \:::\    \  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\  /:::/    /   \:::\    \ 
/:::/____/     \:::\____\/:::/  \:::\   \:::\____\/:::/  \:::\   \:::|    |/:::/____/     \:::\____\
\:::\    \     /:::/    /\::/    \:::\  /:::/    /\::/   |::::\  /:::|____|\:::\    \      \::/    /
 \:::\    \   /:::/    /  \/____/ \:::\/:::/    /  \/____|:::::\/:::/    /  \:::\    \      \/____/ 
  \:::\    \ /:::/    /            \::::::/    /         |:::::::::/    /    \:::\    \             
   \:::\    /:::/    /              \::::/    /          |::|\::::/    /      \:::\    \            
    \:::\  /:::/    /               /:::/    /           |::| \::/____/        \:::\    \           
     \:::\/:::/    /               /:::/    /            |::|  ~|               \:::\    \          
      \::::::/    /               /:::/    /             \::|   |                \:::\____\         
       \::::/    /               /:::/    /              |::|   |                 \::/    /         
        \::/____/                \::/    /               |::|   |                  \/____/          
         ~~                       \/____/                \|___|                                      
    ''')

    # Adding a delay before starting
    delay_time = 3  # Delay in seconds
    print(f"Waiting for {delay_time} seconds before starting...")
    time.sleep(delay_time)

    urls_file = 'urls.txt'
    output_file = 'extracted_keywords.txt'

    try:
        with open(urls_file, 'r') as file:
            urls = [url.strip() for url in file.readlines() if url.strip()]
        logging.info(f"Found {len(urls)} URLs in {urls_file}")
        logging.info("")
        for url in urls:
            logging.info(f"Processing URL: {url}")
            links = crawl(url)
            if links:
                logging.info(f"Found {len(links)} links on {url}")
                for link in links:
                    logging.debug(link)
                logging.info("")
                for link in links:
                    logging.info(f"Processing link: {link}")
                    try:
                        response = requests.get(link, timeout=10)
                        response.raise_for_status()
                        if check_request(response):
                            html_content = response.content
                            # Process data here if needed
                            # extracted_keywords = process_data(html_content, keywords, output_file)
                            # if extracted_keywords:
                            #     logging.info(f"Extracted Keywords for {link}: {extracted_keywords}")
                            # else:
                            #     logging.info(f"No keywords extracted from {link}")
                            logging.info(f"Successfully retrieved {link}")
                        else:
                            logging.warning(f"Request to {link} failed or was blocked.")
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Error fetching URL {link}: {e}")
                    logging.info("")
            else:
                logging.warning(f"No links found on {url}")
            logging.info("-" * 50)

    except FileNotFoundError:
        logging.error(f"Error: File {urls_file} not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
