from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from mtranslate import translate
from pydantic import BaseModel
from langdetect import detect
import CONFIG
import SECRET


app = FastAPI()


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
    uvicorn.run(app, host=SECRET.host, port=SECRET.port)


