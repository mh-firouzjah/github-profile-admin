import asyncio
import json
from datetime import date

from decouple import Csv, config

from github import GithubAdmin
from wakatime import WakaTimeReader

github_token = config('GH_TOKEN', default=None)
waka_token = config("WAKA_TIME_TOKEN", default=None)

show_gists = config('SHOW_GISTS', default=None)
gists_tag = config('GISTS_TAG', cast=Csv(),
                   default="<!-- GISTS:START -->,<!-- GISTS:END -->")

need_view_counter = config('SHOW_VIEWCOUNTER', default=None)
views_tag = config('VIEWS_TAG', cast=Csv(),
                   default="<!-- VIEW_COUNTER:START -->,<!-- VIEW_COUNTER:END -->")

blog_feeds = config('BLOG_FEEDS_LIST', default=None, cast=Csv())
blog_tag = config('BLOG_POSTS_TAG', cast=Csv(),
                  default="<!-- BLOG_POSTS:START -->,<!-- BLOG_POSTS:END -->")
youtube_chanel = config('YOUTUBE_CHANEL', default=None)
youtube_tag = config('YOUTUBE_TAG', cast=Csv(),
                     default="<!-- YOUTUBE_VIDEOS:START -->,<!-- YOUTUBE_VIDEOS:END -->")

truthy = ['true', '1', 't', 'y', 'yes']


def markdown_link(text: str, link: str) -> str:
    '''generates markdown link'''
    return f"[{text}]({link})"


def profile_views_markdown(views: int) -> str:
    return f"![Profile Views](https://img.shields.io/badge/Weekly%20Views-{views}-blue?style=social&logo=github)"


print(show_gists, need_view_counter)

'''
async def main():

    if not github_token:
        return

    gh_admin = GithubAdmin(github_token)

    new_content = None

    if gists_tag:
        data = await gh_admin.gists(5)
        print(data)
        gists_links = []
        for gist in data:
            link = gist["html_url"]
            description = gist["description"]
            gists_links.append(markdown_link(description, link))
        content = '  \n'.join(it for it in gists_links)
        views = await gh_admin.get_repo_views(repo, 'week')
        content = profile_views_markdown(views) + '  \n' + content
    await gh_admin.update_repo_readme(repo)

    waka = WakaTimeReader(waka_token)
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
'''
