import os

import requests
from typing import Dict, Any, Optional, List


# use ENV variables
# Constants
API_URL = "https://google.serper.dev/search"
API_KEY = os.getenv("SERPER_API_KEY")
DEFAULT_LOCATION = 'us'
HEADERS = {
    'X-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}


def get_sources(query: str, pro_mode: bool = False, stored_location: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch search results from Serper API.

    :param query: Search query string
    :param pro_mode: Boolean to determine the number of results
    :param stored_location: Optional location string
    :return: Dictionary containing search results
    """
    try:
        search_location = (stored_location or DEFAULT_LOCATION).lower()
        num_results = 10 if pro_mode else 20

        payload = {
            "q": query,
            "num": num_results,
            "gl": search_location
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            'organic': extract_fields(data.get('organic', []), ['title', 'link', 'snippet', 'date']),
            'topStories': extract_fields(data.get('topStories', []), ['title', 'imageUrl']),
            'images': extract_fields(data.get('images', [])[:6], ['title', 'imageUrl']),
            'graph': data.get('knowledgeGraph'),
            'answerBox': data.get('answerBox')
        }

    except requests.RequestException as e:
        print(f"HTTP error while getting sources: {e}")
    except Exception as e:
        print(f"Unexpected error while getting sources: {e}")

    return {}


def extract_fields(items: List[Dict[str, Any]], fields: List[str]) -> List[Dict[str, Any]]:
    """
    Extract specified fields from a list of dictionaries.

    :param items: List of dictionaries
    :param fields: List of fields to extract
    :return: List of dictionaries with only the specified fields
    """
    return [{key: item[key] for key in fields if key in item} for item in items]
