import logging
from typing import List, Dict, Any

from extract_content_from_website import extract_website_content

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def populate_sources(sources: List[Dict[str, Any]], num_elements: int) -> List[Dict[str, Any]]:
    """
    Enriches source entries with HTML content extracted from their links.

    :param sources: List of source dictionaries containing at least a 'link' key.
    :param num_elements: Number of source elements to process.
    :return: Updated list of sources with 'html' content added where possible.
    """
    if not sources:
        logger.warning("No sources provided to populate.")
        return sources

    num_to_process = min(num_elements, len(sources))
    logger.info(f"Populating HTML content for the first {num_to_process} sources.")

    for i in range(num_to_process):
        source = sources[i]
        if not source:
            logger.warning(f"Source at index {i} is empty. Skipping.")
            continue

        link = source.get('link')
        if not link:
            logger.warning(f"Source at index {i} lacks a 'link'. Skipping.")
            continue

        try:
            html_content = extract_website_content(link)
            source['html'] = html_content
        except Exception as e:
            logger.error(f"Failed to extract content from {link}: {e}")
            source['html'] = ""

    return sources
