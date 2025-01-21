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

if not API_KEY:
    logger.error("JINA_API_KEY is not set in environment variables.")
    raise ValueError("JINA_API_KEY is required but not set.")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

session = requests.Session()
session.headers.update(HEADERS)


def get_reranking_jina(docs: List[str], query: str, top_res: int, timeout: int = 10) -> List[str]:
    """
    Get reranked documents using Jina AI API.

    :param docs: List of documents to rerank
    :param query: Query string
    :param top_res: Number of top results to return
    :param timeout: Request timeout in seconds
    :return: List of reranked documents
    """
    data = {
        "model": MODEL,
        "query": query,
        "documents": docs,
        "top_n": top_res
    }

    try:
        response = session.post(API_URL, json=data, timeout=timeout)
        response.raise_for_status()
        response_data = response.json()

        reranked_docs = [item['document']['text'] for item in response_data.get('results', [])]
        if not reranked_docs:
            logger.warning("No reranked results returned.")
        return reranked_docs

    except RequestException as e:
        logger.error(f"HTTP error occurred while reranking: {e}")
    except KeyError as e:
        logger.error(f"Unexpected response format: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

    return []
