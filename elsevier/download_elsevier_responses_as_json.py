import requests
import time
import json
import data_processing.config_elsevier


BASE_URL = "http://api.elsevier.com/content/search/scopus?"
WAIT_TIME = 1  # wait time between requests in seconds
COUNT_PER_REQUEST = 200
HEADERS = {
    "Accept": "application/json",
    "X-ELS-APIKey": data_processing.config_elsevier.API_KEY
}


def get_number_results(query_str):
    """Return the total number of results for a given query."""
    params = {
        "query": query_str,
        "count": 1     # only need to know the total number of results
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    response_dic = response.json()
    num_results = response_dic.get('search-results', {}).get('opensearch:totalResults', 0)
    return int(num_results)


def fetch_single_request(params):
    """Make a single request to the API and return the response data."""
    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    return response.json()


def fetch_batch_of_articles(query_str, cursor='*'):
    """Return a batch of articles for a given query."""
    params = {
        "query": query_str,
        "count": COUNT_PER_REQUEST,
        "cursor": cursor
    }

    response_dic = fetch_single_request(params)
    next_cursor = response_dic.get('search-results', {}).get('cursor', {}).get('@next', None)

    if response_dic:
        return response_dic.get("search-results", {}).get("entry", []), next_cursor
    return []


def fetch_all_articles(query_str, cursor='*'):
    """Return all articles for a given query."""
    all_articles = []
    num_results = get_number_results(query_str)
    print(f"Total number of results: {num_results}")

    if num_results is None:
        print("Error: Could not get number of results")
        return []

    next_cursor = cursor
    num_fetched_articles = 0
    while num_fetched_articles < num_results:
        batch_articles, next_cursor = fetch_batch_of_articles(query_str, next_cursor)
        all_articles.extend(batch_articles)

        num_fetched_articles = len(all_articles)
        print(f"Number of articles fetched: {num_fetched_articles}")

        time.sleep(WAIT_TIME)

    # for idx in range(start, num_results, COUNT_PER_REQUEST):
    #     all_articles.extend(fetch_batch_of_articles(query_str, idx))
    #     print(idx)
    #     time.sleep(WAIT_TIME)

    return all_articles


def download_responses(query_str, cursor='*'):
    """Download all responses for a given query and save them as a
    JSON file.
    """
    all_data = fetch_all_articles(query_str, cursor)
    with open('out.json', 'w') as f:
        json.dump(all_data, f)

    return 'out.json'
