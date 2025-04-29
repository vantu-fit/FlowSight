import requests
import urllib.parse
import json
from src.config.scraping_settings import USE_SESSION_POOL, MAX_CONNECTIONS, DEFAULT_HEADERS

session = requests.Session()
session.headers.update(DEFAULT_HEADERS)
adapter = requests.adapters.HTTPAdapter(pool_connections=MAX_CONNECTIONS, pool_maxsize=MAX_CONNECTIONS)
session.mount('http://', adapter)
session.mount('https://', adapter)

def encode_url_path(path):
    """Properly encode URL path components"""
    components = path.split('/')
    encoded = '/'.join(urllib.parse.quote(component) for component in components)
    return encoded

def inspect_api_response(base_url, path=""):
    """Print full details of API response to understand the structure"""
    url = base_url + encode_url_path(path)
    try:
        print(f"Inspecting URL: {url}")
        response = session.get(url) if USE_SESSION_POOL else requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Response contains {len(data)} items")
            return data
        else:
            print(f"Failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None