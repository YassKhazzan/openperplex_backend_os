import os
import logging
from typing import List

import cohere

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment Variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
MODEL = os.getenv("COHERE_RERANK_MODEL", "rerank-multilingual-v3.0")

if not COHERE_API_KEY:
    logger.error("COHERE_API_KEY is not set in environment variables.")
    raise ValueError("COHERE_API_KEY is required but not set.")

# Initialize Cohere Client
try:
    co = cohere.Client(api_key=COHERE_API_KEY)
except Exception as e:
    logger.exception(f"Failed to initialize Cohere client: {e}")
    raise


def get_reranking_cohere(docs: List[str], query: str, top_res: int) -> List[str]:
    """
    Re-ranks a list of documents based on a query using Cohere's reranking API.

    Args:
        docs (List[str]): List of documents to be re-ranked.
        query (str): Query string to rank the documents against.
        top_res (int): Number of top results to return.

    Returns:
        List[str]: Top re-ranked documents based on the query.
    """
    if not docs:
        logger.warning("No documents provided for reranking.")
        return []

    if not query:
        logger.warning("Empty query provided for reranking.")
        return []

    if top_res <= 0:
        logger.warning("Invalid top_res value provided. Must be greater than 0.")
        return []

    try:
        response = co.rerank(
            model=MODEL,
            query=query,
            documents=docs,
            top_n=top_res,
            return_documents=True
        )

        reranked_docs = [item.document.text for item in response.results]
        if not reranked_docs:
            logger.warning("Cohere rerank returned no results.")
        return reranked_docs

    except cohere.CohereError as e:
        logger.error(f"Cohere API error during reranking: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred during reranking: {e}")

    return []
