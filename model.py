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
    def __init__(self):
        super().__init__()
        self.url = httpx.URL("https://so.xywy.com")
        self.west_url = httpx.URL("http://jib.xywy.com/")
        self.ctm_url = httpx.URL("http://zzk.xywy.com/")

    def west_ctm(self, section):
        """
        将西医的section转换为中医的section
        :param section:
        :return:
        """
        sections = {
            "diagnosis": "jieshao",
            "symptom": "zhenduan",
            "inspect": "jiancha",
            "cause": "yuanyin"
        }
        return sections[section]

    async def getDiseaseInfo(self, section: str, url: str):
        """
        获取疾病信息
        http://jib.xywy.com/il_sii/symptom/38.htm
        :param section: 栏目分类
        :param url: http://jib.xywy.com/il_sii_38.htm
        :return:
        """

        url_path = url.split('/')[-1]
        if "jib" in url:
            # http://jib.xywy.com/il_sii_38.htm
            # http://jib.xywy.com/il_sii/inspect/38.htm
            disease_id = re.findall(r'il_sii_(\d+)\.htm', url_path)[0]
            url = httpx.URL.join(self.west_url, f"il_sii/{section}/{disease_id}.htm")
        elif "zzk" in url:
            # http://zzk.xywy.com/3370_gaishu.html
            # http://zzk.xywy.com/3370_yuanyin.html
            disease_id = re.findall(r'(\d+)_gaishu', url_path)[0]
            url = httpx.URL.join(self.ctm_url, f"{disease_id}_{self.west_ctm(section)}.html")
        rsp = await self._get_request(url.__str__())
        rsp.encoding = 'gbk'
        return rsp


class Async_xywy(AsyncDisInfo):

    async def searchDisease(self, keyword):
        """
        搜索疾病
        :param keyword:
        :return:
        """
        tar_url = httpx.URL.join(self.url, "jib.php")
        params = {
            'keyword': keyword,
            'src': 'so'
        }
        rsp = await self._get_request(tar_url.__str__(), params=params)
        return rsp

    async def getDisInfo(self, sections: list, url: str):
        """
        获取疾病信息，异步调用getDiseaseInfo
        :param sections:  [
                            "diagnosis",
                            "symptom",
                            "inspect",
                            "cause"
                        ]
        :param url:
        :return:
        """
        tasks = []
        for section in sections:
            tasks.append(asyncio.create_task(self.getDiseaseInfo(section, url)))
        await asyncio.wait(tasks)
        return tasks

    async def run(self, keyword, sections=None):
        """
        运行
        :param sections:
        :param keyword:
        :return:
        """
        if sections is None:
            sections = [
                "diagnosis",
                "symptom",
                "inspect",
                "cause"
            ]
        rsp = await self.searchDisease(keyword)
        prsp = Parse.parseSearchDisease(rsp)
        # print(prsp)
        ids_info={}
        for i in prsp:
            url = i['url']
            tasks = await self.getDisInfo(sections, url)
            for index,task in enumerate(tasks):
                if "jib" in url:
                    ids_info[sections[index]] = Parse.parseWestDiseaseInfo(task.result())
                    # print(Parse.parseWestDiseaseInfo(task.result()))
                elif "zzk" in url:
                    ids_info[self.west_ctm(sections[index])] = Parse.parseCtmDiseaseInfo(task.result())
                    # print(Parse.parseCtmDiseaseInfo(task.result()))
            break

        return ids_info


def main(keyword):
    sections = [
        "diagnosis",
        "symptom",
        "inspect",
        "cause"
    ]
    te = Async_xywy()
    rsp = asyncio.run(te.run(sections, keyword))
    print(rsp)


if __name__ == '__main__':
    main("感冒")
