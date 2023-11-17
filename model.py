from Parse import Parse
from ext import AsyncSpider
import httpx
import asyncio
import re
import json
from loguru import logger
from lxml import etree
from ext import Retry


class AsyncDisInfo(AsyncSpider):
    def __init__(self, headers):
        super().__init__(headers)
        self.url = httpx.URL("https://so.xywy.com")

    async def getDiseaseInfo(self, section:str, url: str):
        """
        http://jib.xywy.com/il_sii/symptom/38.htm
        :param section:
        :param url: http://jib.xywy.com/il_sii_38.htm
        :return:
        """
        url_path = url.split('/')[-1]
        disease_id = re.findall(r'il_sii_(\d+)\.htm', url_path)[0]
        url = httpx.URL.join(self.url, f"il_sii/symptom/{disease_id}.htm")
        rsp = await self._get_request(url)
        return rsp


class Async_xywy(AsyncDisInfo):

    def searchDisease(self, keyword):
        tar_url = httpx.URL.join(self.url, "jib.php")
        params = {
            'keyword': keyword,
            'src': 'so'
        }
        rsp = self._get_request(tar_url, params=params)
        return rsp

    async def getDisInfo(self, url):
        tasks = []


def main():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/102.0.0.0 Safari/537.36"
    }
    te = Async_xywy(header)
    rsp = asyncio.run(te.searchDisease("气滞血瘀"))
    prsp = Parse.parseSearchDisease(rsp)
    print(prsp)


if __name__ == '__main__':
    main()
