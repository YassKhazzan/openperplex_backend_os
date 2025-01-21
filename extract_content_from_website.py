import logging
from typing import Optional

from langchain_community.document_loaders import WebBaseLoader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MAX_CHARACTERS = 4000
MIN_LENGTH = 200


def extract_website_content(url: str) -> str:
    """
    Extracts and cleans the main content from a given website URL.

    Args:
        url (str): The URL of the website from which to extract content.

    Returns:
        str: The first 4000 characters of the cleaned main content if it is sufficiently long; otherwise, an empty string.
    """
    if not url or not isinstance(url, str):
        logger.error("Invalid URL provided for content extraction.")
        return ""

    try:
        loader = WebBaseLoader(url)
        data = loader.load()

        clean_text = []
        for doc in data:
            content = doc.page_content
            if content:
                cleaned = content.replace("\n", " ").strip()
                if cleaned:
                    clean_text.append(cleaned)

        combined_text = " ".join(clean_text)
        if len(combined_text) > MIN_LENGTH:
            return combined_text[:MAX_CHARACTERS]
        else:
            logger.warning(f"Extracted content is too short ({len(combined_text)} characters).")
            return ""

    except Exception as error:
        logger.exception(f"Error extracting main content from {url}: {error}")
        return ""
