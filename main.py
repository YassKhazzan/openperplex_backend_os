import orjson as json
from dotenv import load_dotenv

load_dotenv()

from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq_api import get_answer, get_relevant_questions
from sources_searcher import get_sources
from build_context import build_context
from sources_manipulation import populate_sources


app = FastAPI()

# allow_origins=["https://openperplex.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow all methods or specify like ["POST", "GET"]
    allow_headers=["*"],  # Allow all headers or specify
)

load_dotenv()


@app.get("/")
def root():
    return {"message": "hello world openperplex v1"}


@app.get("/up_test")
def up_test():
    # test for kamal deploy
    return {"status": "ok"}


# you can change to post if typical your query is too long
@app.get("/search")
def ask(query: str, date_context: str, stored_location: str, pro_mode: bool = False):
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    def generate():
        try:
            sources_result = get_sources(query, pro_mode, stored_location)
            yield "data:" + json.dumps({'type': 'sources', 'data': sources_result}).decode() + "\n\n"

            if sources_result.get('organic') is not None and pro_mode is True:
                # set the number of websites to scrape : here = 2
                sources_result['organic'] = populate_sources(sources_result['organic'], 2)

            search_contexts = build_context(sources_result, query, pro_mode, date_context)

            for chunk in get_answer(query, search_contexts, date_context):
                yield "data:" + json.dumps({'type': 'llm', 'text': chunk}).decode() + "\n\n"

            try:
                relevant_questions = get_relevant_questions(search_contexts, query)
                relevant_json = json.loads(relevant_questions)
                yield "data:" + json.dumps({'type': 'relevant', 'data': relevant_json}).decode() + "\n\n"
            except Exception as e:
                print(f"error in relevant questions main.py {e}")
                yield "data:" + json.dumps({'type': 'relevant', 'data': []}).decode() + "\n\n"

            yield "data:" + json.dumps({'type': 'finished', 'data': ""}).decode() + "\n\n"
            yield "event: end-of-stream\ndata: null\n\n"

        except Exception as e:
            print(e)
            yield "data:" + json.dumps(
                {'type': 'error',
                 'data': "We are currently experiencing some issues. Please try again later."}).decode() + "\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
