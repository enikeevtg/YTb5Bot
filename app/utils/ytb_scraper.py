import aiohttp
import asyncio
import bs4
from bs4 import BeautifulSoup
import logging
from fake_useragent import UserAgent
import json


logger = logging.getLogger(__name__)


class YouTubeScraper:
    __ytInitialDataVar = 'var ytInitialData = '
    __request_prefix = 'https://www.youtube.com/results?search_query='
    __link_prefix = 'https://www.youtube.com/watch?v='

    def __init__(self):
        logger.debug('YouTubeScraper launch')

    async def ytb_search_request(self, request: str) -> dict:
        soup = await self.__get_ytb_search_response(request)
        scripts = soup.find_all('script')

        for script in scripts:
            if self.__ytInitialDataVar in str(script):
                return self.__get_data_from_script(script)

    async def __get_ytb_search_response(self, request: str) -> BeautifulSoup:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__request_prefix + request) as response:
                return BeautifulSoup(await response.text(), 'lxml')

    def __get_data_from_script(self, script: bs4.element.Tag) -> list:
        json_dict = self.__extract_json(script)

        # with open('test.json', 'r') as fp:
        #     json_dict = json.load(fp)

        data = []
        contents = json_dict["contents"]
        if "sectionListRenderer" in contents:
            items = (contents["sectionListRenderer"]
                             ["contents"]
                             [0]
                             ["itemSectionRenderer"]
                             ["contents"])
            for item in items:
                item = item.get("videoWithContextRenderer", False)
                if item is not False:
                    item = item["videoWithContextRenderer"]
                    # title = item["headline"]["runs"][0]["text"]
                    # data['title'] = item["videoId"]
                    data.append(self.__link_prefix + item["videoId"])
         
        elif "twoColumnSearchResultsRenderer" in contents:
            items = (contents["twoColumnSearchResultsRenderer"]
                             ["primaryContents"]
                             ["sectionListRenderer"]
                             ["contents"]
                             [0]
                             ["itemSectionRenderer"]
                             ["contents"])
            for item in items:
                item = item.get("videoRenderer", False)
                if item is not False:
                    # title = item["title"]["runs"][0]["text"]
                    # data.append({"title": title,
                    #               "videoId": item["videoId"]})
                    data.append(self.__link_prefix + item["videoId"])
        else:
            logger.debug("Новый формат JSON")
            with open('test.json', 'w') as fp:
                json.dump({"contents": json_dict["contents"]}, fp,
                          indent=2, ensure_ascii=False)
        
        return data

    def __extract_json(self, script: bs4.element.Tag) -> dict:
        text = (script.text.replace('\\x22', '"')
                           .replace('\\x7b', '{')
                           .replace('\\x7d', '}')
                           .replace('\\x5b', '[')
                           .replace('\\x5d', ']')
                           .replace('\\x3d', '=')
                           .replace('\\\\"', '\\"')
                           .replace('\'','')
                           )[len(self.__ytInitialDataVar):-1]
        return json.loads(text)


async def main():
    data = await YouTubeScraper().ytb_search_request('Python')
    for e in data:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
