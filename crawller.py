import requests
from processor import process_data
from request_check import check_request

def crawl(url, output_file):
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    try:
        response = session.get(url)
        if check_request(response):
            html_content = response.content
            process_data(html_content, output_file)
            return True
        else:
            print(f"Request to {url} failed or was blocked.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return False

# Example usage:
if __name__ == "__main__":
    url = "http://qppot46h25jwdu6gotqmlpgc26ehm2hx325e6rdxb6o2lds4qoa4c3yd.onion/hacking-tech-everyday-news"
    output_file = 'extracted_content.txt'
    success = crawl(url, output_file)
    if success:
        print(f"Content extracted from {url} has been written to '{output_file}' file.")
    else:
        print(f"Failed to extract content from {url}.")
