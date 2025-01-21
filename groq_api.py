import json
import os
import logging
from typing import Generator, Dict, Any
from groq import Groq
from langchain_core.prompts import PromptTemplate
from prompts import search_prompt_system, relevant_prompt_system

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment Variables
MODEL = "llama-3.3-70b-versatile"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY is not set in environment variables.")
    raise ValueError("GROQ_API_KEY is required but not set.")

client = Groq(api_key=GROQ_API_KEY)


def get_answer(query: str, contexts: str, date_context: str) -> Generator[str, None, None]:
    """
    Generate an answer based on the query and contexts using Groq API.

    :param query: User's search query.
    :param contexts: Contextual information related to the query.
    :param date_context: Current date and time context.
    :return: Generator yielding chunks of the answer.
    """
    system_prompt = PromptTemplate(input_variables=["date_today"], template=search_prompt_system)

    messages = [
        {"role": "system", "content": system_prompt.format(date_today=date_context)},
        {"role": "user", "content": f"User Question: {query}\n\nCONTEXTS:\n\n{contexts}"}
    ]

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            stop=None,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    except Exception as e:
        logger.exception(f"Error during get_answer_groq call: {e}")
        error_response = json.dumps({
            'type': 'error',
            'data': "We are currently experiencing some issues. Please try again later."
        })
        yield f"data:{error_response}\n\n"


def get_relevant_questions(contexts: str, query: str) -> Dict[str, Any]:
    """
    Generate relevant follow-up questions based on the query and contexts using Groq API.

    :param contexts: Contextual information related to the query.
    :param query: User's search query.
    :return: Dictionary containing follow-up questions.
    """
    messages = [
        {"role": "system", "content": relevant_prompt_system},
        {"role": "user", "content": f"User Query: {query}\n\nContexts:\n{contexts}\n"}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format="json_object",
        )

        content = response.choices[0].message.content
        follow_up = json.loads(content)
        return follow_up

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in get_relevant_questions: {e}")
    except Exception as e:
        logger.exception(f"Error during get_relevant_questions: {e}")

    return {}
