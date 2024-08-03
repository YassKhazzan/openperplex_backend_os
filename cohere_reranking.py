import os

import cohere


# use ENV variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
MODEL = "rerank-multilingual-v3.0"

co = cohere.Client(api_key=COHERE_API_KEY)


def get_reranking_cohere(docs, query, top_res):
    """
    Re-ranks a list of documents based on a query using Cohere's reranking API.

    Args:
    docs (list of str): List of documents to be re-ranked.
    query (str): Query string to rank the documents against.
    top_res (int): Number of top results to return.

    Returns:
    list of str: Top re-ranked documents based on the query.
    """
    try:
        # Call the Cohere rerank API
        response = co.rerank(
            model=MODEL,
            query=query,
            documents=docs,
            top_n=top_res,
            return_documents=True
        )

        # Extract and return the texts of the top documents
        return [item.document.text for item in response.results]

    except Exception as e:
        # Log the error and handle it as needed
        print(f"An error occurred: {e}")
        return []
