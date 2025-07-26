from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from mtranslate import translate
from pydantic import BaseModel
from langdetect import detect


app = FastAPI()

class Query(BaseModel):
    name: str
    age: int

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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)


