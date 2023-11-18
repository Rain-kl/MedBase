import uvicorn
from typing import Union
from model import Async_xywy
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from Parse import Parse

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/search")
def searchDisease(kw: str):
    rsp = asyncio.run(Async_xywy().searchDisease(kw))
    rsp = Parse.parseSearchDisease(rsp)
    print(rsp)
    return rsp


@app.get("/info")
def getDiseaseInfo(kw: str):
    rsp = asyncio.run(Async_xywy().run(kw))
    return rsp


if __name__ == '__main__':
    uvicorn.run(app, reload=True)
