import os
import requests
from typing import List
import logging
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
API_URL = "https://api.jina.ai/v1/rerank"
API_KEY = os.getenv("JINA_API_KEY")
MODEL = "jina-reranker-v2-base-multilingual"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


def get_reranking_jina(docs: List[str], query: str, top_res: int) -> List[str]:
    """
    Get reranked documents using Jina AI API.

    :param docs: List of documents to rerank
    :param query: Query string
    :param top_res: Number of top results to return
    :return: List of reranked documents
    """
    try:
        data = {
            "model": MODEL,
            "query": query,
            "documents": docs,
            "top_n": top_res
        }

        response = requests.post(API_URL, headers=HEADERS, json=data, timeout=10)
        response.raise_for_status()
        response_data = response.json()

        return [item['document']['text'] for item in response_data.get('results', [])]

    except RequestException as e:
        logger.error(f"HTTP error occurred while reranking: {e}")
    except KeyError as e:
        logger.error(f"Unexpected response format: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

    return []
