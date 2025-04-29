# Scraping configuration settings

# Parallel processing settings
ENABLE_PARALLEL = True
MAX_WORKERS = 20  
REQUEST_TIMEOUT = 15  
DELAY_BETWEEN_REQUESTS = 0.2  

# Connection pool settings
USE_SESSION_POOL = True
MAX_CONNECTIONS = 100

# Headers to make the request look like a browser
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Connection': 'keep-alive'
}