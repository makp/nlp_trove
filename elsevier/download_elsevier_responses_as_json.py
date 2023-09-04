import requests
import json
import time
import urllib.parse
import data_processing.config_elsevier


BASE_URL = "http://api.elsevier.com/content/search/scopus?"
WAIT_TIME = 1  # wait time between requests

api_key = data_processing.config_elsevier.API_KEY


def get_number_results(query_str):
    """Return the total number of results for a given query."""
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key
    }
    params = {
        "query": query_str,
        "count": 1     # only need to know the total number of results
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    response_dic = json.loads(response.text)
    num_results = response_dic.get('search-results', {}).get('opensearch:totalResults', 0)
    return int(num_results)


def fetch_single_request(query_str, url, params):
    """Make a single request to the API and return the response data."""
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    return json.loads(response.text)


