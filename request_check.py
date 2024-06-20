import requests

def check_request(response):
    """
    Checks if the request was successful (status code 200) or encountered an error.
    Returns True if successful, False otherwise.
    """
    try:
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return False
