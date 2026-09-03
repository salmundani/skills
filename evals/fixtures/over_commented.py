# This module handles retries.
import time

# Maximum number of retries
MAX_RETRIES = 3
# The base delay
BASE_DELAY = 0.5


# This function fetches a url with retries
def fetch_with_retry(client, url):
    # Loop over the attempts
    for attempt in range(MAX_RETRIES):
        # Try to get the url
        try:
            return client.get(url)
        # Catch the timeout
        except TimeoutError:
            # If this was the last attempt, re-raise
            if attempt == MAX_RETRIES - 1:
                raise
            # Sleep with exponential backoff
            time.sleep(BASE_DELAY * (2**attempt))
            # old version: time.sleep(BASE_DELAY)
