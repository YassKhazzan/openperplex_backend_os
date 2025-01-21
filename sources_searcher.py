import os
import requests
import logging
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants and Environment Variables
API_URL = os.getenv("SERPER_API_URL", "https://google.serper.dev/search")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
DEFAULT_LOCATION = 'us'

if not SERPER_API_KEY:
    logger.error("SERPER_API_KEY is not set in environment variables.")
    raise ValueError("SERPER_API_KEY is required but not set.")

HEADERS = {
    'X-API-KEY': SERPER_API_KEY,
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
    search_location = (stored_location or DEFAULT_LOCATION).lower()
    num_results = 10 if pro_mode else 20

    payload = {
        "q": query,
        "num": num_results,
        "gl": search_location
    }

    try:
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
        logger.error(f"HTTP error while getting sources: {e}")
    except ValueError as e:
        logger.error(f"JSON decoding failed: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error while getting sources: {e}")

    return {}


def extract_fields(items: List[Dict[str, Any]], fields: List[str]) -> List[Dict[str, Any]]:
    """
    Extract specified fields from a list of dictionaries.

    :param items: List of dictionaries
    :param fields: List of fields to extract
    :return: List of dictionaries with only the specified fields
    """
    extracted = []
    for item in items:
        extracted_item = {key: item[key] for key in fields if key in item}
        if extracted_item:
            extracted.append(extracted_item)
    return extracted
