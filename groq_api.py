import json
import os
from groq import Groq
from langchain_core.prompts import PromptTemplate
from prompts import search_prompt_system, relevant_prompt_system

# use ENV variables
MODEL = "llama3-70b-8192"
api_key_groq = os.getenv("GROQ_API_KEY")


client = Groq()


def get_answer(query, contexts, date_context):
    system_prompt_search = PromptTemplate(input_variables=["date_today"], template=search_prompt_system)

    messages = [
        {"role": "system", "content": system_prompt_search.format(date_today=date_context)},
        {"role": "user", "content": "User Question : " + query + "\n\n CONTEXTS :\n\n" + contexts}
    ]

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            stop=None,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        print(f"Error during get_answer_groq call: {e}")
        yield "data:" + json.dumps(
            {'type': 'error', 'data': "We are currently experiencing some issues. Please try again later."}) + "\n\n"


def get_relevant_questions(contexts, query):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system",
                 "content": relevant_prompt_system
                 },
                {"role": "user",
                 "content": "User Query: " + query + "\n\n" + "Contexts: " + "\n" + contexts + "\n"}
            ],
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during RELEVANT GROQ ***************: {e}")
        return {}
