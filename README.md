# GitHub Profile Admin

Python project to manage and keep the github profile content up to date and alive,
though these Python classes are more capable than just manipulate a readme file.

## About The Project

The purpose of this project is to update the `readme.md` file of the github profile
with data from the user's github activities and links to RSS feed urls (if provided).  
The `GithubAdmin` class could be a powerful github management program
هf it can get the required functions and permissions that such a program needs,
but this project was not about this idea.  
The access to user's `gists` on github is provided by github `Personal access token`,
so requires no additional configuration.

## Prerequisites

- A github [Personal access token](https://github.com/settings/tokens) with at least `repo` and `user` scopes checked.

- Optional: If you have or want to access [WakaTime](https://wakatime.com/) account info,
  a `Secret API Key` from [your account settings](https://wakatime.com/settings/account).

- In the `Settings` of your profile repository from the left side menu click on `Secrets`,
  then click `New repository secret`, name it `GH_TOKEN` and for the Value
  enter your `Personal access token`.

- For WakaTime Secret API Key do the same, just name it `WAKA_TIME_TOKEN`.

## How To Use

in your repository create a `.yml` file (no matter the name), in side `.github/workflows`
directory, write the following code down inside of it<sup id="yml">[\*](#yml-footnote)</sup>:

```yml
name: github-profile-admin # Optional - The name of the workflow as it will appear in the Actions tab of the GitHub repository.

on:
  schedule:
    - cron: '0 00 * * *' # runs at 00:00 UTC everyday

jobs: # Groups together all the jobs that run in the yml workflow file.
  build:
    runs-on: ubuntu-latest
    steps:
      - name: checkout repo content
        uses: actions/checkout@v2 # checkout the repository content to github runner

      - name: setup python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9.5' # install the python version needed

      - name: install python packages
        # Using `run: |`, we run multi line python code in the runner.
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: execute py script # run main.py
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
          WAKA_TIME_TOKEN: ${{ secrets.WAKA_TIME_TOKEN }}
          GISTS_TAG: '<!-- GISTS:START -->,<!-- GISTS:END -->' # the same comment tags must be in the readme.md
        run: python main.py
```

### Footnotes

<b id="ifps-footnote">code guid</b>
<a href="https://canovasjm.netlify.app/2020/11/29/github-actions-run-a-python-script-on-schedule-and-commit-changes/#dissecting-the-workflow">
canovasjm.netlify.app</a>. <a href="#yml">↩</a>
