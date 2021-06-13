import asyncio
from xml.etree.ElementTree import Element

import aiohttp
import defusedxml.ElementTree as ET
import requests


async def aiohttp_get(url: str) -> str:
    user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    headers = {"user-agent": user_agent, "Content-Type": "text/xml"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()


def xml_getter(rssfeed: str) -> Element:
    data = requests.get(rssfeed, proxies=dict(http='socks5://:@127.0.0.1:9050',
                                              https='socks5://:@127.0.0.1:9050'))
    data.encoding = data.apparent_encoding
    tree = ET.fromstring(data.content)
    return tree


def youtuber(tree: Element):
    videos = list()
    for entry in tree.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        group = entry.find('{http://search.yahoo.com/mrss/}group')
        link = group.find('{http://search.yahoo.com/mrss/}content').attrib['url']
        thumbnail = group.find('{http://search.yahoo.com/mrss/}thumbnail').attrib['url']
        videos.append((title, link, thumbnail))
    return videos


def stackoverflower(tree: Element):
    activities = list()
    for entry in tree.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
        activities.append((title, link))
    return activities


stackoverflower(xml_getter(stack_feed))

# async def main():
#     data = await aiohttp_get(stack_feed)
#     with open('stack_feed.xml', 'w')as ff:
#         ff.write(data)
#     return


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
