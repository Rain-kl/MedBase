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
