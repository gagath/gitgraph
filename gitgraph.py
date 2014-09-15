import os
import datetime
import re

import pygit2


def stuff():
    dirpath = os.getcwd()

    try:
        gitpath = pygit2.discover_repository(dirpath)
    except KeyError:
        return

    repo = pygit2.Repository(gitpath)

    last = repo[repo.head.target]

    dct = {}
    for commit in repo.walk(last.id, pygit2.GIT_SORT_TIME):
        date = datetime.datetime.fromtimestamp(commit.commit_time)
        delta = datetime.datetime.today() - date
        daydelta = delta.days

        if daydelta not in dct:
            dct[daydelta] = 0
        dct[delta.days] += 1

    days = []
    for i in range(max(dct.keys())):
        if i in dct:
            days.append(dct[i])
        else:
            days.append(0)

    width = len(days)

    print(
        '<?xml version="1.0" encoding="utf-8" ?>'
        '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="100">'
        '<title>test</title>'
        '<rect width="{}" height="100" style="fill:rgb(240,240,240)" />'.format(
            width, width
        )
    )

    max_commits = max(dct.values())
    coef = 100 / max_commits

    for x, day in enumerate(reversed(days)):
        print(
            '<rect x="{}" y="{}" '
            'width="1" height="{}" '
            'style="fill:rgb(255,0,0)">'
            '<title>{} commits</title>'
            '</rect>'.format(
                x * 1,
                100 - (day * coef),
                day * coef,
                day
            )
        )

    regex = re.compile('^refs/tags')
    tags = filter(lambda r: regex.match(r), repo.listall_references())

    for tag in tags:
        commit = repo.lookup_reference(tag).get_object()

        diff = datetime.datetime.today() - datetime.datetime.fromtimestamp(commit.commit_time)
        pos = width - diff.days

        print('<text x="{}" y="0" fill="black" '
              'transform="rotate(90 {} 0)" font-family="Inconsolata" font-size="9">'
              '{}'
              '</text>'.format(
            pos,
            pos,
            tag.split('/')[2]
        ))

    print('</svg>')


if __name__ == "__main__":
    stuff()
