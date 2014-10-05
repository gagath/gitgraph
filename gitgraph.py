import os
import sys
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
    nb_commits = 0
    for commit in repo.walk(last.id, pygit2.GIT_SORT_TIME):
        date = datetime.datetime.fromtimestamp(commit.commit_time)
        delta = datetime.datetime.today() - date
        daydelta = delta.days

        if daydelta not in dct:
            dct[daydelta] = 0
        dct[delta.days] += 1

        nb_commits += 1

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

    print('<text x="{}" y="{}" fill="black" font-family="Inconsolata" font-size="9">{} commits</text>'.format(
        0, 10,
        nb_commits
    ))

    print('</svg>')


def activity_graph(repos):

    dirpath = os.getcwd()
    repo_paths = [os.path.join(dirpath, r) for r in repos]

    nb_commits = 0

    dct = {}
    for path in repo_paths:
        try:
            gitpath = pygit2.discover_repository(path)
        except KeyError:
            continue

        repo = pygit2.Repository(gitpath)
        last = repo[repo.head.target]

        for commit in repo.walk(last.id, pygit2.GIT_SORT_TIME):
            date = datetime.datetime.fromtimestamp(commit.commit_time)
            delta = datetime.datetime.today() - date
            daydelta = delta.days

            if daydelta not in dct:
                dct[daydelta] = 0
            dct[delta.days] += 1

            nb_commits += 1

    # Computing list of days
    days = []
    for i in range(max(dct.keys()) + 1):
        if i in dct:
            days.append(dct[i])
        else:
            days.append(0)

    draw_activity(days)


def compute_color(nb, m):

    if m > 0:
        ratio = nb / m
    else:
        ratio = 0

    if ratio > 0.75:
        color = '1e6823'
    elif ratio > 0.5:
        color = '44a340'
    elif ratio > 0.25:
        color = '8cc665'
    elif ratio > 0:
        color = 'd6e685'
    else:
        color = 'eee'

    return '#{}'.format(color)


def draw_activity(days):

    weeks = 10
    days = list(reversed(days))[-(weeks*7):]

    box_height = 10
    box_width = 10
    max_commits = max(days)
    spacing = 3
    vertical_boxes = 7

    height = int(box_height * (vertical_boxes + spacing))
    width = int((len(days) / vertical_boxes + 1) * (box_width + spacing))

    print(
        '<?xml version="1.0" encoding="utf-8" ?>'
        '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}">'
        '<title>test</title>'.format(width, height)
    )

    for n, day in enumerate(days):
        x = int(n / vertical_boxes) * (10 + spacing)
        y = (n % vertical_boxes) * (10 + spacing)

        print(
            '<g><rect x="{}" y="{}" width="10" height="10" style="fill:{};{}" /><title>{} {}</title></g>'
            .format(
                x, y,
                compute_color(day, max_commits),
                "stroke-width:1px;stroke:red" if n == len(days) - 1 else "",
                datetime.datetime.now() - datetime.timedelta(days=len(days)-(n+1)),
                '{} commits'.format(day)
            )
        )

    print('</svg>')


if __name__ == "__main__":
    activity_graph(sys.argv[1:])
