import time

# The upstream API rate-limits at 4 req/s and returns 200 with an empty body
# instead of 429, so backoff has to be driven by the empty response, not status.
MIN_INTERVAL = 0.25


def fetch_all(client, urls):
    results = []
    for url in urls:
        response = client.get(url)
        if not response.content:
            # Empty body means throttled; retrying immediately makes it worse.
            time.sleep(MIN_INTERVAL * 4)
            response = client.get(url)
        results.append(response)
        time.sleep(MIN_INTERVAL)
    return results
