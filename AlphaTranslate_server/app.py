from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from mtranslate import translate
from pydantic import BaseModel
from langdetect import detect


app = FastAPI()

# ***********************
# HELP
# ***********************
"""
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/translate?user_query=love
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/translate?user_query="i see you"
curl http://91.205.164.229:8090/translate?user_query=123
curl -H "Content-Type: application/json" -d '{"name":"jack"}' http://91.205.164.229:8090/translate2

py -m venv .venv
pip freeze > requirements.txt
pip install -r requirements.txt

response = requests.get('http://127.0.0.1:8000/translate/?user_query=i see you')
print(response.status_code)
print(response.json())
"""


# ***********************
# CONFIG
# ***********************

host= '0.0.0.0'
port=8090


# ***********************
# CLASS
# ***********************

class Query(BaseModel):
    name: str
    age: int


# ***********************
# APP
# ***********************

@app.get("/")
def read_root():
    return JSONResponse(content={"message":"not supported"})


@app.get("/translate")
def ru_eng_translate(user_query: str):

    translated_text = 'error905'

    if user_query[0] == '!':
        translated_text = translate(user_query[1:], to_language="ru", from_language="en")
    if user_query[0] == '?':
        translated_text = translate(user_query[1:], to_language="en", from_language="ru")

    print(user_query, translated_text)
    return JSONResponse(content=translated_text)


@app.post("/translate2")
def ru_eng_translate2(query: list[Query]):
    return {"message": query}


# ***********************
# START
# ***********************

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=port)


