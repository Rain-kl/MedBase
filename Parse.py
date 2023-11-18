import httpx
from loguru import logger
from lxml import etree


class Parse:
    @staticmethod
    def parseSearchDisease(response: httpx.Response):
        html = response.text
        tree = etree.HTML(html)
        # print(html)
        diseases = tree.xpath('//div[@class="result-box1"]/div[@class="result_list"]')
        # print(diseases)
        disease_info = []
        for disease in diseases:
            try:
                title = disease.xpath('./h3/a//text()')[0]
                url = disease.xpath('./h3/a/@href')[0]
                disease_info.append({
                    'title': title,
                    'url': url
                })
            except:
                logger.error(f'无内容')
                return []
        # print(disease_info)
        return disease_info

    @staticmethod
    def parseWestDiseaseInfo(response: httpx.Response):
        html = response.text
        tree = etree.HTML(html)
        # print(html)
        disease = tree.xpath('//div[@class="jib-articl fr f14 jib-lh-articl"]//text()')
        if len(disease) == 0:
            disease = tree.xpath('//div[@class=" jib-articl fr f14 jib-lh-articl"]//text()')
        # print(disease)
        return disease

    @staticmethod
    def parseCtmDiseaseInfo(response: httpx.Response):
        html = response.text
        tree = etree.HTML(html)
        # print(html)
        disease = tree.xpath('//div[@class="zz-articl fr f14"]//text()')
        # print(disease)
        return disease
