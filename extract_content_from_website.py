from langchain_community.document_loaders import WebBaseLoader


def extract_website_content(url):
    """
    Extracts and cleans the main content from a given website URL.

    Args:
    url (str): The URL of the website from which to extract content.

    Returns:
    str: The first 4000 characters of the cleaned main content if it is sufficiently long, otherwise an empty string.
    """
    try:
        clean_text = []
        loader = WebBaseLoader(url)
        data = loader.load()

        # Aggregate content using a list to avoid inefficient string concatenation in the loop
        for doc in data:
            if doc.page_content:  # Check if page_content is not None or empty
                clean_text.append(doc.page_content.replace("\n", ""))

                # Join all parts into a single string after processing
        clean_text = "".join(clean_text)

        # Return up to the first 4000 characters if the content is sufficiently long
        return clean_text[:4000] if len(clean_text) > 200 else ""

    except Exception as error:
        print('Error extracting main content:', error)
        return ""
