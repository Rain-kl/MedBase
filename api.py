import uvicorn
from model import Async_xywy
from fastapi import FastAPI
import asyncio
from Parse import Parse

app = FastAPI()


@app.get("/search")
def searchDisease(kw: str):
    """
    搜索疾病, 返回疾病列表
    :param kw:
    :return:
    """
    rsp = asyncio.run(Async_xywy().searchDisease(kw))
    rsp = Parse.parseSearchDisease(rsp)
    print(rsp)
    return rsp


@app.get("/info")
def getDiseaseInfo(kw: str):
    """
    获取疾病信息
    :param kw:
    :return:
    """
    rsp = asyncio.run(Async_xywy().run(kw))
    return rsp


if __name__ == '__main__':
    uvicorn.run("api:app", reload=True)
