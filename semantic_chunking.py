import os
import logging
from typing import List

from semantic_router.encoders import CohereEncoder
from semantic_chunkers import StatisticalChunker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment Variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    logger.error("COHERE_API_KEY is not set in environment variables.")
    raise ValueError("COHERE_API_KEY is required but not set.")

# Initialize Encoder and Chunker
try:
    encoder = CohereEncoder(
        cohere_api_key=COHERE_API_KEY,
        input_type='search_document',
        name='embed-multilingual-v3.0'
    )
    chunker = StatisticalChunker(encoder=encoder, max_split_tokens=200)
except Exception as e:
    logger.exception(f"Failed to initialize encoder or chunker: {e}")
    raise


def get_chunking(text: str) -> List[str]:
    """
    Splits the provided text into meaningful chunks using a predefined chunker.

    Args:
        text (str): The text to be chunked.

    Returns:
        List[str]: A list of chunks if the text is sufficiently long and non-empty; otherwise, an empty list.
    """
    if not text or len(text.strip()) == 0:
        logger.warning("Empty or whitespace-only text provided for chunking.")
        return []

    try:
        chunks = chunker(docs=[text])
        if not chunks:
            logger.warning("Chunker returned no chunks.")
            return []

        values = [c.content for chunk in chunks for c in chunk if c.content]
        if not values:
            logger.warning("No valid chunk contents extracted.")
        return values

    except Exception as e:
        logger.exception(f"Error during chunking process: {e}")
        return []
