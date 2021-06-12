import asyncio
import json
from datetime import date

from decouple import config

from github import GithubAdmin
from wakatime import WakaTimeReader

GH_TOKEN = config('GH_TOKEN')
gists_tag_start = (gists_tag := config('GISTS_TAG').split())[0]
gists_tag_end = gists_tag[1]
repo = config('REPO_NAME')


def markdown_link(text: str, link: str) -> str:
    '''generates markdown link'''
    return f"[{text}]({link})"


def profile_views_markdown(views: int) -> str:
    return f"![Profile Views](https://img.shields.io/badge/Weekly%20Views-{views}-blue?style=social&logo=github)"


async def main():
    # gh_account = GithubAdmin(config('GH_TOKEN'))
    # data = await gh_account.gists(5)
    # # print(data)
    # gists_links = []
    # for gist in data:
    #     link = gist["html_url"]
    #     description = gist["description"]
    #     gists_links.append(markdown_link(description, link))
    # content = '  \n'.join(it for it in gists_links)
    # views = await gh_account.get_repo_views(repo, 'week')
    # content = profile_views_markdown(views) + '  \n' + content
    # await gh_account.update_repo_readme(repo, gists_tag_start, gists_tag_end, content)

    waka = WakaTimeReader(config("WAKA_TIME_TOKEN"))
    waka_stats = (await waka.read_stats())["data"]
    # with open('waka.json', 'w') as ff:
    #     ff.write(json.dumps(waka_stats))
    print("In last 7 days I was:")
    for category in waka_stats["categories"]:
        print('\t', category["name"], "for", category["text"])
    print(
        '\t For a daily average of: ',
        waka_stats['human_readable_daily_average_including_other_language'])
    print('\t On operating systems:')
    for os in waka_stats["operating_systems"]:
        print('\t\t', os["name"], str(os["percent"])+'%')
    print("\t In programmin langauges:")
    for lang in waka_stats["languages"]:
        print('\t\t', lang["name"], lang["text"], str(lang["percent"])+'%')
    print('\t In editors:')
    for editor in waka_stats["editors"]:
        print('\t\t', editor['name'], str(editor["percent"])+'%')
    print('\t On projects:')
    for project in waka_stats["projects"]:
        print('\t\t', project['name'], project["text"], str(project["percent"])+'%')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
