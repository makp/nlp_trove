import requests
import json
import time
import config_springer  # file containing API key


api_key = config_springer.API_KEY
base_url = "https://api.springernature.com/metadata/json"
WAIT_TIME = 1  # wait time between requests


def get_number_results(query_str):
    """Return the total number of results for a given query."""
    params = {
        "q": query_str,
        "p": 1,   # Number of results per request
        's': 1,   # Return results
        "api_key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    num_results = int(data['result'][0]['total'])
    return num_results


def make_request(query_str, start, records_per_page):
    """Make a single request to the API and return the response data."""
    params = {
        "q": query_str,
        "p": records_per_page,
        's': start,
        "api_key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


def get_responses(query_str, records_per_page):
    """Return all response data for a given query."""
    total_records = get_number_results(query_str)
    all_data = []
    for i in range(0, total_records, records_per_page):
        start = i + 1
        data = make_request(query_str, start, records_per_page)
        all_data.append(data)
        time.sleep(WAIT_TIME)
    return all_data


def download_responses(query_str, records_per_page=50):
    """Download all responses for a given query and save them as a
    JSON file. Example:
    > download_responses("journalid:11229 AND language:en")
    """
    all_data = get_responses(query_str, records_per_page)
    fname = query_str + '.json'
    with open(fname, 'w') as f:
        json.dump(all_data, f)


journalids = {'synthese': 11229}
query_str = "journalid:" + str(journalids['synthese']) + ' AND language:en'

download_responses(query_str)
