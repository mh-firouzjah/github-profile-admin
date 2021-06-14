from datetime import datetime

import aiohttp
import defusedxml.ElementTree as ET  # safe xml parser
import humanize


async def aiohttp_get(url: str) -> bytes:
    user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    headers = {"user-agent": user_agent, "Content-Type": "text/xml"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.read()


async def feedparser(url: str) -> list[tuple[str, str, str, str]]:
    '''will return a list contining tuples of`(title: str, link: str~=url, published: humanized-date, thumbnail: str~=url)`'''
    res = list()
    tree = ET.fromstring(await aiohttp_get(url))  # to read xml from url
    # tree = ET.parse(url)  # to read xml files
    for entry in tree.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']

        published = entry.find('{http://www.w3.org/2005/Atom}published').text
        if published:
            try:
                published = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                published = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                pass
            else:
                published = humanize.naturalday(published)

        # youtube-videos have thumbnail
        thumbnail = ''
        if (group := entry.find('{http://search.yahoo.com/mrss/}group')):
            thumbnail = group.find('{http://search.yahoo.com/mrss/}thumbnail'
                                   ).attrib['url']

        res.append((title, link, published, thumbnail))
    return res
