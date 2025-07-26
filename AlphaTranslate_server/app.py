from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from mtranslate import translate
from pydantic import BaseModel
from langdetect import detect
import CONFIG


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
def ru_eng_translate(user_query):

    to__language = None
    from__language = None

    translated_text = translate(user_query, "ru", "auto")
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
    uvicorn.run(app, host=CONFIG.host, port=CONFIG.port)


