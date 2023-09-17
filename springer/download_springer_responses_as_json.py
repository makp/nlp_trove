import requests
import json
import time
import data_processing.config_springer


BASE_URL = "https://api.springernature.com/metadata/json"
WAIT_TIME = 1  # wait time between requests
COUNT_PER_REQUEST = 50

api_key = data_processing.config_springer.API_KEY


def get_number_results(query_str):
    """Return the total number of results for a given query."""
    params = {
        "q": query_str,
        "p": 1,   # Num of results per request
        's': 1,   # Start index
        "api_key": api_key
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return int(data['result'][0]['total'])


def fetch_single_response(query_str, start):
    """Make a single request to the API and return the response data."""
    params = {
        "q": query_str,
        "p": COUNT_PER_REQUEST,
        's': start,
        "api_key": api_key
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()


def fetch_all_responses(query_str):
    """Return all response data for a given query."""
    total_records = get_number_results(query_str)
    all_data = []
    for start in range(1, total_records + 1, COUNT_PER_REQUEST):
        data = fetch_single_response(query_str, start)
        all_data.append(data)
        time.sleep(WAIT_TIME)
    return all_data


def download_responses_from_springer(query_str):
    """Download all responses for a given query and save them as a
    JSON file.
    """
    all_data = fetch_all_responses(query_str)
    fname = query_str.replace(" ", "_") + '.json'
    with open(fname, 'w') as f:
        json.dump(all_data, f)
    print(f"Saved responses to {fname}")
    return fname
