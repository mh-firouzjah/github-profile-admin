'''connect to github using aiohttp'''

import base64
import json
import re
from datetime import datetime, timedelta
from typing import Literal

import aiohttp


class GithubAdmin(object):
    '''creates an instance of GitHub Account Controller'''

    base_url = "https://api.github.com"

    def __init__(self, token: str) -> None:
        self.token = token

    @property
    def headers(self):
        '''required and recommended github-api headers'''
        return {'Authorization': f'token {self.token}',
                "Accept": "application/vnd.github.v3+json"}

    @property
    async def user(self):
        '''returns the loggen in user(the owner of the token)'''
        return (await self.get_user())['login']

    async def aiohttp_get(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.json()

    async def aiohttp_put(self, url: str, data: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=data, headers=self.headers) as response:
                return await response.json()

    async def get_user(self):
        '''
            Get the authenticated user

            If the authenticated user is authenticated through basic authentication or OAuth with the user scope, then the response lists public and private profile information.

            If the authenticated user is authenticated through OAuth without the `user` scope, then the response lists only public profile information.
        '''
        user_url = f"{self.base_url}/user"
        return await self.aiohttp_get(user_url)

    async def gists(self, list_count: int):
        '''md
            List public gists sorted by most recently updated to least recently updated.

            Note: With pagination, you can fetch up to 3000 gists. For example, you can fetch 100 pages with 30 gists per page or 30 pages with 100 gists per page.

            `GET` `/gists/public`

            Parameters

            | Name      | Type      | In    | Description |
            | ---       | ---       | ---   | ---         |
            | `accept`  | string	| header| Setting to application/vnd.github.v3+json is recommended. |
            | `since`   | string	| query | Only show notifications updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ. |
            | `per_page`| integer	| query | Results per page (max 100). Default: 30 |
            | `page`    | integer	| query | Page number of the results to fetch. Default: 1 |
        '''
        gists_url = f"{self.base_url}/users/{await self.user}/gists?per_page={list_count}"
        gists = await self.aiohttp_get(gists_url)
        return gists

    async def repos(self):
        '''
            Lists repositories that the authenticated user has explicit permission (`:read`, `:write`, or `:admin`) to access.

            The authenticated user has explicit permission to access repositories they own, repositories where they are a collaborator, and repositories that they can access through an organization membership.

            `GET` `/user/repos`

            Parameters

            | Name          | Type      | In        | Description |
            | ---           | ---       | ---       | ---   |
            | accept        | string    | header    | Setting to application/vnd.github.v3+json is recommended. |
            | visibility    | string    | query     | Can be one of all, public, or private. Note: For GitHub AE, can be one of all, internal, or private. Default: all |
            | affiliation   | string    | query     | Comma-separated list of values. Can include:
            |               |           |           |* `owner`: Repositories that are owned by the authenticated user.
            |               |           |           |* `collaborator`: Repositories that the user has been added to as a collaborator.
            |               |           |           |* `organization_member`: Repositories that the user has access to through being a member of an organization. This includes every repository on every team that the user is on.
            |               |           |           |* Default: `owner`,`collaborator`,`organization_member`  |
            | type          | string    | query     | Can be one of all, `owner`, `public`, `private`, `member`. Note: For GitHub AE, can be one of all, `owner`, `internal`, `private`, `member`. Default: `all` Will cause a 422 error if used in the same request as visibility or affiliation. Will cause a 422 error if used in the same request as visibility or affiliation. Default: all |
            | sort          | string    | query     | Can be one of created, updated, pushed, full_name. Default: full_name |
            | direction     | string    | query     | Can be one of asc or desc. Default: asc when using full_name, otherwise desc |
            | per_page      | integer   | query     | Results per page (max 100). Default: 30 |
            | page          | integer   | query     | Page number of the results to fetch. Default: 1 |
            | since         | string    | query     | Only show notifications updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ. |
            | before        | string    | query     | Only show notifications updated before the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ. |
        '''
        repos_url = f'{self.base_url}/user/repos'
        async with aiohttp.ClientSession() as session:
            async with session.get(repos_url, headers=self.headers) as response:
                return await response.json()

    """
    async def get_repo(self, repo_name: str):
        repo_url = f"{self.base_url}/repos/{await self.user}/{repo_name}"
        return await self.aiohttp_get(repo_url)

    async def repo_issues(self, repo_name: str):
        issues_url = f"{self.base_url}/repos/{await self.user}/{repo_name}/issues"
        return await self.aiohttp_get(issues_url)
    """

    async def update_repo(self, repo_name, message, content, sha, path) -> dict:
        '''
            Creates a new file or replaces an existing file in a repository.

            `PUT` `/repos/{owner}/{repo}/contents/{path}`

            Parameters

            | Name        | Type      | In    | Description |
            | ---         | ---       | ---   | ---   |
            | `accept`	  | string	  | header| Setting to application/vnd.github.v3+json is recommended.
            | `owner`     | string    | path  |
            | `repo`      | string    | path  |
            | `path`      | string    | path  | path parameter
            | `message`   | string    | body  | `Required`. The commit message. |
            | `content`   | string    | body  | `Required`. The new file content, using Base64 encoding. |
            | `sha`       | string    | body  | `Required` if you are updating a file. The blob SHA of the file being replaced. |
        '''
        url = f"{self.base_url}/repos/{await self.user}/{repo_name}/contents{path}"
        data = json.dumps({'message': message,
                           'content': content,
                           'sha': sha, })
        return await self.aiohttp_put(url, data=data)

    async def get_repo_readme(self, repo_name: str) -> tuple[str, str]:
        '''
            Gets the preferred README for a repository.

            READMEs support custom media types for retrieving the raw content or rendered HTML.

            `GET` `/repos/{owner}/{repo}/readme`

            Parameters

            | Name  | Type  | In    | Description |
            | ---   | ---   | ---   | ---   |
            | accept| string| header | Setting to application/vnd.github.v3+json is recommended. |
            | owner	| string| path| |
            | repo	| string| path| |
            | ref	| string| query| The name of the commit/branch/tag. Default: the repository’s default branch (usually `master`)
        '''
        repo_readme_url = f"{self.base_url}/repos/{await self.user}/{repo_name}/readme"
        full_detail = await self.aiohttp_get(repo_readme_url)
        sha = full_detail["sha"]
        base64_encoded_readme = full_detail['content']
        content = str(base64.b64decode(base64_encoded_readme), encoding='utf-8')
        return content, sha

    async def update_repo_readme(self, repo_name: str,
                                 start_end_contents: list[tuple[str, str, str]]) -> dict:
        '''
        `updates/creates` repo's `readme` with new content between start and end
        '''
        repo_readme_path = "/README.md"

        old_readme_content, sha = await self.get_repo_readme(repo_name)

        new_readme = self.readme_b64encoder(*start_end_contents[0], old_readme_content)

        if len(start_end_contents) > 1:
            for change in start_end_contents[1:]:
                old_readme_content = new_readme
                new_readme = self.readme_b64encoder(*change, old_readme_content)

        message = 'updated by GitHubAdmin project',

        return await self.update_repo(repo_name, message=message, content=new_readme,
                                      sha=sha, path=repo_readme_path)

    async def get_repo_commits(self, repo_name: str) -> None:
        '''
            Gets list of commits for a repository.

            `GET` `/repos/{owner}/{repo}/commits`

            Parameters

            | name      | type      | in    | description |
            | ---       | :---:     | :---: | ---         |
            | `accept`  | string    | header| Setting to application/vnd.github.v3+json is recommended.
            | `owner`   | string    | path  |
            | `repo`    | string    | path  |             |
            | `sha`     | string    | query | SHA or branch to start listing commits from. Default: the repository’s default branch (usually master).
            | `path`    | string    | query | Only commits containing this file path will be returned.
            | `author`  | string    | query | GitHub login or email address by which to filter by commit author.
            | `since`   | string    | query | Only show notifications updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.
            | `until`   | string    | query | Only commits before this date will be returned. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.
            | `per_page`| integer	| query | Results per page (max 100). Default: 30
            | `page`	| integer	| query | Page number of the results to fetch. Default: 1
        '''
        commits_url = f"{self.base_url}/repos/{await self.user}/{repo_name}/commits"
        today = datetime.today()
        last_week = today - timedelta(days=8)
        since_til = f'?since={last_week.strftime("%Y-%m-%dT%H:%M:%SZ")}&until={today.strftime("%Y-%m-%dT%H:%M:%SZ")}'
        await self.aiohttp_get(commits_url + since_til)

    async def get_repo_views(self, repo_name: str, per: Literal['day', 'week'] = 'day') -> int:
        '''
            `GET` `/repos/{owner}/{repo}/traffic/views`
            ---
            Get the total number of views and breakdown per day or week for the last 14 days. Timestamps are aligned to UTC midnight of the beginning of the day or week. Week begins on Monday.

            | name    | type    | in      | description |
            | ---   | :---:   | :---:   | ---      |
            | accept  | string  | header  | Setting to application/vnd.github.v3+json is recommended.|
            | owner	| string	| path    |     |
            | repo	| string	| path    |     |
            | per	| string	| query   | Must be one of: `day`, `week`.|

            Default: `day`
        '''
        page_views = f"{self.base_url}/repos/{await self.user}/{repo_name}/traffic/views?per={per}"
        async with aiohttp.ClientSession() as session:
            async with session.get(page_views, headers=self.headers) as response:
                return (await response.json())['uniques']

    def readme_b64encoder(self, section_start: str, section_end: str,
                          new_content: str, file_content: str) -> str:
        '''Replace file_content between section_start and section_end (both are excluded) with new_content'''

        commutable = f"{section_start}[\\s\\S]+{section_end}"

        data = f"{section_start}\n{new_content}\n{section_end}"

        content = re.sub(commutable, data, file_content)

        return base64.b64encode(content.encode('utf-8')).decode("utf-8")
